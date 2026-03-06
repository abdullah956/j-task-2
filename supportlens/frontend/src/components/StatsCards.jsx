export default function StatsCards({ analytics }) {
  if (!analytics) {
    return (
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-sm text-gray-600">Total Conversations</p>
          <p className="text-3xl font-bold text-gray-800 mt-2">--</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-sm text-gray-600">Avg Response Time</p>
          <p className="text-3xl font-bold text-gray-800 mt-2">-- ms</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-sm text-gray-600">Top Category</p>
          <p className="text-3xl font-bold text-gray-800 mt-2">--</p>
        </div>
      </div>
    );
  }

  const topCategory =
    analytics.category_breakdown.length > 0
      ? analytics.category_breakdown.reduce((max, curr) =>
          curr.count > max.count ? curr : max
        )
      : null;

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="bg-white p-6 rounded-lg shadow">
        <p className="text-sm text-gray-600">Total Conversations</p>
        <p className="text-3xl font-bold text-gray-800 mt-2">
          {analytics.total_traces}
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <p className="text-sm text-gray-600">Avg Response Time</p>
        <p className="text-3xl font-bold text-gray-800 mt-2">
          {Math.round(analytics.avg_response_time_ms)} ms
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <p className="text-sm text-gray-600">Top Category</p>
        <p className="text-xl font-bold text-gray-800 mt-2">
          {topCategory ? topCategory.category : '--'}
        </p>
        {topCategory && (
          <p className="text-sm text-gray-500 mt-1">
            {topCategory.count} conversations
          </p>
        )}
      </div>
    </div>
  );
}
