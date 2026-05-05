---
title: "Walkthrough"
order: 3
---

This page has the walkthrough and the answer code for each step. The code reveals are here as a backstop for when you're properly stuck (think 10 to 15 minutes of trying without progress on a step), not as a first stop. Working through the difficulty is where the learning is.

If you read code first, you'll think you understood it, then walk away unable to explain it from scratch. If you struggle first, then read code, you'll understand why each line is there. The point of this whole sequence is to grow the skill of going from a screenshot and a list of criteria to working code.

If you finished the editor on your own before opening this page, still read through. Your version might be cleaner, or this might do something you didn't think of, or you might want to ask why a particular choice was made. Comparing your code to someone else's solution is one of the more useful exercises a developer can do.

## 1. Set Up the Project

Create a new Vite + React project and clear out the boilerplate. You want a single component file (`App.jsx`) and one CSS file you'll write your styles in. Start the dev server before you write anything so you can see your changes live.

## 2. Decide What State You Need

You need two pieces of state. First, the grid: a structure that remembers a color for every cell of a 16-by-16 board. Second, the currently selected color: a single color value. Initialize each cell to the default empty color (white works well) and the selected color to whatever feels good as a starting brush color (black or dark grey both look fine).

Define constants for the grid size and default color near the top of the file. A single named constant means you can change it once if you ever want a 32-by-32 grid later, instead of hunting for magic numbers all through the code.

> **With your partner:** What data structure represents a 16-by-16 grid where each cell holds a color? Think about what it would look like in plain JavaScript before you write any React code.

<details>
<summary>Reveal answer</summary>

```jsx
import { useState } from 'react'
import './App.css'

// Constants for the grid. One place to change if dimensions ever shift.
const GRID_SIZE = 16
const DEFAULT_COLOR = '#ffffff' // white = unpainted

// Builds a fresh 16x16 array of arrays, every cell holding the default color.
function makeEmptyGrid() {
  return Array.from(
    { length: GRID_SIZE },                        // outer length: 16 rows
    () => Array(GRID_SIZE).fill(DEFAULT_COLOR)    // each row: 16 cells of white
  )
}

function App() {
  // The grid: a 2D array of color strings.
  const [grid, setGrid] = useState(makeEmptyGrid)

  // The currently selected color, applied the next time a cell is clicked.
  const [currentColor, setCurrentColor] = useState('#1a1a1a')

  return <div></div>
}

export default App
```

</details>

## 3. Render the Grid

Render a button for each cell. The simplest approach is two nested `.map` calls over the grid array: outer over rows, inner over each row's colors. Each button uses the cell's color as its background style. Wrap all the buttons in a container styled as a CSS grid with 16 equal columns so the visual layout matches the data shape.

Every list item React renders needs a unique `key` prop so React can track which cell is which across re-renders. The row plus column position works as a key because no two cells share both.

<details>
<summary>Reveal answer</summary>

{% raw %}
```jsx
return (
  <div className="pixel-art">
    <h1>Pixel Art Editor</h1>

    {/* Container styled as a CSS grid with 16 equal columns */}
    <div
      className="pixel-grid"
      style={{ gridTemplateColumns: `repeat(${GRID_SIZE}, 1fr)` }}
    >
      {/* Outer map walks each row, with row index r */}
      {grid.map((row, r) =>
        // Inner map walks each cell's color in that row, with column index c
        row.map((color, c) => (
          <button
            // Unique key per cell so React reconciles correctly across renders
            key={`${r}-${c}`}
            className="pixel"
            // Use the cell's stored color as the button's background
            style={{ background: color }}
            aria-label={`Pixel ${r}, ${c}`}
          />
        ))
      )}
    </div>
  </div>
)
```
{% endraw %}

```css
/* App.css */
.pixel-grid {
  display: grid;
  gap: 1px;                  /* thin gap creates visible cell borders */
  background: #d4d4d4;       /* shows through the gap as the grid line color */
  border: 1px solid #d4d4d4;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 1;           /* keeps the grid square no matter the width */
  max-width: 640px;
}

.pixel {
  border: none;
  padding: 0;
  cursor: crosshair;
  aspect-ratio: 1;           /* keeps cells square */
}
```

</details>

## 4. Paint a Cell on Click

When a cell is clicked, the cell at that row and column should change to the currently selected color. The trap here is the immutable update rule from the refresher. You cannot reach into the existing grid, change one entry, and call `setGrid` with the same array. React would compare references, see the same array, and skip the re-render. You need a fresh outer array containing a fresh inner row with the change applied.

Write a `paint` function that takes a row and column, builds a copied grid, sets the new color at that position, and passes the new grid to `setGrid`. Wire it to each cell's `onClick`.

<details>
<summary>Reveal answer</summary>

{% raw %}
```jsx
function paint(row, col) {
  // grid.map(r => r.slice()) builds a new outer array containing
  // shallow copies of each inner row. The result shares zero references
  // with the old grid, so React detects the change and re-renders.
  const next = grid.map(r => r.slice())

  // Update only the cell that was clicked.
  next[row][col] = currentColor

  // Hand React the new grid.
  setGrid(next)
}

// In the JSX, on the cell button:
<button
  key={`${r}-${c}`}
  className="pixel"
  style={{ background: color }}
  // Pass r and c through so paint knows which cell was clicked
  onClick={() => paint(r, c)}
  aria-label={`Pixel ${r}, ${c}`}
/>
```
{% endraw %}

</details>

## 5. The Color Picker

Add a native color input above the grid and wire it as a controlled input. Its `value` comes from `currentColor`, and its `onChange` calls `setCurrentColor` with the new value from the input. Now whenever the user changes the picker, state updates, the picker reflects it, and any subsequent click paints with the new color.

<details>
<summary>Reveal answer</summary>

```jsx
{/* Place this inside .pixel-art, above or beside the grid */}
<label className="pixel-tools">
  Color
  <input
    type="color"
    // Value comes from state, not from the input's own internal storage
    value={currentColor}
    // On every change, push the new hex color back into state
    onChange={e => setCurrentColor(e.target.value)}
  />
</label>
```

```css
.pixel-tools {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: #555;
  width: 200px;
}

.pixel-tools input[type="color"] {
  width: 100%;
  height: 44px;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  padding: 4px;
  background: #fff;
}
```

</details>

## 6. Preset Color Swatches

A small palette of buttons, each set to a specific hex color. Clicking one sets `currentColor` to that hex. Render the swatches by mapping over an array of hex strings. Keep the array short, eight to ten colors that look good together. Show the user which swatch is currently selected by giving the matching one a visible style change like a border or scale.

> **With your partner:** Why is the array of presets defined outside the component instead of inside `useState`? What would change if it were inside?

<details>
<summary>Reveal answer</summary>

The presets never change while the app is running, so they're constants, not state. Putting an unchanging value in `useState` would still work, but you'd be paying for state machinery (re-render tracking, the setter function) you never use. Defining it outside the component as a regular `const` is more honest about what it is, which is a fixed list.

{% raw %}
```jsx
// Defined at module scope, outside the App component
const PRESETS = [
  '#000000', '#ffffff', '#e63946', '#f1a208', '#ffd166',
  '#06d6a0', '#118ab2', '#7209b7', '#f72585', '#ff8500',
]

// Inside the JSX, beside the color picker:
<div className="pixel-presets">
  {PRESETS.map(c => (
    <button
      key={c}
      // Add a 'selected' class when this swatch matches the current color
      className={'preset' + (c === currentColor ? ' selected' : '')}
      // Set this button's background to the swatch's hex value
      style={{ background: c }}
      // Clicking a swatch updates the current color, just like the picker does
      onClick={() => setCurrentColor(c)}
      aria-label={`Color ${c}`}
    />
  ))}
</div>
```
{% endraw %}

```css
.pixel-presets {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
}

.preset {
  width: 100%;
  aspect-ratio: 1;
  border: 2px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  padding: 0;
}

.preset.selected {
  border-color: #1a1a1a; /* visible border on the active swatch */
  transform: scale(1.1);
}
```

</details>

## 7. The Clear Button

A button that resets the grid to all empty cells. The implementation is one line: hand `setGrid` a freshly-built empty grid using the helper from step 2.

<details>
<summary>Reveal answer</summary>

```jsx
function clearGrid() {
  // makeEmptyGrid returns a brand-new 2D array of default colors.
  // React sees the new array as a different reference than the old grid,
  // which triggers the re-render.
  setGrid(makeEmptyGrid())
}

// In the JSX, near the tools:
<button className="clear-btn" onClick={clearGrid}>Clear</button>
```

</details>

## Step Back

You now have a working pixel art editor in roughly 80 lines of code. Read your component start to finish. For each piece of state, ask: what reads it, and what writes it? For each function, ask: what does it produce, and what does it depend on?

> **With your partner:** Pick one acceptance criterion from the previous page and trace exactly how your code satisfies it. Which state changes? What re-renders? What does the user see?

If you got it working, the next page has two challenges to extend it.
