import { useState } from 'react'
import FilterPanel, { FilterState } from './components/FilterPanel'

function App() {
  const [filters, setFilters] = useState<FilterState | null>(null)

  const handleFilterChange = (newFilters: FilterState) => {
    setFilters(newFilters)
  }

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Outreach Scraping Toolkit</h1>
        <p style={styles.subtitle}>
          Configure your target audience and start scraping leads
        </p>
      </header>

      <div style={styles.content}>
        <FilterPanel onFilterChange={handleFilterChange} />

        <div style={styles.actionPanel}>
          <h2 style={styles.sectionTitle}>Actions</h2>
          <div style={styles.buttonGroup}>
            <button style={styles.primaryButton}>Run Scrape</button>
            <button style={styles.secondaryButton}>Export to Sheet</button>
            <button style={styles.secondaryButton}>Download CSV</button>
          </div>
        </div>

        {filters && (
          <div style={styles.debugPanel}>
            <h3 style={styles.debugTitle}>Current Filter State (Debug)</h3>
            <pre style={styles.debugText}>{JSON.stringify(filters, null, 2)}</pre>
          </div>
        )}

        <div style={styles.infoPanel}>
          <h2 style={styles.sectionTitle}>Features</h2>
          <ul style={styles.featureList}>
            <li>Multi-platform scraping (LinkedIn, X, Telegram, TikTok, Instagram)</li>
            <li>Advanced audience targeting filters</li>
            <li>Google Sheets export</li>
            <li>CSV download</li>
            <li>Cost estimation</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f9fafb',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  } as React.CSSProperties,
  header: {
    backgroundColor: '#ffffff',
    borderBottom: '1px solid #e5e7eb',
    padding: '2rem',
  } as React.CSSProperties,
  title: {
    fontSize: '2rem',
    fontWeight: '700',
    color: '#111827',
    margin: 0,
    marginBottom: '0.5rem',
  } as React.CSSProperties,
  subtitle: {
    fontSize: '1rem',
    color: '#6b7280',
    margin: 0,
  } as React.CSSProperties,
  content: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '2rem',
  } as React.CSSProperties,
  actionPanel: {
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '1.5rem',
    marginBottom: '1.5rem',
  } as React.CSSProperties,
  sectionTitle: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#111827',
    margin: 0,
    marginBottom: '1rem',
  } as React.CSSProperties,
  buttonGroup: {
    display: 'flex',
    gap: '1rem',
    flexWrap: 'wrap' as const,
  } as React.CSSProperties,
  primaryButton: {
    backgroundColor: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    padding: '0.75rem 1.5rem',
    fontSize: '0.875rem',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  } as React.CSSProperties,
  secondaryButton: {
    backgroundColor: '#ffffff',
    color: '#374151',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    padding: '0.75rem 1.5rem',
    fontSize: '0.875rem',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'all 0.2s',
  } as React.CSSProperties,
  debugPanel: {
    backgroundColor: '#1f2937',
    borderRadius: '8px',
    padding: '1.5rem',
    marginBottom: '1.5rem',
  } as React.CSSProperties,
  debugTitle: {
    fontSize: '1rem',
    fontWeight: '600',
    color: '#f9fafb',
    margin: 0,
    marginBottom: '1rem',
  } as React.CSSProperties,
  debugText: {
    fontSize: '0.75rem',
    color: '#d1d5db',
    margin: 0,
    overflow: 'auto',
  } as React.CSSProperties,
  infoPanel: {
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '1.5rem',
  } as React.CSSProperties,
  featureList: {
    margin: 0,
    paddingLeft: '1.5rem',
    color: '#374151',
    lineHeight: '1.8',
  } as React.CSSProperties,
}

export default App
