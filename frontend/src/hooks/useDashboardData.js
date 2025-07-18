// src/hooks/useDashboardData.js
import { useEffect, useState } from "react";
import { useDateFilter } from "../context/DateFilterContext";
const API_BASE = import.meta.env.VITE_API_URL;

const useDashboardData = (ticker) => {
  const [data, setData] = useState(null);              // 🧠 Sentiment pipeline output
  const [headlines, setHeadlines] = useState([]);      // 🗞 FinBERT sentiment table
  const [sentiment, setSentiment] = useState([]);      // 📊 FinBERT sentiment scores
  const [extremes, setExtremes] = useState([]);        // 📈 Extreme sentiment headlines
  const [timeline, setTimeline] = useState([]);        // ⏳ Timeline data
  const [error, setError] = useState(null);            // ❌ Error tracker
  const [loading, setLoading] = useState(true);        // ⏳ Loading state
  const { startDate, endDate } = useDateFilter(); // ✅


  useEffect(() => {
    if (!ticker || !startDate || !endDate) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const query = `ticker=${ticker}&start=${startDate}&end=${endDate}`; // ✅ Append dates

        const [
          pipelineRes,
          headlineRes,
          sentimentRes,
          extremesRes,
          timelineRes,
        ] = await Promise.all([
            fetch(`${API_BASE}/api/pipeline-output?${query}`),
            fetch(`${API_BASE}/api/news-table?${query}`),
            fetch(`${API_BASE}/api/news-table?ticker=${ticker}`),
            fetch(`${API_BASE}/api/sentiment?${query}`),
            fetch(`${API_BASE}/api/extreme-scores?${query}`),
            fetch(`${API_BASE}/api/sentiment-over-time?${query}`),
          ]);


        // 🧱 Check for errors
        if (!pipelineRes.ok) throw new Error("Failed to fetch pipeline output.");
        if (!headlineRes.ok) throw new Error("Failed to fetch headlines.");
        if (!sentimentRes.ok) throw new Error("Failed to fetch sentiment.");
        if (!extremesRes.ok) throw new Error("Failed to fetch extreme scores.");
        if (!timelineRes.ok) throw new Error("Failed to fetch timeline.");

        // 📦 Parse and extract `.data` fields
        const pipelineData = await pipelineRes.json();
        const headlinesData = await headlineRes.json();
        const sentimentData = await sentimentRes.json();
        const extremesData = await extremesRes.json();
        console.log("🧠 Raw extremesData from API:", extremesData);
        const timelineData = await timelineRes.json();

        // ✅ Set with .data fallback
        setData(pipelineData?.data || []);
        setHeadlines(Array.isArray(headlinesData) ? headlinesData : []);
        setSentiment(Array.isArray(sentimentData) ? sentimentData : []);
        setExtremes(Array.isArray(extremesData) ? extremesData : []);
        console.log("📡 Raw timelineData from API:", timelineData);
        setTimeline(Array.isArray(timelineData) ? timelineData : []);
      } catch (err) {
        console.error("❌ Error in useDashboardData:", err);
        setError(err.message || "Unknown error occurred.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [ticker]);

  return {
    data,
    headlines,
    sentiment,
    extremes,
    timeline,
    error,
    loading,
  };
};

export default useDashboardData;
