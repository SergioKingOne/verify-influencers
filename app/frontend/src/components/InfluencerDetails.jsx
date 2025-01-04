import React, { useState } from 'react';
import { Search } from 'lucide-react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import useInfluencerData from '@/hooks/useInfluencerData';

const InfluencerDetails = () => {
  const [activeCategory, setActiveCategory] = useState('All Categories');
  const [activeStatus, setActiveStatus] = useState('All Statuses');
  
  const { data: influencerData, loading, error } = useInfluencerData('hubermanlab');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!influencerData) return <div>No data available</div>;

  const categories = [
    'All Categories', 'Sleep', 'Performance', 'Hormones', 'Nutrition',
    'Exercise', 'Stress', 'Cognition', 'Motivation', 'Recovery', 'Mental Health'
  ];

  const statuses = ['All Statuses', 'Verified', 'Questionable', 'Debunked'];

  const claims = [
    {
      id: 1,
      title: 'Viewing sunlight within 30-50 minutes of waking enhances cortisol release',
      status: 'Verified',
      date: '14/01/2024',
      trustScore: 92,
      aiAnalysis: 'Multiple studies confirm morning light exposure affects cortisol rhythms. Timing window supported by research.',
    },
    {
      id: 2,
      title: 'Non-sleep deep rest (NSDR) protocols can accelerate learning and recovery',
      status: 'Verified',
      date: '28/12/2023',
      trustScore: 88,
    }
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Profile Section */}
        <div className="mb-8">
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 rounded-full bg-gray-700">
              {influencerData.profile_image && (
                <img 
                  src={influencerData.profile_image} 
                  alt="Profile" 
                  className="w-full h-full rounded-full"
                />
              )}
            </div>
            <div>
              <h1 className="text-2xl font-bold">{influencerData.username}</h1>
              <div className="flex gap-2 text-gray-400 mt-1">
                <span>Neuroscience</span>
                <span>•</span>
                <span>Sleep</span>
                <span>•</span>
                <span>Performance</span>
                <span>•</span>
                <span>Hormones</span>
              </div>
              <p className="text-gray-400 mt-2 max-w-2xl">
                Stanford Professor of Neurobiology and Ophthalmology, focusing on neural development, 
                brain plasticity, and neural regeneration. Host of the Huberman Lab Podcast, translating 
                neuroscience into practical tools for everyday life.
              </p>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-4 gap-4 mt-8">
            <Card className="bg-gray-800 border-0">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm text-gray-400">Trust Score</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-emerald-400">89%</div>
                <div className="text-xs text-gray-400 mt-1">Based on 127 verified claims</div>
              </CardContent>
            </Card>
            
            <Card className="bg-gray-800 border-0">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm text-gray-400">Yearly Revenue</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-emerald-400">$5.0M</div>
                <div className="text-xs text-gray-400 mt-1">Estimated earnings</div>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-0">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm text-gray-400">Products</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-emerald-400">1</div>
                <div className="text-xs text-gray-400 mt-1">Recommended products</div>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-0">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm text-gray-400">Followers</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-emerald-400">4.2M+</div>
                <div className="text-xs text-gray-400 mt-1">Total following</div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Navigation */}
        <div className="flex gap-6 border-b border-gray-800 mb-6">
          <button className="text-emerald-400 pb-2 border-b-2 border-emerald-400">
            Claims Analysis
          </button>
          <button className="text-gray-400 pb-2">Recommended Products</button>
          <button className="text-gray-400 pb-2">Monetization</button>
        </div>

        {/* Search and Filters */}
        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          <div className="relative mb-6">
            <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search claims..."
              className="w-full bg-gray-900 text-white pl-10 pr-4 py-2 rounded-md border border-gray-700 focus:outline-none focus:border-emerald-400"
            />
          </div>

          <div className="space-y-4">
            <div>
              <div className="text-sm text-gray-400 mb-2">Categories</div>
              <div className="flex flex-wrap gap-2">
                {categories.map((category) => (
                  <button
                    key={category}
                    className={`px-3 py-1 rounded-full text-sm ${
                      activeCategory === category
                        ? 'bg-emerald-400 text-white'
                        : 'bg-gray-900 text-gray-400'
                    }`}
                    onClick={() => setActiveCategory(category)}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <div className="text-sm text-gray-400 mb-2">Verification Status</div>
              <div className="flex gap-2">
                {statuses.map((status) => (
                  <button
                    key={status}
                    className={`px-3 py-1 rounded-full text-sm ${
                      activeStatus === status
                        ? 'bg-emerald-400 text-white'
                        : 'bg-gray-900 text-gray-400'
                    }`}
                    onClick={() => setActiveStatus(status)}
                  >
                    {status}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Claims List */}
        <div className="space-y-4">
          <div className="text-sm text-gray-400">Showing 10 claims</div>
          {claims.map((claim) => (
            <div key={claim.id} className="bg-gray-800 rounded-lg p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-1 text-xs rounded-full bg-emerald-400/20 text-emerald-400">
                    verified
                  </span>
                  <span className="text-gray-400 text-sm">{claim.date}</span>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-emerald-400">{claim.trustScore}%</div>
                  <div className="text-xs text-gray-400">Trust Score</div>
                </div>
              </div>
              <h3 className="text-lg font-medium mb-4">{claim.title}</h3>
              {claim.aiAnalysis && (
                <div className="flex items-start gap-2 bg-gray-900 rounded-lg p-4">
                  <div className="w-6 h-6 rounded-full bg-emerald-400/20 flex items-center justify-center">
                    AI
                  </div>
                  <div className="text-sm text-gray-400">
                    {claim.aiAnalysis}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default InfluencerDetails;