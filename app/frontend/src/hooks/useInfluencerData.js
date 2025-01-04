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
    // Debug current mode
    console.log("Current mode:", import.meta.env.MODE);

    // Only use mock data if explicitly in development mode
    if (import.meta.env.MODE === "development") {
      console.log("Using mock data in dev mode for", username);
      setData(mockInfluencerData);
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        console.log("About to fetch data for", username);
        console.log("Fetch URL:", `/api/influencer/${username}`);

        const response = await fetch(`/api/influencer/${username}`);
        console.log("Response received:", response.status, response.statusText);

        const jsonData = await response.json();
        console.log("Parsed data:", jsonData);

        // Cache only in production mode
        if (import.meta.env.MODE === "production") {
          console.log("Caching response for", username);
          cache.set(username, jsonData);
        }
        setData(jsonData);
      } catch (err) {
        console.error("Detailed error:", {
          message: err.message,
          stack: err.stack,
          err,
        });
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [username]);

  return { data, loading, error };
};

export default useInfluencerData;
