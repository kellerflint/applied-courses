---
title: "What Is React?"
order: 1
---

React is a JavaScript library for building user interfaces. The core idea: you build your UI out of **components**. A component is a reusable function that returns markup.

Here's the simplest possible component:

```jsx
function FunFactCard({ fact }) {
  return <p>{fact}</p>;
}
```

This is a function. It takes `fact` as input (called a **prop**) and returns a `<p>` tag with that value inside. The `{ }` curly braces are how you drop a JavaScript value into your markup.

You use the component like an HTML element, and pass data in as an attribute:

```jsx
<FunFactCard fact="I have visited 12 countries" />
```

React takes that and renders:

```html
<p>I have visited 12 countries</p>
```

The power is that the same component works with any data. Define it once, use it as many times as you want with different values.

Try it below. Type a fun fact and click "Render Card" to see it go through the component:

{% activity "component-as-template.html", "Components as Templates", "600px" %}

> **With your partner:** Add several cards. What would this look like if you wrote it as plain HTML instead, with no components? What changes as you add more cards?

<details>
<summary>Reveal answer</summary>

In plain HTML you'd copy-paste the full card structure for every fact:

```html
<div>
  <h2>Fun Fact</h2>
  <p>I have visited 12 countries</p>
</div>
<div>
  <h2>Fun Fact</h2>
  <p>I can solve a Rubik's cube</p>
</div>
```

Every card repeats the `<h2>Fun Fact</h2>`. If you wanted to change that label to "Did you know?" you'd update every single card by hand.

With a component, the structure is defined once. Change `<h2>Fun Fact</h2>` in `FunFactCard.jsx` and every card on the page updates automatically.

</details>
