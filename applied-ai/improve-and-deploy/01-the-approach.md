---
title: "The Approach"
order: 1
---

Last time you built a digit recognizer. The model worked, but accuracy left room for improvement. This unit takes a different approach to getting there.

You'll use AI to build a better training pipeline, then deploy the model to a web server. The goal is to practice directing AI to build something specific, verifying each step as you go, and understanding what you built well enough to explain it.

## The full pipeline

Here's everything you'll build across this unit. Click each step to see what it does and why.

{% activity "training-pipeline.html", "Training Pipeline Overview", "560px" %}

> **With your partner:** Before reading ahead, click through each step. Which parts are familiar from previous units? Which ones are new?

## How to work with AI on this

You'll use an AI assistant to write most of the code. That's intentional. The skill being practiced is knowing what to ask for and how to verify that you got it.

**Build in steps.** Ask AI for one piece at a time. Prompting for an entire training notebook at once gives you something that mostly works and is very hard to debug. Prompting for one function at a time gives you something you can test immediately.

**Read what it gives you.** Before running any AI-generated code, read through it. Do you understand what it does? Does it match what you asked for? AI will confidently produce code that looks correct but has subtle bugs. Reading first catches most of them.

**Verify before moving on.** Several steps include verification code. Run it. Look at the output. Confirm the data looks right before continuing. A bug in preprocessing can cause training to fail silently and produce misleading results that are hard to trace later.

## AI tools

Use whatever you have access to. ChatGPT, Claude, and Google Gemini all work well for this kind of task. Gemini has a free tier available to students if you need one.
