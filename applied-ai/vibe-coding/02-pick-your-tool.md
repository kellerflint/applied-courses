---
title: "Pick Your Tool"
order: 2
---

You'll be working through an **agentic editor**. That's an AI that lives inside your project, reads and writes your files directly, and runs commands like building and testing on its own. It's a step beyond a chat window where you copy code back and forth. You describe what you want, and the agent edits the actual files and tells you what it did.

## Your options

Any of these work. Use whatever you already have access to.

**Claude Code** (Sonnet or Opus). In my experience these are the strongest models available right now for this kind of work. They are not free, so use it only if you already pay for it or have credits.

**GitHub Copilot** in VS Code. You may already have access through GitHub's student benefits, and the agent mode is solid.

**Cursor.** A popular standalone agentic editor. Word is they offer a free student plan, so it's worth checking whether you qualify.

**Antigravity.** This is a good option if you don't already pay for one. You get a decent amount of use of their fast Flash model for free, plus a smaller allowance of their smarter models.

## A note on burning through your allowance

If you're on a free tier, the smarter models typically burn through your token allowance much faster and take a long time to refresh. Mostly stick with the fast model. Save the expensive one for a moment where the fast model is genuinely stuck and you need a stronger reasoning pass to break the loop.

You can always switch editors as well. There's no reason you couldn't use Copilot until you run out of tokens and then swap over to Antigravity, for instance.

## Get set up

1. Install your chosen editor and sign in.
2. Make an empty folder for your project and open it in the editor.
3. Initialize Git right away with `git init`. You want version control in place before the first line of code exists, so every working state can be saved.

## Let the agent install the rest

Installing Rust and scaffolding a Bevy project is the agent's job, and watching it do this is your first read on how it behaves. You don't have to know how to do any of it yourself.

Tell it your operating system and ask it to walk you through installing Rust and creating a minimal Bevy project that opens a window. Ask it to explain each command before you run it.

The one thing worth knowing yourself: the official Rust installer lives at **rustup.rs**. If the agent points you somewhere else to install Rust, stop and check. You should never paste a random install command from an AI into your terminal without knowing what it does and where it came from.