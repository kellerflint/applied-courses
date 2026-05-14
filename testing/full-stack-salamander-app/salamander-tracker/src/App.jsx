import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home.jsx';
import Videos from './pages/Videos.jsx';
import Preview from './pages/Preview.jsx';

export default function App() {
  return (
    <div className="max-w-3xl mx-auto p-6">
      <nav className="flex gap-4 p-4 border-b mb-6">
        <Link to="/" className="text-blue-600 hover:underline">Home</Link>
        <Link to="/videos" className="text-blue-600 hover:underline">Videos</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/videos" element={<Videos />} />
        <Route path="/preview/:filename" element={<Preview />} />
      </Routes>
    </div>
  );
}
