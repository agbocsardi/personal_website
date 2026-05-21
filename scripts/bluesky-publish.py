#!/usr/bin/env python3
"""Publish new blog posts to Bluesky and inject the comments shortcode.

Scans posts/ for .qmd files that are not drafts and don't yet have a
bluesky-comments shortcode. Posts each one to Bluesky (title + description
+ link), then appends the comments shortcode to the source so the Quarto
extension renders reply threads.

First run will backfill all existing non-draft posts. Subsequent runs are
no-ops unless new posts are added.

Env vars (set in .env for local runs, or as GitHub Actions secrets):
    BLUESKY_HANDLE         your Bluesky handle (e.g. "agbocsardi.com")
    BLUESKY_APP_PASSWORD   Bluesky app password (Settings → App Passwords)
    BLUESKY_PDS            optional PDS URL (default: https://bsky.social)
    REPO_PUSH_PAT          GitHub PAT with Contents read+write on this repo

Usage:
    uv run scripts/bluesky-publish.py           # post to Bluesky
    uv run scripts/bluesky-publish.py --dry-run # show what would happen
"""

# /// script
# requires-python = ">=3.10"
# dependencies = ["python-frontmatter", "atproto"]
# ///

import os
import sys
import time
from datetime import date, datetime
from pathlib import Path

import frontmatter
from atproto import Client, client_utils
from atproto_client.exceptions import UnauthorizedError

SITE_URL = os.environ.get("SITE_URL", "https://agbocsardi.com")
REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "posts"

COMMENTS_START = "{{< bluesky-comments"
COMMENTS_TEMPLATE = "{{{{< bluesky-comments {uri} >}}}}"


def get_client() -> Client:
    """Log into Bluesky and return the client."""
    handle = os.environ["BLUESKY_HANDLE"]
    password = os.environ["BLUESKY_APP_PASSWORD"]
    pds = os.environ.get("BLUESKY_PDS", "https://bsky.social")

    if not handle or not password:
        raise RuntimeError(
            "BLUESKY_HANDLE and BLUESKY_APP_PASSWORD must be set "
            "(in .env for local, or as GitHub Actions secrets)"
        )

    client = Client(base_url=pds)
    try:
        client.login(handle, password)
    except UnauthorizedError:
        raise RuntimeError(
            "Bluesky login failed. Check your handle and app password. "
            "The app password must be from Settings → App Passwords, "
            "not your main account password."
        ) from None

    print(f"  Logged in as {client.me.handle} via {pds}")
    return client


def parse_date(val) -> datetime | None:
    """Try to turn a frontmatter date value into a datetime for sorting.

    Handles: strings like '2025-09-13', '2026-05-18T09:00', '2024.12.06',
    quoted strings, and native datetime/date objects.
    Returns None if parsing fails (posts without dates sort last).
    """
    if isinstance(val, datetime):
        return val
    if isinstance(val, date):
        return datetime(val.year, val.month, val.day)

    if not isinstance(val, str):
        return None

    val = val.strip().strip('"').strip("'")

    # ISO datetime (with or without time)
    try:
        return datetime.fromisoformat(val)
    except ValueError:
        pass

    # Dotted format: yyyy.mm.dd
    try:
        return datetime.strptime(val, "%Y.%m.%d")
    except ValueError:
        pass

    return None


def find_unposted_posts() -> list[tuple[Path, dict]]:
    """Return (path, frontmatter_dict) for posts that need a Bluesky post.

    A post "needs" posting if:
        - it's a .qmd file (or index.qmd inside a directory)
        - not a draft (frontmatter `draft` is not true)
        - doesn't already contain `{{< bluesky-comments`

    Results are sorted by frontmatter date, oldest first.
    """
    results = []

    for qmd in POSTS_DIR.rglob("*.qmd"):
        rel = qmd.relative_to(REPO_ROOT)

        content = qmd.read_text()

        # Already has comments shortcode — skip
        if COMMENTS_START in content:
            continue

        try:
            post = frontmatter.loads(content)
        except Exception as e:
            print(f"  Skipping {rel}: failed to parse frontmatter ({e})")
            continue

        if not post.metadata:
            print(f"  Skipping {rel}: no frontmatter")
            continue

        if post.metadata.get("draft"):
            print(f"  Skipping {rel}: draft")
            continue

        results.append((qmd, post.metadata))

    # Sort by date, oldest first. Posts without a parsable date go last.
    def _sort_key(item):
        return parse_date(item[1].get("date")) or datetime(9999, 1, 1)

    results.sort(key=_sort_key)
    return results


def publish_post(client: Client, post_path: Path, metadata: dict) -> str | None:
    """Post to Bluesky (with clickable link), return the at:// URI or None on failure."""
    title = metadata.get("title", "")
    description = metadata.get("description", "")
    slug = metadata.get("slug")

    # Prefer explicit slug in frontmatter; fall back to directory name
    if not slug:
        if post_path.name == "index.qmd":
            slug = post_path.parent.name
        else:
            slug = post_path.stem

    url = f"{SITE_URL.rstrip('/')}/posts/{slug}/"

    # Build text with title as clickable link, then description
    tb = client_utils.TextBuilder()
    tb.link(title, url)
    if description:
        tb.text("\n\n")
        tb.text(description)

    rel = post_path.relative_to(REPO_ROOT)
    print(f"\n  Posting: {title}")
    print(f"  URL:     {url}")

    try:
        response = client.send_post(text=tb)
    except Exception as e:
        print(f"  ERROR: failed to post to Bluesky: {e}")
        return None

    at_uri = response.uri
    print(f"  Posted:  https://bsky.app/profile/{client.me.handle}/post/{at_uri.split('/')[-1]}")
    return at_uri


def inject_comments(post_path: Path, at_uri: str) -> None:
    """Append the bluesky-comments shortcode to the post and verify it persisted."""
    shortcode = COMMENTS_TEMPLATE.format(uri=at_uri)
    with post_path.open("a") as f:
        f.write(f"\n{shortcode}\n")

    updated = post_path.read_text()
    if shortcode not in updated:
        raise RuntimeError(
            f"Posted to Bluesky but failed to persist comments shortcode in {post_path}. "
            f"Add this manually before rerunning: {shortcode}"
        )

    print(f"  Added:   {shortcode}")


def main() -> int:
    dry_run = "--dry-run" in sys.argv

    # --- Find posts ----------------------------------------------------------
    posts = find_unposted_posts()

    if not posts:
        print("No new posts to publish.")
        return 0

    print(f"Found {len(posts)} post(s) to publish:")
    for _, meta in posts:
        print(f"  - {meta.get('title', '(untitled)')}")

    if dry_run:
        print("\n[Dry run — no changes made.]")
        return 0

    # --- Bluesky client ------------------------------------------------------
    try:
        client = get_client()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # --- Publish each post ---------------------------------------------------
    any_failure = False
    for i, (post_path, metadata) in enumerate(posts):
        if i > 0:
            time.sleep(2)  # avoid rate limits during backfill
        at_uri = publish_post(client, post_path, metadata)
        if at_uri is None:
            any_failure = True
            continue
        try:
            inject_comments(post_path, at_uri)
        except Exception as e:
            print(f"  CRITICAL: {e}", file=sys.stderr)
            print("  Stop here. Do not rerun until the shortcode above is added manually.", file=sys.stderr)
            return 1

    if any_failure:
        print("\nSome posts failed. Skipping commit — fix the errors and re-run.")
        return 1

    print("\nAll posts published. Above files were edited — commit them to trigger a re-deploy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
