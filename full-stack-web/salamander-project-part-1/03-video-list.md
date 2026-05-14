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

## Three states, four stages

Every fetch is in one of three states at any moment: **loading**, **error**, or **success**. You handled all three in the API Data Display pair program. Same shape here.

You'll build it in four stages, with a quick verify after each: success path → loading → error → navigation. The point is to never have more than one moving piece between you and a working test.

## Stage 1: Render the list (success path)

Start with the smallest thing that satisfies criterion 1: fetch and render. No loading, no error, no navigation yet.

Replace the contents of `src/pages/Videos.jsx`:

```jsx
import { useEffect, useState } from 'react';
import { getVideos } from '../mockApi.js';

export default function Videos() {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    getVideos().then((data) => setVideos(data));
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

Reload `/videos`. You should see four bullet-pointed filenames. If you see the heading but no list, the fetch failed silently; check the DevTools console for an import error.

## Stage 2: Add the loading state

There's currently a brief window between mount and resolve where the page shows the heading with an empty `<ul>`. The user can't tell whether the page is broken or still working. Fix that.

Three small additions to `Videos.jsx`:

A new piece of state alongside `videos`, defaulting to `true`:

```jsx
const [loading, setLoading] = useState(true);
```

A line inside your `.then` that flips it to false once the data lands:

```jsx
setLoading(false);
```

And an early return above the main return that short-circuits while it's true:

```jsx
if (loading) {
  return <p>Loading videos...</p>;
}
```

### Test it

Reload `/videos`. The 400ms mock delay makes the loading message blink-and-miss-it. To actually see it, **temporarily** bump the delay in `src/mockApi.js` to `delay(2000)`. Confirm "Loading videos..." shows for about two seconds, then revert.

## Stage 3: Add the error state

If the real backend goes down, your loading message would just hang forever. Add a failure path.

Same shape as the loading state. Three additions:

A new state:

```jsx
const [error, setError] = useState(null);
```

A `.catch` chained after your `.then`. **Both branches** should set `loading` to `false` so the loading message goes away no matter what:

```jsx
.catch((err) => {
  setError(err.message);
  setLoading(false);
});
```

A second early return above the main one:

```jsx
if (error) {
  return <p>Could not load videos: {error}</p>;
}
```

### Test it

The mock always succeeds right now, so force a failure. **Temporarily** replace the body of `getVideos` in `src/mockApi.js` with a `throw`:

```js
throw new Error("server unavailable");
```

Reload `/videos`, confirm the error message renders, then revert.

## Stage 4: Add navigation

Three things needed: wrap each filename in a `Link`, build the Preview component, register the route.

### 1. Wrap the filename in a Link

Add `Link` to the existing `react-router-dom` import in `Videos.jsx`, then update the `<li>`:

```jsx
<li key={filename}>
  <Link to={`/preview/${filename}`}>{filename}</Link>
</li>
```

The template literal builds a URL like `/preview/salamander1.mp4` per entry.

### 2. Create the Preview page

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

`useParams` reads the dynamic segment from the URL. For `/preview/salamander1.mp4`, `filename` is `"salamander1.mp4"`. That's what makes one Preview component work for any video.

### 3. Register the route

Import Preview in `src/App.jsx` and add a third `<Route>` next to the existing two:

```jsx
<Route path="/preview/:filename" element={<Preview />} />
```

The `:filename` is the dynamic segment. Any URL like `/preview/anything` matches and `useParams` reads what was in that slot.

### Test it

Click an entry on `/videos`. You should land on `/preview/<filename>` with the filename in the heading. "Back to videos" should bring you back. Try a few different entries.

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
