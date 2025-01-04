import { useState, useEffect } from "react";
import { mockInfluencerData } from "../mock/influencerData";

// Cache object outside the hook
const cache = new Map();

const useInfluencerData = (username) => {
  const [data, setData] = useState(() => cache.get(username) || null);
  const [loading, setLoading] = useState(!cache.has(username));
  const [error, setError] = useState(null);

  useEffect(() => {
    // If we already have cached data, don't fetch again
    if (cache.has(username)) {
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null); // Reset error state

        const response = await fetch(`/api/influencer/${username}`);

        // Handle 429 rate limit specifically
        if (response.status === 429) {
          // Fall back to mock data in case of rate limit
          setData(mockInfluencerData);
          cache.set(username, mockInfluencerData);
          return;
        }

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const jsonData = await response.json();
        setData(jsonData);
        cache.set(username, jsonData);
      } catch (err) {
        setError(err.message);
        console.error("Error fetching data:", err);

        // Fallback to mock data on error in development
        if (import.meta.env.DEV) {
          setData(mockInfluencerData);
          cache.set(username, mockInfluencerData);
          setError(null); // Clear error since we're using fallback data
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [username]);

  return { data, loading, error };
};

export default useInfluencerData;
