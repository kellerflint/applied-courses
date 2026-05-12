---
title: "How LLMs Work"
order: 1
---

This unit is your first hands-on lesson using **Large Language Models** (LLMs) in code. By the end of it you will have called an LLM from a Python notebook, given a chatbot memory, and chained multiple model calls together to do something none of them could do alone.

Before you write any of that code, you need a working mental model of what an LLM actually is. A lot of the design decisions in the rest of the unit (why you have to manage chat history yourself, why splitting work into steps produces better results, why the model sometimes confidently makes things up) only make sense once you understand the basic mechanism.

## The basic mechanism: predict the next token

An LLM does one thing. It looks at everything it has seen so far and predicts what the next **token** should be. A token is usually a word or piece of a word. The model produces a probability for every token in its vocabulary, picks one, adds it to the output, and runs the whole process again with the new token included.

That's it. Every paragraph ChatGPT has ever written was produced by that loop.

The activity below shows the loop in slow motion. Start the playback, watch the probability bars on the right update at each step, then speed it up.

{% activity "genai-token-predictor.html", "How an LLM generates text", "600px" %}

> **With your partner:** The model always picks the top-ranked token in this demo. What would happen to the writing style if the model picked a lower-ranked token sometimes? What would happen if it always picked the lowest-ranked token?

<details>
<summary>Reveal answer</summary>

Picking only the top token every time produces text that sounds correct but is repetitive and boring. It plays it safe at every step. Real models add some randomness so the output stays varied and interesting.

Picking the lowest-ranked token at every step produces nonsense. The model's probabilities encode what makes a sentence coherent, so steering away from them breaks the output.

Most production models sit somewhere in the middle, controlled by a setting called **temperature** that you'll use directly later in this unit.

</details>

## Implications you need to carry into the rest of this unit

Once you accept that an LLM is "predict the next token" in a loop, several useful facts fall out.

### The model has no memory between requests

The model is a function. You give it text, it gives you text back. The next time you call it, it starts fresh with whatever text you send. It does not remember the last conversation. It does not remember you.

Every chatbot you have ever used handles this the same way. The app stores the conversation, and on every new message it sends the entire conversation history back to the model so the model has the context it needs to reply. The "memory" lives in the app rather than the model. You will build exactly this pattern on page 4.

### The model generates, it does not look up

LLMs were trained on huge piles of text. During training they picked up patterns: which words go together, what arguments look like, what code looks like, what a polite email sounds like. None of that text is stored verbatim. When the model writes an answer, it is generating one likely next token at a time based on those patterns.

That's why LLMs can produce confident-sounding text that turns out to be wrong. The technical term is **hallucination**. The model is doing the same thing it always does (picking plausible next tokens) but plausible is not the same as correct. When you build with LLMs, you assume any factual claim could be wrong and you design around it.

### There is a hard limit on input size

The model can only consider so much text at once. That limit is called the **context window**. Tokens that fall outside the window simply do not influence the output. Different models have different limits, ranging from a few thousand tokens to over a million.

This matters because chat history grows. A conversation that runs long enough will eventually overflow the window, and you will have to decide what to keep and what to drop. Page 4 shows two common strategies for that.

### Temperature controls randomness

You can tell the model how adventurous to be when picking tokens. Low temperature means it almost always picks the top-ranked token, so output is repeatable and conservative. High temperature flattens the probabilities so lower-ranked tokens get picked more often, and output gets more varied and surprising.

Different jobs want different temperatures. You want low temperature for things like summarization, classification, or pulling structured data out of text. You want higher temperature for brainstorming, creative writing, or anything where the same answer every time would be boring.

## Why this matters for the rest of the unit

Everything you're about to build is a workaround for what the model can't do on its own.

- The model has no memory, so you'll build memory by replaying the whole conversation each turn.
- The context window is finite, so you'll trim or summarize the history as it grows.
- Each call produces a fixed kind of output, so when you need a more sophisticated result you'll **chain** multiple calls together and pass each one's output into the next.

If any of that feels abstract right now, that's fine. The next pages turn each of these ideas into code you run.

> **With your partner:** Think about a chatbot you have used recently. What evidence have you seen that it remembers earlier parts of the conversation? What evidence have you seen that it doesn't? What might be happening behind the scenes in each case?
