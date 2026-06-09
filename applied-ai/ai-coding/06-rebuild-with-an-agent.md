---
title: "Pair Program: Rebuild With an Agent"
order: 6
---

You're going to take a full stack project you've already built (or one that you'd like to build and know how to approach already), and build/re-build it with an agent doing the work.

## Why a project you already know

The game vibe coding was the opposite of this. There you worked in a stack you couldn't read, to see the agent's raw capability with you mostly along for the ride. Here you pick something you understand deeply, so you can direct it well and actually judge whether the output is right.

**Domain knowledge is what makes you a good director and a good verifier.** Recall from the verification layer that the agent has no insight into your intent or whether its code truly works. You supply both. That only works when you genuinely know the domain, so pick something with real substance where you already know how it works, where the tricky parts are, and what "done" looks like. If you'd rather build something new instead, you can, as long as it's a domain you know well.

> **With your partner:** Pitch your project to each other. What's the part you already know will be tricky, the part where you'll need to watch the agent closely?

## Step 1: Spec it out first

Start with **spec-driven development**. Write a clear, detailed specification and hand the agent that target to build toward.

Write a spec that covers:

- **What the tool is.** Full detail on what it does and who it's for.
- **How it should work.** The features and behaviors, walked through as the main flows. Call out the edge cases and the tricky parts you already know are likely to be tricky.
- **The stack.** Languages, frameworks, libraries, and how the project is structured. Choose deliberately. Research first or have the agent make a POC if you need to decide on a tool, library, or language you haven't used before.
- **How it should be tested.** What the test suite needs to cover, especially the end-to-end flows. Name the specific cases that matter.
- **Anything else that matters.** Constraints, data shapes, performance needs, and things you explicitly want it to avoid.

Make it **detailed and clear**.

> **With your partner:** Trade specs and poke holes. Where is it vague enough that the agent could build something you didn't mean? Tighten those spots before you start.

## Step 2: Set the dial to the middle

You're aiming for the middle of the convenience–control dial. You are not writing the code yourself, and you are not handing it off and walking away.

In practice:

- **Let the agent write the code, but read what it produces.** Actually open the files and review, or at least spot check.
- **Guide and correct at the architectural level.** You're the architect and the agent is the implementer. When it makes a structural choice you don't like, redirect it before that choice spreads through the codebase.
- **Check in often.** Review each chunk before moving on. Catch wrong turns before you build on top of them.
- **Use your domain knowledge.** You can probably tell when something is off here in a way you couldn't in the game session. Correct as needed.

## Step 3: Verify with automated testing, and keep control of it

- **Dictate the test cases yourself.** Tell it the scenarios and flows that matter, then let it write the test code.
- **Make the agent run those tests before reporting anything as done.** "Done" means the suite actually passes. Have it run the suite and test against it as part of the work every time.
- **Audit the tests.** Open them and confirm they check something real. Remember the agent writes hollow tests and degrades over time, so keep watching them.
- **Keep timeouts aggressive** so a failing suite fails fast instead of spinning for minutes.
- **Maintain high quality.** You know what right looks like for this project, so hold the output to that standard and keep correcting until it meets it.

## Submit

Push your project to GitHub and post it to the Canvas discussion for this assignment.

In the post include:

- **A link to your repository.** Include a README with the spec you wrote from step 1.
- **A short reflection:** How did middle-ground control feel compared to the game session? Where did the agent need correcting at the architectural level, and how well did your tests actually hold up?

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Applied+AI&unit=AI+Coding" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
