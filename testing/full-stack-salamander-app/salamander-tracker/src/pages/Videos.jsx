import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getVideos } from '../mockApi.js';

export default function Videos() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getVideos()
      .then((data) => {
        setVideos(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p className="text-gray-500 italic">Loading videos...</p>;
  }

  if (error) {
    return <p className="text-red-600">Could not load videos: {error}</p>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Available Videos</h1>
      <ul className="space-y-2">
        {videos.map((filename) => (
          <li key={filename}>
            <Link to={`/preview/${filename}`} className="text-blue-600 hover:underline">
              {filename}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
