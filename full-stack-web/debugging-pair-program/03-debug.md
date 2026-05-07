---
title: "Debug"
order: 3
---

Now you do the debugging. Pick a buggy repo from the Canvas discussion, clone it, find the bugs, fix them. See how many repos you can fix before class ends.

## Pick a Repo

Open the Canvas discussion. Pick a repo that doesn't already have many "completed" comments on it. The goal across the class is for every team's repo to get fixed by at least one other team, so spread out instead of all piling onto the same one. When choosing the next repo, look for the ones with the fewest completions first.

> **With your partner:** Look at the discussion and pick your first repo together. Read the reproduction steps before you start so you know what symptoms you're hunting.

## Clone and Check Out the Buggy Branch

Clone the repo to a fresh folder on whichever machine you're driving from:

```bash
git clone <repo-url>
cd <repo-folder>
git checkout buggy
```

Use whatever branch name the team posted in their Canvas link. Then install dependencies and run the app:

```bash
npm install
npm run dev
```

Open the app in your browser and walk through the reproduction steps for each bug. Confirm you can see the actual buggy behavior they described. If something looks off and it's not in the steps, that's still a bug worth fixing, but make sure you can reproduce all the documented ones first.

## The One Rule

**Don't look at the git history or diffs.**

Don't run `git log`, don't open the GitHub commits view, don't compare the buggy branch to main. The whole point is to find and understand the bugs by reading the code and observing the behavior. Looking at the diff bypasses the entire exercise.

This is also closer to real debugging. Most bugs you encounter in your career won't come with a diff that highlights the broken line. You'll have a complaint from a user, an error in a log, and a working knowledge of the codebase. That's it. Today is practice for that.

## Find, Explain, Fix

For each bug, follow the same process from page 1:

1. **Reproduce.** Run through the steps until you've seen the bug with your own eyes.
2. **Observe.** Open the console. Open React DevTools. Look at the actual data flowing through. Read any error messages out loud.
3. **Hypothesize.** What in the code could produce this exact symptom? Be specific.
4. **Verify.** Check the suspected code. Add a `console.log` if you need confirmation. Inspect the component in DevTools.

Once you can explain the bug to your partner in plain language, fix it. Run the reproduction steps again to confirm the fix works.

> **With your partner:** Trade off who's driving every bug or two. The navigator's job is to slow the driver down when they start guessing. If your partner says "let me just try changing this," ask them what they think will happen and why. If they can't say, they're guessing.

### When you're stuck

If you've been on one bug for more than ten or fifteen minutes without progress, stick with it. Try these in order:

1. **Reset and re-observe.** Go back to step 1. Reproduce the bug with fresh eyes. Look at the console output you skimmed past the first time. Open a component in DevTools that you haven't opened yet. Often the thing you missed is sitting right there.
2. **Ask the team that planted the bug for a hint.** Walk over to them and tell them what you've already checked and what your current best hypothesis is. Ask for a nudge in the right direction, not the answer outright.

Still no peeking at the git history or the diff. A hint from the team is the way through if you need one.

## Mark Completion

When you've found and fixed every bug in a repo, post a comment on the original team's Canvas post saying you and your partner completed it. Include both names. Something simple is fine:

> Completed by Alex and Jordan.

This helps everyone see which repos still need a pair to take a crack at them.

You don't need to push your fixes anywhere. The fix lives on your own machine. The original team's repo stays as-is for the next pair.

Then pick the next repo from the discussion and start again.

## Goal

See how many repos you can successfully fix before the share-out at the end of class. Complete at least one. One fully understood repo is more valuable than three half-guessed ones. If you breeze through one, go grab another.

When picking your next repo, prioritize ones with the fewest completion comments. The point is for every team's repo to get fixed by at least one pair.

## Share-Out

We'll wrap class with a share-out. Each pair picks **the most challenging bug** from the repos you debugged and walks another team through it. Make sure to cover:

- **What was the symptom?** What did the app do that it shouldn't have?
- **What was the actual cause?** Show the line or two of code that was wrong, and explain why that produced the symptom you saw.
- **How did you find it?** What did you check, what did the console or DevTools tell you, what was the hypothesis that finally cracked it?

The "how did you find it" part is the most important one. Explaining your debugging path is what teaches the rest of the class something useful.

> **With your partner:** Before the share-out starts, agree on which bug you're going to walk through and rehearse the explanation between yourselves once. The bug you pick should be one where the diagnosis was interesting, not necessarily the trickiest fix.

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Full+Stack+Web+Development&unit=Debugging+Practice" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
