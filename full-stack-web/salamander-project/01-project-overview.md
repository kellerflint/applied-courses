---
title: "Project Overview"
order: 1
---

# 🦎 Salamander Tracker Project 🦎

This quarter, you'll be building a React application that interacts with a backend system developed in your 334 course. Your frontend app will allow users to detect salamanders in videos using interactive tools and visual feedback. The backend provides the core processing logic and APIs. Your focus is exclusively on the frontend: creating a responsive, user-friendly interface that follows React best practices.

We'll be breaking this project into pieces over the rest of the quarter. Many of our in-class pair programs after week 6 will focus on one component or user story at a time. By the end, you'll have integrated everything into a polished app.

Below is a basic example of what some of the main parts of the application might include:

{% image "sal-available-videos-page.png", "Available videos page example" %}

{% image "sal-preview-processing-page.png", "Preview and processing page example" %}

## Learning Objectives

By completing this project, you will:

- Practice building a full React app with routing, props, and state
- Use `useEffect` for data fetching and side effects
- Handle client-side image manipulation and rendering
- Apply consistent styling using CSS and Tailwind
- Implement project requirements from user stories and acceptance criteria

## Tech Stack

- React via Vite
- React Router for client-side routing
- Styling with CSS and Tailwind

## User Stories and Acceptance Criteria

The project is organized around three groups of user stories. Each story describes what a user should be able to do, followed by the acceptance criteria that define "done." These are the specs we'll work against for the rest of the quarter.

### Browsing and Selecting a Video

#### View the list of available videos

> As a researcher, I want to see a list of all videos available on the server so that I can pick one to analyze.

Acceptance Criteria:

- Given I am on the Video Chooser page, when the page loads, then the app fetches `GET /api/videos` and renders each video as a clickable entry.
- Given the video list request is in flight, when I look at the page, then a loading state is visible.
- Given the video list has loaded, when I click a video entry, then I am navigated to the preview page for that video (e.g. `/preview/:filename`).
- Given the API is unavailable, when the page attempts to fetch the video list, then an error message is shown to the user.

### Previewing and Tuning a Video

#### See a thumbnail of the selected video

> As a researcher, I want to see a preview frame of the video I selected so that I can confirm I'm working with the right one before tuning.

Acceptance Criteria:

- Given a video has been selected, when the preview page loads, then the app fetches `GET /thumbnail/{filename}` and displays the thumbnail prominently.
- Given the preview page has loaded, when I look at the page, then the filename of the selected video is visible.
- Given I am on the preview page, when I look at the page, then a link or button to return to the video chooser is visible and functional.

#### Tune detection settings and see the binarized result live

> As a researcher, I want to adjust a color target and brightness threshold and see the binarized image update immediately so that I can set good detection settings before running a full processing job.

Acceptance Criteria:

- Given the thumbnail has loaded, when I look at the preview page, then the thumbnail and a binarized version are shown side by side, along with a color picker and threshold slider.
- Given the thumbnail is displayed, when I change the color picker or threshold slider, then the binarized image updates in real time without requiring any form submission.
- Given the binarized image is displayed, when I inspect the implementation, then the binarization logic matches the Java tuning code from Auberon's course exactly and is computed client-side using canvas pixel manipulation.

#### See where the largest connected region is

> As a researcher, I want to see a visible marker on the centroid of the largest detected region so that I can tell whether my tuning is picking up the salamander.

Acceptance Criteria:

- Given the binarized image contains active pixels, when the image is rendered, then a dot is drawn at the centroid of the largest connected group.
- Given a dot is currently displayed, when the tuning settings change and the image updates, then the dot position updates to match.
- Given the binarized image has no active pixels, when the image is rendered, then no dot is drawn and the app does not crash.
- Given the algorithm runs, when the implementation is inspected, then the logic matches the Java version from the 334 course.

### Submitting and Tracking Processing Jobs

#### Submit a processing job with chosen settings

> As a researcher, once I've tuned my settings I want to submit the video for full processing so that the backend can produce a detection CSV.

Acceptance Criteria:

- Given I am on the preview page with tuning settings chosen, when I look at the controls, then a button labeled "Process Video with These Settings" is visible.
- Given I have chosen tuning settings, when I click the submit button, then `POST /process/{filename}?targetColor=<hex>&threshold=<int>` is called with the current values, with `targetColor` as a hex string without the `#`.
- Given a job submission is in flight, when I look at the button, then it is disabled and shows a pending state.
- Given the submission request completes successfully, when the response is received, then the returned `jobId` is stored so the app can track the job.
- Given the submission request fails, when the error is returned, then an error message is shown and the user can try again.

#### Track job progress and access the final CSV

> As a researcher, I want to see the status of my processing job and get a link to the CSV results when it finishes so that I don't have to keep guessing whether it's done.

Acceptance Criteria:

- Given a jobId has been received from a successful submission, when the app is running, then it polls `GET /process/{jobId}/status` on a regular interval.
- Given the job is in a non-terminal state, when a status response is received, then the current status (e.g. queued, running) and a progress indicator (spinner, progress bar, or percent) are displayed.
- Given the job is in progress, when the status response indicates completion, then a link to the resulting CSV file is displayed and polling stops.
- Given the job is in progress, when the status response indicates failure, then an error message is shown and polling stops.

## Other Technical Requirements

Your app must include:

- React state and props used meaningfully
- `useEffect` for side effects and API calls
- React Router with at least two routes
- One unique feature of your choice (something beyond the stories above; be ready to demo it)

## API Reference

You'll be building this API in 334. Here's a quick reference for the endpoints your frontend will consume. Full examples live at: https://github.com/auberonedu/salamander-api

- `GET /api/videos` → Returns a list of available videos
- `GET /thumbnail/{filename}` → Returns the first frame of the video as a JPEG
- `POST /process/{filename}?targetColor=ff0000&threshold=50` → Submits a video processing job
- `GET /process/{jobId}/status` → Tracks the status of a job

## Final Submission (End of Quarter)

Your GitHub repo must contain:

- A complete, working application that meets all the user stories above
- A `README.md` with setup instructions and screenshots (screenshots optional but encouraged)

## Demo

At the end of the quarter you'll schedule a time to demo the project and answer questions about your approach and implementation. Schedule one meeting per team; both members attend. Expect it to take 10 to 15 minutes.
