const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");

module.exports = function (eleventyConfig) {
  eleventyConfig.addPlugin(syntaxHighlight);
  // Pass through activity files per course without processing as templates
  eleventyConfig.addPassthroughCopy("*/activities");
  eleventyConfig.ignores.add("*/activities/**");

  // Activity shortcode — auto-detects course from the current page URL
  eleventyConfig.addShortcode("activity", function (filename, title, height) {
    const h = height || "560px";
    const urlParts = this.page.url.split("/").filter(Boolean);
    const courseSlug = urlParts[0] || "";
    const src = courseSlug ? `/${courseSlug}/activities/${filename}` : `/activities/${filename}`;
    return `<div class="activity-embed">
  <div class="activity-header">
    <a class="activity-title" href="${src}" target="_blank" rel="noopener">${title}</a>
    <button class="activity-fullscreen-btn" onclick="(function(btn){var f=btn.closest('.activity-embed').querySelector('iframe');if(f.requestFullscreen)f.requestFullscreen();else if(f.webkitRequestFullscreen)f.webkitRequestFullscreen();})(this)" title="Open fullscreen">
      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>
      Fullscreen
    </button>
  </div>
  <iframe src="${src}" title="${title}" style="height:${h}" allowfullscreen></iframe>
</div>`;
  });

  // Courses — index pages tagged "course"
  eleventyConfig.addCollection("courses", (api) =>
    api.getFilteredByTag("course").sort((a, b) => (a.data.order || 0) - (b.data.order || 0))
  );

  // Pages — all lesson pages tagged "page"
  eleventyConfig.addCollection("pages", (api) =>
    api.getFilteredByTag("page").sort((a, b) => (a.data.order || 0) - (b.data.order || 0))
  );

  // Filter: group a list of pages by their unitTitle, sorted by unitOrder then page order
  eleventyConfig.addFilter("groupByUnit", function (pages) {
    const groups = {};
    for (const p of pages) {
      const key = p.data.unitTitle || "Other";
      if (!groups[key]) {
        groups[key] = { title: key, order: p.data.unitOrder ?? 99, pages: [] };
      }
      groups[key].pages.push(p);
    }
    return Object.values(groups)
      .sort((a, b) => a.order - b.order)
      .map((g) => ({
        ...g,
        pages: g.pages.sort((a, b) => (a.data.order || 0) - (b.data.order || 0)),
      }));
  });

  // Filter: extract the course root URL from any page URL
  eleventyConfig.addFilter("courseUrl", function (pageUrl) {
    const parts = pageUrl.split("/").filter(Boolean);
    return parts.length > 0 ? "/" + parts[0] + "/" : "/";
  });

  // Filter: all pages whose URL starts with the same /course/unit/ prefix
  eleventyConfig.addFilter("pagesInUnit", function (allPages, pageUrl) {
    const parts = pageUrl.split("/").filter(Boolean);
    if (parts.length < 2) return [];
    const prefix = "/" + parts[0] + "/" + parts[1] + "/";
    return allPages
      .filter((p) => p.url.startsWith(prefix))
      .sort((a, b) => (a.data.order || 0) - (b.data.order || 0));
  });

  // Filter: all pages whose URL starts with the same /course/ prefix, ordered by unit then page
  eleventyConfig.addFilter("pagesInCourse", function (allPages, pageUrl) {
    const parts = pageUrl.split("/").filter(Boolean);
    if (parts.length < 1) return [];
    const prefix = "/" + parts[0] + "/";
    return allPages
      .filter((p) => p.url.startsWith(prefix))
      .sort((a, b) => {
        const uDiff = (a.data.unitOrder ?? 99) - (b.data.unitOrder ?? 99);
        return uDiff !== 0 ? uDiff : (a.data.order || 0) - (b.data.order || 0);
      });
  });

  return {
    dir: { input: ".", includes: "_includes", output: "_site" },
    markdownTemplateEngine: "njk",
  };
};
