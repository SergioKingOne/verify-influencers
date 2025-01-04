import { useState, useEffect } from "react";
import { mockInfluencerData } from "../mock/influencerData";

const useInfluencerData = (username) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Check if we're in development mode and should use mock data
        if (import.meta.env.MODE === "development") {
          // Simulate network delay
          await new Promise((resolve) => setTimeout(resolve, 500));
          setData(mockInfluencerData);
        } else {
          // Real API call
          const response = await fetch(`/api/influencer/${username}`);
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          const jsonData = await response.json();
          setData(jsonData);
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
