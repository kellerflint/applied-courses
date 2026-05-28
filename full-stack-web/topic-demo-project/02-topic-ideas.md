---
title: "Topic Ideas"
order: 2
---

Here are topics we have not covered, grouped by what they help you do. Each one lists what it is and a demo idea to get you started. The demo idea is just a suggestion. If you think of a better way to show the same topic, run with it.

## Saving and Sharing State

**Local Storage**
What it is: a built-in browser feature that saves data on the user's own machine, so it survives a refresh or closing the tab with no database involved.
Demo idea: a to-do list or notes app whose items are still there after you reload the page.

**Redux Toolkit**
What it is: a library that holds your app's state in one central store, so many components can read and update the same data without passing props through every layer.
Demo idea: a shopping cart where an "Add to cart" button in one component updates a cart total shown in a completely separate component.

**Context API with useReducer**
What it is: React's built-in way to share state across many components without prop drilling, paired with a reducer for organized updates. The built-in alternative to Redux.
Demo idea: a theme or a cart shared across several components, built with only what React ships with.

**TanStack Query (React Query)**
What it is: a library that manages server data for you, including caching, loading and error states, and automatic refetching.
Demo idea: a search app that instantly shows results you have searched before, because they are cached.

## Look and Feel

**Animations with Framer Motion**
What it is: a library for adding smooth, declarative animations and transitions to React components.
Demo idea: a list where items slide and fade in as they appear, or a button that springs when you click it.

**Tailwind CSS**
What it is: a styling approach where you compose small utility classes directly in your markup instead of writing separate CSS files.
Demo idea: rebuild one of your existing components with Tailwind and walk through how the classes map to the design.

**Component Libraries (Material UI or shadcn/ui)**
What it is: collections of pre-built, accessible components like buttons, dialogs, and menus that you drop into your app.
Demo idea: a small app built from a library's components, showing how much polished UI you get for free.

**Dark Mode and Theming**
What it is: switching a whole app between light and dark (or other) themes, usually with CSS variables, and remembering the user's choice.
Demo idea: a site with a working light and dark toggle that stays on your chosen theme after a refresh. This pairs naturally with Local Storage.

## Interaction

**Form Handling with React Hook Form**
What it is: a library that manages form state and validation with much less code, and shows users clear error messages.
Demo idea: a sign-up form that validates fields as you type and blocks submission until everything is valid.

**Drag and Drop (dnd-kit)**
What it is: a library for letting users drag items to reorder a list or move them between groups.
Demo idea: a kanban board where you drag task cards between "To Do," "Doing," and "Done."

**Charts and Data Visualization (Recharts or Chart.js)**
What it is: a library that turns data into graphs and charts.
Demo idea: a dashboard that charts data from an API or from a dataset you find online.

**Debounced Search**
What it is: a technique that waits until the user stops typing before firing a request, instead of one request per keystroke.
Demo idea: a search box that calls an API only after a short pause, shown side by side with the naive version that fires on every key.

## Talking to the Outside World

**A Real Database with Firebase or Supabase**
What it is: a cloud service that stores your data so it persists across devices and across different users.
Demo idea: an app where something you save on one laptop shows up on another.

**Authentication (Firebase Auth or Clerk)**
What it is: letting users sign in, and protecting pages so only signed-in users can reach them.
Demo idea: a login flow with a members-only page that redirects you when you are signed out.

**Real-Time Updates**
What it is: data that updates live across clients without anyone refreshing, often using WebSockets or a realtime database.
Demo idea: a shared counter or a chat that updates instantly in two browser windows side by side.

**Maps with Leaflet**
What it is: an interactive map you can embed in your app, with markers and popups.
Demo idea: a map that drops a marker for each location in a small dataset.

## Browser and Device Features

**Geolocation**
What it is: a browser API that, with the user's permission, gives you their location.
Demo idea: a "what's near me" feature that shows your position on a map or sorts a list by distance.

**Web Speech API**
What it is: a built-in browser API for turning speech into text and text into speech.
Demo idea: a notes app you can dictate to, or a page that reads its own content out loud.

## Code Quality

**Testing React (Vitest and React Testing Library)**
What it is: writing automated tests that check your components behave correctly, so you catch breakage before your users do.
Demo idea: write a few tests for one of your existing components, then break the component on purpose and watch the tests catch it.

**TypeScript with React**
What it is: a layer on top of JavaScript that adds types, catching a whole class of bugs before you ever run the code.
Demo idea: convert a small component to TypeScript and show an error it catches that plain JavaScript would have let slip through.

## Pick Your Own

Anything React or full-stack that we have not covered is fair game. If you are not sure whether something counts or is the right size, ask. A good gut check: can you show it working in a few minutes and explain why someone would use it? If yes, it will make a good demo.
