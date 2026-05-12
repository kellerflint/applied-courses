---
title: "useEffect Refresher"
order: 1
---

You've used `useEffect` in your Scrimba prep to fetch data from an API. Before you start this pair program, take a few minutes to confirm you and your partner are solid on how the dependency array controls when an effect runs. Getting this wrong is the most common way an API call accidentally fires on every keystroke or never fires at all.

## The Three Forms

A `useEffect` call takes a function plus an optional **dependency array**. The array decides when the function runs:

- **No array.** The effect runs after every render.
- **`[]`** (empty array). The effect runs once, right after the component first mounts.
- **`[someValue]`.** The effect runs once on mount and again any time `someValue` changes.

For an API fetch on page load you almost always want `[]`. For a fetch that re-runs when a search term changes you want `[searchTerm]`.

## Watch It Run

The activity below mounts a tiny component with two pieces of state and four `useEffect` calls, each with a different dependency array. Interact with the controls on the left and watch which effects fire on the right.

{% activity "useeffect-watcher.html", "useEffect Watcher", "640px" %}

> **With your partner:** Predict before you click. What fires when you press "+1 count"? What about typing one letter into the name input? What about "Force re-render"? Confirm your predictions, then talk through anything that surprised you.
