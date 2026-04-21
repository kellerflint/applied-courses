// App.jsx
import data from './data.json'
import ArtistList from './components/ArtistList'

function App() {
  return (
    <div>
      <header>
        <h1>{data.label}</h1>
        <p>{data.tagline}</p>
      </header>
      <ArtistList artists={data.artists} />
    </div>
  )
}

export default App



// ArtistList.jsx
import ArtistCard from './ArtistCard'

function ArtistList({ artists }) {
  return (
    <div className="artist-list">
      {artists.map(artist => (
        <ArtistCard key={artist.id} artist={artist} />
      ))}
    </div>
  )
}

export default ArtistList


.map() loops over the array and returns one ArtistCard for each artist. The key prop is required on any list of elements in React. Use a unique value from your data, like id.


// ArtistCard.jsx
import AlbumItem from './AlbumItem'

function ArtistCard({ artist }) {
  return (
    <div className="artist-card">
      <h2>{artist.name}</h2>
      <span>{artist.genre}</span>
      <p>{artist.bio}</p>
      <div className="albums">
        {artist.albums.map(album => (
          <AlbumItem key={album.title} album={album} />
        ))}
      </div>
    </div>
  )
}

export default ArtistCard

// AlbumItem.jsx
function AlbumItem({ album }) {
  return (
    <div className="album">
      <span>{album.title}</span>
      <span>{album.year}</span>
    </div>
  )
}

export default AlbumItem