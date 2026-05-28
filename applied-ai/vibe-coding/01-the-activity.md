---
title: "The Activity"
order: 1
---

Today you're going to vibe code. You'll point an AI agent at a problem, describe what you want, and let it write the code while you steer. The agent is your coding partner here. You'll still pause to compare notes with the person beside you, but the one writing the code is the AI.

You're going to build a small game in **Bevy**, a game engine written in **Rust**. You almost certainly don't know Rust, and you almost certainly don't know Bevy. That's the point. You're going to find out how far you can get building something real in a stack you can't read fluently, with an agent doing the typing.

## Why a game in Bevy

This setup was picked on purpose to show you something specific about working with agents.

**It's all code.** Engines like Unity and Godot expect a lot of work to happen in a visual editor by dragging things around. An agent can't drag things around an editor for you. Bevy is pure code, so the agent can actually do the whole job, and you get a clean read on what it can and can't do when nothing is hidden behind a UI.

**Games expose weaknesses fast.** Visual, interactive, real-time software is unforgiving. A web form either submits or it doesn't. A game has motion, collisions, timing, and feel, and there are a hundred ways for it to look almost right and be subtly broken. Depending on what you build, you'll hit the agent's limits quickly, and that's exactly what we want you to see.

**Rust is unfamiliar to you.** When you build in a language you know, you can't tell where your skill ends and the agent's begins. Here you have almost no skill to lean on, so what you're left watching is the raw capability of the tool.

> **With your partner:** Before you start, write down one prediction. What part of building a game do you think the agent will handle easily, and what part do you think will break? You'll check these against reality at the end.

## The rules

**Start with an MVP, then build up.** Get the smallest possible thing on screen first. A square that moves. Then add one feature at a time. Asking the agent for a whole finished game in one prompt produces a pile of code that looks plausible and falls apart the moment you run it.

**Use Git, and commit the moment something works.** This one is not optional. Agents are notorious for breaking everything out of nowhere, confidently rewriting a working file into a broken one. The instant you get something running, commit it. That commit is your save point. When the agent wrecks the next thing, you can get back to solid ground instead of losing your afternoon.

**Make something original.** Pick your own idea, or put a real twist on something familiar. Don't build Snake or Flappy Bird or Pong. Those games have so much public code that the agent was trained on huge amounts of it, so it'll breeze through them and you'll learn nothing about its actual limits. A weird, specific, personal idea is where the agent starts to struggle, and the struggle is the lesson.

> **With your partner:** Pitch each other your game idea in two sentences. Is it specific enough that the agent can't just recite a tutorial? If it sounds like a classic game, twist it until it doesn't.

## If Bevy fights you

Claude (Sonnet or Opus) and similar frontier models do reasonably well with Bevy and Rust. Smaller or cheaper models often don't, and you may find yourself stuck in a loop where nothing compiles.

If that's where you land, switch to a full-stack web app instead. Agents handle web stacks more reliably. To keep the spirit of the activity, **pick a stack you don't know**. Try Angular, Vue, or HTMX on the frontend, and FastAPI, Flask, or Spring Boot on the backend. The goal is the same: build something real in tools you can't read fluently, and watch how the agent does.

Make the call early. If you've burned 30 minutes and have nothing that runs, switch. Don't spend the whole session fighting the compiler.

## What you'll walk away with

By the end you'll have a janky, half-working, possibly delightful game (or app), a Git history showing how it got there, and a set of observations about how the agent behaved. Those observations are the real deliverable. You're learning to read the tool so that later, in stacks you actually know, you can direct it far better than someone who's only ever trusted it blindly.
