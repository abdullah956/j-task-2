import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

const COLORS = {
  'Billing': '#3b82f6',
  'Refund': '#ef4444',
  'Account Access': '#f59e0b',
  'Cancellation': '#fb923c',
  'General Inquiry': '#10b981',
};

export default function CategoryChart({ categoryBreakdown }) {
  if (!categoryBreakdown || categoryBreakdown.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Category Distribution</h3>
        <div className="h-64 flex items-center justify-center text-gray-500">
          No data available
        </div>
      </div>
    );
  }

  const chartData = categoryBreakdown.map((item) => ({
    name: item.category,
    count: item.count,
    percentage: item.percentage,
  }));

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Category Distribution</h3>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
          <YAxis />
          <Tooltip
            formatter={(value, name) => {
              if (name === 'count') return [value, 'Count'];
              if (name === 'percentage') return [`${value}%`, 'Percentage'];
              return [value, name];
            }}
          />
          <Legend />
          <Bar dataKey="count" fill="#3b82f6">
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#3b82f6'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
