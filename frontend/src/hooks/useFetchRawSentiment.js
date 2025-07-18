// frontend/src/hooks/useFetchRawSentiment.js
import { useEffect, useState } from "react";
import { useDateFilter } from "../context/DateFilterContext";
import useTickers from './useTickers'; // ✅ Make sure this is imported


const API_BASE = import.meta.env.VITE_API_URL;

export default function useFetchRawSentiment(ticker) {
  const { selectedTicker } = useTickers();  // ✅ get selectedTicker
  const { startDate, endDate } = useDateFilter();
  const [sentiment, setSentiment] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ticker || !startDate || !endDate) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      setSentiment([]); // Clear previous data

      try {
        const url = `${API_BASE}/api/sentiment?ticker=${ticker}&start=${startDate}&end=${endDate}`;
        console.log("📡 Fetching RAW sentiment from:", url);

        const res = await fetch(url);
        if (!res.ok) {
          const text = await res.text();
          console.error("❌ Response not ok:", text);
          throw new Error(`Fetch failed with status ${res.status}`);
        }

        const json = await res.json();
        setSentiment(Array.isArray(json) ? json : []);
        console.log("✅ Fetched sentiment:", json);
      } catch (err) {
        console.error("❌ Error fetching raw sentiment:", err);
        setError(err.message || "Unknown error");
        setSentiment([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [ticker, startDate, endDate]);

  return { selectedTicker, sentiment, error, loading };
}
