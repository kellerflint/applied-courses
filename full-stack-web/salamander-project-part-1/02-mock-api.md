---
title: "Building the Mock API"
order: 2
---

Your frontend needs data to display, but the backend you'll eventually call doesn't exist yet. Auberon's 334 students are building it this quarter. You're building this frontend alongside that work.

The fix is a **mock API**: a small module in your project that pretends to be the real backend. Your components call it the same way they'd call a real API. When the real backend is ready, you swap a few lines of code and everything else keeps working.

## Why a module of async functions

There are a few ways to mock an API. The simplest one that won't bite you later is a module that exports `async` functions which return fake data wrapped in `Promise.resolve`.

This shape has two benefits:

1. **Your components call it with `await` just like they'd call a real `fetch`.** No code in your components has to change when you swap to the real API.
2. **No extra processes to manage.** You don't have to remember to start a mock server every time you work on the project.

You can absolutely swap to a real mock server later (`json-server` is a popular option) if you want to practice network calls more authentically. Start with the module approach.

## What the real API will look like

From the [project overview page](/full-stack-web/salamander-project/01-project-overview/), the real API will eventually have these endpoints:

- `GET /api/videos` returns a list of available videos.
- `GET /thumbnail/{filename}` returns the first frame of a video.
- `POST /process/{filename}?targetColor=<hex>&threshold=<int>` submits a processing job.
- `GET /process/{jobId}/status` checks the status of a submitted job.

Full examples live at [auberonedu/salamander-api](https://github.com/auberonedu/salamander-api). Read through that repo with your partner so you know what response shapes you're mocking.

> **With your partner:** Open the linked repo and look at one example response for each endpoint. Note the shape of each one. The closer your mock matches reality, the less rework when you swap to the real API.

## Create the mock module

Make a new file at `src/mockApi.js`. Put the fake data at the top and the async functions below:

```js
// Fake data the mock functions return. Replace these with realistic
// values once you've looked at the real API's example responses.
const videos = [
  "salamander1.mp4",
  "salamander2.mov",
  "forest_intro.mp4",
  "tank_view_long.mp4",
];

const thumbnails = {
  // Map filename -> URL of an image to use as its thumbnail.
  // For now, use any salamander image you have or a placeholder service.
  "salamander1.mp4": "https://placehold.co/320x180?text=salamander1",
  "salamander2.mov": "https://placehold.co/320x180?text=salamander2",
  "forest_intro.mp4": "https://placehold.co/320x180?text=forest_intro",
  "tank_view_long.mp4": "https://placehold.co/320x180?text=tank_view_long",
};

// Tiny helper that adds a fake delay so loading states are visible
// during development. Real networks aren't instant; pretending they
// are will hide UI bugs.
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export async function getVideos() {
  await delay(400);
  return videos;
}

export async function getThumbnail(filename) {
  await delay(300);
  if (!thumbnails[filename]) {
    throw new Error(`No thumbnail for ${filename}`);
  }
  return thumbnails[filename];
}

export async function submitProcessingJob(filename, targetColor, threshold) {
  await delay(500);
  // Pretend the server gave us a job id.
  return { jobId: `mock-${Date.now()}` };
}

export async function getJobStatus(jobId) {
  await delay(300);
  // For the mock, always say the job finished successfully.
  return {
    jobId,
    status: "complete",
    csvUrl: "https://example.com/results.csv",
  };
}
```

A few things worth noticing:

- Every function is `async` and uses `await`. That matches how you'd call a real `fetch`, so your components don't care whether the API is real or fake.
- The `delay` helper simulates network latency. Without it, your loading states would never be visible because the mock would resolve before React could even render.
- `getThumbnail` throws if the filename is unknown. Real APIs return errors too, and your components need to handle that. Mocking errors is part of mocking the API.

You only need the functions for endpoints you're actually about to use. Adding `submitProcessingJob` and `getJobStatus` now is fine since it costs almost nothing, but skip them if you'd rather add them when you get to those user stories.

## Test it from the Videos page

Before you wire this into UI, prove the module actually works. Open `src/pages/Videos.jsx` and add a `useEffect` that calls `getVideos` and logs the result:

```jsx
import { useEffect } from 'react';
import { getVideos } from '../mockApi.js';

export default function Videos() {
  useEffect(() => {
    getVideos().then((data) => {
      console.log("getVideos returned:", data);
    });
  }, []);

  return (
    <div>
      <h1>Available Videos</h1>
      <p>Video list will go here.</p>
    </div>
  );
}
```

Refresh the Videos page in your browser. Open the DevTools console. You should see:

```
getVideos returned: ["salamander1.mp4", "salamander2.mov", "forest_intro.mp4", "tank_view_long.mp4"]
```

If you don't, fix it before moving on. Common issues:

- **Import path wrong.** `from '../mockApi.js'` because `Videos.jsx` is in `src/pages/` and `mockApi.js` is in `src/`.
- **`useEffect` dependency array missing.** Without `[]`, the effect runs on every render and you'll see the log over and over.
- **Effect didn't run at all.** Make sure you actually imported `useEffect` from `'react'`.

> **With your partner:** Look at your `useEffect` together. What does the empty dependency array `[]` mean? What would happen if you removed it? What would happen if you put `[someState]` instead? If you're not sure, peek at the [useEffect Watcher activity](/full-stack-web/api-pair-program/01-useeffect-refresher/) from the API Data Display unit.

## Commit

Mock API in place and verified. Commit it:

```bash
git add .
git commit -m "Add mock API module with getVideos verified from Videos page"
```

Next you'll turn that `console.log` into a real list on the page, with loading and error states, and make each entry clickable.
