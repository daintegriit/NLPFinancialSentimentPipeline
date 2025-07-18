import { useState, useEffect } from "react";

const API_BASE = import.meta.env.VITE_API_URL;

const usePipelineData = () => {
  const [pipelineOutput, setPipelineOutput] = useState({});
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true); // ✅ Add loading state for UX

  useEffect(() => {
    const fetchPipelineData = async () => {
      setLoading(true);
      setError(null);

      try {
        const res = await fetch(`${API_BASE}/api/pipeline-output?ticker=${ticker}`);
        if (!res.ok) throw new Error("Failed to fetch pipeline output");
        const data = await res.json();

        // ✅ Group by ticker
        const grouped = data.reduce((acc, item) => {
          const t = item.ticker;
          if (!acc[t]) acc[t] = [];
          acc[t].push(item);
          return acc;
        }, {});

        setPipelineOutput(grouped);
      } catch (err) {
        console.error("❌ Error fetching pipeline data:", err);
        setError(err.message || "Unknown error");
      } finally {
        setLoading(false);
      }
    };

    fetchPipelineData();
  }, []);

  return { pipelineOutput, error, loading };
};

export default usePipelineData;
