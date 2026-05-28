---
title: "Running the Session"
order: 3
---

Now you build. The way you run the session matters more than the idea itself. A great idea steered badly turns into a broken mess, and a modest idea steered well turns into something that actually runs.

## The loop

Work in a tight cycle and repeat it the whole session:

1. **Ask for one small piece.** A window. A square. Movement. One mechanic. Never a whole feature set in a single prompt.
2. **Run it.** See it with your own eyes. "It compiles" is not the same as "it works."
3. **Commit it the moment it works.** `git add -A && git commit -m "what changed"`. This is your save point.
4. **Go back to step one** for the next small piece.

The reason this works is that small, verified steps keep the broken surface area tiny. When something goes wrong, you know it's in the last little change, not buried somewhere in a thousand lines you've never read.

> **With your partner:** How small is your first step? If your opening ask is bigger than "open a window with a colored background," it's too big. Shrink it.

## Directing the agent

You can't write the Rust yourself, but you can steer hard. A few moves that consistently help:

**Be specific about the goal, not the implementation.** "The player square should stop at the walls instead of sliding through them" gives the agent a clear target. "Fix the collision" gives it nothing to aim at.

**Feed it the actual error.** When something breaks, copy the real compiler error or the real behavior back to the agent word for word. Don't paraphrase it as "it's broken." The exact text is the most useful thing you can hand it.

**Stop a loop early.** If the agent tries the same fix two or three times and keeps failing, it's stuck in a loop and more attempts usually make it worse. Reset to your last commit, then describe the problem differently, or break it into a smaller piece.

**Reset instead of digging.** When the project is badly broken and you can't tell why, `git checkout .` back to your last good commit is faster than debugging a hole the agent dug. This only works if you've been committing. This is why you commit.

> **With your partner:** Show each other one prompt that worked well and one that sent the agent down a bad path. What was different about how you phrased them?

## Watch carefully

The build is the activity, but the watching is the point. As you go, pay attention to where the agent is strong and where it falls apart. You'll need these observations for your post, and they're hard to reconstruct after the fact, so capture them as they happen.

Keep an eye out for:

- **What types of things does it handle well?** Boilerplate, setup, well-known patterns, explaining errors?
- **Where does it fail consistently?** Spatial reasoning, game feel, anything visual, holding the whole project in its head, a specific kind of bug it keeps reintroducing?
- **What recurring issues show up?** Does it break things it already fixed? Forget what you told it? Confidently claim something works when it doesn't?
- **What communication got the best results?** What you said right before its best and worst moments is gold.

Use the field notebook below to log these as you build. Drop a quick note in the right quadrant whenever something stands out, then pull the whole thing back up when you write your post.

{% activity "agent-field-notes.html", "Agent Field Notebook", "560px" %}

> **With your partner:** Glance at each other's notebooks. Are you noticing the same kinds of failures, or did your different ideas and tools push the agents in different directions?
