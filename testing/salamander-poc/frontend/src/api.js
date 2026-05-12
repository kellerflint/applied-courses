// All backend calls go through here so the API base URL lives in one place.
// Change this if you run the FastAPI server somewhere else.
export const API_BASE = "http://localhost:8000";

export async function postVideo(endpoint, file) {
  const form = new FormData();
  form.append("video", file);

  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Request failed (${res.status}): ${text}`);
  }
  return res.json();
}

// The backend returns video_url as a path like "/outputs/abc.mp4".
// Prepend the API base so it loads in a <video> tag.
export function absoluteVideoUrl(path) {
  return `${API_BASE}${path}`;
}
