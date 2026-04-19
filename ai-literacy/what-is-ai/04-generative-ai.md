---
title: "Generative AI"
order: 4
---

**Generative AI** uses deep neural networks to create new content: text, images, code, audio, video. ChatGPT generates text. DALL-E and Midjourney generate images. Suno generates music. All of them are generative AI.

The core mechanism behind a text generator is simpler than it sounds. The model predicts the next word (technically the next **token**) based on everything it has seen so far. It adds that token to its output and predicts the next one. Then the next. Over and over until it stops.

The activity below shows that process step by step. Watch the probability bars on the right update as each new token is chosen. Start slow so you can see what's happening, then speed it up.

{% activity "genai-token-predictor.html", "How an LLM generates text", "600px" %}

Every word you've ever read from ChatGPT was produced by roughly the same loop, running on a much bigger model with many more possible tokens at each step.

> **Reflect:** The model picks the highest-probability token each time. What would happen if it always picked the most predictable word? Why might that produce boring or repetitive output?
