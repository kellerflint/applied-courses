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

You can think of the whole process as a sophisticated autocomplete. The model looks at the text so far, predicts what's likely to come next, and commits to it. One detail of this commit matters a lot when you're building with LLMs. **Once a token has been generated, the model cannot go back and change it.** Every new token is just appended to what came before. That's part of why a model will sometimes commit to a wrong opening (start an answer with "Yes" when the right answer was "No," or with a misread of your question) and then spend the rest of the response trying to justify it. The only move the model has is to keep going.

## Pattern matching, not understanding

The model picked up everything it knows from the patterns in its training data, mostly text scraped from the internet plus follow-up training that nudges it toward being helpful and safe. What it learned during that training is how words relate to other words. It learned which words tend to follow which other words, what an argument structure looks like, what a polite email sounds like, what working Python code looks like. The actual concepts behind those words, the things in the real world the text was describing, mostly didn't come along for the ride. The model has the patterns. It has the meanings only as far as the patterns reveal them.

That distinction matters a lot. The same model that can produce a clean, coherent essay on a topic might completely botch the execution on that exact same topic. It can fluently explain how to solve a problem and then fumble the actual solving. It often understands the relationships between concepts without necessarily understanding the concepts themselves.

Imagine someone learning a foreign language by reading a huge amount of it without ever being told what any of the words actually mean. They could still pick up which words tend to appear together, which structures are well-formed, what arguments tend to look like. They could probably start producing fluent-looking text. That fluency would not mean they understood the underlying reality the text was describing.

That said, this picture can undersell what LLMs are capable of. Language can describe almost anything, which means a system fluent in language can do useful work on almost any topic. Linguistic pattern matching, combined with the right tooling around it, has turned out to be enough to build genuinely impressive systems. The piece worth holding onto is what a confident-sounding answer actually tells you. **A model's confidence reflects how typical-sounding the answer is, which usually overlaps with whether it's correct, but is not the same thing.**

## Implications you need to carry into the rest of this unit

Once you accept that an LLM is "predict the next token" in a loop, several useful facts fall out.

### The model has no memory between requests

The model is a function. You give it text, it gives you text back. The next time you call it, it starts fresh with whatever text you send. It does not remember the last conversation. It does not remember you.

Every chatbot you have ever used handles this the same way. The app stores the conversation, and on every new message it sends the entire conversation history back to the model so the model has the context it needs to reply. The "memory" lives in the app rather than the model. You will build exactly this pattern on page 4.

### The model generates, it does not look up

The model produces text by extending patterns rather than retrieving stored facts. None of its training data is sitting in there verbatim waiting to be quoted. When the model writes an answer, it is making one likely next token after another based on the patterns it learned.

That's why LLMs can produce confident-sounding text that turns out to be wrong. The technical term is **hallucination**, and mechanically it works the same as every other output the model produces. The model picks the most plausible next token. When the resulting sentence happens to be a factual claim, plausible and correct sometimes line up and sometimes don't. When you build with LLMs, you assume any factual claim could be wrong and you design around it.

### There is a hard limit on input size

The model can only consider so much text at once. That limit is called the **context window**. Tokens that fall outside the window simply do not influence the output. Different models have different limits, ranging from a few thousand tokens to over a million.

This matters because chat history grows. A conversation that runs long enough will eventually overflow the window, and you will have to decide what to keep and what to drop. You'll see two common strategies for dealing with that in this unit.

### Temperature controls randomness

You can tell the model how adventurous to be when picking tokens. Low temperature means it almost always picks the top-ranked token, so output is repeatable and conservative. High temperature flattens the probabilities so lower-ranked tokens get picked more often, and output gets more varied and surprising.

Different jobs want different temperatures. You want low temperature for things like summarization, classification, or pulling structured data out of text. You want higher temperature for brainstorming, creative writing, or anything where the same answer every time would be boring.

## Why this matters for the rest of the unit

Everything you're about to build is a workaround for what the model can't do on its own.

- The model has no memory, so you'll build memory by collecting and sending the whole conversation each turn.
- The context window is finite, so you'll trim or summarize the history as it grows.
- Each call produces a fixed kind of output, so when you need a more sophisticated result you'll **chain** multiple calls together and pass each one's output into the next.

If any of that feels abstract right now, that's fine. The next pages turn each of these ideas into code you run.

> **With your partner:** Think about a chatbot you have used recently. What evidence have you seen that it remembers earlier parts of the conversation? Does it ever seem to forget? What might be happening behind the scenes in each case?
