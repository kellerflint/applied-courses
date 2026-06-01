---
title: "Add Your Own Feature"
order: 4
---

The project requires **one feature of your own**, something beyond the user stories. This is where you get to make the app yours and show you can extend a system, not just follow a spec.

## The bar

The feature should have a little real scope to it, enough that building it teaches you something, but not so much that it becomes a second project. Aim for something you could build well in a focused weekend. Be ready to demo it and explain how it works at your final meeting.

It should be a genuine addition. Restyling a button or renaming a page doesn't count. Adding a capability the app didn't have does.

## Ideas at the right scope

Pick one of these or invent your own. These are sized roughly right:

- **A real database on the backend.** Persist the jobs a user has submitted so the frontend can show a history of past runs with their settings and CSV links.
- **Analyze the detection CSV.** When a job finishes, fetch the CSV and compute something from it. Which quadrant of the frame the salamander spent the most time in. Total distance traveled. A simple heatmap or a small chart of position over time.
- **Pin or tag videos.** Let a researcher mark videos and filter the list, persisted in `localStorage` or your backend.
- **A processing queue view.** If you can submit multiple jobs, show them all with live status, not just the most recent one.

## Ideas that are too big or too small

- **Too small:** a color theme toggle, renaming things, a single extra static page with no behavior.
- **Too big:** user accounts with authentication, training your own detection model, a full real-time multi-user system. These are great instincts for later, but they'll eat the time you need for the required stories. Start with something smaller and built it out as time permits.

> **With your partner:** Pick your feature and write a one-sentence description of what it does and why it's useful to a researcher. Then list the 3 to 5 concrete steps to build it. If the step list is short and clear, the scope is right. If you can't break it down, it's probably too big or too vague. Run it by a tutor or by me if you're unsure about the scope.

## Build it last, but plan it now

Finish and verify the required user stories first. The feature is what you add once the core app works, because a clever feature bolted onto a broken app won't demo well. But decide what the feature is now, so you can leave room for it and so it can inform small choices you make while building the rest.
