import { useEffect, useState } from "react";

// Use environment variable for backend API base URL
const API_BASE = import.meta.env.VITE_API_URL;

const useTickers = () => {
  const [tickers, setTickers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTickers = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/tickers`);
        if (!res.ok) throw new Error("Failed to fetch tickers");
        const data = await res.json();
        setTickers(data.tickers);  // 👈 extracts the array directly
      } catch (err) {
        console.error("❌ Error fetching tickers:", err);
        setError(err.message || "Unknown error");
      } finally {
        setLoading(false);
      }
    };

    fetchTickers();
  }, []);

  return { tickers, loading, error };
};

export default useTickers;
