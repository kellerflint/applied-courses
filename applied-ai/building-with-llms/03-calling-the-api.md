---
title: "Calling the API"
order: 3
---

The first part of the notebook (cells 1 through 9) walks through the simplest possible interaction. You send a single message, you get a reply back. Run each cell as you read this page. The code snippets below are pulled from the notebook so you know what to look at.

## Install the client and bring it in

The Groq Python client is a small library that wraps the HTTP request to Groq's servers. You install it once per Colab session.

```python
!pip install groq
```

```python
from groq import Groq
```

Most providers ship a Python client like this. The library handles authentication, retries, JSON serialization, and other plumbing so you can focus on the prompt rather than the protocol.

## Drop in your API key

Paste your key into the `api_key` variable:

```python
api_key = ""  # Your API key here
```

This is fine for Colab where the notebook is private to you. Never push a notebook with a real key in it to a public GitHub repo. If you do, anyone who finds it can rack up usage on your account.

## The text-wrapping helper

Cell 5 defines a custom `print` function that wraps long lines. It is purely cosmetic so the AI's output doesn't run off the side of the Colab cell. You can ignore it.

## The generate_response function

This is the core of every call you'll make in this notebook.

```python
client = Groq(api_key=api_key)

def generate_response(messages, model="llama-3.1-8b-instant", max_tokens=150, temperature=0.7):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return chat_completion.choices[0].message.content
```

Three things to notice:

**`messages` is a list, not a single string.** Every modern chat API takes a list of message objects, each with a `role` ("system", "user", or "assistant") and a `content` (the text). You build that list up over time as a conversation grows.

**The function returns just the text content.** The API actually returns a much richer object that includes token counts, finish reasons, and other metadata. For most prompts you only care about the text, so the wrapper digs it out for you with `.choices[0].message.content`.

**The function takes parameters you can change per call.** `model`, `max_tokens`, and `temperature` are knobs you can turn on every request. We'll come back to each of those.

## Send your first message

Cell 9 calls the function in a tiny loop:

```python
for i in range(2):
    user_message = input("Enter a prompt")
    if user_message == "exit":
        break
    response = generate_response([{"role": "user", "content": user_message}])
    print(colored("AI:", "green"), response)
```

Run it. For your first message, type something like `Hi my name is Keller`. For your second, type `What is my name?`.

You'll see something like this:

```
You: Hi my name is Keller
AI: Nice to meet you, Keller. Is there something I can help you with?

You: What is my name?
AI: I don't have any information about your name. Our conversation just started...
```

The model answered the first message fine, but the second time it had no idea who you were. This is the "no memory between requests" behavior from page 1, now visible in real code.

Look closely at what gets sent on the second call:

```python
generate_response([{"role": "user", "content": "What is my name?"}])
```

The first message is gone. The list only contains the current message. The API has no way to know about the earlier exchange because you didn't include it. That's the entire mechanism for "no memory." It is not a limitation of the model, it is a consequence of what you chose to send.

You'll fix that on page 4 by building the message list up over time.

> **With your partner:** If the model has no memory but ChatGPT clearly seems to remember things across a conversation, what must ChatGPT (the product) be doing behind the scenes that ChatGPT (the model) isn't?

<details>
<summary>Reveal answer</summary>

The ChatGPT product stores your conversation in its own database. Every time you send a new message, the product packages up the whole conversation (or a trimmed-down version of it) and sends it to the model. The model only ever sees the current request, but the product makes it look like a continuous conversation by handling the history for you. That's the same pattern you're about to build.

</details>

## The parameters you control

The `model`, `max_tokens`, and `temperature` arguments on `generate_response` are the basic dials of every LLM call. You'll change them throughout the rest of this notebook for different jobs.

### Model

The notebook defaults to `llama-3.1-8b-instant`. The "8b" means 8 billion parameters, which is small for a modern LLM but plenty for chat and brainstorming. It is fast and free on Groq.

You can swap in larger models from the Groq console's model list when a task needs more reasoning power. Bigger models cost more (in money or rate-limit) and run slower, so you only reach for them when you need them. A common pattern is to use a small model for most steps in a chain and reserve the bigger model for the one step that really benefits from it.

### max_tokens

A cap on how many tokens the model can generate before it has to stop. If you set this too low, replies get cut off mid-sentence. If you set it too high, the model can ramble. Pick a value that matches the job. Around 150 tokens is fine for short chat replies. A few hundred is reasonable for an outline. Keep it tight when you can. You pay per token and short responses come back faster.

### temperature

The randomness setting from page 1, now as a number you can pass in. The notebook uses values between 0.5 and 0.9 depending on the step. Lower values make output more focused and repeatable. Higher values make it more varied.

Some quick guidance you can use as a starting point:

- `0.0` to `0.3`: deterministic answers, structured extraction, classification, "pick one of these options."
- `0.4` to `0.7`: general chat, explanation, normal writing.
- `0.8` to `1.0` and higher: brainstorming, creative writing, anything where variety is the goal.

You'll see the notebook use `0.9` during the brainstorm step of the chain example, then drop to `0.5` for the final summarization. Same model, very different jobs.

## Try a few prompts

Before you move on, take a few minutes and experiment.

> **With your partner:** Run the same prompt twice with `temperature=0.2`, then run it twice more with `temperature=1.1`. What changes between runs? Try a few different `max_tokens` values too. What does a very small value do to the output?

When you've got a feel for those dials, move to page 4 and we'll teach this thing to remember you.
