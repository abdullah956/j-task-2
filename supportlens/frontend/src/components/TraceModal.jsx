const CATEGORY_COLORS = {
  'Billing': 'bg-blue-100 text-blue-800',
  'Refund': 'bg-red-100 text-red-800',
  'Account Access': 'bg-yellow-100 text-yellow-800',
  'Cancellation': 'bg-orange-100 text-orange-800',
  'General Inquiry': 'bg-green-100 text-green-800',
};

export default function TraceModal({ trace, onClose }) {
  if (!trace) return null;

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      onClick={handleOverlayClick}
    >
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-start mb-4">
            <h2 className="text-xl font-bold text-gray-800">Conversation Details</h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-2xl"
            >
              ✕
            </button>
          </div>

          <div className="space-y-4">
            <div>
              <p className="text-sm font-semibold text-gray-600">User Message</p>
              <p className="mt-1 text-gray-800 whitespace-pre-wrap">{trace.user_message}</p>
            </div>

            <div>
              <p className="text-sm font-semibold text-gray-600">Bot Response</p>
              <p className="mt-1 text-gray-800 whitespace-pre-wrap">{trace.bot_response}</p>
            </div>

            <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
              <div>
                <p className="text-sm font-semibold text-gray-600">Category</p>
                <span
                  className={`inline-block mt-1 px-3 py-1 text-sm font-semibold rounded-full ${
                    CATEGORY_COLORS[trace.category] || 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {trace.category}
                </span>
              </div>

              <div>
                <p className="text-sm font-semibold text-gray-600">Response Time</p>
                <p className="mt-1 text-gray-800">{trace.response_time_ms} ms</p>
              </div>

              <div>
                <p className="text-sm font-semibold text-gray-600">Timestamp</p>
                <p className="mt-1 text-gray-800 text-sm">{formatTimestamp(trace.timestamp)}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
