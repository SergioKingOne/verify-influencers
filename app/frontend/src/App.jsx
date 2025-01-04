import { useState } from 'react'
import InfluencerDetails from './components/InfluencerDetails'
import InfluencerLeaderboard from './components/InfluencerLeaderboard'

function App() {
  const [activeView, setActiveView] = useState('leaderboard')

  return (
    <div>
      {/* Navigation */}
      <nav className="bg-gray-800 text-white p-4">
        <div className="max-w-7xl mx-auto flex gap-4">
          <button 
            className={`px-4 py-2 rounded-lg ${activeView === 'leaderboard' ? 'bg-emerald-400' : 'bg-gray-700'}`}
            onClick={() => setActiveView('leaderboard')}
          >
            Leaderboard
          </button>
          <button 
            className={`px-4 py-2 rounded-lg ${activeView === 'details' ? 'bg-emerald-400' : 'bg-gray-700'}`}
            onClick={() => setActiveView('details')}
          >
            Influencer Details
          </button>
        </div>
      </nav>

      {/* Content */}
      {activeView === 'leaderboard' ? (
        <InfluencerLeaderboard />
      ) : (
        <InfluencerDetails />
      )}
    </div>
  )
}

export default App
