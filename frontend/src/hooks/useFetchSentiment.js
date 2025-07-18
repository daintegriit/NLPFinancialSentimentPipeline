// src/hooks/useFetchSentiment.js
import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_URL;

export default function useFetchSentiment(ticker) {
  const [sentiment, setSentiment] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ticker) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      setSentiment([]); // ✅ CLEAR OLD DATA RIGHT AWAY


      try {
        const url = `${API_BASE}/api/sentiment-over-time?ticker=${ticker}`;
        console.log("🔍 Fetching sentiment data from:", url);
        const res = await fetch(url);

        console.log("📡 Response Status:", res.status, res.statusText);
        console.log("📡 Response Headers:", res.headers);

        const text = await res.text(); // capture raw response
        console.log("🧪 Raw response text:", text);

        if (!res.ok) {
          console.error("❌ Response not OK:", text);
          throw new Error(`Fetch failed with status ${res.status}`);
        }

        let json;
        try {
          json = JSON.parse(text);
        } catch (e) {
          console.error("❌ Failed to parse JSON:", e);
          throw new Error("Invalid JSON response from server");
        }

        console.log("✅ Parsed JSON:", json);
        setSentiment(Array.isArray(json) ? json : []);
      } catch (err) {
        console.error("🔥 Error fetching sentiment data:", err);
        setError(err.message || "Unknown error");
        setSentiment([]); // ✅ Always fall back to empty
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [ticker]);

  return { sentiment, error, loading };
}
