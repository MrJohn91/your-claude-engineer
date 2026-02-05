import { useState, useEffect } from 'react';

interface AudienceConfig {
  platforms: string[];
  industries: string[];
  roles: string[];
  regions: string[];
}

interface FilterPanelProps {
  onFilterChange?: (filters: FilterState) => void;
}

export interface FilterState {
  platform: string;
  industries: string[];
  roles: string[];
  regions: string[];
  searchQuery: string;
}

export default function FilterPanel({ onFilterChange }: FilterPanelProps) {
  const [config, setConfig] = useState<AudienceConfig | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [filters, setFilters] = useState<FilterState>({
    platform: '',
    industries: [],
    roles: [],
    regions: [],
    searchQuery: '',
  });

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/config/audience');
        if (!response.ok) {
          throw new Error('Failed to load audience configuration');
        }
        const data = await response.json();
        setConfig(data);
        setLoading(false);
      } catch (err) {
        // Fallback to demo data if backend is not available
        console.warn('Backend not available, using demo data');
        setConfig({
          platforms: ['LinkedIn', 'X (Twitter)', 'Telegram', 'TikTok', 'Instagram'],
          industries: ['Technology', 'Finance', 'Marketing', 'Healthcare', 'Education', 'E-commerce', 'Media'],
          roles: ['Founder', 'CEO', 'CTO', 'Engineer', 'Designer', 'Product Manager', 'Marketing Manager'],
          regions: ['San Francisco, CA', 'New York, NY', 'Austin, TX', 'Seattle, WA', 'Los Angeles, CA', 'Boston, MA'],
        });
        setLoading(false);
      }
    };

    fetchConfig();
  }, []);

  useEffect(() => {
    if (onFilterChange) {
      onFilterChange(filters);
    }
  }, [filters, onFilterChange]);

  const handlePlatformChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFilters({ ...filters, platform: e.target.value });
  };

  const handleMultiSelectChange = (
    field: 'industries' | 'roles' | 'regions',
    value: string
  ) => {
    const currentValues = filters[field];
    const newValues = currentValues.includes(value)
      ? currentValues.filter((v) => v !== value)
      : [...currentValues, value];
    setFilters({ ...filters, [field]: newValues });
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters({ ...filters, searchQuery: e.target.value });
  };

  const handleClearFilters = () => {
    setFilters({
      platform: '',
      industries: [],
      roles: [],
      regions: [],
      searchQuery: '',
    });
  };

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <p className="text-center text-gray-600 dark:text-gray-400">Loading filters...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <p className="text-center text-red-600 dark:text-red-400">Error: {error}</p>
      </div>
    );
  }

  if (!config) {
    return null;
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Target Audience Filters
        </h2>
        <button
          onClick={handleClearFilters}
          className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          Clear All
        </button>
      </div>

      {/* Platform Selector */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Platform
        </label>
        <select
          value={filters.platform}
          onChange={handlePlatformChange}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        >
          <option value="">Select Platform</option>
          {config.platforms.map((platform) => (
            <option key={platform} value={platform}>
              {platform}
            </option>
          ))}
        </select>
      </div>

      {/* Industries Multi-Select */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Industries
        </label>
        <div className="flex flex-wrap gap-2">
          {config.industries.map((industry) => (
            <button
              key={industry}
              onClick={() => handleMultiSelectChange('industries', industry)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                filters.industries.includes(industry)
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {industry}
            </button>
          ))}
        </div>
      </div>

      {/* Roles Multi-Select */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Roles
        </label>
        <div className="flex flex-wrap gap-2">
          {config.roles.map((role) => (
            <button
              key={role}
              onClick={() => handleMultiSelectChange('roles', role)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                filters.roles.includes(role)
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {role}
            </button>
          ))}
        </div>
      </div>

      {/* Regions Multi-Select */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Regions
        </label>
        <div className="flex flex-wrap gap-2">
          {config.regions.map((region) => (
            <button
              key={region}
              onClick={() => handleMultiSelectChange('regions', region)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                filters.regions.includes(region)
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {region}
            </button>
          ))}
        </div>
      </div>

      {/* Search Query */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Search Query
        </label>
        <input
          type="text"
          value={filters.searchQuery}
          onChange={handleSearchChange}
          placeholder="Enter search keywords..."
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        />
      </div>

      {/* Filter Summary */}
      <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          <strong>Active Filters:</strong>{' '}
          {filters.platform && `Platform: ${filters.platform}`}
          {filters.industries.length > 0 &&
            `, Industries: ${filters.industries.length}`}
          {filters.roles.length > 0 && `, Roles: ${filters.roles.length}`}
          {filters.regions.length > 0 && `, Regions: ${filters.regions.length}`}
          {!filters.platform &&
            filters.industries.length === 0 &&
            filters.roles.length === 0 &&
            filters.regions.length === 0 &&
            'None'}
        </p>
      </div>
    </div>
  );
}
