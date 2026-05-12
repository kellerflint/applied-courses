---
title: "Chat & Memory"
order: 4
---

You proved on page 3 that the API has no memory between calls. This page shows the standard fix. Your app keeps the conversation in a list, and on every new turn it sends the whole list back to the API. Cells 10 through 16 in the notebook are what we're walking through here.

## The pattern: messages accumulate in a list

The whole "memory" trick is that the `messages` argument is a list. If you keep appending to it as the conversation grows and send the full list on every call, the model sees the whole conversation each turn. Three small helpers do all the appending:

```python
def add_user_message(messages, user_message):
    messages.append({"role": "user", "content": user_message})
    return messages

def add_ai_message(messages, ai_message):
    messages.append({"role": "assistant", "content": ai_message})
    return messages

def add_system_message(messages, system_message):
    messages.append({"role": "system", "content": system_message})
    return messages
```

Each one tacks one more dictionary onto the list with the correct `role`. The roles matter because the model uses them to figure out who said what.

**user** is the human talking to the model. **assistant** is the model's own previous replies. **system** is the high-priority instruction that sets the assistant's behavior (typically the first message in the list). The activity below shows what this list actually looks like as a chat grows.

{% activity "messages-array-inspector.html", "What you send to the API", "640px" %}

The conversation you see on screen and the list of dictionaries sent to the API are two views of the same thing. When you want the model to "remember" something, you keep that something in the list.

## The chat_with_ai helper

Cell 11 wraps the loop you'd otherwise write out by hand:

```python
def chat_with_ai(chat, user_message):
    chat = add_user_message(chat, user_message)
    response = generate_response(chat)
    chat = add_ai_message(chat, response)
    return chat
```

One call does all three things: append the user message, send the whole list to the API, append the model's reply. The returned `chat` is now one user/assistant turn longer than when you started.

## Run the chat loop

Cell 13 is a small REPL that uses the helper:

```python
chat = []
chat = add_system_message(chat, "You are a helpful assistant.")

while True:
    user_message = input("Enter a prompt: ")
    if user_message == "exit":
        break
    chat = chat_with_ai(chat, user_message)
```

Tell it your name. Ask it what your name is. This time it will know. Type `exit` to leave the loop, then print `chat` and read through it. Every turn is in there. That is the memory.

> **With your partner:** Compare cells 9 and 13 in the notebook. Cell 9 forgot your name and cell 13 didn't. The model didn't change. The function calling the model didn't change. What's the one structural difference between them, and why does it produce such different behavior?

<details>
<summary>Reveal answer</summary>

Cell 9 builds a fresh single-message list for every call. Cell 13 holds onto one growing list across turns and passes it back every time. Same model, same `generate_response`, completely different behavior, all because of where the message list lives. This is the entire trick to chat memory.

</details>

## What about long conversations?

Once you start storing everything, you bump into a real constraint: the **context window** from page 1. Every token in your messages list counts against the model's input limit, and you also pay for those tokens on each call. A long conversation will eventually overflow or get too expensive to keep sending in full.

There are two common strategies. The notebook shows both.

### Strategy 1: sliding window

Keep only the most recent N messages and drop the rest. Cell 14 implements a basic version that trims messages until the total character count falls under a limit:

```python
def maintain_window(chat, max_char=200):
    current_token_count = sum(len(msg['content']) for msg in chat)
    while current_token_count > max_char and len(chat) > 1:
        removed = chat.pop(1)  # Remove the oldest message
        current_token_count -= len(removed['content'])
    return chat
```

Notice it pops from index `1`, not `0`. That preserves the system message at the top while throwing away the oldest user/assistant turns. The example in cell 14 runs through a few messages, calls `maintain_window`, then asks "Do you remember my name?" The model has no idea, because the message where the user said their name has been dropped from the list.

That's the tradeoff. Sliding windows are cheap and simple, but they cause the assistant to forget things that fell off the back of the list. Use this when the recent context is all that matters (think a focused coding session, or a step in a workflow where earlier details don't apply anymore).

### Strategy 2: summarization

A more sophisticated approach is to compress instead of drop. When the conversation gets long, ask the model to summarize what happened so far and replace the old messages with that summary. Cell 16 does exactly that:

```python
def summarize_context(chat):
    summary_prompt = "Summarize the following conversation concisely:\n" + "\n".join(
        f"{msg['role']}: {msg['content']}" for msg in chat
    )
    summary = generate_response([{"role": "user", "content": summary_prompt}])
    return [{"role": "system", "content": "Summary of prior conversation: " + summary}]
```

The function flattens the existing conversation into a single string, sends it through the model with a "summarize this" prompt, then returns a new messages list that contains only the summary. The next time you call the model, it sees a compressed version of the history instead of the full transcript.

Run cell 16 and watch the difference. After summarization, the model still knows the user's name is Joe because that fact survived the summarization step. Compare that to the sliding-window run on cell 14, where the same question got "I don't know."

The trade is that summarization costs an extra API call (and some tokens worth of input/output), and the model is the one deciding what is important to keep. Sometimes it drops details you actually wanted. There is no perfect answer. Real apps usually combine strategies: keep the last few messages verbatim, summarize everything older.

> **With your partner:** Think about an app you might build (a tutor, a customer support bot, a coding pair). Which strategy fits better, and what would each of them get wrong in your scenario?

## Wrap-up

You now have two important pieces of the puzzle:

- The model is stateless, and you make a chat by sending a growing list of messages.
- Once that list grows too large you either trim it or compress it.

Both pieces show up in basically every real LLM app. Next, on page 5, you'll use these same tools to do something more ambitious than a single chat reply.
