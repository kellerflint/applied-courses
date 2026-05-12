---
title: "Chains"
order: 5
---

You can ask one big question and get one big answer back. You can also break the work into a sequence of smaller asks, where each step uses the output of the previous step. That second approach is called a **chain**, and it's how a lot of the more reliable AI behavior is built.

This page maps to cells 17 through 20 in the notebook.

## Single-shot: ask for everything at once

Cell 18 is the "ask for everything at once" version. The prompt tells the model to brainstorm three story ideas, pick the best one, expand on it, outline it, and summarize it, all in a single response:

```python
one_shot_prompt = """
You are a creative and insightful storyteller. Your task is to create a compelling story by brainstorming, exploring, outlining, and summarizing the narrative in a structured and concise way. Follow these steps in your response:

1. **Brainstorm**: Generate three unique story ideas in different genres...
2. **Explore**: Pick the most interesting of the three ideas and expand on it...
3. **Outline**: Create a structured outline for the chosen story...
4. **Summarize**: Write a concise and engaging paragraph summarizing the story...
"""

chat = add_user_message(chat, one_shot_prompt)
response = generate_response(chat, model="llama-3.1-8b-instant", max_tokens=1000, temperature=0.8)
```

Run it. Read what comes back. It is fine. It does the four steps. It also has some real limitations baked in.

**You can't intervene.** The model picks one of its own brainstormed ideas without asking you. If you wanted to choose, you can't. The whole pipeline ran in one shot.

**Every step uses the same settings.** Brainstorming wants high temperature for variety. Summarization wants low temperature for focus. Single-shot has to pick one number and use it for all four steps.

**You can't swap models per step.** Maybe brainstorming runs fine on a small fast model, but the final summary really wants a smarter one. Single-shot can't do that.

**A long output spends its token budget across all four steps.** The brainstorm section might be detailed, then the outline gets cut short because there are no tokens left. You can't redirect attention to where it matters.

**Big asks usually go worse than small asks.** Asking a model to juggle many sub-tasks in one prompt is one of the most reliable ways to make every individual sub-task come out worse. Each thing the model is tracking competes for attention with every other thing. Chains let you focus the model on one well-defined job at a time. You also get to decide what context flows into each call, so you can hand step 3 the chosen idea and the expanded version, while leaving behind the two brainstormed options you rejected.

**Errors compound silently.** If step 2 picks a weird idea, every later step is built on that weird foundation, and you find out only at the end.

## Chains: do the steps one at a time

Cell 20 is the chain version. The same four jobs (brainstorm, explore, outline, summarize) are split across four separate API calls. The full code is in the notebook, but the structure of one step looks like this:

```python
step_1_prompt = (
    "Let's brainstorm story ideas. Please generate three interesting and unique story ideas "
    "in different genres. Be creative and ensure each idea is summarized in a single sentence."
)
chat = add_user_message(chat, step_1_prompt)
response = generate_response(chat, model="llama-3.1-8b-instant", max_tokens=200, temperature=0.9)
chat = add_ai_message(chat, response)
```

Then between steps, there's a `chosen_idea = input(...)` that lets a human pick which brainstorm to explore. Step 2 uses that input to build its own prompt:

```python
step_2_prompt = (
    f"I like {chosen_idea}. Can you expand on this idea? Describe the main plot points, "
    "the protagonist, and any other key details that will make this story interesting."
)
chat = add_user_message(chat, step_2_prompt)
response = generate_response(chat, model="llama-3.1-8b-instant", max_tokens=300, temperature=0.7)
chat = add_ai_message(chat, response)
```

Each step is its own API call with its own prompt and its own parameters. The same `chat` list is passed in every time, so each call sees the full history (just like the chat memory pattern from page 4). The activity below shows the whole chain visually so you can see the inputs and outputs lined up.

{% activity "chain-visualizer.html", "Single-shot vs chain", "880px" %}

## Why chains can be better

Splitting work into steps is more code than asking once, and you still pay for the same total tokens (sometimes more). The reasons to do it anyway:

**Each step gets its own settings.** Look at the four `generate_response` calls in cell 20. Temperature climbs to `0.9` for brainstorming and drops to `0.5` for the final summary. `max_tokens` is bigger in the middle steps where detail matters and tighter in the summary where you want concision. Single-shot can't do this. Chains do it naturally.

**A human can steer mid-stream.** The `input(...)` between step 1 and step 2 lets a person pick which idea to develop. You could just as easily run a different model, an automated check, or another LLM call there. Chains are where you wire in the human-in-the-loop and the deterministic logic that doesn't belong inside the prompt.

**You can swap models per step.** If step 3 needs heavier reasoning, run that one step on a bigger model. Keep the cheap fast model for the others. You can't do that in single-shot.

**Failures are catchable.** If step 2's output looks wrong, you see it right then, before step 3 builds on top of it. You can re-run that one step, tweak its prompt, fall back to a different approach, or ask the user. Single-shot only tells you something went wrong at the end, and the only fix is "run the whole thing again."

**You spend tokens where they matter.** Each step has its own `max_tokens` budget. The brainstorm gets enough to produce three real ideas. The outline gets enough to flesh things out. The summary stays tight on purpose.

## What a chain looks like in your head

You can describe most chains as a sequence of intent. The brainstorming chain in the notebook is roughly:

1. **Diverge.** Generate options. High temperature, short outputs, multiple ideas.
2. **Choose.** A human (or a rule, or another model) picks the most promising option.
3. **Develop.** Expand the choice into something more concrete. Medium temperature.
4. **Structure.** Turn the expanded version into a clear shape. Lower temperature.
5. **Compress.** Boil it down to its essential pitch. Low temperature, short output.

A lot of useful tools follow that general arc: diverge to gather options, narrow down, develop the choice, polish the result. Once you start seeing it, you'll notice that single-shot prompts often work because the model is doing all of that internally in one pass. Chains make it explicit, controllable, and inspectable.

> **With your partner:** Pick a task you'd reasonably ask an AI to do (write a unit test, generate study questions from notes, plan a trip, debug an error, anything). Sketch what the chain would look like as a numbered list of steps. For each step, name what kind of output it produces and roughly what temperature you'd want.

Bring your sketch to page 6. That's where you'll build one for real.
