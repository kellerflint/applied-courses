---
title: "Phase 1: Initial Implementation"
order: 2
---

You and your partner will build a React app that fetches and displays data from a public API. You're practicing `useEffect` for data fetching, the three states of an async request (loading, error, success), and passing data down through a small component tree.

## What It Could Look Like

The app you build does not have to look like this. The screenshot is one example so you have a target shape in mind: a header, a search control, an item card with multiple sub-pieces, and a footer.

{% image "pokedex-search.png", "Mobile view of an example Pokémon search app showing a header, search input, and a card with image, types, and stats" %}

## Choose Your API

Pick a public API that returns items with at least five properties (or nested sub-properties) each. More properties means more for your sub-components to display. Some options:

- **[PokéAPI](https://pokeapi.co/).** Pokémon data, no key needed.
- **[TheMealDB](https://www.themealdb.com/api.php).** Recipes, no key needed for basic endpoints.
- **[REST Countries](https://restcountries.com/).** Country information, no key needed.
- **[OpenWeather](https://openweathermap.org/api).** Weather data, free key required.
- **[NASA APOD](https://api.nasa.gov/).** Astronomy picture of the day, free key required.
- **[NewsAPI](https://newsapi.org/).** News articles, free key required.
- Anything else that catches your eye.

Read the docs for whichever API you pick so you know the response shape before you start writing fetch logic. Picking an API where the response shape surprises you mid-build is a frustrating way to spend an hour.

> **With your partner:** Agree on the API and look at one sample response together. Note the top-level structure and which fields you want to display.

## Initial Fetch

Set up a fresh Vite + React project. In the component that owns your data, use `useEffect` to fetch a default set of items as soon as the component mounts. Hard-code the initial query, ID, or default term. You'll add the user-driven version in Phase 2.

Handle all three states of an async request:

- **Loading.** Show a message while the fetch is in flight.
- **Error.** Show a message if the fetch fails or returns nothing useful.
- **Success.** Render the data once it arrives.

## Component Architecture

Build a small component tree to display the data. At minimum:

- A **Header** component
- A **Footer** component
- An **Item** component that displays one piece of data from the API
- At least **two sub-components** inside Item, each responsible for a different slice of the data. One could handle an image, another a stats list, another a row of tags. Pick whatever fits your API.

Pass data down through props from parent to children. The point is practice splitting a UI into smaller pieces and passing the right slice of data to each one.

> **With your partner:** Sketch the tree before you write components. Note which props each component takes and where the API data lives.

## Display the Data

In the parent component, map over the array of items returned by the API and render an Item for each one. Each Item should display multiple properties from the API response, distributed across its sub-components.

If your API returns a single object instead of a list, wrap it in an array of one so your map still works. That keeps your render path identical for Phase 2.

## Checkpoint: Commit and Deploy

**Stop here before moving to Phase 2.** Getting the deploy working with simpler code is much easier than debugging both the deploy and the interaction layer at the same time.

- Initialize a git repository if you haven't already
- Commit your work with a descriptive message
- Push to a new GitHub repository
- Deploy to GitHub Pages, following [Hosting React Project with GitHub Pages](/full-stack-web/orientation/05-github-pages/)
- Open the live URL and confirm it works

> **With your partner:** Both partners should pull and run the repo locally before you call this checkpoint done. If one machine can't run it, find out why now.
