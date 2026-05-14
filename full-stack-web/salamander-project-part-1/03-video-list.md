---
title: "First User Story: Video List"
order: 3
---

You have routing. You have a mock API. Time to actually build something a user could use.

## The user story

From the [project overview](/full-stack-web/salamander-project/01-project-overview/):

> As a researcher, I want to see a list of all videos available on the server so that I can pick one to analyze.

And the acceptance criteria:

- Given I am on the Video Chooser page, when the page loads, then the app fetches `GET /api/videos` and renders each video as a clickable entry.
- Given the video list request is in flight, when I look at the page, then a loading state is visible.
- Given the video list has loaded, when I click a video entry, then I am navigated to the preview page for that video (e.g. `/preview/:filename`).
- Given the API is unavailable, when the page attempts to fetch the video list, then an error message is shown to the user.

That's your spec. Everything you build on this page should map back to one of those four bullets. When you think you're done, you'll come back and check each one.

> **With your partner:** Read the four criteria out loud. For each one, name the visible thing on the page that proves it works. If you can't name something visible, you don't have a way to test that criterion.

## Three states of an async request

Every fetch your app makes is in one of three states at any given time:

- **Loading.** The request has started and hasn't come back yet. Show something so the user knows the page hasn't frozen.
- **Error.** The request came back as a failure. Tell the user what went wrong and ideally give them a way to retry.
- **Success.** The request came back with data. Render it.

You handled this same shape in the API Data Display pair program. You'll build the success path first, verify it works, then layer on loading, error, and navigation in that order. After each layer you'll have something concrete to test before adding the next piece.

## Stage 1: Render the list (success path)

Start with the simplest version that satisfies criterion 1: fetch the videos and render them. No loading text, no error handling, no navigation yet.

Replace the current contents of `src/pages/Videos.jsx`:

```jsx
import { useEffect, useState } from 'react';
import { getVideos } from '../mockApi.js';

export default function Videos() {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    getVideos().then((data) => {
      setVideos(data);
    });
  }, []);

  return (
    <div>
      <h1>Available Videos</h1>
      <ul>
        {videos.map((filename) => (
          <li key={filename}>{filename}</li>
        ))}
      </ul>
    </div>
  );
}
```

What's happening:

- **`useState([])`** starts the list empty so the first render has something to map over.
- **`useEffect` with `[]`** runs the fetch exactly once when the component mounts.
- **`setVideos(data)`** triggers a re-render with the real list once the promise resolves.

### Test it

Reload `/videos` in the browser. You should see the heading and four filenames as bullet points. If you don't, fix it before moving on:

- **Empty page or just the heading.** The fetch may have failed silently. Open the DevTools console and look for errors. Most likely an import path issue.
- **Filenames render but no bullets.** That's fine for now. The `<ul>` is there; styling comes later.

## Stage 2: Add the loading state

Right now there's a tiny window between mount and resolve where the page shows "Available Videos" with an empty list. The user can't tell whether the page is broken or still working. Add a loading state to fix that.

Update `Videos.jsx`:

```jsx
import { useEffect, useState } from 'react';
import { getVideos } from '../mockApi.js';

export default function Videos() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getVideos().then((data) => {
      setVideos(data);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <p>Loading videos...</p>;
  }

  return (
    <div>
      <h1>Available Videos</h1>
      <ul>
        {videos.map((filename) => (
          <li key={filename}>{filename}</li>
        ))}
      </ul>
    </div>
  );
}
```

The early `return` when `loading` is true keeps the rest of the function clean. By the time you reach the main return, you know the fetch is done.

### Test it

Reload `/videos` and watch closely. You might catch "Loading videos..." flicker for a fraction of a second before the list shows up. With a 400ms mock delay, it's blink-and-miss-it.

To actually see it, **temporarily** bump the delay in `src/mockApi.js`:

```js
export async function getVideos() {
  await delay(2000);
  return videos;
}
```

Reload `/videos`. You should see "Loading videos..." for about two seconds, then the list. Once you've confirmed it, revert the delay back to `400`.

## Stage 3: Add the error state

The mock always succeeds right now, so users would never see the loading message turn into a blank page if the real backend went down. Add an error state so failures are visible.

Update `Videos.jsx`:

```jsx
import { useEffect, useState } from 'react';
import { getVideos } from '../mockApi.js';

export default function Videos() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getVideos()
      .then((data) => {
        setVideos(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading videos...</p>;
  }

  if (error) {
    return <p>Could not load videos: {error}</p>;
  }

  return (
    <div>
      <h1>Available Videos</h1>
      <ul>
        {videos.map((filename) => (
          <li key={filename}>{filename}</li>
        ))}
      </ul>
    </div>
  );
}
```

Both `.then` and `.catch` set `loading` to `false`. Whatever happens, the loading message goes away.

### Test it

The mock isn't throwing right now, so you need to force a failure. **Temporarily** change `getVideos` in `src/mockApi.js`:

```js
export async function getVideos() {
  await delay(400);
  throw new Error("server unavailable");
}
```

Reload `/videos`. You should see "Could not load videos: server unavailable". Once you've confirmed it, revert the change so `getVideos` returns the array again.

## Stage 4: Add navigation

The acceptance criteria say clicking a video should navigate to a preview page. That needs three things: a `Link` wrapping each filename, a Preview component, and a route registered for it.

### Wrap each filename in a Link

Update the `<li>` in `Videos.jsx` (only the JSX changes; the rest of the file stays the same):

```jsx
import { Link } from 'react-router-dom';
// ...keep the existing imports too
```

```jsx
<ul>
  {videos.map((filename) => (
    <li key={filename}>
      <Link to={`/preview/${filename}`}>{filename}</Link>
    </li>
  ))}
</ul>
```

The template literal `` `/preview/${filename}` `` builds a URL like `/preview/salamander1.mp4` for each entry.

### Create the Preview page

Create `src/pages/Preview.jsx`:

```jsx
import { Link, useParams } from 'react-router-dom';

export default function Preview() {
  const { filename } = useParams();

  return (
    <div>
      <h1>Preview: {filename}</h1>
      <p>Thumbnail and tuning controls will go here in a future pair program.</p>
      <Link to="/videos">Back to videos</Link>
    </div>
  );
}
```

`useParams` reads the dynamic segment from the URL. For `/preview/salamander1.mp4`, `filename` is `"salamander1.mp4"`. That's what makes the page reusable for any video the user clicks.

### Register the route

Add the Preview route in `src/App.jsx`:

```jsx
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home.jsx';
import Videos from './pages/Videos.jsx';
import Preview from './pages/Preview.jsx';

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
        <Route path="/preview/:filename" element={<Preview />} />
      </Routes>
    </div>
  );
}
```

The `:filename` in the path is the dynamic segment. Any URL like `/preview/anything` matches that route, and `useParams` reads whatever was in that slot.

### Test it

1. Reload `/videos`. The filenames should now look like links (probably underlined and a different color).
2. Click `salamander1.mp4`. You should land on `/preview/salamander1.mp4` and see "Preview: salamander1.mp4".
3. Click "Back to videos". You should land back on the list.
4. Try a few different filenames. Each one should produce a Preview page with the correct filename in the heading.

## Final check against the criteria

You tested each piece as you built it. Walk through all four criteria one more time so you're confident nothing regressed:

1. **List of clickable entries.** `/videos` shows four filename links.
2. **Loading state visible.** Bump the delay temporarily and confirm the loading message still shows. Revert.
3. **Click navigates to preview.** Click an entry, land on `/preview/<filename>`.
4. **Error state on failure.** Throw in the mock temporarily and confirm the error message renders. Revert.

> **With your partner:** Walk through all four checks together. If any of them fail or feel off, fix them now. Don't move on with a half-working video list.

If you have time left, talk through what the next user story will need (the thumbnail page) and sketch how you'd structure it. You don't have to build it. Just talk through what changes.

> **With your partner:** Look at the second user story on the project overview page (the thumbnail one). What new pieces of state would the Preview page need? What new mock function would you call? Don't write the code; just talk it through so the next session has less ramp-up.

## Commit

```bash
git add .
git commit -m "Implement video list user story with loading, error, and navigation"
```
