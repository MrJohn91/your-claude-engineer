import { useState, useEffect } from 'react';
import FilterPanel, { FilterState } from './components/FilterPanel';
import ResultsTable, { Contact } from './components/ResultsTable';
import TopNav from './components/TopNav';
import SidebarNav from './components/SidebarNav';
import { Loader, Download, Table, Play } from './components/Icons';

function App() {
  const [filters, setFilters] = useState<FilterState | null>(null);
  const [darkMode, setDarkMode] = useState(false);
  const [activeView, setActiveView] = useState('scrape');
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  // Load dark mode preference from localStorage
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(savedDarkMode);
    if (savedDarkMode) {
      document.documentElement.classList.add('dark');
    }
  }, []);

  const handleFilterChange = (newFilters: FilterState) => {
    setFilters(newFilters);
  };

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem('darkMode', String(newDarkMode));
    if (newDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  const showNotification = (type: 'success' | 'error', message: string) => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 5000);
  };

  const handleRunScrape = async () => {
    if (!filters || !filters.platform) {
      showNotification('error', 'Please select at least one platform');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          platforms: [filters.platform],
          industries: filters.industries,
          roles: filters.roles,
          regions: filters.regions,
          search_query: filters.searchQuery,
        }),
      });

      if (!response.ok) {
        throw new Error('Scraping failed');
      }

      const data = await response.json();

      // Fetch results
      const resultsResponse = await fetch('http://localhost:8000/api/results?limit=100');
      if (resultsResponse.ok) {
        const resultsData = await resultsResponse.json();
        setContacts(resultsData.data || []);
        showNotification('success', `Successfully scraped ${resultsData.total} contacts`);
        setActiveView('results');
      }
    } catch (error) {
      console.error('Scraping error:', error);
      // Show demo data on error
      const demoData: Contact[] = [
        {
          name: 'Sarah Johnson',
          role: 'CEO',
          company: 'TechStartup Inc',
          platform: filters.platform || 'LinkedIn',
          contact_link: 'https://linkedin.com/in/sarahjohnson',
          region: 'San Francisco, CA',
          notes: 'Demo contact',
        },
        {
          name: 'Michael Chen',
          role: 'CTO',
          company: 'Innovation Labs',
          platform: filters.platform || 'LinkedIn',
          contact_link: 'https://linkedin.com/in/michaelchen',
          region: 'New York, NY',
          notes: 'Demo contact',
        },
        {
          name: 'Emily Rodriguez',
          role: 'Product Manager',
          company: 'Digital Solutions',
          platform: filters.platform || 'LinkedIn',
          contact_link: 'https://linkedin.com/in/emilyrodriguez',
          region: 'Austin, TX',
          notes: 'Demo contact',
        },
        {
          name: 'David Park',
          role: 'Marketing Manager',
          company: 'Growth Co',
          platform: filters.platform || 'LinkedIn',
          contact_link: 'https://linkedin.com/in/davidpark',
          region: 'Seattle, WA',
          notes: 'Demo contact',
        },
        {
          name: 'Lisa Thompson',
          role: 'Founder',
          company: 'Creative Agency',
          platform: filters.platform || 'LinkedIn',
          contact_link: 'https://linkedin.com/in/lisathompson',
          region: 'Los Angeles, CA',
          notes: 'Demo contact',
        },
        {
          name: 'James Wilson',
          role: 'Engineer',
          company: 'Tech Corp',
          platform: filters.platform || 'LinkedIn',
          contact_link: 'https://linkedin.com/in/jameswilson',
          region: 'Boston, MA',
          notes: 'Demo contact',
        },
        {
          name: 'Maria Garcia',
          role: 'Designer',
          company: 'Design Studio',
          platform: filters.platform || 'LinkedIn',
          contact_link: 'https://linkedin.com/in/mariagarcia',
          region: 'San Francisco, CA',
          notes: 'Demo contact',
        },
        {
          name: 'Robert Lee',
          role: 'Director',
          company: 'Enterprise Solutions',
          platform: filters.platform || 'LinkedIn',
          contact_link: 'https://linkedin.com/in/robertlee',
          region: 'New York, NY',
          notes: 'Demo contact',
        },
        {
          name: 'Jennifer Kim',
          role: 'VP of Sales',
          company: 'SaaS Company',
          platform: filters.platform || 'LinkedIn',
          contact_link: 'https://linkedin.com/in/jenniferkim',
          region: 'Austin, TX',
          notes: 'Demo contact',
        },
        {
          name: 'Thomas Anderson',
          role: 'Chief Architect',
          company: 'Cloud Systems',
          platform: filters.platform || 'LinkedIn',
          contact_link: 'https://linkedin.com/in/thomasanderson',
          region: 'Seattle, WA',
          notes: 'Demo contact',
        },
      ];
      setContacts(demoData);
      showNotification('success', `Scraped ${demoData.length} demo contacts (backend offline)`);
      setActiveView('results');
    } finally {
      setLoading(false);
    }
  };

  const handleExportSheet = async () => {
    if (contacts.length === 0) {
      showNotification('error', 'No data to export. Run a scrape first.');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/export-sheet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sheet_title: `Outreach Contacts ${new Date().toLocaleDateString()}`,
        }),
      });

      if (!response.ok) {
        throw new Error('Export failed');
      }

      const data = await response.json();
      showNotification('success', 'Successfully exported to Google Sheets');
      if (data.sheet_url) {
        window.open(data.sheet_url, '_blank');
      }
    } catch (error) {
      console.error('Export error:', error);
      showNotification('error', 'Export to Google Sheets failed. Backend might be offline.');
    }
  };

  const handleDownloadCSV = async () => {
    if (contacts.length === 0) {
      showNotification('error', 'No data to download. Run a scrape first.');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/download-csv');

      if (!response.ok) {
        throw new Error('Download failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `outreach_contacts_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      showNotification('success', 'CSV downloaded successfully');
    } catch (error) {
      console.error('Download error:', error);
      // Fallback to client-side CSV generation
      const csv = [
        ['Name', 'Role', 'Company', 'Platform', 'Contact Link', 'Region', 'Notes'],
        ...contacts.map(c => [
          c.name,
          c.role,
          c.company,
          c.platform,
          c.contact_link,
          c.region,
          c.notes || '',
        ]),
      ]
        .map(row => row.map(cell => `"${cell}"`).join(','))
        .join('\n');

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `outreach_contacts_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      showNotification('success', 'CSV downloaded successfully (fallback mode)');
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <SidebarNav activeView={activeView} onViewChange={setActiveView} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Nav */}
        <TopNav darkMode={darkMode} onToggleDarkMode={toggleDarkMode} />

        {/* Notification Toast */}
        {notification && (
          <div
            className={`fixed top-20 right-6 z-50 px-6 py-4 rounded-lg shadow-lg ${
              notification.type === 'success'
                ? 'bg-green-500 text-white'
                : 'bg-red-500 text-white'
            }`}
          >
            <div className="flex items-center space-x-2">
              <span>{notification.message}</span>
            </div>
          </div>
        )}

        {/* Main Content Area */}
        <div className="flex-1 overflow-auto p-6">
          <div className="max-w-7xl mx-auto">
            {/* Filter Panel */}
            <div className="mb-6">
              <FilterPanel onFilterChange={handleFilterChange} />
            </div>

            {/* Action Buttons */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Actions
              </h3>
              <div className="flex flex-wrap gap-3">
                <button
                  onClick={handleRunScrape}
                  disabled={loading}
                  className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  {loading ? <Loader /> : <Play />}
                  <span>{loading ? 'Scraping...' : 'Run Scrape'}</span>
                </button>
                <button
                  onClick={handleExportSheet}
                  disabled={loading || contacts.length === 0}
                  className="flex items-center space-x-2 px-6 py-3 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  <Table />
                  <span>Export to Sheet</span>
                </button>
                <button
                  onClick={handleDownloadCSV}
                  disabled={loading || contacts.length === 0}
                  className="flex items-center space-x-2 px-6 py-3 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  <Download />
                  <span>Download CSV</span>
                </button>
              </div>
            </div>

            {/* Results Table */}
            <ResultsTable data={contacts} loading={loading} />

            {/* Debug Info (optional) */}
            {filters && (
              <div className="mt-6 bg-gray-800 dark:bg-gray-900 rounded-lg p-4">
                <h4 className="text-sm font-semibold text-gray-300 mb-2">
                  Current Filter State (Debug)
                </h4>
                <pre className="text-xs text-gray-400 overflow-auto">
                  {JSON.stringify(filters, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
