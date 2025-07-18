// src/components/HeadlinesFetcher.jsx
import React, { useState, useEffect } from "react";
import HeadlinesTable from "./HeadlinesTable";

const HeadlinesFetcher = ({ ticker, sector, region, marketCap, type }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const buildQuery = () => {
      const params = new URLSearchParams();
      if (ticker) params.append("ticker", ticker);
      if (sector) params.append("sector", sector);
      if (region) params.append("region", region);
      if (marketCap) params.append("marketCap", marketCap);
      if (type) params.append("type", type);
      return params.toString();
    };

    const fetchData = async () => {
      try {
        const query = buildQuery();
        const res = await fetch(`/api/data?${query}`);
        if (!res.ok) throw new Error("API Error");
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error("🔥 Fetch error:", err);
        setError("Failed to load headlines.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [ticker, sector, region, marketCap, type]);

  if (loading) return <p className="text-yellow-400">🔄 Loading headlines...</p>;
  if (error) return <p className="text-red-500">❌ {error}</p>;

  return <HeadlinesTable data={data} />;
};

export default HeadlinesFetcher;
