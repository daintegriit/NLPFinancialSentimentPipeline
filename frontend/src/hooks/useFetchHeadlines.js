// src/hooks/useFetchHeadlines.js
import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_URL;

export default function useFetchHeadlines(ticker) {
  const [headlines, setHeadlines] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ticker) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const res = await fetch(`${API_BASE}/api/news-table?ticker=${ticker}`);
        if (!res.ok) throw new Error("Failed to fetch headlines");

        const json = await res.json();
        setHeadlines(Array.isArray(json) ? json : []);
      } catch (err) {
        console.error("❌ Error fetching headlines:", err);
        setError(err.message || "Unknown error occurred.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [ticker]);

  return { headlines, error, loading };
}
