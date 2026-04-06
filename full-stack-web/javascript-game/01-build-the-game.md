---
title: "Build the Game"
order: 1
---

Today you're building a browser game with your partner using HTML, CSS, and vanilla JavaScript. You'll build a clicker game: click a button to earn points, spend points on upgrades that make future clicks worth more.

Next class you'll build something similar in React. Starting with raw JavaScript first is deliberate. React is built on JavaScript, and every concept you practice today (responding to events, updating the DOM, managing data in arrays and objects) maps directly to how React works. When React does the same things automatically, you'll understand what it's doing because you've done it by hand.

Find your partner and get set up.

## What You're Building

By the end of today your game will:
- Track a score that increases when you click a button
- Have upgrades stored as data that get rendered onto the page
- Let you buy upgrades that permanently increase your points per click
- Disable upgrade buttons when you can't afford them

That's the core loop. Once it's working, you'll extend it in whatever direction interests you.

## 1. Set Up the Project

Create a new folder for your project. Inside it, create two files: `index.html` and `game.js`.

Start with this HTML structure:

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

> **With your partner:** Decide on a theme. It doesn't have to be a generic clicker. Collecting resources, brewing potions, building a company, anything goes. Rename the button and score labels to match your theme.

## 2. Track the Score

In `game.js`, start with two variables to hold the game's state:

```js
let score = 0;
let pointsPerClick = 1;
```

**State** is the data that changes as the player interacts. Everything the game displays should come from these variables. When a variable changes, the page updates to match. That's the core pattern you'll be working with all quarter.

Add a function that updates both displays at once:

```js
function updateDisplay() {
  document.getElementById('score-display').textContent = 'Score: ' + score;
  document.getElementById('rate-display').textContent = 'Points per click: ' + pointsPerClick;
}
```

Now add the click handler:

```js
document.getElementById('click-btn').addEventListener('click', function() {
  score += pointsPerClick;
  updateDisplay();
});
```

Open `index.html` in your browser and click the button. The score should increment.

> **With your partner:** Verify the counter works for both of you before moving on. If one machine isn't showing updates, troubleshoot it together.

## 3. Upgrades as Data

One button gets boring fast. Add upgrades, things players can buy to increase `pointsPerClick`.

Instead of hardcoding each upgrade into your HTML, store them as an array of objects. This is the **data-driven pattern**: define your content as data, then write code that reads the data and builds the DOM from it. When you want a new upgrade, you add one object to the array. The rendering code doesn't need to change.

Here's a starting set:

```js
const upgrades = [
  { id: 1, name: "Better Mouse",    cost: 10,  bonus: 1  },
  { id: 2, name: "Click Farm",      cost: 75,  bonus: 5  },
  { id: 3, name: "Robot Assistant", cost: 300, bonus: 20 },
];
```

Each object has:
- `id`: a unique number used to find this upgrade later
- `name`: what shows up on the button
- `cost`: how many points to buy it
- `bonus`: how much gets added to `pointsPerClick` when purchased

> **With your partner:** Pick a few more upgrades that fit your theme and add them to the array. You haven't written the rendering code yet, so just define the data for now.

## 4. Render the Upgrades

Write a function that reads the array and builds the DOM:

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

This clears the container, loops through every upgrade, creates a `<div>` for each one with content pulled from the data, and appends it. Calling `renderUpgrades()` at the bottom runs it once on page load.

Look at the flow happening here: an event fires, a function runs, a variable changes, and the DOM updates. This is the cycle that drives every interactive web app.

{% activity "dom-update-cycle.html", "The Update Cycle", "440px" %}

React is built around managing this same cycle. Right now you're doing it manually. React gives you tools that handle the re-rendering automatically. The underlying pattern is identical.

## 5. Buy an Upgrade

When a player clicks Buy, three things happen: deduct the cost, apply the bonus, and re-render so the display reflects the new state.

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

`upgrades.find()` searches the array for the object whose `id` matches. The `if` check prevents spending points you don't have.

> **With your partner:** Test buying an upgrade. Verify that `pointsPerClick` increases and that subsequent clicks score more. If the upgrade buttons disappear after buying, check that `renderUpgrades()` is being called.

## 6. Disable Buttons You Can't Afford

Right now the Buy button does nothing if you can't afford it. That's correct, but it gives no feedback. Update `renderUpgrades` to disable the button when the score is too low.

Inside the `forEach`, create the button separately so you can set its `disabled` property:

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

For this to work correctly, `renderUpgrades()` needs to run any time the score changes, not just on page load. Make sure it's called inside the click handler and inside `buyUpgrade`.

> **With your partner:** Take turns explaining the full sequence out loud. One person goes first: the player has just clicked the button enough times to afford an upgrade and buys it. Walk through your code line by line: which line runs first, what it does, what changes, what runs next. No hand-waving. Then switch and have the other person do the same explanation from scratch.
