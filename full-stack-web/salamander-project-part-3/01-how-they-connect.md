---
title: "How the Front End and Back End Connect"
order: 1
---

Up to now your app has been talking to a fake. The `mockApi.js` module returned hard-coded data so you could build the UI before the real backend existed. Today you swap the fake for the real thing: your own backend, the one you built in 334, running on your machine right next to your React app.

This is the moment the two halves of "full stack" actually meet. Before you wire anything up, you and your partner need a shared mental model of what's about to happen, because most of the bugs in this pair program come from not understanding the picture.

## Two programs, one machine

When you run your React app, you start a **dev server** (Vite) on your computer. It listens on a port, usually `5173`. Your browser loads the app from `http://localhost:5173`.

Your backend is a **completely separate program**. It also runs on your computer, but it listens on a *different* port, something like `http://localhost:3000`. It doesn't know or care that your React app exists. It just sits there waiting for HTTP requests and answering them.

So right now you have two programs running side by side:

- **The frontend server** (Vite) serves your React app to the browser.
- **The backend server** answers data requests like "give me the list of videos."

They are strangers living in the same building on different floors. The only way they talk is by sending HTTP requests to each other's address.

> **With your partner:** Explain the setup back to each other in plain language. What is running on port `5173`? What is running on the backend port? Which one does your browser load the page from? Which one has the salamander data?

## What a request actually is

When your `getVideos` function calls `fetch("/api/videos")`, the browser opens a connection to a server, sends a small message that starts with `GET /api/videos`, and waits. The server reads that message, runs whatever code is attached to that route, and sends back a response: a status code (like `200 OK` or `404 Not Found`) and a body (your JSON).

That round trip is the same whether the server is across the world or on your own laptop. `localhost` just means "this machine." The request still goes out through the network stack and comes back. That's why you still get loading states and can still get errors even with both programs on one computer.

## The same-origin problem

Here's the catch that trips everyone up. The browser has a security rule called the **same-origin policy**. A page loaded from `http://localhost:5173` is allowed to make requests back to `localhost:5173` freely. But when that page tries to `fetch` from `http://localhost:3000`, the browser sees a *different origin* (different port counts as different) and gets suspicious. By default it blocks your code from reading the response and logs a **CORS error** in the console.

It's worth being precise about what "blocks" means, because it's subtler than it sounds. For a normal GET, the browser still **sends** the request and your backend still **answers** it normally. The block happens on the way back in. When the response arrives, the browser checks whether the backend included a header granting this origin permission to read it. If that header is missing, the browser throws the response away before your code can touch it. The backend isn't the one saying no. It answered fine and has no idea anything is wrong. The browser is the one blocking, on the response's way back, because only the backend can authorize who reads its data and this time it didn't.

CORS (Cross-Origin Resource Sharing) is the browser protecting users. Without it, any website you visited could quietly read data from your bank's API using your logged-in session. The rule exists for good reasons. It's just inconvenient during development when you genuinely do want your own two programs to talk.

There are two normal ways to get past it, and you'll pick one on the next page:

- **A dev proxy.** You tell Vite "any request to `/api` should be quietly forwarded to the backend." The browser only ever sees requests going to `localhost:5173`, so it never complains.
- **CORS headers.** You configure the backend to add a header that says "requests from other origins are allowed." This works too, but it has a sharp edge for this project that we'll explain.

Don't worry about choosing yet. First, play with the picture below until the request flow feels obvious.

{% activity "client-server-http.html", "Client, Server, and the Proxy", "560px" %}

> **With your partner:** Using the activity, send a request with the proxy **off** first. Where does it fail, and why? Now turn the proxy **on** and send it again. What changed about where the browser thinks the request is going? Explain the difference to each other before moving on.

## Why this matters for your canvas

There's a specific reason the proxy is the right call for *this* project. In Part 2 you read pixels out of the thumbnail with `getImageData` to build the binarized view. The browser will only let you read pixels from an image that came from the **same origin** as your page. If your thumbnail loads from `http://localhost:3000` (a different origin), the canvas becomes "tainted" and `getImageData` throws a security error. Your tuning feature would break the moment you switched off mock data.

Routing the thumbnail through the proxy keeps it same-origin, so the canvas work you already did keeps running untouched. Keep this in your back pocket; it's the kind of bug that costs an hour if you don't know the cause.
