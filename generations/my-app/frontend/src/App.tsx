import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Outreach Scraping Toolkit</h1>
      <p>Welcome to the Outreach Scraping Toolkit</p>

      <div style={{ marginTop: '2rem' }}>
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      </div>

      <div style={{ marginTop: '2rem' }}>
        <h2>Features (Coming Soon)</h2>
        <ul>
          <li>LinkedIn Profile Scraping</li>
          <li>Instagram Profile Scraping</li>
          <li>Google Sheets Export</li>
          <li>Cost Estimation</li>
        </ul>
      </div>
    </div>
  )
}

export default App
