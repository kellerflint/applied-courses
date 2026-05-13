import Track from "./pages/Track.jsx";

export default function App() {
  return (
    <div className="app">
      <header className="topbar">
        <span className="brand">Salamander Tracker</span>
      </header>
      <main className="main">
        <Track />
      </main>
    </div>
  );
}
