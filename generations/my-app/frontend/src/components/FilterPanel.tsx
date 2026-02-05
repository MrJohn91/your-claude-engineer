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
        setError(err instanceof Error ? err.message : 'Unknown error');
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
      <div style={styles.panel}>
        <p style={styles.loadingText}>Loading filters...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.panel}>
        <p style={styles.errorText}>Error: {error}</p>
      </div>
    );
  }

  if (!config) {
    return null;
  }

  return (
    <div style={styles.panel}>
      <div style={styles.header}>
        <h2 style={styles.title}>Target Audience Filters</h2>
        <button onClick={handleClearFilters} style={styles.clearButton}>
          Clear All
        </button>
      </div>

      {/* Platform Selector */}
      <div style={styles.filterGroup}>
        <label style={styles.label}>Platform</label>
        <select
          value={filters.platform}
          onChange={handlePlatformChange}
          style={styles.select}
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
      <div style={styles.filterGroup}>
        <label style={styles.label}>Industries</label>
        <div style={styles.chipContainer}>
          {config.industries.map((industry) => (
            <button
              key={industry}
              onClick={() => handleMultiSelectChange('industries', industry)}
              style={{
                ...styles.chip,
                ...(filters.industries.includes(industry)
                  ? styles.chipActive
                  : {}),
              }}
            >
              {industry}
            </button>
          ))}
        </div>
      </div>

      {/* Roles Multi-Select */}
      <div style={styles.filterGroup}>
        <label style={styles.label}>Roles</label>
        <div style={styles.chipContainer}>
          {config.roles.map((role) => (
            <button
              key={role}
              onClick={() => handleMultiSelectChange('roles', role)}
              style={{
                ...styles.chip,
                ...(filters.roles.includes(role) ? styles.chipActive : {}),
              }}
            >
              {role}
            </button>
          ))}
        </div>
      </div>

      {/* Regions Multi-Select */}
      <div style={styles.filterGroup}>
        <label style={styles.label}>Regions</label>
        <div style={styles.chipContainer}>
          {config.regions.map((region) => (
            <button
              key={region}
              onClick={() => handleMultiSelectChange('regions', region)}
              style={{
                ...styles.chip,
                ...(filters.regions.includes(region) ? styles.chipActive : {}),
              }}
            >
              {region}
            </button>
          ))}
        </div>
      </div>

      {/* Search Query */}
      <div style={styles.filterGroup}>
        <label style={styles.label}>Search Query</label>
        <input
          type="text"
          value={filters.searchQuery}
          onChange={handleSearchChange}
          placeholder="Enter search keywords..."
          style={styles.input}
        />
      </div>

      {/* Filter Summary */}
      <div style={styles.summary}>
        <p style={styles.summaryText}>
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

const styles = {
  panel: {
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '1.5rem',
    marginBottom: '1.5rem',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  } as React.CSSProperties,
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1.5rem',
  } as React.CSSProperties,
  title: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#111827',
    margin: 0,
  } as React.CSSProperties,
  clearButton: {
    backgroundColor: 'transparent',
    border: '1px solid #d1d5db',
    borderRadius: '4px',
    padding: '0.5rem 1rem',
    fontSize: '0.875rem',
    color: '#6b7280',
    cursor: 'pointer',
    transition: 'all 0.2s',
  } as React.CSSProperties,
  filterGroup: {
    marginBottom: '1.5rem',
  } as React.CSSProperties,
  label: {
    display: 'block',
    fontSize: '0.875rem',
    fontWeight: '500',
    color: '#374151',
    marginBottom: '0.5rem',
  } as React.CSSProperties,
  select: {
    width: '100%',
    padding: '0.625rem',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    fontSize: '0.875rem',
    backgroundColor: '#ffffff',
    color: '#111827',
    cursor: 'pointer',
    transition: 'border-color 0.2s',
  } as React.CSSProperties,
  input: {
    width: '100%',
    padding: '0.625rem',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    fontSize: '0.875rem',
    backgroundColor: '#ffffff',
    color: '#111827',
    boxSizing: 'border-box' as const,
  } as React.CSSProperties,
  chipContainer: {
    display: 'flex',
    flexWrap: 'wrap' as const,
    gap: '0.5rem',
  } as React.CSSProperties,
  chip: {
    padding: '0.5rem 0.875rem',
    border: '1px solid #d1d5db',
    borderRadius: '20px',
    fontSize: '0.875rem',
    backgroundColor: '#ffffff',
    color: '#374151',
    cursor: 'pointer',
    transition: 'all 0.2s',
    whiteSpace: 'nowrap' as const,
  } as React.CSSProperties,
  chipActive: {
    backgroundColor: '#3b82f6',
    borderColor: '#3b82f6',
    color: '#ffffff',
  } as React.CSSProperties,
  summary: {
    marginTop: '1.5rem',
    paddingTop: '1rem',
    borderTop: '1px solid #e5e7eb',
  } as React.CSSProperties,
  summaryText: {
    fontSize: '0.875rem',
    color: '#6b7280',
    margin: 0,
  } as React.CSSProperties,
  loadingText: {
    fontSize: '0.875rem',
    color: '#6b7280',
    textAlign: 'center' as const,
  } as React.CSSProperties,
  errorText: {
    fontSize: '0.875rem',
    color: '#ef4444',
    textAlign: 'center' as const,
  } as React.CSSProperties,
};
