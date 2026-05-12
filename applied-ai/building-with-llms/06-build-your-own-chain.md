---
title: "Build Your Own Chain"
order: 6
---

Pair up. You're going to design and build a small chain together, then submit it.

## The assignment

Pick a problem that benefits from multiple steps. Build a chain of at least **three LLM calls** in a Colab notebook that solves it. You're welcome to start from the example notebook as boilerplate. Copy any of the helper functions you find useful and replace the story-generation chain with your own.

You don't need a polished product. You need a working chain that does something more interesting than a single prompt could do alone, and that demonstrates the ideas from this unit.

## Pick a problem worth chaining

You're looking for something that has natural phases. A few prompts that work well:

- **Tech troubleshooter.** Step 1 gathers symptoms (what's broken, what they tried). Step 2 proposes the three most likely causes. Step 3 takes the user's "the second one matches" and produces step-by-step instructions for that specific cause.
- **Study buddy.** Step 1 takes a chunk of class notes and pulls out the key concepts. Step 2 turns each concept into a flashcard. Step 3 generates a short quiz over the flashcards.
- **Recipe adapter.** Step 1 reads a recipe. Step 2 asks the user what dietary restrictions or substitutions they need. Step 3 rewrites the recipe with those substitutions and explains what changed.
- **Bug report polisher.** Step 1 takes a messy bug report. Step 2 asks clarifying questions. Step 3 produces a clean rewrite in the style your team expects.
- **Trip planner.** Step 1 brainstorms destinations from constraints (budget, duration, vibe). Step 2 picks one and proposes a day-by-day outline. Step 3 turns the outline into a packing list.
- **Code reviewer.** Step 1 reads a function and lists potential issues. Step 2 picks the most important issue and explains it in detail. Step 3 proposes a specific fix.

Or come up with your own. The bar is whether a single prompt would do a worse job than splitting it into steps.

## Requirements

Your chain must include:

1. **At least three sequential LLM calls,** where later calls use information produced (or selected) by earlier calls.
2. **At least one place where a human or your code intervenes between calls.** That can be an `input(...)` prompt, a Python parsing step, or a hard-coded routing decision based on the previous output.
3. **At least two different parameter configurations across steps.** For example, a higher `temperature` on a brainstorm step and a lower one on a summarization step. Or different `max_tokens` budgets. Or different models.
4. **A short markdown cell at the top** that says (in 3-5 sentences) what your chain does, who it's for, and why a chain is a better fit than a single prompt.

The notebook should run top to bottom without errors. Make sure your API key is in a clearly labeled cell that a reader can replace with their own.

## How to work as a pair

You'll be more productive if you do this part together, not divided.

**First 10 minutes.** Talk only. No code. Sketch the chain on paper or in a markdown cell: what does each step take as input, what does it return, what parameters does it use, where does the human or code intervene. Don't write any prompts until you have the shape of the whole thing.

**Then alternate driver/navigator.** Whoever isn't typing is reading along, watching for issues, and thinking about the next step. Swap every step or every 10 minutes. Pair programming only works when both of you actually engage with what's happening on screen.

**Test as you go.** Get step 1 working in isolation before you write step 2. Get step 2 working before you write step 3. Don't build the whole chain at once and try to debug it as a unit.

**Use AI to help you build it.** This is allowed and expected. You can ask Claude, ChatGPT, or Copilot for help with syntax, prompt design, or debugging. The standard from the syllabus still applies: you have to be able to explain every line of what you submit. If I (or your partner) asks "why does this step use temperature 0.3?" you should have an answer.

## Submit

Once your chain works:

1. In Colab, click **Share** in the top right.
2. Under "General access," change it to **"Anyone with the link"** and set the role to **Viewer**.
3. Copy the link.

**Both partners submit individually on Canvas** with the shared notebook link. Put both partner names in the submission comment so I can find the pair.

## A small encouragement

This is the first time most of you have called an LLM from code. The mental model from page 1 (predict the next token, no memory, finite context), the messages list pattern from page 4, and the chain pattern from page 5 are the foundation of essentially every LLM-powered app you'll see in industry. The frameworks people use (LangChain, the OpenAI Assistants API, Anthropic's Claude SDK, agent frameworks) all sit on top of these same ideas. Once you've built a chain by hand, those frameworks become much easier to read because you already know what they're abstracting over.

Have fun with it.

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Applied+AI&unit=Building+with+LLMs" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
