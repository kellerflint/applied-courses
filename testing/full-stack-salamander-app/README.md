# Full Stack Salamander App (reference build)

This is a working reference implementation built by following the
[Salamander Project Part 1](../../full-stack-web/salamander-project-part-1/)
pair program lesson end to end, exactly as written, to verify the
instructions produce a working app.

It exists so the lesson can be re-validated quickly when React, Vite,
or React Router release breaking changes.

## What's verified here

By page of the lesson:

- **01-routes-and-pages.md** — Vite + React project scaffolded, React
  Router installed and wrapping `App`, Home and Videos pages render,
  client-side navigation between them works.
- **02-mock-api.md** — `src/mockApi.js` exports `getVideos`,
  `getThumbnail`, `submitProcessingJob`, `getJobStatus` as async
  functions. The Videos page's `useEffect` logs the array on mount.
- **03-video-list.md** — All four acceptance criteria for the
  "list of available videos" user story pass:
  1. Page renders four clickable entries on load.
  2. Loading state is visible during the fetch.
  3. Clicking an entry navigates to `/preview/:filename`.
  4. Error state renders when the mock throws.

## Run it

```bash
cd salamander-tracker
npm install
npm run dev
```

Then open the URL Vite prints. Navigate to `/videos` and confirm the
list loads.

## Notes captured while validating

Three places where the lesson needed updating against current Vite 8 /
React 19 / React Router 7 (all applied):

1. **`main.jsx`** uses the modern `import { StrictMode }` /
   `createRoot` style. Lesson updated to show students editing what's
   already there instead of replacing with the old `React.StrictMode`
   style.
2. **`App.jsx`** scaffolded by Vite is no longer the tiny click-counter
   demo. The page now explicitly says "Replace the entire file."
3. **StrictMode double-invocation** in dev means the page-2 console.log
   shows twice. Page 2 now preempts that confusion with a one-paragraph
   explanation.

### Staged-test restructure

A second pass added incremental verify points so students test each
piece as they build it instead of waiting until the end:

- **Page 1: Routes and Pages** — routes are now wired before the nav
  links, so students verify routing by typing `/` and `/videos` in
  the address bar before any UI exists for navigation. Adding nav
  links is its own step with its own verify.
- **Page 3: Video List** — split into four stages with a test after
  each: render the success path → add loading state → add error state
  → add navigation. Students see something working at each step
  instead of building everything blind and debugging the result.
