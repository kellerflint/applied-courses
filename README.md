# Course Site

Static site built with [Eleventy](https://www.11ty.dev/). Lessons are Markdown files. Activities are standalone HTML files embedded via iframe.

## Run locally

```
npm install
npm run dev
```

## Build

```
npm run build
```

Output goes to `_site/`.

---

## Structure

```
/{course}/
  index.md                  ← course landing page
  {course}.json             ← sets courseTitle for all pages in this course
  /{unit}/
    {unit}.json             ← sets unitTitle, unitOrder, layout for all pages in this unit
    01-page.md
    02-page.md
  /activities/
    my-activity.html
```

---

## Adding a course

1. Create a folder at the root (e.g. `web-development/`)
2. Add `index.md`:
```yaml
---
title: Web Development
layout: course.njk
tags:
  - course
order: 2
description: Optional subtitle shown on the home page.
---
```
3. Add `web-development.json` (directory data — applies to all pages in this course):
```json
{ "courseTitle": "Web Development" }
```

---

## Adding a unit

Inside a course folder, create a subfolder and a JSON file with the same name:

```json
// web-development/html-css/html-css.json
{
  "layout": "page.njk",
  "tags": ["page"],
  "unitTitle": "HTML & CSS",
  "unitOrder": 1
}
```

`unitOrder` controls the order units appear on the course page.

---

## Adding a page

Create a Markdown file inside a unit folder:

```yaml
---
title: The Box Model
order: 2
---

Your content here.
```

`order` controls the sequence within the unit. Pages are also sequenced across units for prev/next navigation.

---

## Adding an activity

1. Drop a standalone HTML file into `{course}/activities/`
2. Embed it in any page with the shortcode:

```
{% activity "my-activity.html", "Activity Title" %}
```

Optional third argument sets height (default `560px`):

```
{% activity "my-activity.html", "Activity Title", "800px" %}
```

Activity files must be fully self-contained — all CSS and JS inline. They have no access to the parent site.
