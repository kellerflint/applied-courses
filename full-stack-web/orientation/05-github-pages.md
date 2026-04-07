---
title: "Hosting with GitHub Pages"
order: 5
---

Every project in this course gets deployed to a live URL. This page covers both methods you'll use: plain static sites and React/Vite projects.

## What is GitHub Pages?

GitHub Pages is a free hosting service built into GitHub. Upload your files to a repository, turn on Pages, and GitHub gives you a public URL at `yourusername.github.io/repositoryname`. It works for any static front-end project: plain HTML/CSS/JavaScript, or a built React app.

If you don't have a GitHub account yet, create one at [github.com](https://github.com/). Use your personal email rather than your school email so you keep the account after graduation. Pick a username you'd be comfortable sharing with employers.

---

## Method 1: Static Sites (Plain HTML/CSS/JavaScript)

Use this method for projects that are just HTML, CSS, and JavaScript files with no build step.

### 1. Create a new repository on GitHub

Sign in, click the **+** icon in the top right, and select **New repository**.

### 2. Name it, make it public, and create it

Give it a descriptive name, set it to **Public**, and click **Create repository**.

### 3. Upload your files

Click **uploading an existing file**, then drag in your project files. Make sure your main HTML file is named `index.html`. GitHub Pages looks for this file specifically.

Click **Commit changes**.

If you know Git from the command line, pushing from a local repo is the better option and will save you time as projects get more complex.

### 4. Enable GitHub Pages

Go to your repository, then **Settings > Pages**. Under **Branch**, select **main** and click **Save**.

### 5. Wait, then check

It takes 1-2 minutes for the site to go live. Reload the Settings > Pages screen after a minute and the URL will appear. Paste it into a browser and verify the site loads correctly before submitting it.

### Updating a static site

To update a deployed site, go to the repository, click **Add file > Upload files**, and upload your updated files. Files with the same name replace the old version. Changes take a few minutes to appear on the live site.

---

## Method 2: React/Vite Projects

Vite React projects need a build step before they can be hosted. The `gh-pages` package handles this.

<iframe width="100%" height="420" src="https://www.youtube.com/embed/hn1IkJk24ow?si=5WqbFR5a_Gi6jNtG" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### 1. Create a repository and push your project

Create a new GitHub repository, then push your local Vite project to it using Git.

### 2. Install the gh-pages package

```bash
npm install --save-dev gh-pages
```

### 3. Add your homepage URL to package.json

```json
"homepage": "https://<yourusername>.github.io/<your-repository-name>"
```

### 4. Add deploy scripts to package.json

```json
"predeploy": "npm run build",
"deploy": "gh-pages -d dist"
```

### 5. Add the base path to vite.config.js

```js
base: '/<your-repository-name>/'
```

### 6. Deploy

```bash
npm run deploy
```

This builds your project and pushes the output to a `gh-pages` branch on GitHub. The site will be live at the homepage URL you set in step 3.

### Redeploying after changes

Any time you make changes and want to update the live site, run `npm run deploy` again.
