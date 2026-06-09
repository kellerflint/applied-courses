---
title: "Layer 3: Verification"
order: 5
---

The first two layers were dials you set per task. This one is different. Verification sits underneath everything as a step you never skip, and it's the most important thing you do in agentic workflows.

## Why an agent is bad at verifying itself

**It has poor tools for touching the full environment.** Claude Code and Antigravity can in theory drive a browser and click through an app, but those loops are slow, laborious, and not native to how the model thinks. This may improve, but today it's clumsy.

**Even with the tools, it lacks what you have.** It doesn't know your intent. It has no common sense, no human intuition, and no real understanding of your project and where it's headed.

**It has no insight into whether its own code actually works.** Compiling and running is one level of "working." The real test, as any developer knows, is whether the thing behaves the way you want across all the normal cases and all the edge cases. The agent can't typically see the difference between "it ran" and "it's right."

So the burden of verification falls on you. There's always a verification step, and it's non-negotiable, even for personal tooling you wrote for yourself. 

Strong verification is what lets you hand more off to the agent. When you can reliably confirm the output is correct, you can safely turn the usage dial further toward convenience.

## The high level: manual checking

The most basic form of verification is doing it yourself by hand.

**Always click through it yourself.** Test the path you expect to work, and the paths you expect to fail. Agents are very good at building a compelling working demo and then falling apart around the edges, so the edges are where you look.

**Target your riskiest functions first.** The code you don't understand, and the areas where you never specified the implementation, are where the agent had the most freedom to do something you didn't intend. Verify those behave the way you need before you trust anything built on top of them.

## The low level: automated testing

Because you're developers, you can go deeper than clicking around. You can write tests!

**End-to-end is hugely valuable for agents.** An end-to-end test runs the whole system together, all the pieces combined, similar to the way a real user would. That gives the agent insight into exactly what it's worst at: how the whole thing functions as a system at a high level. A unit test checks one function in isolation; an end-to-end test checks that the function actually does its job inside the running app.

If there's a single highest-value recommendation in this whole unit, it's this. **Write end-to-end tests, and make them genuinely good.** That alone gets noticeably better results out of agents, because it hands them a reliable way to know whether they broke something.

## Don't trust the agent to test itself

The agent is the one thing you'll most want to lean on for writing tests, and it's the thing you can least trust to do it well.

**By default, no agent, Claude Code included, does a good job testing itself.** This is improving slowly, but in the current generation you have to give explicit instructions.

**It writes stupid tests.** It will sometimes claim it did end-to-end testing while the tests check essentially nothing. I've repeatedly watched agents fail to implement meaningful end-to-end tests and then report success.

**Its verification is only as good as its test suite.** If the suite is hollow, the green checkmark is meaningless, so you have to be explicit about how tests are implemented and keep watching them.

**It degrades over time.** Good tests on the first pass don't mean it keeps writing good ones. You have to keep auditing and reminding.

The higher-control move is to step in and dictate the exact test cases you want. Tell it which scenarios matter and the flow. Then it's usually good at writing the actual test code and fixing small issues. 

The bottom line: telling it to "test" does not produce useful tests. Left alone, it often picks bad, incomplete, or wrong areas to cover.

## Check in often

Verification isn't only about how you check. It's about how often. Check in frequently and don't let the agent spin for long stretches before you look.

The mental model is a micro version of agile: very short feedback cycles. Let the agent finish one small thing, then review that thing, then move on.

**A concrete cadence:** for most projects, don't let it work for more than ~15 minutes without verification. The clearer your plan and the more specific your spec and deliverables, the more you can stretch that interval.

This matters because agents tend to drift. The agent makes wrong turns and assumptions, and you don't want to build on top of those. Frequent review catches them before they compound. More than that, the agent does better when you're actively shaping what it builds. The less active you are, the more it drifts from your intent, your vision, and a cohesive codebase.

## A specific gotcha: timeouts

One concrete thing because every agent I've used falls into it.

When an end-to-end test fails, the agent's reflex is "maybe it just needs more time," and it bumps the timeout to 30, 60, or 120 seconds before troubleshooting anything.

The problem is ten failing tests on long timeouts means minutes of the agent spinning it's wheels on failures. A failed end-to-end test almost always fails within the first couple of seconds. The long timeout buys you nothing.

**Set aggressive timeouts, typically no more than about five seconds, unless something legitimately needs longer.** The whole suite, run locally, should take only a few seconds. And keep an eye out, because the agent will quietly bump the timeouts back up when you're not looking.
