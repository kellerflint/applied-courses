---
title: "Show the Thumbnail"
order: 1
---

Picking up where Part 1 left off. You have a Videos page that lists videos and links each one to `/preview/:filename`. The Preview page currently shows the filename and nothing else.

This pair program tackles two user stories from the [project overview](/full-stack-web/salamander-project/01-project-overview/). The first is short. The second is the meat of the session.

## The user story for this page

> As a researcher, I want to see a preview frame of the video I selected so that I can confirm I'm working with the right one before tuning.

Acceptance criteria:

- Given a video has been selected, when the preview page loads, then the app fetches `GET /thumbnail/{filename}` and displays the thumbnail prominently.
- Given the preview page has loaded, when I look at the page, then the filename of the selected video is visible.
- Given I am on the preview page, when I look at the page, then a link or button to return to the video chooser is visible and functional.

The "return to the video chooser" part is already done from Part 1.

## Sample image

Your mock API needs to return *something* when asked for a thumbnail. Right click and save this image into the `public/` folder of your project as `salamander1.jpg`. The file in `public/` is served at the root of your dev server, so it'll be available at `/salamander1.jpg`.

{% image "sample-salamander-frame.jpg", "Sample salamander frame extracted from a research video" %}

> **With your partner:** Make sure both partners pull the latest from your repo and that the image is on both machines. Verify it loads at `http://localhost:5173/salamander1.jpg` before continuing.

## Update the mock

Open `src/mockApi.js`. The `thumbnails` object currently maps each filename to a placeholder URL. Update the entry for `salamander1.mp4` to point at your local image:

```js
"salamander1.mp4": "/salamander1.jpg",
```

Leave the other entries as placeholders. They'll show a generic image while you build, which is fine.

## Extend the Preview page

`Preview.jsx` already reads the `:filename` param from the URL. Now it needs to fetch the thumbnail URL and render the image, with the same loading/error/success pattern you used for the video list.

You've done this shape three times now (API Data Display, Videos page). Same drill: `useEffect` to fetch on mount, three pieces of state, early returns for loading and error.

Build it on your own. Here's the import you'll need:

```jsx
import { getThumbnail } from '../mockApi.js';
```

The function takes a filename and resolves to a URL string. Once you have the URL, render it in an `<img>` tag with an `alt` attribute (use the filename).

### Verify it

1. Click `salamander1.mp4` from the Videos page. The Preview page should show the salamander frame.
2. While the fetch is in flight, a loading state should be visible. The mock delay is 300ms, so bump it to `2000` temporarily if you want to actually see it. Revert when done.
3. Click any other filename. The Preview page should show whatever placeholder image the mock returns for that filename.
4. Force an error: in `mockApi.js`, temporarily make `getThumbnail` throw for one filename. Confirm the error state renders. Revert.

> **With your partner:** Walk through all four checks. If any fail, fix before you move on. The next page is heavier and you'll want this part solid first.
