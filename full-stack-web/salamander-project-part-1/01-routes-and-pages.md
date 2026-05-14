---
title: "Routes and Pages"
order: 1
---

This is the first pair program where you start actually building the Salamander Tracker app. You'll get the project scaffolded, add routing so it can have multiple pages, build a mock API so you have data to work with, and implement your first user story.

You should be pair programming. Swap the driver every 20 or so minutes.

## What you're building today

By the end of this session your repo will have:

- A Vite + React project with React Router set up
- A Home page and a Videos page (and whatever other pages your wireframes call for)
- A mock API module that returns fake data shaped like the real API will
- The first user story implemented: **"As a researcher, I want to see a list of all videos available on the server so that I can pick one to analyze."**

Your wireframes might call for more pages than just Home and Videos. That's fine. Build whatever pages your wireframes call for as stubs (a heading and a sentence is plenty), and we'll flesh them out in later pair programs.

> **With your partner:** Pull up your wireframes. List every distinct page in your design and the URL path you want each one to live at. Write the list down somewhere you can reference for the rest of the session.

## Create the project

If you already have a repo for this project from the wireframes assignment, work in that repo. Otherwise create a new one now.

Scaffold a new Vite + React app at the root of the repo.

## React Router

A React app served by Vite is a **single-page application**. The browser loads one HTML file once, and React swaps content in and out of that page as the user navigates. There is no full page reload when you go from `/` to `/videos`.

To make the URL bar match what's on screen, and to let users use the back button, share links, and refresh without losing their place, you need a **client-side router**. React Router is the standard library for this. It watches the URL and renders the component you've associated with that path.

## Install React Router

Stop the dev server, then:

```bash
npm install react-router-dom
```

This adds React Router to your dependencies. Restart the dev server.

## Wrap the app in BrowserRouter

React Router needs to wrap your whole app so any component inside it can read the current URL and render route-aware UI. The wrapper lives in `src/main.jsx`.

Open `src/main.jsx`. The scaffolded file looks something like this:

```jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

Add a `BrowserRouter` import and wrap `<App />` with it:

```jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
```

`BrowserRouter` uses the browser's real URL bar (so `localhost:5173/videos` works as you'd expect). Anything inside it can use the routing hooks and components.

**Quick check.** Save the file and look at the browser. The default Vite + React page should still render exactly the same as before. `BrowserRouter` is invisible until something inside it actually uses routing. If the page went blank or threw an error in the console, fix that here before moving on.

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

Open `src/App.jsx`. The Vite template ships with a demo hero section, some imports, and a counter button. **Replace the entire file** (imports and all) with a route table that maps URL paths to page components:

```jsx
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home.jsx';
import Videos from './pages/Videos.jsx';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/videos" element={<Videos />} />
    </Routes>
  );
}
```

What's happening:

- `Routes` is the container that decides which `Route` to render based on the current URL.
- Each `Route` ties a `path` to an `element` (the component to render).

If your wireframes call for more pages, add a `Route` for each one.

### Verify the routes work

Before adding any nav links, prove the routes themselves work by **typing URLs directly in the browser address bar**:

1. Go to `http://localhost:5173/`. You should see the Home page heading.
2. Change the URL to `http://localhost:5173/videos` and hit Enter. The Videos page should render.
3. Hit the browser back button. You should land back on Home.

If any of those don't work, fix it before you add nav links.

## Add nav links

Now that the routes work, give users a way to move between them without typing URLs.

Update `src/App.jsx` to add a `nav` with `Link` components:

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

`Link` renders an `<a>` tag, but clicking it does a client-side navigation instead of a full page reload. That keeps the app fast and preserves React state across navigations.

If your wireframes call for more pages, add a `Link` for each one in the nav.

### Verify the links work

1. Reload `http://localhost:5173/`. You should see the nav and the Home page.
2. Click "Videos." The URL changes to `/videos` and the Videos page renders.
3. Hit the browser back button. You should land on Home with the URL back to `/`.
4. Refresh on `/videos`. The Videos page should still render.
