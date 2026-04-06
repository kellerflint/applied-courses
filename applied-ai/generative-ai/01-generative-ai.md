---
title: "Generative AI"
order: 1
---

Generative AI creates new content based on patterns it learned during training. Text, code, images, video, audio, 3D models. If you've used ChatGPT, Claude, DALL-E, or Midjourney, you've used generative AI.

Text-based generative AI runs on Large Language Models (LLMs). This page covers how they actually work.

## Autocomplete at Scale

LLMs are trained to predict the next most likely word given everything that came before it. That's the core mechanism. Word by word, token by token, it builds a response.

The reason this works so well is scale. Trained on most of the internet, a model sees so many examples of how words relate to each other that it can produce coherent, accurate-sounding text on almost any topic.

The reason it fails is also scale. The model predicts words based on patterns. It does not reason from an understanding of the world. Give it a familiar pattern and it performs well. Put it in a novel situation that doesn't match its training data and it will confidently generate something wrong.

That's how you get a model that can write your entire lab report one minute and can't understand the punchline of a joke the next.

## How LLMs Are Trained

Training happens in two stages:

1. **Self-supervised learning.** The model reads massive amounts of raw text and learns to predict the next word. No human labels are needed. Doing this billions of times builds a general understanding of language and the relationships between concepts.

2. **Reinforcement Learning from Human Feedback (RLHF).** Humans rank the model's outputs. Those rankings steer the model toward more helpful, accurate, and safe responses. This is the step that turns a raw word-predictor into something you'd want to talk to.

## Tools to Try

- <a href="https://gemini.google.com/" target="_blank">Gemini</a> - Google's AI assistant
- <a href="https://claude.ai" target="_blank">Claude</a> - Anthropic's AI assistant
- <a href="https://openrouter.ai/" target="_blank">Open Router</a> - access to many different LLMs in one place
- <a href="https://gamma.app" target="_blank">Gamma</a> - AI-powered presentation maker
- <a href="https://console.groq.com/playground?model=whisper-large-v3-turbo" target="_blank">Groq Playground</a> - fast audio transcription with Whisper

> **With your partner:** Pick a tool you haven't used before and spend a few minutes with it. What does it do well? Where does it fall apart? Try to find the edges.
