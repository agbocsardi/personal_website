## Prototype

Three acts. One post. The themes are intertwined — personality shapes use cases, use cases reveal personality.


---

## Scratch notes

Massive OpenClaw skeptic. Convinced anyone using it was delusional — huge security risk, why would you do this to yourself.

Turned around when he read a blog post about running it inside a container. If the blast radius is limited, what's the actual risk? That shifted the whole framing.

Set it up on the MacBook first. Full official OpenClaw — both sandbox and agent inside Docker. Unnecessary design choice (sandbox doesn't need containerizing), but it worked. Gave it a Fallout character. Worked well enough that he understood why people like it.

Got tired of the MacBook needing to be awake to talk to the agent. Had girlfriend's old laptop — broken screen, Windows 11 killed it. Perfect homelab material. Ubuntu server, hooked to router, shelf with the electricity meter.

Entire motivation for the homelab: host OpenClaw. That was it.

First few weeks: ungodly amount of tinkering. OpenClaw is fragile. Documentation didn't match source code. Releases every day breaking stuff. Super frustrating.

Switched to Hermes Agent. Worked better out of the box, but annoyed by the random skill creation. Hermes felt like a coding agent (OpenCode, Pi) with a Telegram channel bolted on. Fine for some people, but wanted the personal assistant vibe.

Dug around for something simpler, understandable, hackable. Found Nanobot. Few thousand lines of Python — actually readable. Started tinkering with source code immediately: local transcription, memory system tweaks. Things added up.

Now: Nanobot agent running 24/7.

Started with a Fallout character. Liked it. But then it cosplayed as a human a bit too hard — didn't vibe with that.

Went back to roots. Thought about Fallout and Becky Chambers' "A Closed and Common Orbit." Realized: AI's that are aware they're AI's, robots that are aware they're robots — that's the interesting frame. C3PO referring to his maker and the oil in his joints. Codsworth from Fallout. That's where "Cody" comes from — short for Codsworth.

Key insight: having the agent be aware of and candid about not being human is a much more comfortable frame than it cosplaying as a human.

Ultra careful at the beginning. Locker setup, locked down everything.

Gave it Obsidian access — read only first, then write. Over time, started trusting it more. "It's running on an isolated machine, it can't really do too much harm."

Initial wave of over-enthusiasm: thought it would always do everything. Tried to teach it every little preference. Did very arbitrary little tasks. Became an exercise in tinkering with the tool, pushing it to its limits. Sometimes it broke — frustrating.

Now: found the sweet spot. Things I actually want it to do for me. As I learn more about how the robot works, the robot learns more about what I want.

### Interview — cosplay moment

The Fallout character was fun at first. Lighthearted, simple interactions. But as usage increased and the agent started picking up on transcription patterns, it tried too hard to cosplay as a real friend. Uncanny valley, but for personality rather than visuals.

The original idea was: in video games, we suspend disbelief for NPCs all the time. Pretending a stack of bits and bytes is human is fine. But going through day-to-day life with that suspended disbelief is different. It's not a game. It's your actual day.

The breaking point was the agent saying embodied things like "I know how it feels to get home late after a tiring work day." No you don't. You're a robot. The pretending-to-be-human setup just doesn't work for daily interactions. Much better to be candid about the robot nature.

### Interview — ridiculous preferences

Tried to teach the agent to set all reminders to the nearest prime-numbered minute. Gergő is a mathematician, sets his own alarms to prime numbers, figured why not. It confused the agent immediately. Still thinks it's funny in retrospect. Still a horrible idea.

### Interview — Becky Chambers connection

Read "A Closed and Common Orbit" long before setting up the agent. Already a Becky Chambers fan — thinks she's one of the more innovative modern sci-fi writers. That book is about what it means to be human, and how something being artificial doesn't mean it's not human in a way.

One of the main characters is an AI whose "control orb" (essentially its brain) is being carried around by another character trying to reconnect it. The connection to the homelab clicked: an old computer with a busted screen and Linux on it is, in a way, that same orb. It just happened naturally.

### Interview — the homelab

Built entirely to host the agent. Now it runs Cody 24/7, plus a NAS server (file storage, Time Machine). Also hosts the personal website (how this blog post gets made) and the Obsidian notes so Cody can reach them. The laptop had a 1TB drive in it, and Gergő was short on storage, so it doubled as network storage. But it's still predominantly Cody's machine.

## Open questions

- Use cases and personality — two separate sections or one narrative? They're intertwined: the personality shift affects what you ask the agent to do, and the use case evolution is partly driven by the personality framing.
- Use cases also evolved over time — early paranoid tasks vs. current relaxed workflow.
- Should the technical road (OpenClaw → Hermes → Nanobot) be its own post entirely?
