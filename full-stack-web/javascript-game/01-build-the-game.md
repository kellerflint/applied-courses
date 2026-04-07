---
title: "Build the Game"
order: 1
---

Today you're building a browser game with your partner using HTML, CSS, and vanilla JavaScript. You'll build a clicker game: click a button to earn points, spend points on upgrades that make future clicks worth more.

Next class we'll start building in React, but starting with raw JavaScript first is deliberate. React is built on JavaScript, and every concept you practice today (responding to events, updating the DOM, managing data in arrays and objects) maps directly to how React works. When React does the same things automatically, you'll understand what it's doing because you've done it by hand first.

For each step below, read the description and write the code yourself before opening the reveal. These are things you already know how to do. Give it a real attempt first.

Find a partner and get set up.

## What You're Building

By the end of today your game will:
- Track a score that increases when you click a button
- Have upgrades stored as data that get rendered onto the page
- Let you buy upgrades that permanently increase your points per click
- Disable upgrade buttons when you can't afford them

That's the core loop. Once it's working, you'll extend it in whatever direction interests you.

## 1. Set Up the Project

Create a new folder for your project. Inside it, create two files: `index.html` and `game.js`.

Write an HTML page that includes: a heading for your game's name, a paragraph with the id `score-display`, a paragraph with the id `rate-display`, a button with the id `click-btn`, a heading for an upgrades section, a div with the id `upgrades`, and a script tag linking to `game.js`.

<details>
<summary>Reveal answer</summary>

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Clicker Game</title>
</head>
<body>
  <h1>Your Game Name</h1>
  <p id="score-display">Score: 0</p>
  <p id="rate-display">Points per click: 1</p>
  <button id="click-btn">Click!</button>
  <h2>Upgrades</h2>
  <div id="upgrades"></div>
  <script src="game.js"></script>
</body>
</html>
```

</details>

> **With your partner:** Decide on a theme. It doesn't have to be a generic clicker. Collecting resources, brewing potions, building a company, anything goes. Rename the button and score labels to match your theme.

## 2. Track the Score

In `game.js`, declare two variables to hold the game's state: `score` starting at 0 and `pointsPerClick` starting at 1.

<details>
<summary>Reveal answer</summary>

```js
let score = 0;
let pointsPerClick = 1;
```

</details>

**State** is the data that changes as the player interacts. Everything the game displays should come from these variables. When a variable changes, the page updates to match. That's the core pattern you'll be working with all quarter.

Write an `updateDisplay` function that reads both variables and updates the text content of `score-display` and `rate-display` to reflect the current values.

<details>
<summary>Reveal answer</summary>

```js
function updateDisplay() {
  document.getElementById('score-display').textContent = 'Score: ' + score;
  document.getElementById('rate-display').textContent = 'Points per click: ' + pointsPerClick;
}
```

</details>

Now add a click event listener on `click-btn` that adds `pointsPerClick` to `score` and calls `updateDisplay`.

<details>
<summary>Reveal answer</summary>

```js
document.getElementById('click-btn').addEventListener('click', function() {
  score += pointsPerClick;
  updateDisplay();
});
```

</details>

Open `index.html` in your browser and click the button. The score should increment.

> **With your partner:** Verify the counter works for both of you before moving on. If one machine isn't showing updates, troubleshoot it together.

## 3. Upgrades as Data

One button gets boring fast. Add upgrades, things players can buy to increase `pointsPerClick`.

Instead of hardcoding each upgrade into your HTML, store them as an array of objects. This is the **data-driven pattern**: define your content as data, then write code that reads the data and builds the DOM from it. When you want a new upgrade, you add one object to the array. The rendering code doesn't need to change.

Create an `upgrades` array. Each object should have an `id` (unique number), `name` (string), `cost` (points required to buy), and `bonus` (amount added to `pointsPerClick` on purchase). Start with at least three upgrades.

<details>
<summary>Reveal answer</summary>

```js
const upgrades = [
  { id: 1, name: "Better Mouse",    cost: 10,  bonus: 1  },
  { id: 2, name: "Click Farm",      cost: 75,  bonus: 5  },
  { id: 3, name: "Robot Assistant", cost: 300, bonus: 20 },
];
```

</details>

> **With your partner:** Pick a few more upgrades that fit your theme and add them to the array. You haven't written the rendering code yet, so just define the data for now.

## 4. Render the Upgrades

Write a `renderUpgrades` function that clears the `upgrades` div, loops through the array, and creates a `<div>` for each upgrade containing its name, cost, bonus, and a Buy button that calls `buyUpgrade` with the upgrade's id. Call `renderUpgrades()` once at the bottom to run it on page load.

<details>
<summary>Reveal answer</summary>

```js
function renderUpgrades() {
  const container = document.getElementById('upgrades');
  container.innerHTML = '';

  upgrades.forEach(upgrade => {
    const div = document.createElement('div');
    div.innerHTML = `
      <strong>${upgrade.name}</strong>
      Cost: ${upgrade.cost} | +${upgrade.bonus} per click
      <button onclick="buyUpgrade(${upgrade.id})">Buy</button>
    `;
    container.appendChild(div);
  });
}

renderUpgrades();
```

</details>

Look at the flow happening here: an event fires, a function runs, a variable changes, and the DOM updates. This is the cycle that drives every interactive web app.

{% activity "dom-update-cycle.html", "The Update Cycle", "440px" %}

React is built around managing this same cycle. Right now you're doing it manually. React gives you tools that handle the re-rendering automatically.

## 5. Buy an Upgrade

Write a `buyUpgrade` function that takes an `id`, finds the matching upgrade in the array, and if the player can afford it, deducts the cost from `score`, adds the bonus to `pointsPerClick`, then calls `updateDisplay` and `renderUpgrades`.

<details>
<summary>Reveal answer</summary>

```js
function buyUpgrade(id) {
  const upgrade = upgrades.find(u => u.id === id);

  if (score >= upgrade.cost) {
    score -= upgrade.cost;
    pointsPerClick += upgrade.bonus;
    updateDisplay();
    renderUpgrades();
  }
}
```

</details>

> **With your partner:** Test buying an upgrade. Verify that `pointsPerClick` increases and that subsequent clicks score more. If the upgrade buttons disappear after buying, check that `renderUpgrades()` is being called.

## 6. Disable Buttons You Can't Afford

Right now the Buy button does nothing if you can't afford it. That's correct, but it gives no feedback. Update `renderUpgrades` so that each Buy button is disabled when the current score is less than the upgrade's cost. To set a `disabled` property on the button, you'll need to create it as a separate element rather than building it with `innerHTML`.

<details>
<summary>Reveal answer</summary>

```js
upgrades.forEach(upgrade => {
  const div = document.createElement('div');

  const button = document.createElement('button');
  button.textContent = 'Buy';
  button.onclick = () => buyUpgrade(upgrade.id);
  button.disabled = score < upgrade.cost;

  div.innerHTML = `
    <strong>${upgrade.name}</strong>
    Cost: ${upgrade.cost} | +${upgrade.bonus} per click
  `;
  div.appendChild(button);
  container.appendChild(div);
});
```

</details>

For this to work correctly, `renderUpgrades()` needs to run any time the score changes. Make sure it's called inside the click handler and inside `buyUpgrade`.

> **With your partner:** Take turns explaining the full sequence out loud. One person goes first: the player has just clicked the button enough times to afford an upgrade and buys it. Walk through your code line by line: which line runs first, what it does, what changes, what runs next. No hand-waving. Then switch and have the other person do the same explanation from scratch.
