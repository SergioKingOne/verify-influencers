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

        if (import.meta.env.MODE === "development") {
          await new Promise((resolve) => setTimeout(resolve, 500));
          setData(mockInfluencerData);
          cache.set(username, mockInfluencerData);
        } else {
          const response = await fetch(`/api/influencer/${username}`);
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          const jsonData = await response.json();
          setData(jsonData);
          cache.set(username, jsonData);
        }
      } catch (err) {
        setError(err.message);
        console.error("Error fetching data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [username]);

  return { data, loading, error };
};

export default useInfluencerData;
