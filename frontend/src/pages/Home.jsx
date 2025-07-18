// frontend/src/pages/Home.jsx
import React, { useState } from "react";
import Dashboard from "../components/Dashboard";
import Sidebar from "../components/Sidebar";
import useDashboardData from "../hooks/useDashboardData";

const Home = () => {
  const [ticker, setTicker] = useState("AAPL"); // ✅ Initial default to trigger loading

  const {
    data,
    headlines,
    sentiment,
    extremes,
    timeline,
    error,
    loading,
  } = useDashboardData(ticker); // ✅ Syncs on change

  return (
    <div className="flex min-h-screen bg-black text-white">
      <Sidebar ticker={ticker} setTicker={setTicker} />
      <Dashboard
        ticker={ticker}
        data={data}
        headlines={headlines}
        sentiment={sentiment}
        extremes={extremes}
        timeline={timeline}
        error={error}
        loading={loading}
      />
    </div>
  );
};

export default Home;
