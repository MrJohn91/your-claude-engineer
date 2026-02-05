import { Moon, Sun } from './Icons';

interface TopNavProps {
  darkMode: boolean;
  onToggleDarkMode: () => void;
}

export default function TopNav({ darkMode, onToggleDarkMode }: TopNavProps) {
  return (
    <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Outreach Scraping Toolkit
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Multi-platform lead generation and scraping dashboard
          </p>
        </div>
        <button
          onClick={onToggleDarkMode}
          className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          aria-label="Toggle dark mode"
        >
          {darkMode ? <Sun /> : <Moon />}
        </button>
      </div>
    </div>
  );
}
