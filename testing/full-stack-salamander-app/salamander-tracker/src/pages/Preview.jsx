import { useEffect, useRef, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getThumbnail } from '../mockApi.js';

export default function Preview() {
  const { filename } = useParams();

  // Thumbnail state (first user story: see a preview frame).
  const [thumbnailUrl, setThumbnailUrl] = useState(null);
  const [thumbnailError, setThumbnailError] = useState(null);

  // Tuning state (second user story: adjust color + tolerance, see live result).
  // Default target color is a brown so the salamander matches by default.
  const [color, setColor] = useState('#6b4423');
  const [tolerance, setTolerance] = useState(80);

  // Refs for canvas + the loaded image element. Refs (not state) because we
  // don't want re-renders just because the image finished loading; we'll
  // flip a separate boolean for that.
  const canvasRef = useRef(null);
  const imgRef = useRef(null);
  const [imageReady, setImageReady] = useState(false);

  // 1. Fetch the thumbnail URL from the (mock) backend.
  useEffect(() => {
    setImageReady(false);
    setThumbnailError(null);
    setThumbnailUrl(null);
    getThumbnail(filename)
      .then(setThumbnailUrl)
      .catch((err) => setThumbnailError(err.message));
  }, [filename]);

  // 2. Once we have the URL, decode the image into an Image element.
  //    Store it on a ref; flip imageReady to trigger the draw effect.
  useEffect(() => {
    if (!thumbnailUrl) return;
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      imgRef.current = img;
      setImageReady(true);
    };
    img.src = thumbnailUrl;
  }, [thumbnailUrl]);

  // 3. Redraw whenever the image is loaded OR any tuning input changes.
  //    This is the real-time-update mechanism. The body of this effect is
  //    intentionally tiny + naive color masking: for each pixel, compare it
  //    to the picked target color; if the RGB distance is below the
  //    tolerance, mark it as a match (white), else mark it as background
  //    (black). NOT the real algorithm from Auberon's course. Students
  //    replace this body with their own.
  useEffect(() => {
    if (!imageReady) return;
    const img = imgRef.current;
    const canvas = canvasRef.current;
    if (!img || !canvas) return;

    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);

    const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const px = data.data;

    // Parse #rrggbb -> r,g,b ints. This is the target color the salamander
    // is supposed to be close to.
    const tr = parseInt(color.slice(1, 3), 16);
    const tg = parseInt(color.slice(3, 5), 16);
    const tb = parseInt(color.slice(5, 7), 16);

    for (let i = 0; i < px.length; i += 4) {
      const dr = px[i]     - tr;
      const dg = px[i + 1] - tg;
      const db = px[i + 2] - tb;
      const distance = Math.sqrt(dr * dr + dg * dg + db * db);
      const matches = distance <= tolerance;
      px[i]     = matches ? 255 : 0;
      px[i + 1] = matches ? 255 : 0;
      px[i + 2] = matches ? 255 : 0;
      // alpha (px[i + 3]) left as-is
    }
    ctx.putImageData(data, 0, 0);
  }, [imageReady, color, tolerance]);

  if (thumbnailError) {
    return (
      <div>
        <p className="text-red-600">Could not load thumbnail: {thumbnailError}</p>
        <Link to="/videos" className="text-blue-600 hover:underline">Back to videos</Link>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Preview: {filename}</h1>

      {!thumbnailUrl && <p className="text-gray-500 italic">Loading thumbnail...</p>}

      {thumbnailUrl && (
        <>
          <div className="flex gap-6 items-start mb-6">
            <figure>
              <figcaption className="text-sm text-gray-500 mb-1">Original</figcaption>
              <img src={thumbnailUrl} alt={`Thumbnail for ${filename}`} className="border" />
            </figure>
            <figure>
              <figcaption className="text-sm text-gray-500 mb-1">Binarized (live)</figcaption>
              <canvas ref={canvasRef} className="border" />
            </figure>
          </div>

          <div className="flex gap-6 items-center mb-6">
            <label className="flex items-center gap-2">
              Target color
              <input
                type="color"
                value={color}
                onChange={(e) => setColor(e.target.value)}
              />
            </label>
            <label className="flex items-center gap-2 flex-1">
              Color tolerance
              <input
                type="range"
                min="0"
                max="255"
                value={tolerance}
                onChange={(e) => setTolerance(Number(e.target.value))}
                className="flex-1"
              />
              <span className="w-10 text-right tabular-nums">{tolerance}</span>
            </label>
          </div>
        </>
      )}

      <Link to="/videos" className="text-blue-600 hover:underline">Back to videos</Link>
    </div>
  );
}
