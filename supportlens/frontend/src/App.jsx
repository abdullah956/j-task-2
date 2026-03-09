import Chatbot from './components/Chatbot';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="flex h-screen">
      {/* Left Column - Chatbot (35%) */}
      <div className="w-[35%]">
        <Chatbot />
      </div>

      {/* Right Column - Dashboard (65%) */}
      <div className="w-[65%]">
        <Dashboard />
      </div>
    </div>
  );
}

export default App;
