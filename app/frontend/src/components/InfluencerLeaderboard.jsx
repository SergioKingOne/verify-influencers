import React, { useState, useMemo } from 'react';
import { Users, CheckCircle, TrendingUp, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import {
  Card,
  CardContent,
} from "@/components/ui/card";
import { mockLeaderboardData } from '@/mock/leaderboardData';

const InfluencerLeaderboard = () => {
  const [activeCategory, setActiveCategory] = useState('All');
  const [sortDirection, setSortDirection] = useState('desc');

  // Use mock data in development mode
  const data = import.meta.env.DEV ? mockLeaderboardData : null; // You'll replace null with your API data in production

  // Get unique categories from influencers data
  const categories = useMemo(() => {
    const uniqueCategories = ['All', ...new Set(data.influencers.map(inf => inf.category))];
    return uniqueCategories;
  }, [data.influencers]);

  // Filter and sort influencers
  const filteredInfluencers = useMemo(() => {
    let filtered = [...data.influencers];
    
    // Apply category filter
    if (activeCategory !== 'All') {
      filtered = filtered.filter(inf => inf.category === activeCategory);
    }
    
    // Apply sorting
    filtered.sort((a, b) => {
      const modifier = sortDirection === 'desc' ? -1 : 1;
      return (a.trustScore - b.trustScore) * modifier;
    });
    
    return filtered;
  }, [data.influencers, activeCategory, sortDirection]);

  const toggleSort = () => {
    setSortDirection(prev => prev === 'desc' ? 'asc' : 'desc');
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Influencer Trust Leaderboard</h1>
          <p className="text-gray-400">
            Real-time rankings of health influencers based on scientific accuracy, credibility, and transparency. Updated daily using AI-powered analysis.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <Card className="bg-gray-800 border-0">
            <CardContent className="flex items-center gap-4 p-6">
              <div className="p-2 bg-emerald-400/10 rounded-lg">
                <Users className="h-6 w-6 text-emerald-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">{data.stats.activeInfluencers}</div>
                <div className="text-sm text-gray-400">Active Influencers</div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-800 border-0">
            <CardContent className="flex items-center gap-4 p-6">
              <div className="p-2 bg-emerald-400/10 rounded-lg">
                <CheckCircle className="h-6 w-6 text-emerald-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">{data.stats.claimsVerified}</div>
                <div className="text-sm text-gray-400">Claims Verified</div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-800 border-0">
            <CardContent className="flex items-center gap-4 p-6">
              <div className="p-2 bg-emerald-400/10 rounded-lg">
                <TrendingUp className="h-6 w-6 text-emerald-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">{data.stats.averageTrustScore}%</div>
                <div className="text-sm text-gray-400">Average Trust Score</div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Category Filters */}
        <div className="flex gap-2 mb-6">
          {categories.map((category) => (
            <button
              key={category}
              className={`px-4 py-2 rounded-full text-sm ${
                activeCategory === category
                  ? 'bg-emerald-400 text-white'
                  : 'bg-gray-800 text-gray-400'
              }`}
              onClick={() => setActiveCategory(category)}
            >
              {category}
            </button>
          ))}
          <div className="ml-auto">
            <button 
              className="px-4 py-2 rounded-full text-sm bg-gray-800 text-gray-400"
              onClick={toggleSort}
            >
              {sortDirection === 'desc' ? '↑' : '↓'} {sortDirection === 'desc' ? 'Highest' : 'Lowest'} First
            </button>
          </div>
        </div>

        {/* Table */}
        <div className="bg-gray-800 rounded-lg overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="text-gray-400 text-sm">
                <th className="px-6 py-4 text-left">RANK</th>
                <th className="px-6 py-4 text-left">INFLUENCER</th>
                <th className="px-6 py-4 text-left">CATEGORY</th>
                <th className="px-6 py-4 text-left">TRUST SCORE</th>
                <th className="px-6 py-4 text-left">TREND</th>
                <th className="px-6 py-4 text-left">FOLLOWERS</th>
                <th className="px-6 py-4 text-left">VERIFIED CLAIMS</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {filteredInfluencers.map((influencer) => (
                <tr key={influencer.rank} className="hover:bg-gray-700/50">
                  <td className="px-6 py-4 text-gray-400">#{influencer.rank}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <img
                        src={influencer.avatar}
                        alt={influencer.name}
                        className="w-10 h-10 rounded-full"
                      />
                      <span>{influencer.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-3 py-1 bg-gray-700 rounded-full text-sm">
                      {influencer.category}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-emerald-400 font-medium">
                      {influencer.trustScore}%
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {influencer.trend === 'up' ? (
                      <ArrowUpRight className="w-5 h-5 text-emerald-400" />
                    ) : (
                      <ArrowDownRight className="w-5 h-5 text-red-400" />
                    )}
                  </td>
                  <td className="px-6 py-4">{influencer.followers}</td>
                  <td className="px-6 py-4">{influencer.claims}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default InfluencerLeaderboard; 