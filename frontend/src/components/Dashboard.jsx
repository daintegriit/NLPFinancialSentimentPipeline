// frontend/src/components/Dashboard.jsx
import React, { useContext } from "react";
import { ThemeContext } from "../context/ThemeContext";
import DecisionEngineChart from "./DecisionEngineChart";
import HeadlinesTable from "./HeadlinesTable";
import ExtremeScoresTable from "./ExtremeScoresTable";
import SentimentChart from "./SentimentChart";
import SentimentOverTimeChart from "./SentimentOverTimeChart";
import ModelLegend from "./ModelLegend";
import useDashboardData from "../hooks/useDashboardData";
import { useDateFilter } from "../context/DateFilterContext"; 


const Dashboard = ({ ticker }) => {
  const { theme } = useContext(ThemeContext);
  const { startDate, endDate } = useDateFilter();


  const {
    data,
    headlines,
    extremes,
    timeline,
    error,
    loading,
  } = useDashboardData(ticker, startDate, endDate);

  console.log("✅ Loaded data for", ticker);
  console.log("data =", data);

  if (loading) {
    return (
      <div className="p-6 md:ml-64 text-yellow-400 px-4">
        ⚠️ Loading sentiment data...
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 px-4">
        ❌ Error loading data: {error.message || "Unknown error"}
      </div>
    );
  }

  if (!data || !Array.isArray(data)) {
    return (
      <div className="text-red-500 px-4">
        ❗ Unexpected data format. Please check backend response.
      </div>
    );
  }

  const sentimentCounts = data.reduce((acc, cur) => {
    const sentiment = cur.sentiment;
    acc[sentiment] = (acc[sentiment] || 0) + 1;
    return acc;
  }, {});



  return (
    <div className={`p-6 md:ml-64 ${theme.fontFamily} ${theme.textColor}`}>
      <h1 className={`text-6xl mb-4 ${theme.titleFont}`}>
        {ticker} Stock Sentiment Analyzer
      </h1>

      <p className="font-body">
        This dashboard uses Google News headlines and the FinBERT model to analyze investor sentiment.
        Future phases will add price forecasting, portfolio strategies, and a global AI brain.
      </p>

      {/* Mission */}
      <div className={`mt-6 mb-8 p-6 rounded-lg shadow border ${theme.secondaryBackgroundColor} ${theme.borderColor}`}>
        <h2 className={`text-2xl font-bold flex items-center gap-2 ${theme.primaryColor}`}>
          Mission
        </h2>
        <h3 className="mt-2 leading-relaxed">
          Build a{" "}
          <strong>
            future-proof, AI-driven market intelligence and trading system
          </strong>{" "}
          capable of scaling to{" "}
          <strong>millions, billions, or trillions</strong> in trades, data, and revenue — with a self-improving decision core.
        </h3>
      </div>

      {/* 🧬 Phases of Evolution */}
      <h2 className={`text-4xl font-bold ${theme.titleFont} mt-10 mb-2`}>
        Phases of Evolution
      </h2>
        <table className={`w-full text-sm`}>
          <thead>
            <tr className={`bg-gradient-to-r ${theme.gradientFrom} ${theme.gradientTo} text-white`}>
              <th className="text-left px-4 py-2 rounded-tl-md">Phase</th>
              <th className="text-left px-4 py-2 rounded-tr-md">Goal</th>
            </tr>
          </thead>
          <tbody>
            {[
              "Real-time sentiment extraction from news",
              "Price correlation and next-day return tracking",
              "Trend prediction using LSTM / XGBoost",
              "Reinforcement Learning for trade actions (DQN, PPO)",
              "Portfolio optimization with Genetic Algorithms",
              "Global deployment of a centralized Decision Engine"
            ].map((goal, idx) => (
              <tr
                key={idx}
                className={`${
                  idx % 2 === 0 ? theme.rowBackground1 : theme.rowBackground2
                } border-b ${theme.borderColor}`}
              >
                <td className={`px-4 py-2 font-bold ${theme.primaryColor}`}>{idx + 1}</td>
                <td className="px-4 py-2">{goal}</td>
              </tr>
            ))}
          </tbody>
        </table>

      {/* 🧠 Decision Engine */}
      <h2 className={`text-4xl font-bold mt-12 mb-2 ${theme.titleFont}`}>
        🤖 Decision Engine: AI Stack
      </h2>
      <p className="mb-4">
        This is the central AI brain composed of tightly integrated models, each with a mission-critical role.
      </p>
      <DecisionEngineChart />
      <ModelLegend />

      {/* 📊 Sentiment Chart */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-12">
        <div className="md:col-span-2">
          <SentimentChart data={data} sentimentCounts={sentimentCounts} />
        </div>
        <div className={`rounded-md p-4 ${theme.secondaryBackgroundColor} ${theme.textColor}`}>
          <h3 className={`font-bold text-2xl mb-2 ${theme.primaryColor}`}>
            📚 How to Read FinBERT & RoBERTa Scores
          </h3>
          <ul className="list-disc ml-6 text-sm">
            <li>🔴 0.00 to 0.65: Low confidence</li>
            <li>🟠 0.66 to 0.80: Moderate sentiment</li>
            <li>🟢 0.81 to 1.00: Strong sentiment</li>
            <li>⚫️ &lt;0.5 or &gt;1.00: Outliers (rare)</li>
          </ul>
          <p className="text-sm italic mt-2 text-gray-400">
            Score is the model’s confidence in the predicted label, not strength of emotion.
          </p>
        </div>
      </div>

      {/* 📰 Headlines + 📉 Extreme Scores + 📈 Timeline */}
      <div className="mt-10">
        <HeadlinesTable data={headlines} />
      </div>
      <div className="mt-10">
        <ExtremeScoresTable data={extremes} />
      </div>
      <div className="mt-10">
        <SentimentOverTimeChart timeline={timeline} />
      </div>
    </div>
  );
};

export default Dashboard;
