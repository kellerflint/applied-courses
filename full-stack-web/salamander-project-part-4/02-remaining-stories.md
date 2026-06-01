---
title: "The Remaining Stories"
order: 2
---

Three user stories are left. This page won't walk you through the code. It points you at what you already know and the decisions you'll have to make. Treat the acceptance criteria on the [project overview](/full-stack-web/salamander-project/01-project-overview/) as the real spec; this is just orientation.

## Story: See where the largest connected region is

You already binarize the image on a canvas. This story adds a dot on the **centroid of the largest connected region** of active pixels, so a researcher can see whether the tuning is locking onto the salamander.

The acceptance criteria are explicit that the logic should match the connected-region algorithm from your 334 course. You've already written this algorithm once, in Java. The work here is porting that logic to run over the pixel data you already have on the canvas.

## Story: Submit a processing job with chosen settings

Once tuning looks right, the researcher submits the job. You built `submitProcessingJob` back in your API module. This story wires it to a button and handles the request's lifecycle.

The acceptance criteria spell out the contract precisely.

> **With your partner:** This is the same loading / error / success pattern you've used on every fetch, applied to a button instead of a page. Sketch the states the button moves through: idle, submitting, submitted, error. What should the app show for each?

## Story: Track job progress and access the final CSV

This is the new one. After submitting, the app **polls** the status endpoint on an interval until the job reaches a terminal state, showing progress along the way and a link to the CSV when it finishes.

Polling means calling `GET /process/{jobId}/status` over and over on a timer, not just once. The standard React tool for this is a `useEffect` that sets up an interval and cleans it up. The cleanup is the part that bites people. An interval that's never cleared keeps firing after the component unmounts or after the job is done, which leaks and can fire requests forever.

The shape might look something like this, though the details will depend on your project.

```jsx
useEffect(() => {
  if (!jobId) return;

  const id = setInterval(async () => {
    const status = await getJobStatus(jobId);
    // update progress state from the response
    // if the job is complete or failed, stop polling: clearInterval(id)
  }, 1500);

  // cleanup runs when jobId changes or the component unmounts
  return () => clearInterval(id);
}, [jobId]);
```

> **With your partner:** Talk through when polling should stop. What are the terminal states? What happens to your interval if you navigate away mid-job? Test it by submitting a job and watching the Network tab: you should see status requests fire on the interval and then stop the moment the job finishes.
