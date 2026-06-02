---
title: "Connect Your Front End"
order: 3
---

Now you'll point your React app at the backend. The work has two parts: set up the proxy so requests are allowed through, and swap your mock functions for real `fetch` calls.

## Set up the dev proxy

Tell Vite to forward backend-bound requests to your backend. Open `vite.config.js` and add a `server.proxy` block:

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api': 'http://localhost:3000',
      '/thumbnail': 'http://localhost:3000',
      '/process': 'http://localhost:3000',
      '/results': 'http://localhost:3000',
    },
  },
})
```

Each key is a path prefix. When the browser requests `/api/videos`, Vite sees that it starts with `/api` and forwards the request to `http://localhost:3000/api/videos`. The browser only ever sees a request to `localhost:5173`, so the same-origin policy is satisfied and there's no CORS error.

**List every path prefix your API uses.** If your backend serves thumbnails at `/thumbnail/...` and you forget to proxy `/thumbnail`, those requests fall through to Vite, which has no idea what they are, and your images break while everything else works. Match this list to *your* backend's routes and *your* backend's port.

**You must restart Vite after editing `vite.config.js`.** The proxy config is read once at startup. Stop the dev server and run `npm run dev` again, or the proxy won't take effect.

## Swap the mock for real fetch

In Part 1 the plan was always to swap mock data for real API calls once the backend existed. Now you do it. The cleanest way is to make a real API module that exports the same function names your components already import, so the components don't have to change.

Create `src/api.js` next to your `mockApi.js`.

Try writing the routes on your own first! Sample code is below if you need it.

<details>
<summary>Reveal answer</summary>

```js
export async function getVideos() {
  const res = await fetch('/api/videos');
  if (!res.ok) {
    throw new Error(`Server responded ${res.status}`);
  }
  return res.json();
}

export async function getThumbnail(filename) {
  const url = `/thumbnail/${filename}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`No thumbnail for ${filename}`);
  }
  return url;
}

export async function submitProcessingJob(filename, targetColor, threshold) {
  // The contract wants the hex with no leading '#'.
  const hex = targetColor.replace('#', '');
  const res = await fetch(
    `/process/${filename}?targetColor=${hex}&threshold=${threshold}`,
    { method: 'POST' }
  );
  if (!res.ok) {
    throw new Error(`Server responded ${res.status}`);
  }
  return res.json();
}

export async function getJobStatus(jobId) {
  const res = await fetch(`/process/${jobId}/status`);
  if (!res.ok) {
    throw new Error(`Server responded ${res.status}`);
  }
  return res.json();
}
```

</details>

## Flip the imports

Your components currently import from `'../mockApi.js'`. Change those import lines to point at `'../api.js'`. That's the entire swap. The component code, the loading and error states, the rendering, all of it stays the same because the function names and return shapes match.

```jsx
// before
import { getVideos } from '../mockApi.js';
// after
import { getVideos } from '../api.js';
```

Do this for every component that imported a mock function. Keep `mockApi.js` in the repo. It's useful to be able to flip back to it when the backend is down and you want to work on UI.

## Verify every story against the real backend

You're done when each user story works against real backend. Walk through your existing stories with the backend running:

1. **Video list.** Load `/videos`. The list comes from the real `GET /api/videos`. Stop your backend and reload: you should see your error state, not a blank page or a frozen spinner.
2. **Thumbnail.** Open a video's preview page. The image loads from the backend through the proxy. Your binarized canvas from Part 2 still updates as you move the sliders, because the proxy kept the image same-origin.

> **With your partner:** Open DevTools, go to the **Network** tab, and reload. Find the request to your backend. Click it. Look at the status code, the request URL, and the response body. Being able to read the Network tab is how you'll want to debug API problems from here on.

### If something's broken

- **CORS error in the console.** Your fetch is going to the backend's origin directly instead of through the proxy. Check that your fetch paths are relative and that you restarted Vite after editing the config.
- **404 on a request that works in curl.** The path prefix probably isn't in your proxy config, so Vite is handling it instead of forwarding it.
- **Tainted canvas / `getImageData` security error.** The thumbnail is loading cross-origin. Route it through the proxy with a relative URL.
- **The list loads but the shape is wrong.** Add an adapter in `api.js` to reshape the response before returning it.
