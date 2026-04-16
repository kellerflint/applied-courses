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

## Deploy

```
npm run deploy
```

Builds the site and rsyncs it to the server. **Before first use, update the deploy script in `package.json`:**

```
"deploy": "npm run build && rsync -avz --delete _site/ YOUR_USER@YOUR_SERVER:/var/www/courses/"
```

- `YOUR_USER` — your SSH username on the VM
- `YOUR_SERVER` — your VM's IP or domain
- `/var/www/courses/` — path nginx serves from (must exist on the server)

**One-time server setup:**
1. Install Caddy: https://caddyserver.com/docs/install
2. Create the folder: `sudo mkdir -p /var/www/courses && sudo chown YOUR_USER /var/www/courses`
3. Create/edit `/etc/caddy/Caddyfile`:
```
your-domain.com {
    root * /var/www/courses
    file_server
}
```
4. Start Caddy: `sudo systemctl enable --now caddy`
5. Add your SSH public key to the server so deploys don't prompt for a password

Caddy automatically obtains and renews SSL via Let's Encrypt. Just make sure your domain's DNS points to the VM before starting Caddy.

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

`order` controls the sequence within the unit. The prev/next navigation buttons only move between pages within the same unit — they do not cross unit boundaries.

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
