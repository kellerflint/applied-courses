---
title: "Build and Ship"
order: 3
---

Your stories are written, your acceptance criteria are set, and your backlog is ready. Now you build.

## Pull Your First Story

Go to your GitHub Project board and drag your first user story from **Backlog** into **In Progress**. Do this before writing any code. In a real team, the board is how everyone knows what's being worked on. Moving a card signals that work has actually started.

## Set Up the Project

Create a new Vite React project:

```bash
npm create vite@latest
```

Choose React and JavaScript when prompted. Once it's running, delete everything inside the `return ()` in `App.jsx` and clear out both CSS files. Start with a blank page.

Copy your `data.json` into the `src` folder.

> **With your partner:** Get both machines running with a blank page before continuing.

## Import and Verify Your Data

Importing JSON in React works like importing any other file:

```js
import data from './data.json'
```

Before building anything, verify the import actually worked. Add a `console.log(data)` inside your `App` function and check the browser console. You should see the full Wavelength Records object with all five artists.

If you see `undefined` or an error, the file path is wrong. Fix it before continuing.

> **With your partner:** Confirm the data is showing in the console on both machines before moving on. Don't skip this step.

## Plan Your Components

Your app needs a tree of components. Each level receives data from its parent and passes pieces of it further down.

Here's the structure to build toward:

```
App
  reads data.json directly
  renders: label header, then ArtistList

ArtistList
  receives: the artists array as a prop
  renders: one ArtistCard per artist

ArtistCard
  receives: a single artist object as a prop
  renders: name, genre, bio, then one AlbumItem per album

AlbumItem
  receives: a single album object as a prop
  renders: the album title and year
```

Try to sketch out what each component file will look like before writing code. What props does it accept? What does it render? What does it pass down?

<details>
<summary>Show example code</summary>

```jsx
// App.jsx
import data from './data.json'
import ArtistList from './components/ArtistList'

function App() {
  return (
    <div>
      <header>
        <h1>{data.label}</h1>
        <p>{data.tagline}</p>
      </header>
      <ArtistList artists={data.artists} />
    </div>
  )
}

export default App
```

```jsx
// ArtistList.jsx
import ArtistCard from './ArtistCard'

function ArtistList({ artists }) {
  return (
    <div className="artist-list">
      {artists.map(artist => (
        <ArtistCard key={artist.id} artist={artist} />
      ))}
    </div>
  )
}

export default ArtistList
```

`.map()` loops over the array and returns one `ArtistCard` for each artist. The `key` prop is required on any list of elements in React. Use a unique value from your data, like `id`.

```jsx
// ArtistCard.jsx
import AlbumItem from './AlbumItem'

function ArtistCard({ artist }) {
  return (
    <div className="artist-card">
      <h2>{artist.name}</h2>
      <span>{artist.genre}</span>
      <p>{artist.bio}</p>
      <div className="albums">
        {artist.albums.map(album => (
          <AlbumItem key={album.title} album={album} />
        ))}
      </div>
    </div>
  )
}

export default ArtistCard
```

```jsx
// AlbumItem.jsx
function AlbumItem({ album }) {
  return (
    <div className="album">
      <span>{album.title}</span>
      <span>{album.year}</span>
    </div>
  )
}

export default AlbumItem
```

</details>

> **With your partner:** Before writing your own components, trace the path a single album title takes from the import in `App.jsx` all the way to the screen. Which components does it pass through?

## Build One Component at a Time

Build and test each component before moving to the next. Don't try to wire up the whole tree at once.

A good order:

1. Get `App` rendering the label name and tagline from `data` and confirm it on screen
2. Build `ArtistCard` and render one artist manually in `App` with hardcoded data to confirm the layout
3. Build `ArtistList` and switch to rendering all artists from the array
4. Build `AlbumItem` and render albums inside `ArtistCard`

After each step, look at the page and verify it's showing what you expect. Fix any problems before continuing.

> **With your partner:** After getting `ArtistCard` working with one hardcoded artist, swap to rendering from the array. Confirm all five artists show up before adding albums.

## Style and Check Your Criteria

Work through the styling. When you think a story is done, go back to your acceptance criteria and check each one against what you've actually built. Read them line by line. Open the page at a narrow browser width and test the mobile criteria.

A story is done when every acceptance criterion passes. "Basically works" is a different standard from the one you wrote down.

> **With your partner:** When your first story is complete, move its card to **Done** on the board and pull the second story into **In Progress**.

## Deploy

Get your project live using GitHub Pages: [Hosting with GitHub Pages](/full-stack-web/orientation/05-github-pages/)

Run `npm run deploy` to push the latest version to your live URL.

Once it's live, go through your acceptance criteria one more time from the deployed URL, not just localhost. Mobile behavior in particular can differ.

> **With your partner:** Get both sites live. Move your remaining stories to Done when everything checks out.

## Submit

Submit a link to your GitHub repository and your live GitHub Pages URL on Canvas. Your GitHub Project board should show all stories in the Done column.

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Full+Stack+Web+Development&unit=Agile+Basics" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
