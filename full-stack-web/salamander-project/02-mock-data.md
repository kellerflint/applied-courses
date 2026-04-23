---
title: "Working with Mock Data"
order: 2
---

While the backend is still being developed, you'll need to mock API responses to build and test your frontend.

## What is mock data?

Mock data is placeholder data you define locally to simulate real API responses. You can mock:

- Video lists
- Thumbnail previews
- Job statuses
- Final CSV URLs

## How to use mock data

Use the [API examples](https://github.com/auberonedu/salamander-api) as a guide for what the real responses will look like, and structure your mock data accordingly. There's a sample video provided at the top of this assignment; you can download it for your mock setup. If you prefer, you may also use [json-server](https://www.geeksforgeeks.org/json-server-setup-and-introduction/) to simulate an API during development.

### 1. Create a mock data file

Make a `mock` folder in your project and create files like:

```js
export const mockVideoList = [
  "salamander1.mp4",
  "salamander2.mov",
  "forest_intro.mp4"
];
```

### 2. Use it in your components

Instead of calling the real API, import and use your mock data during development:

```js
import { mockVideoList } from '../mock/videos';

function VideoChooser() {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    // Simulate API call
    setVideos(mockVideoList);
  }, []);
  // ...
}
```

### 3. Replace with real API later

When the backend is ready, swap the mock data for `fetch()` or `axios` calls to the real API:

```js
useEffect(() => {
  const fetchVideos = async () => {
    try {
      const res = await fetch("/api/videos");
      const data = await res.json();
      setVideos(data);
    } catch (error) {
      console.error(error);
    }
  };

  fetchVideos();
}, []);
```
