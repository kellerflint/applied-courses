---
title: "Layer 1: Suitability"
order: 3
---

The first question for any task is whether it's a good fit for an agent at all. You read that fit against three preconditions:

- **Scope** is how big the task is. How many files, features, and moving parts.
- **Complexity** is how hard the logic is. Involved algorithms, subtle state, intricate edge cases.
- **Novelty** is how unusual the task is. How little public code exists that looks like it.

**Lower on all three means better suited.** A small, straightforward, familiar task is where an agent shines. High on all three is where it fails most.

## They trade off against each other

The three preconditions aren't independent. A task can be high on one and still be a good fit if the others stay low.

- **Big scope is fine** if novelty and complexity stay low. A large amount of routine, familiar work is something an agent can grind through.
- **High complexity can work** with a capable thinking agent, as long as scope and novelty stay low. A small, gnarly, but well-understood problem may be within reach.

What tends to fail is being high on all three at once. A big, intricate, unfamiliar project is exactly where you should expect the agent to flounder.

> **With your partner:** Before reading on, sketch a quick task and rate it low, medium, or high on each of scope, complexity, and novelty. Then take a guess. Would it be a good fit for an agent, or not?

## A mixer for the three preconditions

Use the activity below to build intuition for how the three combine. The lower the total, the better suited the task; the higher the total, the worse.

{% activity "suitability-mixer.html", "Suitability mixer", "600px" %}

> **With your partner:** Think of a project you've worked on recently and rate it. Where does it fall? Do you agree or disagree?

## There's no clean line

Notice the activity gives you a gradient, not a pass/fail. There's no clean suited/unsuited boundary where a task flips from "agent" to "no agent."

Impressive stories shared online often deserve a second look. When you hear "the AI did something brilliant," like finding a real security vulnerability in a codebase, there's almost always a human who aimed it at a specific domain. Someone pointed it at a narrow, well-defined target. That's very different from a greenfield "go do a thing" which tends to give much worse results.

## When a task is high on all three

Plenty of real projects are big, complex, and novel all at once. That doesn't mean you can't use an agent.

You break it into chunks so each piece is lower-scope, lower-complexity, and lower-novelty than the whole. A scary project becomes a series of tasks that each sit lower on the gradient, and you hold more control across all of them.
