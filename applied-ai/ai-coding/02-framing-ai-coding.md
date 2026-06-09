---
title: "Framing AI Coding"
order: 2
---

This unit is going to present a framework for agentic coding. It will discuss when you should hand work to an agent, how much to lean on it, and how to verify what it builds.

This is a current read on a fast-moving tool. The field is only a few years old, the tooling moves fast, and something next year could change the math. The patterns here are what hold up across the subset of tools available today, and probably for at least the next few years.

## What "AI coding" means here

When this unit says AI coding, it means **agentic coding** specifically. You develop real software by directing an agent that builds the tool at whatever scale, with you guiding it the whole way. Tools like Claude Code, Antigravity, and Copilot are what we're talking about.

That's narrower than "using AI to help you code." Using AI as a smarter search engine, or copy-pasting a snippet into ChatGPT and pasting the answer back, is a different use case. The interesting question is what happens when the agent is the one writing and changing the software itself while you step back to direct.

## The debate

Arguments about AI coding can sometimes sound like "is AI better or worse than a human," or "pure agentic versus pure manual," or "who wins." Almost nobody actually operates in either pure form, and the purists at both ends are probably wrong.

**The pure-manual purist** refuses to let AI touch anything. There is almost certainly somewhere it would add real value, and they're leaving that on the table.

**The pure-agentic believer** says no human direction is needed and expertise is mostly irrelevant, just let the agent run. Anyone making that claim hasn't built anything at real scale.

The truth lives in between, and that's where this unit aims. The useful is reading where a specific task sits and deciding how to work with the agent on it.

## The three layers

The rest of this unit is built around three questions you ask about any task.

1. **Suitability.** Is this task a good fit for an agent at all?
2. **Usage.** How much do you lean on the agent?
3. **Verification.** How do you confirm the output actually works?
