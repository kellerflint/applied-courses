---
title: "Challenges"
order: 4
---

You have a working editor. Now extend it. There are two recommended challenges below. If you finish both and have time, you're welcome to add additional features of your own.

These are intentionally less guided than the walkthrough. Spec out what you want, sketch the state changes you'll need, and try it. The walkthrough's reveals were complete answer keys. The challenges below give you a direction and leave the implementation to you.

## Challenge 1: Click and Drag to Paint

Right now you have to click each cell individually. For anything more involved than five pixels, that's tedious. Make it so the user can hold down the mouse button and drag across cells to paint a streak.

You don't need a library for this. Plain DOM events give you everything you need. Think about which mouse events fire when:

- The user presses the button down on an element
- The user moves into a new element while the button is still held
- The user releases the button

You'll also want a small piece of state that tracks whether the user is currently in "painting" mode, and you'll need to make sure painting stops cleanly when they let go of the mouse, even if they release outside the grid.

> **With your partner:** Before you code, draw a quick state diagram on paper or a whiteboard. What events flip "is painting" on? What events flip it off? Where does each event live (which element listens for it)?

## Challenge 2: Export Your Art as a PNG

Add an Export button that downloads the user's painting as an image file. This is a real feature: the student should be able to save their pixel art and use it as a profile picture, a sticker, anything.

The browser has a `<canvas>` element you can draw onto programmatically. Here's the approach:

1. Create a canvas element in JavaScript. It doesn't need to be on the page, since `document.createElement('canvas')` works fine.
2. Set its width and height. Each grid cell will map to a square in the image, so decide on a per-cell scale. 20 pixels per cell gives you a 320×320 image, which is a reasonable size.
3. Get the canvas's 2D drawing context with `canvas.getContext('2d')`. The context is the API for actually drawing on the canvas. You'll use `ctx.fillStyle = '...'` to set a color and `ctx.fillRect(x, y, w, h)` to fill a rectangle of that color.
4. Walk over your grid state and fill one rectangle per cell, in the right position and the right color.
5. Call `canvas.toDataURL('image/png')` to get the image as a base64-encoded string.
6. Trigger the download by creating an anchor element with `download="filename.png"` and `href=<the data URL>`, then calling `.click()` on it programmatically.

That's the flow. The pieces you'll need to figure out yourself: the math that maps a (row, column) pair to (x, y) coordinates on the canvas, and the loop structure that walks the grid.

If you get stuck on canvas (which is possible seeing as you probably haven't used it before) feel free to reference the export function below


<details>
<summary>Reveal answer</summary>

```jsx
function exportPng() {
  const canvas = document.createElement('canvas')
  canvas.width = GRID_SIZE * EXPORT_SCALE
  canvas.height = GRID_SIZE * EXPORT_SCALE
  const ctx = canvas.getContext('2d')
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
    ctx.fillStyle = grid[r][c]
    ctx.fillRect(c * EXPORT_SCALE, r * EXPORT_SCALE, EXPORT_SCALE, EXPORT_SCALE)
    }
  }
  const link = document.createElement('a')
  link.download = 'pixel-art.png'
  link.href = canvas.toDataURL('image/png')
  link.click()
}
```

</details>

## Optional: Add Your Own Feature

If you finish both challenges and still have time, add a feature of your own. Some ideas if nothing comes to mind: an eraser tool, undo, save and reload to localStorage, a "fill" tool that paints all connected cells of the same color, a way to save your favorite color combinations as a custom palette. Build whatever you'd want to try.
