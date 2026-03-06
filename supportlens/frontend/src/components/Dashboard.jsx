import { useState, useEffect } from 'react';
import StatsCards from './StatsCards';
import CategoryChart from './CategoryChart';
import TraceTable from './TraceTable';
import TraceModal from './TraceModal';
import { getTraces, getAnalytics, searchTraces } from '../api/client';

export default function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [traces, setTraces] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedTrace, setSelectedTrace] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedSearchQuery, setDebouncedSearchQuery] = useState('');

  // Fetch analytics on mount
  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await getAnalytics();
        setAnalytics(data);
      } catch (error) {
        console.error('Error fetching analytics:', error);
      }
    };

    fetchAnalytics();
  }, []);

  // Debounce search query
  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      setDebouncedSearchQuery(searchQuery);
    }, 400);

    return () => clearTimeout(debounceTimer);
  }, [searchQuery]);

  // Fetch traces on mount and poll every 5 seconds
  useEffect(() => {
    const fetchTracesData = async () => {
      try {
        // If search query exists, use search endpoint
        if (debouncedSearchQuery.trim().length > 0) {
          const data = await searchTraces(debouncedSearchQuery);
          setTraces(data);
        } else {
          // Otherwise use category filter
          const category = selectedCategory === 'All' ? null : selectedCategory;
          const data = await getTraces(category);
          setTraces(data);
        }
      } catch (error) {
        console.error('Error fetching traces:', error);
      }
    };

    fetchTracesData();

    // Poll every 5 seconds
    const interval = setInterval(fetchTracesData, 5000);

    return () => clearInterval(interval);
  }, [selectedCategory, debouncedSearchQuery]);

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
  };

  const handleRowClick = (trace) => {
    setSelectedTrace(trace);
  };

  const handleCloseModal = () => {
    setSelectedTrace(null);
  };

  const handleSearchChange = (query) => {
    setSearchQuery(query);
  };

  return (
    <div className="h-screen bg-gray-50 overflow-y-auto">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Support Analytics</h1>

        <StatsCards analytics={analytics} />

        <div className="mt-6">
          <CategoryChart categoryBreakdown={analytics?.category_breakdown} />
        </div>

        <div className="mt-6">
          <TraceTable
            traces={traces}
            onRowClick={handleRowClick}
            selectedCategory={selectedCategory}
            onCategoryChange={handleCategoryChange}
            searchQuery={searchQuery}
            onSearchChange={handleSearchChange}
          />
        </div>
      </div>

      {selectedTrace && (
        <TraceModal trace={selectedTrace} onClose={handleCloseModal} />
      )}
    </div>
  );
}
