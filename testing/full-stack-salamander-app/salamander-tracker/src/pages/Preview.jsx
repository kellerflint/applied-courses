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
    // img.crossOrigin = 'anonymous';
    img.onload = () => {
      imgRef.current = img;
      setImageReady(true);
    };
    img.src = thumbnailUrl;
  }, [thumbnailUrl]);

  // 3. Redraw whenever the image is loaded OR any tuning input changes.
  //    The pixel pipeline is in place (getImageData + putImageData) but the
  //    algorithm itself is empty: pixels are read and written back unchanged.
  //    Drop your algorithm from 334 into the for-loop slot below.
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

    for (let i = 0; i < px.length; i += 4) {
      // px[i]     = red channel of this pixel (0-255)
      // px[i + 1] = green channel
      // px[i + 2] = blue channel
      // px[i + 3] = alpha (transparency, usually leave alone)
      //
      // Your algorithm from 334 goes here. Read the pixel above, look at
      // `color` and `tolerance`, decide the pixel's new value, and write it
      // back the same way:
      //   px[i]     = newRed;
      //   px[i + 1] = newGreen;
      //   px[i + 2] = newBlue;
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
              <figcaption className="text-sm text-gray-500 mb-1">Canvas (algorithm output)</figcaption>
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
