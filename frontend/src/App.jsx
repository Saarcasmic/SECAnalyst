import { useState } from 'react';
import ChatInterface from './ChatInterface';
import { MessageSquare, Plus, Settings, History } from 'lucide-react';

function App() {
  const [recentQueries] = useState([
    "Apple vs Microsoft Revenue",
    "Risks for Nvidia",
    "Tesla 2023 Income",
  ]);

  return (
    <div className="relative w-full h-screen bg-obsidian overflow-hidden">
      <ChatInterface />
    </div>
  );
}

export default App;
