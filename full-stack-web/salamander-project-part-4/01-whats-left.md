---
title: "Finishing the Project"
order: 1
---

This is the last unit. There's no guided pair program this time. You and your partner take everything you've built across the previous parts and finish the project: the remaining user stories, a deliberate visual design, and one feature of your own.

You'll do this mostly on your own time outside of class, working with your partner. You have the scaffolding across Parts 1 through 3. The rest of the wiring is up to you. The skill you're developing is reading a spec, figuring out how the pieces connect, and building the rest without someone walking you through the approach.

## How to work when you're stuck

"Figure it out yourself" doesn't mean "suffer alone." It means do your own research first, then use the people around you. In order:

1. **Re-read the data contract and your own code.** Most blocks are a mismatch between what the API returns and what your component expects. The answer is usually already on the page.
2. **Ask your peers.** Other teams are solving the same problems this week.
3. **Ask the tutors.** Every tutor has built this project. They know exactly where it gets tricky.
4. **Come to my office hours.** Bring a specific question and what you've already tried. Come early in the week if you can, not the night before it's due.

> **With your partner:** Before you start, agree on how you'll split the work and when you'll meet. This project is due at the end of the quarter and the last week fills up fast. Put your work sessions on a calendar now.

FYI: I will be checking commit history for these projects. I need to see a roughly even split between you and your partner to get full credit.

## What you've already built

Here's a quick reminder of all the user stories from the [project overview](/full-stack-web/salamander-project/01-project-overview/). The ones you completed in earlier pair programs are crossed out. The rest are what's left for you to do.

### Browsing and Selecting a Video

- ~~**View the list of available videos.** Fetch `GET /api/videos`, render clickable entries, loading state, error state, navigate to preview.~~ *(Part 1)*

### Previewing and Tuning a Video

- ~~**See a thumbnail of the selected video.** Fetch `GET /thumbnail/{filename}`, show it with the filename and a way back to the chooser.~~ *(Part 2)*
- ~~**Tune detection settings and see the binarized result live.** Color picker and threshold slider, live canvas binarization matching the 334 algorithm.~~ *(Part 2)*
- **See where the largest connected region is.** A dot drawn on the centroid of the largest detected region, updating live with the tuning.

### Submitting and Tracking Processing Jobs

- **Submit a processing job with chosen settings.** A "Process Video with These Settings" button that calls `POST /process/{filename}` with your tuning values and stores the returned `jobId`.
- **Track job progress and access the final CSV.** Poll `GET /process/{jobId}/status`, show progress, link to the CSV when done, handle failure.

> **With your partner:** Read the three crossed-out stories again. Crossed out means you wrote code for it, but you still need to verify it. Open your app and confirm every acceptance criterion for those stories still passes against the real backend now that you're off mock data. Fix any that regressed when you connected the API in Part 3. Don't move on to new stories until the old ones are solid.

A story is done when **every one of its acceptance criteria** passes. The acceptance criteria are the checklist. Go through them literally, one bullet at a time, with the app open in front of you. "It mostly works" is not done. Each criterion names a specific, visible behavior. If you can't point to the thing on screen that proves a criterion, that criterion isn't met yet.
