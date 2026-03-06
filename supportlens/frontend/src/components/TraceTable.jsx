const CATEGORY_COLORS = {
  'Billing': 'bg-blue-100 text-blue-800',
  'Refund': 'bg-red-100 text-red-800',
  'Account Access': 'bg-yellow-100 text-yellow-800',
  'Cancellation': 'bg-orange-100 text-orange-800',
  'General Inquiry': 'bg-green-100 text-green-800',
};

const CATEGORIES = ['All', 'Billing', 'Refund', 'Account Access', 'Cancellation', 'General Inquiry'];

export default function TraceTable({ traces, onRowClick, selectedCategory, onCategoryChange, searchQuery, onSearchChange }) {
  const truncate = (text, maxLength) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Recent Conversations</h3>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-600">Search:</label>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => onSearchChange(e.target.value)}
                placeholder="Search conversations..."
                className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 w-64"
              />
            </div>

            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-600">Filter:</label>
              <select
                value={selectedCategory}
                onChange={(e) => onCategoryChange(e.target.value)}
                disabled={searchQuery.length > 0}
                className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              >
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {traces.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No conversations yet
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Timestamp
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Category
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    User Message
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Bot Response
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Response Time
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {traces.map((trace) => (
                  <tr
                    key={trace.id}
                    onClick={() => onRowClick(trace)}
                    className="hover:bg-gray-50 cursor-pointer"
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {formatTimestamp(trace.timestamp)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 py-1 text-xs font-semibold rounded-full ${
                          CATEGORY_COLORS[trace.category] || 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {trace.category}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-800">
                      {truncate(trace.user_message, 60)}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-800">
                      {truncate(trace.bot_response, 60)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {trace.response_time_ms} ms
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
