---
title: "Getting Set Up"
order: 2
---

You need two things before you can write code that calls an LLM:

1. An account with a provider that hosts LLM models.
2. An **API key** from that provider, which is a secret token your code uses to identify itself.

For this unit you'll use **GroqCloud**. Groq runs popular open models like Llama on extremely fast hardware, and they have a generous free tier that doesn't ask for a credit card. Faster responses mean less waiting when you're iterating on your code, which matters a lot when you're new to this.

> Quick clarification: **Groq** (the company you're signing up for) is different from **Grok**, the chatbot from xAI. Same pronunciation, different products. We're using Groq.

## Sign up for GroqCloud

1. Go to [console.groq.com](https://console.groq.com/) and create a free account.
2. Verify your email if asked.
3. In the sidebar, click **API Keys**, then **Create API Key**. Give it a name like "applied-ai-class."
4. Copy the key somewhere safe. **You will only see it once.** If you lose it, you can always make a new one.

The free tier is rate-limited (you can only send so many requests per minute), but it is more than enough for this unit. They should not ask you for a credit card during signup. If something is asking you to pay, you're probably on the wrong page.

## Treat your API key like a password

Anyone with your key can run requests on your account. Some basic hygiene:

- Don't paste it into chat, email, or screenshots you share with anyone.
- Don't commit it to GitHub. If you accidentally do, rotate the key immediately by deleting it in the Groq console and making a new one.
- For this unit you'll paste it into the Colab notebook directly, which is fine because your Colab is private. For real apps later in the quarter you'll move keys into environment variables.

## If you'd rather use a different provider

The notebook examples use Groq because it is free and fast. The patterns you'll learn are the same for every provider, and switching is mostly a matter of changing the client library and one or two parameter names. If you have a strong preference, you can substitute:

- **OpenRouter** ([openrouter.ai](https://openrouter.ai/)). Routes requests to many different models. They offer some free models you can use without a credit card.
- **OpenAI, Anthropic, Google, or any provider you already have access to.** You will need to swap out the `groq` Python client for theirs and adjust the model name. Ask me or your AI assistant for help getting the equivalent setup running.

If you go that route, keep up with the lesson conceptually, and translate the code into your provider's equivalent as you go.

> **With your partner:** Have either of you used an AI API before? If yes, what did you build? If no, what kind of small project would you want to try first? Hold onto that idea, you'll come back to it on page 6.

## Open the notebook

Open the example notebook here: [Chat, Memory, and Chains notebook (Colab)](https://colab.research.google.com/drive/1s2TK8G6FNQdFX1RZkeIH99GPwxxLdiJ4?usp=sharing).

In Colab, click **File → Save a copy in Drive** so you have your own editable copy. The rest of this unit walks through the notebook section by section, with explanations of what each part is doing and why. Keep both the notebook and these lesson pages open side by side as you work.

Once you have:

- A GroqCloud account
- An API key copied somewhere safe
- Your own copy of the notebook open in Colab

you're ready for page 3.
