---
title: "The Debugging Mindset"
order: 1
---

Today is a debugging day. You and your partner will introduce some bugs into one of your previous React pair programs, swap repos with another team, and then track down and fix what they broke.

Before any of that, this page is about the habit of mind that makes debugging actually work. Most people are bad at debugging because they skip the part where they understand what's happening. They jump straight to changing things, hoping something sticks. We're going to do the opposite.

## The Trap

The most common debugging mistake looks like this: something's wrong, you have a hunch, you change a line, you reload, it's still broken, you try a different change, reload, still broken, try another, reload. Twenty minutes in you've made eight changes, you don't remember what most of them were, and you have no idea whether the bug is closer to fixed or further from it.

You'll see AI assistants do exactly this. Ask one to fix a bug and watch what happens: many of them spit out a numbered list of "things to try" without ever pinning down the actual cause. You go down the list one by one. None of them work. Now you have a tangled mess and you've learned nothing.

That habit is one of the worst things you can pick up as a developer. It feels productive because you're typing. Underneath, all you're doing is guessing.

> **With your partner:** Have either of you fallen into this loop before? What did it feel like, and what eventually got you out of it?

## The Bar

There's one rule for this activity, and it's the rule that separates real debugging from guessing:

**You don't get to fix the bug until you can explain the cause completely.**

Out loud, to your partner, in plain language. What is the buggy code doing? Why is it doing that? Why does that produce the symptom you're seeing? If you can't answer those, you're not ready to change anything. Keep diagnosing.

Once you can explain it, the fix is usually short and obvious. The hard part was the understanding. The fix follows from it.

## The Process

Debugging works in four steps. They're simple. Most people just skip them and jump to step five.

**1. Reproduce the bug reliably.** Find the exact steps that trigger it. If you can't reproduce it on demand, you can't tell whether your fix actually fixed anything. The reproduction is the test.

**2. Observe what's happening.** Open your browser's console and the React DevTools. Look at the actual values flowing through your app. Don't assume what a variable contains. Look at it.

**3. Form a specific hypothesis.** Something like: "I think `count` is being set to a string instead of a number, so the comparison fails." A hypothesis specific enough that you can make a prediction from it. If yours is vaguer than the example above, sharpen it.

**4. Test the hypothesis.** Add a `console.log`, set a breakpoint, inspect the component in DevTools, whatever it takes to confirm or rule out the hypothesis. If the hypothesis was wrong, that's information. Form a new one.

When the hypothesis is confirmed and you can explain the chain of cause and effect, then you fix it. Not before.

## React DevTools

The browser's regular DevTools show you the rendered HTML, network requests, and console output. That's useful, and you should keep using it. For React apps, you also need a tool that lets you see what's happening inside React: which components rendered, what props they received, what their state holds, and how that state changes over time.

That tool is the **React Developer Tools** extension.

Install it from React's official guide: [react.dev/learn/react-developer-tools](https://react.dev/learn/react-developer-tools)

Pick your browser (Chrome, Firefox, or Edge) and follow the install link from that page. It takes about one minute.

### What it gives you

After installing, open any React site in your browser, then open DevTools. You'll see two new tabs:

- **Components** shows the tree of React components on the page. Click any component and you can see its current props, its state, and the hooks it's using. You can edit any of those values live and watch the page update.
- **Profiler** records re-renders so you can see what re-rendered, when, and why. You won't need this much today, but it's there.

The Components tab is the one that matters for debugging. When something on screen looks wrong, the question is almost always "is the data feeding this component correct?" The Components tab answers that question directly.

### Try it

Open one of your existing React projects. Run it locally with `npm run dev`. Open the browser, open DevTools, and click the **Components** tab.

Click around the component tree. Find a component that holds state. Watch the state change as you interact with the page.

> **With your partner:** Pick a piece of state in one of your components. Predict what its value will be after some action (clicking a button, typing in an input). Take that action. Was the value what you predicted? If not, was the prediction wrong, or is the state itself behaving in a way you didn't expect?

This is the move you'll lean on the most while debugging today. When the page does something surprising, the Components tab tells you what the React side actually looks like, which is usually different from what you think it looks like.

## A note on the console

The browser's regular **Console** tab is still your best friend. Errors and stack traces show up there. `console.log` calls show up there. When you don't know where to start, opening the console and looking for red is a good first move.

A surprising number of bugs reveal themselves the moment you open the console. The error message names the file and the line. People often spend ten minutes guessing without ever reading what the console already told them.

When both of you have React DevTools installed and have looked through one of your projects with it, you're ready for the next page.
