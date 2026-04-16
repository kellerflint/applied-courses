---
title: "The Client Project"
order: 2
---

Time to put user stories to work on a real project. You've been hired by a small indie record label to build a page showcasing their artist roster.

## The Client Brief

Here's what the client sent over:

> Hey! We're Wavelength Records, a small independent label based out of Seattle. We've been around since 2018 and we have five artists on our roster right now. We need a simple page that shows off who we are and who our artists are. For each artist, we want people to see their name, their genre, a short bio, and the albums they've put out. The design should feel clean and modern. Also, a lot of music fans are on their phones, so it definitely needs to look good on mobile. We can host it ourselves once it's done. Thanks!

That's the whole brief. It's informal, it's missing details, and it does not tell you how to build anything. That's normal. Your job is to translate it into user stories and acceptance criteria before writing a single line of code.

## Your Data

The client has provided their artist data. Save this as `data.json` in your project's `src` folder.

```json
{
  "label": "Wavelength Records",
  "founded": 2018,
  "city": "Seattle, WA",
  "tagline": "Independent music for independent minds",
  "artists": [
    {
      "id": 1,
      "name": "Luna Park",
      "genre": "Indie Pop",
      "bio": "Dreamy melodies and introspective lyrics from Portland's Luna Park have earned them a devoted following across the Pacific Northwest.",
      "albums": [
        { "title": "Soft Machinery", "year": 2021 },
        { "title": "Glass Ceiling", "year": 2023 }
      ]
    },
    {
      "id": 2,
      "name": "The Hollow Grove",
      "genre": "Folk Rock",
      "bio": "Drawing from Appalachian folk traditions and modern rock, The Hollow Grove craft timeless songs rooted in storytelling.",
      "albums": [
        { "title": "Roots & Wire", "year": 2020 },
        { "title": "Quiet Season", "year": 2022 }
      ]
    },
    {
      "id": 3,
      "name": "Neon Drifter",
      "genre": "Synthwave",
      "bio": "Late-night drives and neon-lit cityscapes inspire Neon Drifter's pulsing synthesizer-driven sound.",
      "albums": [
        { "title": "Midnight Protocol", "year": 2022 },
        { "title": "Signal/Noise", "year": 2024 }
      ]
    },
    {
      "id": 4,
      "name": "Calla Frost",
      "genre": "Dream Pop",
      "bio": "Calla Frost's ethereal vocals and layered production create soundscapes that feel both intimate and expansive.",
      "albums": [
        { "title": "Still Water", "year": 2019 },
        { "title": "Passerine", "year": 2021 },
        { "title": "Blue Hours", "year": 2024 }
      ]
    },
    {
      "id": 5,
      "name": "Broken Compass",
      "genre": "Post-Rock",
      "bio": "Instrumental journeys through dynamic tension and release, Broken Compass build songs that need no words.",
      "albums": [
        { "title": "Exit Signs", "year": 2021 },
        { "title": "Cartography", "year": 2023 }
      ]
    }
  ]
}
```

## Step 1: Write Your User Stories

Read the client brief again. Identify the two distinct things a visitor to this page needs to be able to do. Write a user story for each one.

Keep the user specific. "A visitor" is fine here since this page has no login, but "a user" is too generic. Think about who is actually coming to this page and why.

> **With your partner:** Write both user stories before moving on.

## Step 2: Write Acceptance Criteria

For each user story, write at least three acceptance criteria using the Given/When/Then format.

At least one criterion for each story should address:
- What specific data is visible on screen
- How the page behaves on mobile (the client explicitly mentioned this)

> **With your partner:** Write your acceptance criteria. Be specific enough that someone who had never seen the brief could run a test from each criterion alone.

## Step 3: Check Your Work With AI

AI is useful for getting feedback on whether your stories and criteria are well-formed. But a vague prompt produces vague feedback. You need to tell the AI exactly what to look for, the same way good acceptance criteria tell a developer exactly what "done" means.

This is actually the same skill. When you work with AI effectively, you're doing the same kind of thinking as when you write user stories. You're defining who the AI is, what you want it to do, and what good output looks like. Vague requests get vague results, just like vague requirements produce the wrong software.

Your instructor will show you how to access Google Gemini. When you open it, paste this prompt in as your first message, then follow up with your user stories and acceptance criteria.

```
You are reviewing user stories and acceptance criteria written by software development students. Give specific feedback on the following.

For each user story, check:
- Is it in the correct format: "As a [specific type of user], I want [goal] so that [reason]"?
- Is the user specific enough to rule out wrong interpretations? Flag anything too vague, like "as a user" with no further context.
- Does the goal describe a user outcome, not a developer task? Flag any story written from a developer's perspective or that describes an implementation rather than what the user needs.
- Is the reason meaningful and specific, or is it vague filler?

For each acceptance criterion, check:
- Is it in the correct Given / When / Then format?
- Is it specific enough to actually run as a test? Flag anything that uses vague language like "works correctly," "looks good," or "displays properly" without measurable specifics.
- Does the "then" describe an observable, verifiable outcome?

List each issue separately. If something is correct, say so briefly. Do not rewrite anything for the student. Describe what needs to change and let them fix it.
```

Read the feedback critically. AI is a useful reviewer but it is not always right. If it flags something, decide whether the feedback actually applies to what you wrote. Fix what you agree with. Be ready to explain anything you kept.

> **With your partner:** After getting AI feedback, revise your stories and criteria until you're satisfied with them. Then move on to Step 4.

## Step 4: Set Up Your GitHub Project

A GitHub Project is a Kanban board that lives alongside your repository. You'll use it to track your stories through development.

### Create the project

1. Go to your GitHub repository page
2. Click the **Projects** tab
3. Click **Link a project**, then **New project**
4. Choose the **Board** template
5. Name it **Wavelength Records**
6. Click **Create project**

You now have a board with three columns: **Todo**, **In Progress**, and **Done**. Rename **Todo** to **Backlog** by clicking the column header.

### Add your stories

1. Click **+ Add item** at the bottom of the **Backlog** column
2. Type the title of your first user story and press Enter
3. Repeat for your second user story

These cards are draft issues. They're not linked to any actual code changes, which is fine for now. The point is to have a visible record of what needs to be built before you start building it.

> **With your partner:** Get both user stories into the Backlog column before moving on. Your board should show two cards in Backlog and nothing in the other columns.
