---
title: Pair Programming
order: 3
---

## What It Is

Pair programming means two people, one keyboard, building something together. One person is the **driver**: they have the keyboard and are actively writing code. The other is the **navigator**: they're watching, thinking ahead, catching mistakes, asking questions, and guiding direction.

Both of you stay engaged in the same problem at the same time, so both of you understand it.

## Swapping Roles

You must swap roles regularly. Swap at least every 25 minutes, set a timer if you need to. Shorter swaps are also fine.

Swapping often keeps both people sharp and makes sure neither person is just along for the ride. The driver role forces you to translate understanding into actual code. The navigator role forces you to follow closely enough to catch what's wrong and explain what should come next. You need practice at both. 

The skill of technical communication is a large part of what you are trying to build.

## The Git Workflow

You both need the project cloned on your own machines before you start. Set this up at the beginning of each session.

When you swap, the driver commits and pushes their work. The new driver pulls before touching the keyboard.

```bash
# Driver (finishing their turn):
git add .
git commit -m "brief description of what was just built"
git push

# New driver (before taking the keyboard):
git pull
```

This keeps both names appearing in the commit history. At the end of a pair program, I should be able to look at your commits and see contributions from both people. If I only see one name, that's a problem.

Keep commit messages short and accurate. "added upgrade rendering" is fine. "did some stuff" is not.

## What the Navigator Should Be Doing

Navigating is active work. While the driver is writing, you should be:

- Reading ahead in the walkthrough so you know what's coming
- Catching typos and syntax errors before they turn into bugs
- Asking out loud when something doesn't make sense to you
- Suggesting what to try next
- Checking that you both understand each piece before moving on

If you're the navigator and you're lost, say so. That's exactly when you should slow down and talk it through together.

## Why This Matters

Explaining code out loud forces you to actually know it. You can read something and feel like you understand it and still be fuzzy on the details. The moment your partner asks "wait, why does that work?" you find out fast whether you really understood it or were just following along. That friction is where the learning happens.

Pair programming is also a real industry practice. Many teams use it for complex problems, onboarding, and review. Being able to sit down with another developer, think through a problem together, and communicate clearly about what you're doing is a skill that shows up constantly. This is practice for that.
