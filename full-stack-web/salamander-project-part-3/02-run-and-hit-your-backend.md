---
title: "Run Your Backend and Prove You Can Hit It"
order: 2
---

Before you touch React, get your backend running and confirm you can reach it on its own. Debugging the connection is much harder when you don't know whether the problem is the backend, the frontend, or the wiring between them. Prove the backend works in isolation first, then add the frontend.

Everyone's backend is a little different. That's fine. The steps are the same regardless of stack: start it, find its address, hit its endpoints, read the responses.

## Start the backend

Open a second terminal. Leave your Vite dev server running in the first one. You're going to have two long-running programs now, one per terminal, and that's normal for full-stack work.

Start your backend however your project starts it. When it boots, it almost always prints the address and port it's listening on. Read that line and note the address.

> **With your partner:** Find the exact line in your backend's startup output that tells you its address. What's the full base URL (protocol, host, and port)? If you can't find it, that's the first thing to fix.

## Hit it without React

Your backend speaks HTTP, and so does your browser and so does `curl`. You don't need your React app to test a backend. You just need to send it a request.

### Option A: the browser

A `GET` endpoint is just a URL. Paste your videos endpoint straight into the address bar:

```
http://localhost:3000/api/videos
```

(Use *your* backend's port.) If it works, you'll see the raw JSON list of videos rendered in the browser tab. That alone proves the backend is up and the endpoint works.

### Option B: curl

`curl` sends an HTTP request from the terminal and prints the response. It's the fastest way to check an endpoint:

```bash
curl http://localhost:3000/api/videos
```

You should get back something like:

```
["salamander1.mp4","salamander2.mov","forest_intro.mp4"]
```

> **With your partner:** Hit an endpoint from the browser or curl. Read the response. Does the shape match what your `mockApi.js` was pretending to return? Note any differences now, because those differences are what you'll have to handle when you wire up the frontend.

## When the response doesn't match your mock

Your mock was a guess at the real API's shape. The real backend is the source of truth. If the real `GET /api/videos` returns objects like `{ "filename": "salamander1.mp4" }` but your mock returned plain strings, your UI code expects the wrong thing.

You have two choices, and either is fine:

- **Adapt the frontend** to the real shape (change how you read the data in your components).
- **Adapt the response** in the function that fetches it, so the rest of your app still receives the shape it already expects.
