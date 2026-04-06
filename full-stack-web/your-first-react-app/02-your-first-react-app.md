---
title: "Your First React App"
order: 2
---

You're going to build a fun fact board: a page full of cards, each showing one fact about you or your partner. It's a simple project, but it's a perfect fit for React because you'll be rendering the same component over and over with different data.

## Create the Project

React projects need a build step to turn JSX into JavaScript browsers can run. **Vite** handles all of that setup for you. Run this in your terminal:

```bash
npm create vite@latest
```

Vite will prompt you for a few things. Answer them like this:

```
◇  Project name:
│  fun-facts
│
◇  Select a framework:
│  React
│
◇  Select a variant:
│  JavaScript
│
◇  Install with npm and start now?
│  Yes
```

When it finishes, it starts a local development server and prints a URL (usually `http://localhost:5173`). Open it in your browser. You should see the default Vite + React page.

If you chose "No" to install and start, run these manually:

```bash
cd fun-facts
npm install
npm run dev
```

> **With your partner:** Get both machines running before continuing. If one hits an error, troubleshoot it together before moving on.

## Clean the Slate

Open `src/App.jsx`. It has a bunch of default code in it. Delete everything inside `return ( )` and replace it with a single empty `<div>`. You're starting fresh.

Your App.jsx should now look like this:

```jsx
import './App.css'

function App() {
  return (
    <div>
    </div>
  );
}

export default App;
```

Save it and confirm the browser shows a blank page with no errors.

## Step 1: Write a Static Component

Create a new file: `src/FunFactCard.jsx`

A component is just a function that returns JSX. Start with the simplest possible version: hardcoded text, no props yet:

```jsx
function FunFactCard() {
  return (
    <div>
      <h2>Fun Fact</h2>
      <p>This is a fun fact.</p>
    </div>
  );
}

export default FunFactCard;
```

Now import it in `App.jsx` and drop it in:

```jsx
import FunFactCard from './FunFactCard';

function App() {
  return (
    <div>
      <FunFactCard />
    </div>
  );
}

export default App;
```

Save and check the browser. You should see "This is a fun fact." on the page.

> **With your partner:** You just wrote a React component. In plain JavaScript, how would you have put text on the page? How is this different?

## Step 2: Add a Prop

To make the component reusable, you pass data in using a **prop**.

Update `FunFactCard.jsx`:

```jsx
function FunFactCard({ fact }) {
  return (
    <div>
      <h2>Fun Fact</h2>
      <p>{fact}</p>
    </div>
  );
}

export default FunFactCard;
```

`{ fact }` in the function parameters is how you receive the prop. `{fact}` in the JSX is how you render it. Now update `App.jsx` to pass a real fact in:

```jsx
<FunFactCard fact="I have visited more than 10 countries." />
```

Save and check the browser. The text on screen should update to the fact you passed in.

> **With your partner:** Trace exactly how the value gets from `App.jsx` to the screen. Start at `fact="..."` and follow it step by step through the code.

## Step 3: Render Multiple Cards

Come up with at least 5 fun facts between the two of you. They can be about hobbies, things you've done, skills, whatever. Add a `<FunFactCard />` for each one:

```jsx
function App() {
  return (
    <div>
      <h1>Fun Facts</h1>
      <FunFactCard fact="I have visited more than 10 countries." />
      <FunFactCard fact="I started programming in middle school." />
      <FunFactCard fact="I can solve a Rubik's cube." />
      <FunFactCard fact="My first computer was a hand-me-down from 2008." />
      <FunFactCard fact="I have a cat named Pixel." />
    </div>
  );
}
```

Fill these in with your actual facts.

> **With your partner:** What would this look like written as plain HTML, without components? Count how many lines you'd have to change if you wanted to update the structure of each card.

## Step 4: Style It

Open `App.css` and delete everything in it. Add some basic styles using regular CSS element selectors:

```css
body {
  max-width: 600px;
  margin: 2rem auto;
  padding: 0 1rem;
  font-family: system-ui, sans-serif;
}

h1 {
  margin-bottom: 1.5rem;
}

h2 {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #888;
  margin-bottom: 0.25rem;
}

p {
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 0.75rem 1rem;
  margin-bottom: 1.5rem;
}
```

This is plain CSS. React doesn't change how CSS works. Adjust the styles until the cards look clean.
