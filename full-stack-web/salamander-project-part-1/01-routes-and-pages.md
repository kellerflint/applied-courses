---
title: "Routes and Pages"
order: 1
---

This is the first pair program where you start actually building the Salamander Tracker app. Today is all setup. You'll get the project scaffolded, add routing so it can have multiple pages, build a mock API so you have data to work with, and implement your first user story.

You and your partner should be at one machine, pair programming. Swap the driver every 20 to 30 minutes.

## What you're building today

By the end of this session your repo will have:

- A Vite + React project with React Router set up
- A Home page and a Videos page (and whatever other pages your wireframes call for)
- A mock API module that returns fake data shaped like the real API will
- The first user story implemented: **"As a researcher, I want to see a list of all videos available on the server so that I can pick one to analyze."**

Your wireframes might call for more pages than just Home and Videos. That's fine. Build whatever pages your wireframes call for as stubs (a heading and a sentence is plenty), and we'll flesh them out in later pair programs.

> **With your partner:** Pull up your wireframes. List every distinct page in your design and the URL path you want each one to live at. Write the list down somewhere you can reference for the rest of the session.

## Why React Router

A React app served by Vite is a **single-page application**. The browser loads one HTML file once, and React swaps content in and out of that page as the user navigates. There is no full page reload when you go from `/` to `/videos`.

To make the URL bar match what's on screen, and to let users use the back button, share links, and refresh without losing their place, you need a **client-side router**. React Router is the standard library for this. It watches the URL and renders the component you've associated with that path.

## Create the project

If you already have a repo for this project from the wireframes assignment, work in that repo. Otherwise create a new one now.

Scaffold a fresh Vite + React app at the root of the repo:

```bash
npm create vite@latest
```

Answer the prompts:

```
◇  Project name:
│  salamander-tracker
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

Open the URL Vite prints (usually `http://localhost:5173`). You should see the default Vite + React page.

> **With your partner:** Get both machines cloning the repo and running `npm install && npm run dev` before continuing. If one machine can't run it, troubleshoot it now while the project is still tiny.

## Install React Router

Stop the dev server (`Ctrl+C`), then:

```bash
npm install react-router-dom
```

This adds React Router to your dependencies. Restart the dev server with `npm run dev`.

## Wrap the app in BrowserRouter

React Router needs to wrap your whole app so any component inside it can read the current URL and render route-aware UI. The wrapper lives in `src/main.jsx`.

Open `src/main.jsx` and add the import and wrapper:

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
```

`BrowserRouter` uses the browser's real URL bar (so `localhost:5173/videos` works as you'd expect). Anything inside it can use the routing hooks and components.

## Create your page components

Make a `src/pages/` folder. Inside it, create one file per page. At minimum you need `Home.jsx` and `Videos.jsx`. If your wireframes call for more pages, create those too (a Preview page, a Results page, whatever you sketched).

Start with a placeholder version of each one so you have something to render. Here's `src/pages/Home.jsx`:

```jsx
export default function Home() {
  return (
    <div>
      <h1>Salamander Tracker</h1>
      <p>Pick a video from the Videos page to start analyzing.</p>
    </div>
  );
}
```

And `src/pages/Videos.jsx`:

```jsx
export default function Videos() {
  return (
    <div>
      <h1>Available Videos</h1>
      <p>Video list will go here.</p>
    </div>
  );
}
```

The Home page is the landing page where you explain what the app does. The Videos page is where the first user story lives. Keep them simple for now.

## Wire up the routes

Open `src/App.jsx`. Replace its contents with a route table that maps URL paths to page components:

```jsx
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home.jsx';
import Videos from './pages/Videos.jsx';

export default function App() {
  return (
    <div>
      <nav>
        <Link to="/">Home</Link>
        {' | '}
        <Link to="/videos">Videos</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/videos" element={<Videos />} />
      </Routes>
    </div>
  );
}
```

A few things are happening here:

- `Routes` is the container that decides which `Route` to render based on the current URL.
- Each `Route` ties a `path` to an `element` (the component to render).
- `Link` renders an `<a>` tag, but clicking it does a client-side navigation instead of a full page reload. That keeps the app fast and preserves React state across navigations.

If your wireframes call for more pages, add a `Route` for each one and a corresponding `Link` in the nav.

## Verify it works

Go to `http://localhost:5173/`. You should see the Home page. Click the Videos link. The URL changes to `/videos` and the Videos page renders. The browser back button takes you back to Home. Refreshing the page on `/videos` still shows the Videos page.

If any of that doesn't work, fix it before you move on. The most common issues:

- **Blank page or "Cannot read properties of undefined"** usually means `BrowserRouter` is missing in `main.jsx`.
- **Refreshing on a non-root URL works in dev but fails when deployed.** That's a different problem you'll handle at deploy time. Dev is fine for now.

> **With your partner:** Predict what happens if you put the wrong path in a `Link` (like `to="/vidoes"`). Then try it. What renders? How would a user know they hit a typo'd link? When you're done, fix the typo.

## Commit

You've got a routed multi-page app. Commit it before moving on:

```bash
git add .
git commit -m "Add React Router with Home and Videos pages"
```

Now the project has a skeleton you can hang real features on.
