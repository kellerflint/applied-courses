---
title: "The Tuning Challenge"
order: 2
---

Next user story is the meat of this pair program:

> As a researcher, I want to adjust a color target and brightness threshold and see the binarized image update immediately so that I can set good detection settings before running a full processing job.

There are two new ideas in that story you haven't dealt with before: **what binarization actually does to an image**, and **how to make a `<canvas>` redraw in response to React state changes**. This page covers both. The next page is where you actually build it.

## What binarization is

Binarization turns a color image into a two-color image. Every pixel becomes either "on" or "off" based on some rule. For our purposes the rule is: if a pixel's brightness is above some threshold, it's "on"; otherwise it's "off."

It's the simplest possible step toward detecting something in an image. A salamander on a light tank floor is going to be darker than the floor, so if you set the threshold somewhere between "tank floor brightness" and "salamander brightness," everything dark stays in the "on" group and you get a silhouette.

Play with the activity below. It uses a real frame from a research video. Drag the slider and watch the image on the right change.

{% activity "binarization-threshold.html", "Binarization Threshold", "520px" %}

> **With your partner:** Find a threshold value where the salamander is clearly visible as a separate shape from the background. What happens at threshold 0? At 255? At the value where the salamander first disappears, what percentage of pixels are still above? Talk about what that number means.

The thing you just did with the slider is what your app needs to do in React, except your version will also let the user pick a color (which becomes the "on" pixel color) on top of the threshold.

## Why canvas is different from anything you've built so far

So far every React component you've built ends with some JSX that the browser turns into HTML. React owns the markup: when state changes, it figures out the diff and updates the DOM for you.

A `<canvas>` doesn't work like that. The element itself is just a rectangle. What you see *inside* it (pixels, shapes, images) isn't HTML; it's a drawing buffer you talk to through JavaScript methods like `getContext('2d')`, `drawImage`, `fillRect`. React doesn't know about any of that. There's no JSX for "a red circle on a canvas."

To draw on a canvas from inside a React component, you need a way to **reach the actual `<canvas>` DOM element** so you can call its methods directly. The hook for that is `useRef`.

{% activity "useref-canvas.html", "useRef + Canvas", "500px" %}

> **With your partner:** Read the three numbered callouts in the code panel. Click "Draw a circle" a few times. Then talk through what each number does in your own words. If one of them isn't clear, look at it side by side with the canvas behavior until it clicks.

That's the whole `useRef` story you need for now. You'll use it twice on the next page: once for the canvas (so you can draw on it), and once for the loaded image (so you can hang onto it without making it part of React state). The second use is the same pattern. We'll cover it inline when you get there.

## Two gotchas to know in advance

Two things will bite you on the next page if you don't know to expect them:

- **The drawing surface and the display size are different.** A `<canvas>` has CSS dimensions (how big it looks on the page) and intrinsic dimensions (how many pixels are in its drawing buffer). If you only set the CSS size, everything you draw gets stretched. Set `canvas.width` and `canvas.height` programmatically, not via CSS, to make them match.
- **Cross-origin images can taint the canvas.** If you load an image from a different origin and try to read its pixels, the browser may refuse with a "tainted canvas" error. Set `img.crossOrigin = 'anonymous'` on the Image object before you assign `.src`, and use images served from your own origin (which is what `public/salamander1.jpg` will be) or hosts that send proper CORS headers.

Both are easier to handle if you know they exist. Both are infuriating mysteries if you don't.
