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

You handled this same shape in the API Data Display pair program. The acceptance criteria explicitly require loading and error states, so build all three from the start.

## Update the Videos page

Replace `src/pages/Videos.jsx` with the full implementation:

```jsx
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
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
          <li key={filename}>
            <Link to={`/preview/${filename}`}>{filename}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

Walking through what changed:

- **Three pieces of state** (`videos`, `loading`, `error`) cover the three states of the fetch.
- **The `useEffect` calls `getVideos`** when the component mounts. The empty dependency array `[]` means it runs exactly once, not on every render.
- **`.then` and `.catch`** handle the success and error paths. Both set `loading` to `false` so the loading message goes away in either case.
- **The early returns** for loading and error states keep the success path simple. By the time you get to the `return` at the bottom, you know the data is real.
- **`Link to={\`/preview/${filename}\`}`** uses a template literal to build the URL for that specific video. Clicking it does a client-side navigation to a route like `/preview/salamander1.mp4`.

## Add a Preview route

The Videos page links to `/preview/:filename`, so you need a route that matches. Create `src/pages/Preview.jsx`:

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

Then register the route in `src/App.jsx`:

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

The `:filename` in the path is the dynamic segment. Any URL like `/preview/anything` matches that route, and `useParams` will give you whatever was in that slot.

## Verify against the acceptance criteria

Now check your work against the spec. For each criterion, do the thing it describes and confirm what's supposed to happen actually happens.

**1. Page loads and renders each video as a clickable entry.** Reload `/videos`. After a brief moment, you should see four video filenames, each one a link.

**2. Loading state is visible while the request is in flight.** Reload the page and watch carefully. The "Loading videos..." text should appear for a fraction of a second before the list shows up. If it's too fast to see, bump the `delay(400)` in `mockApi.js` to `delay(2000)` temporarily.

**3. Clicking a video navigates to its preview page.** Click `salamander1.mp4`. You should land on `/preview/salamander1.mp4` and see "Preview: salamander1.mp4". The back-to-videos link should bring you home.

**4. Error state is shown if the API fails.** Force an error in your mock to test this. Temporarily change `getVideos` in `mockApi.js`:

```js
export async function getVideos() {
  await delay(400);
  throw new Error("server unavailable");
}
```

Reload `/videos`. You should see "Could not load videos: server unavailable". When you've confirmed it works, revert the change.

> **With your partner:** Walk through all four checks together. If any of them fail or feel off, fix them now. Don't move on with a half-working video list.

## What "done" looks like

When all four acceptance criteria pass, the first user story is done. That's the bar for this pair program.

If you have time left, talk through what the next user story will need (the thumbnail page) and sketch how you'd structure it. You don't have to build it. Just talk through what changes.

> **With your partner:** Look at the second user story on the project overview page (the thumbnail one). What new pieces of state would the Preview page need? What new mock function would you call? Don't write the code; just talk it through so the next session has less ramp-up.

## Commit

```bash
git add .
git commit -m "Implement video list user story with loading, error, and navigation"
```
