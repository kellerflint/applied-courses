# Lesson Writing Guide

## What lessons are

Lessons are walkthroughs of building real things. Every unit should result in students having built something applied. Concepts are taught as they become relevant to what students are building, and interactive activities are embedded where they help students understand something that would be confusing as text. They should be clear, approachable, and easy to follow.

Lessons are written for pairs. Partner discussion prompts should appear at natural pause points throughout.

## Process

Lesson writing happens in four separate passes. Do each pass fully before moving to the next. Trying to do everything at once produces worse results than sequential focused passes.

### Pass 1: Content and structure

Write the walkthrough from start to finish. Focus on what students are building, the steps to get there, and the concepts they need along the way. Explain why at each step (why this tool, why this approach, why this matters). Include partner prompts where discussion would be valuable.

For reflection or review pages: lead with questions, not explanations. Have students work through questions with their partner before revealing answers. Use `<details><summary>Reveal answer</summary>` for factual answers. Keep the summary label generic ("Reveal answer"). Do not put hints, answer keywords, or leading context in the question itself.

### Pass 2: Interactive activities

Review the draft and identify where an interactive activity would teach a concept better than just text. Prioritize places where:
- The concept is abstract or hard to visualize
- An activity can replace a wall of explanation
- Anywhere else it might just be fun or effective

Small activities, demos, and visuals are nearly always better than text alone. If a concept or idea can be supplemented with an easy and effective activity it almost certainly should be.

Build the activity as a self-contained HTML file in the course's `activities/` folder. Embed it with the `{% raw %}{% activity %}{% endraw %}` shortcode.

### Pass 3: Flow and clarity review

Read through the full unit with activities in place. Check:
- Does the order still make sense with the activities inserted?
- Are there concepts that need additional context now that the structure changed?
- Are there sections that became redundant because an activity covers the same ground?
- Does every page end with students having done something, or are there pages that are purely passive reading?
- Is the submission/deliverable clearly stated on the last page of the unit?

### Pass 4: Language revision

Go through the text and fix these specific patterns. Check each one individually across the entire document.

**Write plain, natural sentences.** Avoid punctuation patterns that substitute for clear writing. Zero em dashes (`—`) and zero ` - ` used as clause separators in prose. Colons are only for introducing lists or blocks of code, not for connecting two thoughts mid-sentence. If you're reaching for one of these, rewrite the sentence instead.

**Remove via negativa framing.** Find every place where text says what something is NOT before saying what it IS. Rewrite to lead with what it is. Patterns to catch:
- "No X, no Y. Just Z." -> State Z directly.
- "You didn't do X. You just did Y." -> State Y directly.
- "This isn't X. It's Y." -> State Y directly.

**Check for walls of text.** Paragraphs over 3-4 sentences should be split. Use subheadings as visual anchors. Bold key terms so students scanning can find what matters. After code blocks, briefly explain what the code does.

**Check every section for "why."** Each step, concept, or instruction should have motivation. If the text only says what to do, add why.

## Formatting conventions

These patterns are used consistently across all lesson pages. Don't invent new forms for these — use the established ones.

**Partner prompts**
Always a blockquote with bold label:
```
> **With your partner:** Question or prompt here.
```
Never plain text, never a different label. Use for discussion questions, exploration tasks, or anything students work through together. Open-ended prompts don't need a reveal.

**Reveals**
For factual questions with a correct answer:
```
<details>
<summary>Reveal answer</summary>

Answer content here.

</details>
```
For open-ended questions where there are multiple valid answers, still use `Reveal answer` as the label — the content can acknowledge there's no single right answer. Keep the label generic. Never put hints or answer keywords in the summary.

Reveals always follow directly below the partner prompt that precedes them, with no content between.

**Reveal styling** is handled globally in `_includes/base.njk`. The `<summary>` renders as a small pill-shaped button in the accent color so it reads as interactive rather than as plain text. A triangle indicator (▶/▼) shows open/closed state. `<details>` has `margin: 1.25em 0` so there is consistent spacing above and below it whether it is open or closed. Do not add inline styles to `<details>` or `<summary>` elements — the global styles handle everything.

**Q&A sections**
When a page is structured around questions (like a reflect/review page), each question gets its own `##` section with a short descriptive heading. The partner prompt goes directly under the heading (with optional 1–2 sentence framing if context is needed), and the reveal follows the prompt.

If questions are grouped under a parent section (like `## Check Your Understanding`), use `###` for the individual question headings to avoid duplicate `##` anchors.

**Activity embeds**
```
{% activity "filename.html", "Display Title", "height" %}
```
Always a self-contained HTML file in the `activities/` folder. Height in px (e.g. `"520px"`). The display title renders as a link that opens the activity directly in a new tab, so anyone can link to or embed it standalone.

**Feedback embed**
Every unit's final page (the submit/wrap-up page) ends with a feedback form. Add this after the last content section:

```html
<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=COURSE+TITLE&unit=UNIT+TITLE" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
```

Replace `COURSE+TITLE` and `UNIT+TITLE` with URL-encoded versions of the course and unit names (spaces become `+`). Pull the values from the unit's `.json` file (`unitTitle`) and the course's root `.json` file (`courseTitle`). Orientation units do not get a feedback embed.

The `.tally-embed-wrapper` dark mode styles are defined globally in `base.njk` — no per-page styles needed.

## Tone

- Address students directly ("you")
- Casual and direct
- Short sentences where possible
- Define technical terms the first time they appear, in context
- External links open in new tabs (handled automatically by base template)
