---
title: "Build the Pixel Art Editor"
order: 2
---

Now you'll build the editor. The brief is below: a user story, acceptance criteria, and a screenshot. There's a walkthrough on the next page if you get stuck. Try this from the brief alone first. Working from a spec is the skill you're practicing.

## What You're Building

A small React app where users paint pixel art by clicking cells in a grid. They pick a color from a palette or a color picker, click a cell to paint it, and clear the canvas when they want to start over.

{% image "pixel-art-editor.png", "Pixel art editor with color picker, preset palette, clear button, and 16x16 grid" %}

## User Story

> As a user, I want to paint pixel art on a small grid so that I can make a piece of art and see the result.

## Acceptance Criteria

- Given the page loads, when I look at the page, then I see a 16×16 grid of empty cells, a color picker, a row of preset color swatches, and a Clear button.
- Given the page loads, when I look at the color picker, then a default color is already selected.
- Given a color is selected, when I click a cell in the grid, then that cell fills with the selected color.
- Given a cell is already painted, when I click it again with a different color selected, then it changes to the new color.
- Given I click a preset color swatch, when I look at the color picker, then the picker now shows that color, and clicking a cell paints with it.
- Given I have painted on the grid, when I click Clear, then every cell returns to the default empty color.

## Try It

Set up a fresh Vite + React project and build to the acceptance criteria above. The structure is lighter than your last React project, so a single component file is fine.

> **With your partner:** Before you write any code, talk through what state you need and what shape it should have. What's the minimum number of state variables that lets you satisfy every criterion above?

Spend at least 15 minutes attempting this from the brief before opening the walkthrough. Getting stuck is part of it. Working through "what state do I need" and "how do I render the grid from that state" is exactly the skill you're here to practice.

If you've worked through it for a while and want hints on structure, the walkthrough on the next page steps through one possible approach.