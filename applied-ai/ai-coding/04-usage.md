---
title: "Layer 2: Usage"
order: 4
---

Once you've decided a task is a reasonable fit, the next question is how much to lean on the agent. The core trade-off is **convenience versus control**.

**Convenience** is the upside of agentic mode. If the code can essentially write itself while you do something else, that's genuinely valuable, and you should want it.

**Control** is the other end. You specify more, decompose more, and review more. You get a better understanding of the code and tighter alignment with your vision.

## Where convenience shines

Leaning all the way toward convenience makes the most sense when the stakes are low.

- **Small** and won't grow into something larger.
- **Throwaway**, not something you'll maintain or ship.
- **Free of security or user-data stakes**, so a bug can't hurt anyone.

When all of that is true, the agent's speed is pure upside and there's little reason to slow down and grab the wheel.

## It's a dial

Agentic coding isn't on or off. It's a dial that you can set per task.

{% activity "usage-dial.html", "The convenience–control dial", "560px" %}

> **With your partner:** Pick a real task each of you has. Where on the dial would you set it and why?

## A worked example: the 305 grading script

Here's a real task that shows both the suitability and usage layers at once.

I needed to grade a course's worth of student projects. I needed to clone every student's repo from their submitted GitHub link, set each one up locally, click through each project running on its port, tear it down, and load the next one. Dozens of repos with the same loop every time. I wanted a tool to that made this setup and tear down process easy.

I handed this to the agent completely. It roughly one-shot it, with a few minor corrections, using libraries I wasn't even familiar with, and I let it.

**On the suitability layer**, this task is low scope, with a little complexity, and a little novelty, well into the green for agent handoff.

**On the usage layer**, I turned the dial all the way to convenience. Here's why that was safe:

- It was pure convenience with no real need for control.
- There was no data to protect and no security concern.
- Bugs weren't a big deal. If it misbehaved, I'd just rerun it.
- I never intended to maintain or expand it.

**The payoff:** a task that might have taken me half a day once you count the research, writing, and debugging the script myself, came down to about ten minutes.

> **With your partner:** What would have to change about this task to make full convenience the wrong call? Name one change that would force you to grab back control.

## What never changes, even at full convenience

Turning the dial to convenience buys you speed. It does not buy you out of one rule.

**You always review the output, carefully, every time.** Even when you've handed everything off, you read what came back. The 305 script was pure convenience and I still read what it did before running it against real repos.

There's one thing convenience does relax. At the pure-convenience end, you don't necessarily need to fully understand the code, line by line, the way you would for something you'll maintain. But that only applies when the work is truly personal, small, or throwaway. The moment a task is none of those, understanding comes back onto the table, and so does turning the dial toward control.
