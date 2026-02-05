interface SidebarNavProps {
  activeView: string;
  onViewChange: (view: string) => void;
}

export default function SidebarNav({ activeView, onViewChange }: SidebarNavProps) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'scrape', label: 'Scrape Leads', icon: '🔍' },
    { id: 'results', label: 'Results', icon: '📋' },
  ];

  return (
    <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 h-screen sticky top-0">
      <div className="p-6">
        <div className="flex items-center space-x-2 mb-8">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
            OS
          </div>
          <span className="font-semibold text-gray-900 dark:text-white">Scraper</span>
        </div>

        <nav className="space-y-2">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onViewChange(item.id)}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeView === item.id
                  ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          <div className="text-xs text-gray-500 dark:text-gray-400">
            <p className="font-semibold mb-2">Quick Stats</p>
            <div className="space-y-1">
              <p>Platforms: 5</p>
              <p>Total Leads: 0</p>
              <p>Last Run: Never</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
