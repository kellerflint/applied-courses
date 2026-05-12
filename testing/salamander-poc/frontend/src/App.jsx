import { Link, NavLink, Route, Routes } from "react-router-dom";
import Detect from "./pages/Detect.jsx";
import Track from "./pages/Track.jsx";

export default function App() {
  return (
    <div className="app">
      <header className="topbar">
        <Link to="/" className="brand">Salamander Tracker</Link>
        <nav>
          <NavLink to="/" end>Detect</NavLink>
          <NavLink to="/track">Track</NavLink>
        </nav>
      </header>

      <main className="main">
        <Routes>
          <Route path="/" element={<Detect />} />
          <Route path="/track" element={<Track />} />
        </Routes>
      </main>
    </div>
  );
}
