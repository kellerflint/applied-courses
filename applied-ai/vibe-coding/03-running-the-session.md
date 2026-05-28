---
title: "Running the Session"
order: 3
---

## The loop

Work in a tight cycle and repeat it the whole session:

1. **Ask for one small piece.** A window. A square. Movement. One mechanic. Never a whole feature set in a single prompt.
2. **Run it.** See it with your own eyes. "It compiles" is not the same as "it works."
3. **Commit it the moment it works.**
4. **Go back to step one** for the next small piece.

The reason this works is that small, verified steps keep the broken surface area tiny. When something goes wrong, you know it's in the last little change, not buried somewhere in a thousand lines you've never read.

## Directing the agent

You can't write the Rust yourself, but you can steer. A few moves that consistently help:

**Be specific about the goal.** "The player square should stop at the walls instead of sliding through them" gives the agent a clear target. "Fix the collision" makes the agent guess and it often guesses poorly.

**Feed it the actual error.** When something breaks, copy the real compiler error or the real behavior back to the agent word for word. Don't paraphrase it as "it's broken." The exact text or a very clear description is the most useful thing you can hand it. Treat it like filing a bug report for another developer. You'll get better results. 

**Stop a loop early.** If the agent tries the same fix two or three times and keeps failing, it's stuck in a loop and more attempts usually make it worse. Reset to your last commit, then describe the problem differently, or break it into a smaller piece.

**Reset instead of digging.** When the project is badly broken and you can't tell why, going back to your last good commit is often faster than debugging a hole the agent dug.

## Watch carefully

The build is the activity, but the watching is the point. As you go, pay attention to where the agent is strong and where it falls apart. You'll need these observations for your post, and they're hard to reconstruct after the fact, so capture them as they happen.

You can use the field notebook below to log these as you build or write your own. Keeping track now will be useful when you go to write your reflection in the next step.

{% activity "agent-field-notes.html", "Agent Field Notebook", "560px" %}
