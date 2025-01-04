import { useState, useEffect } from "react";
import { mockInfluencerData } from "../mock/influencerData";

// Cache object outside the hook
const cache = new Map();

const useInfluencerData = (username) => {
  // Initialize with cached data if available
  const [data, setData] = useState(() => cache.get(username));
  const [loading, setLoading] = useState(!cache.has(username));
  const [error, setError] = useState(null);

  useEffect(() => {
    // If we have cached data, use it and don't fetch
    if (cache.has(username)) {
      console.log("Using cached data for", username);
      setData(cache.get(username));
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        console.log("Fetching data for", username);

        const response = await fetch(`/api/influencer/${username}`);
        const jsonData = await response.json();

        // Cache and use the successful response
        console.log("Caching response for", username);
        cache.set(username, jsonData);
        setData(jsonData);
      } catch (err) {
        console.error("Error fetching data:", err);
        if (import.meta.env.DEV) {
          setData(mockInfluencerData);
        } else {
          setError(err.message);
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
