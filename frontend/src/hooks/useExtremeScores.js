// src/hooks/useExtremeScores.js
import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_URL;

export default function useExtremeScores(ticker) {
  const [extremes, setExtremes] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ticker) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const res = await fetch(`${API_BASE}/api/extreme-scores?ticker=${ticker}`);
        if (!res.ok) throw new Error("Failed to fetch extreme scores");

        const json = await res.json();
        setExtremes(Array.isArray(json) ? json : []);
      } catch (err) {
        console.error("❌ Error fetching extreme scores:", err);
        setError(err.message || "Unknown error");
        setExtremes([]); // fallback for broken JSON
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [ticker]);

  return { extremes, error, loading };
}
