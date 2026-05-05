---
title: "Project Review"
order: 2
---

Each team will book a 15 minute 1:1 review meeting with me before you start building. The point is to make sure your plan is achievable in the time you have, that the components you've picked actually fit together, and to surface any issues early while there's still time to adjust.

## Schedule your meeting

The scheduling link is on Canvas. Pick a slot that works for everyone on your team and book it as a group. One booking per team, not one per person.

If your team can't find a time that works for everyone, message me on Canvas and we'll figure something out.

## What to bring

Come to the review with a written proposal that covers the points below. Keep it brief and focused. A shared doc, a markdown file in your repo, or a simple slide deck all work equally well. What matters is that you've actually thought through each item.

### The components

List your ML-based components and what each one does in your app. Be specific. Aim for the level of detail in: "We'll use Groq's Llama 3.1 70B to take the user's spoken question plus the OCR-extracted card list and return a natural language strategy suggestion." Vague descriptions like "we'll use an LLM" leave the most important questions unanswered.

For each component, include:

- **What it is** (specific model or API)
- **What it takes as input** in your app
- **What it produces as output** in your app
- **Where it runs** (local, hosted API, on-device)
- **Why this one** instead of an alternative

### The architecture

A diagram or short description of how data flows through the app. Which component runs first, what it hands off, and how the user interacts with the system. A whiteboard photo or a hand-drawn sketch is fine.

### The stack

What you're building it in. Frontend, backend, any frameworks, deployment target. The major pieces should be decided. Smaller details can stay open.

### Concerns and risks

List the parts you're least sure about. This is the most useful section for the review because it's what we'll spend the most time on. Common things to flag:

- A component you've never used before and aren't sure how to integrate
- An API you haven't checked the pricing or rate limits on
- A piece of the data flow where you don't yet know how to get from one component's output to the next component's input
- Performance concerns (latency, memory, cost)
- Anything else nagging at you

### Who's doing what

A rough split of work across the team. Each person should know what they're owning going in. The exact breakdown can shift as the project develops.

## What we'll talk about

In the meeting we'll go through your proposal together. I'll push on the parts that look risky, suggest tweaks where something's off, and confirm the scope is reasonable for your team size and the time you have.

> **With your team:** Before the meeting, take a few minutes to dry run of your proposal as if you were presenting it to me. Come ready to discuss your choices.