---
title: "Introduce Bugs"
order: 2
---

You and your partner will pick one of your earlier React pair programs, deliberately break it in 2-3 places, and post the broken version on Canvas for another team to fix.

You have **25 minutes** for this part. The actual debugging happens after.

## Pick a Project

Pick any React project you and your partner built together earlier this quarter. Anything that uses React works. Skip the very first project or two, those are too small to hide a bug well. Something with multiple components and some state is ideal.

> **With your partner:** Decide which repo you're using and pull the latest version on the machine you're going to use to introduce the bugs.

## Make a New Branch

You're not breaking the main branch. You're committing the bugs to a separate branch so the original code stays intact.

```bash
git checkout -b buggy
```

Use whatever branch name you want. `buggy`, `bugs`, `debug-me`, anything that's clearly the broken version.

Confirm you're on the new branch:

```bash
git branch
```

The asterisk should be on the buggy branch, not on `main`.

## Introduce 2-3 Bugs

This is the creative part, and the part where the constraints matter most.

### The rules

**Each bug is one or two lines of changes, max.** You're not allowed to nuke a whole file or rip out a component. The bug has to be a small, surgical edit that another team could plausibly find and reverse.

**Avoid simple typos.** Renaming `useState` to `useStaet` is too easy to spot. The interesting bugs are the ones that look like reasonable code but produce wrong behavior.

**Prefer logic bugs over crashes.** A bug that makes the app crash with a clear error message is fine, but the better bugs change what the app does without obviously breaking it. The kind of bug another team has to actually read your code to find, instead of jumping straight to a stack trace.

**Most bugs should be in `.jsx` files.** That's where React logic lives, and that's the most useful surface to practice on. CSS is fair game for at most one of your bugs, and only if the bug is actually interesting. One boring CSS bug doesn't teach anything, so make it count or skip it.

**No invisible bugs.** The buggy behavior has to be observable when you run the app. If a team can't see anything wrong, they can't find it.

> **With your partner:** Look through your project together and brainstorm where you could plant something. Don't reach for a generic recipe. Look at what your app actually does and find the spots where a small change would produce surprising behavior. Pick two or three that feel like a good puzzle.

### Make the changes

Open the files. Make the edits. Save.

Run the app locally and confirm each bug actually shows up the way you expect. If you planted a bug and the app behaves the same as before, the bug is invisible and another team won't be able to find it. Adjust until each one is observable.

Take a moment to write down, just for your own reference, what each bug is and what it does. You'll need this in a minute when you write reproduction steps, and you'll also need it at the end of class if your bug is the one your pair walks another team through.

## Commit and Push

Commit the bugs to your branch and push it to GitHub.

```bash
git add .
git commit -m "introduce bugs for debugging activity"
git push -u origin buggy
```

The `-u origin buggy` part sets up the remote tracking the first time. After this you can just `git push`.

> **With your partner:** Open the branch on GitHub in your browser. Confirm the buggy branch is visible and that the commit is there. Copy the URL of the branch (the URL bar should look something like `github.com/your-name/your-repo/tree/buggy`).

## Post to Canvas

Open the Canvas discussion for this activity and create a new post. Your post should include:

1. The link to the buggy branch on GitHub.
2. Reproduction steps for each bug, written like a real bug report.

A real bug report has three parts. Use this template for each bug:

> **Steps to Reproduce:**
> 1. [first action]
> 2. [next action]
> 3. [final action that triggers the bug]
>
> **Expected Result:** What should happen when those steps are followed.
>
> **Actual Result:** What actually happens when the bug is in place.

The point of writing it this way is so another team can follow the steps, observe the bug, and confirm they're hunting the right thing. Vague descriptions ("something's wrong with the buttons") don't tell them what to look for and waste their time.

**Do not** explain what's actually wrong, where the bug is in the code, or how to fix it. The whole point is for the other team to figure that out themselves.

> **With your partner:** Read each other's reproduction steps before posting. Could a stranger follow them without your help? Does each one clearly distinguish what should happen from what does happen?

Once your post is up, head to the next page.
