---
title: "useState Refresher"
order: 1
---

This unit's project is a React app where you click cells in a grid to paint pixel art. Before you build it, you need to be solid on `useState`, the React hook that powers the whole thing.

You've already worked with state in the clicker game. There you stored values in plain variables (`let score = 0`) and called an `updateDisplay` function whenever they changed. React handles the "update the screen" part for you. You tell it the value changed, and it re-renders the component automatically. That auto-rerender is the whole point of using React.

## The useState Hook

`useState` is how a function component remembers a value across renders. Import it from React and call it inside your component.

```jsx
import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  )
}
```

`useState(0)` does two things. It declares a piece of state with `0` as the initial value, and it returns an array with two items: the current value and a function to update it. We destructure them out as `count` and `setCount`. The naming is a convention you'll see everywhere: `[thing, setThing]`.

When you call `setCount(...)` with a new value, React stores it and schedules a re-render of the component so the screen reflects the change. State is read-only from the component's perspective. The setter is the only way to change it, and calling the setter is what gives React the signal it needs to re-render.

> **With your partner:** Why does React require you to go through `setCount` rather than letting you write `count = 5` directly?

<details>
<summary>Reveal answer</summary>

Direct assignment wouldn't notify React that anything had changed. The setter call is React's signal: "this value moved, redraw what depends on it." Without that signal, your screen would silently fall out of sync with your data.

</details>

## State Can Hold Anything

The initial value can be any JavaScript value: a number, string, boolean, array, or object.

```jsx
const [name, setName] = useState('')
const [isOpen, setIsOpen] = useState(false)
const [todos, setTodos] = useState([])
const [user, setUser] = useState({ id: 1, name: 'Alex' })
```

Each call to `useState` is a separate piece of state. A component can have as many as it needs.

## Updating Arrays and Objects

When state holds an array or object, hand the setter a brand new copy of it. Modifying the existing one and setting it back will not trigger a re-render.

```jsx
// Wrong: mutates the existing array, then sets it back unchanged.
todos.push(newTodo)
setTodos(todos)

// Right: pass a new array, with the old items spread in plus the new one.
setTodos([...todos, newTodo])
```

The reason is that React decides whether to re-render by comparing the old reference against the new one. The same array (even with extra items pushed in) is the same reference, so React sees no change. A fresh array is a fresh reference, and React knows to update.

This rule extends to nested data. To change one row of a 2D array, build a new outer array containing a new inner row, leaving the rest unchanged.

```jsx
const next = grid.map(row => row.slice()) // copy every row into a new outer array
next[r][c] = 'red'                        // modify the copy
setGrid(next)                             // hand the copy to React
```

You'll be using exactly this pattern when you paint pixels.

## Controlled Inputs

When you wire an input's `value` and `onChange` both to state, the input is called a **controlled input**. State is the source of truth for what's in the box, and the input just displays it.

```jsx
function NameForm() {
  const [name, setName] = useState('')

  return (
    <div>
      <input
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <p>Hello, {name}!</p>
    </div>
  )
}
```

Every keystroke fires `onChange`, which calls `setName`, which updates state, which re-renders the component, which puts the new value into `<input value={name}>`. The greeting paragraph updates as the user types because it reads from the same state.

This pattern is the same shape for every input element: `<input type="color">`, `<input type="number">`, `<select>`, `<textarea>`. All of them take `value` from state and call the setter from `onChange`. You'll use this pattern for the color picker.

{% activity "controlled-input-trace.html", "Controlled Input Trace", "560px" %}

> **With your partner:** Trace what happens when a user types a single character into the input. Walk through every step from the keystroke to the screen showing the new letter.

<details>
<summary>Reveal answer</summary>

1. The user presses a key, and the browser fires a native `input` event on the `<input>` element
2. React calls the `onChange` handler with an event object, and the handler calls `setName(e.target.value)` with the new full string
3. React stores the new value and schedules a re-render of the component
4. The component function runs again, this time reading the updated `name`
5. React compares the new JSX to the previous render, updates the DOM where they differ, and the user sees the new letter in the input and the updated greeting below

</details>

## Warm Up

Before moving on, build a tiny controlled input in a fresh component to make sure the pattern is fresh in your hands. Spin up a Vite + React project (or modify an existing one) and write a component that has a text input and shows a live preview of what's been typed.

> **With your partner:** Take five minutes to build the warm-up. One person types, the other names what's happening at each keystroke. Then switch.

When that feels easy, move to the next page.
