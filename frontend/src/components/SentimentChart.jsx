// src/components/SentimentChart.jsx
import React from "react";
import ReactECharts from "echarts-for-react";
import useFetchRawSentiment from "../hooks/useFetchRawSentiment"; // ✅ NEW
import { useDateFilter } from "../context/DateFilterContext"; // ✅ GLOBAL DATES

const SentimentChart = ({ theme }) => {
  const { ticker } = useDateFilter(); // ✅ pulls from context
  const { sentiment: data, loading, error } = useFetchRawSentiment(ticker);
  const { selectedDate } = useDateFilter(); // ✅ NEW

  if (loading) return <p className="text-yellow-300">⏳ Loading sentiment data...</p>;
  if (error) return <p className="text-red-500">❌ {error}</p>;
  if (!data || data.length === 0) return <p className="text-yellow-400">⚠️ No sentiment data loaded.</p>;

  console.log("📊 SentimentChart received data:", data);


  // Initialize label counters
  const finbertCounts = {};
  const robertaCounts = {};
  const labelDates = {}; // { POSITIVE: Set([...]), NEGATIVE: Set([...]) }

  // Normalize and count FinBERT and RoBERTa sentiment labels
  data.forEach((curr) => {
    const fLabel = (curr.label_finbert || "").toUpperCase();
    const rLabel = (curr.label_roberta || "").toUpperCase();
    const date = curr.date;

    if (!fLabel && !rLabel) return;

    console.log("🧪 Row Label Check:", { label, robertaLabel, date });

    if (fLabel) {
      finbertCounts[fLabel] = (finbertCounts[fLabel] || 0) + 1;
      if (!labelDates[fLabel]) labelDates[fLabel] = new Set();
      labelDates[fLabel].add(date);
    }

    if (rLabel) {
      robertaCounts[rLabel] = (robertaCounts[rLabel] || 0) + 1;
      if (!labelDates[rLabel]) labelDates[rLabel] = new Set();
      labelDates[rLabel].add(date);
    }
  });

  // Get a combined list of all labels (POSITIVE, NEGATIVE, etc.)
  const allLabels = Array.from(new Set([
    ...Object.keys(finbertCounts),
    ...Object.keys(robertaCounts),
  ]));

  console.log("🧠 All Labels:", allLabels);
  console.log("📊 FinBERT Counts:", finbertCounts);
  console.log("📊 RoBERTa Counts:", robertaCounts);
  console.log("🧮 allValuesZero:", allValuesZero);


  // ✅ NEW: Guard clause to prevent rendering if all values are zero
  const allValuesZero =
    Object.keys(finbertCounts).length === 0 &&
    Object.keys(robertaCounts).length === 0;


  if (allLabels.length === 0 || allValuesZero) {
    return (
      <div className="text-center text-yellow-500 mt-4">
        No sentiment data available to display.
      </div>
    );
  }

  // Utility: get color by label
  const getColor = (label) => {
    if (label === "POSITIVE") return "#00ff00";
    if (label === "NEGATIVE") return "#ff0040";
    if (label === "NEUTRAL") return "#999999";
    return theme === "Cyber Dark" ? "#00ffff" : "#39f1f4";
  };

  const option = {
    title: {
      text: `FinBERT vs RoBERTa Sentiment Overview ${selectedDate ? `(${selectedDate})` : ""}`, // ✅ dynamic
      left: "center",
      textStyle: {
        color: theme === "Cyber Dark" ? "#ffffff" : "#333333",
      },
    },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      formatter: function (params) {
        const label = params[0].name;
        const finbertCount = params.find(p => p.seriesName === "FinBERT")?.value || 0;
        const robertaCount = params.find(p => p.seriesName === "RoBERTa")?.value || 0;
        const dates = labelDates[label]
          ? Array.from(labelDates[label]).sort((a, b) => new Date(b) - new Date(a))
          : [];

        return `
          <b>${label}</b><br/>
          FinBERT: ${finbertCount}<br/>
          RoBERTa: ${robertaCount}<br/>
          ${dates.length > 0 ? `Dates:<br/>` + dates.slice(0, 5).join("<br/>") : ""}
          ${dates.length > 5 ? `<i>+${dates.length - 5} more...</i>` : ""}
        `;
      },
    },
    legend: {
      data: ["FinBERT", "RoBERTa"],
      top: 30,
      textStyle: {
        color: theme === "Cyber Dark" ? "#dddddd" : "#333333",
      },
    },
    xAxis: {
      type: "category",
      data: allLabels,
      axisLabel: {
        color: theme === "Cyber Dark" ? "#ffffff" : "#000000",
      },
    },
    yAxis: {
      type: "value",
      name: "Count",
      axisLabel: {
        color: theme === "Cyber Dark" ? "#ffffff" : "#000000",
      },
    },
    series: [
      {
        name: "FinBERT",
        type: "bar",
        data: allLabels.map((label) => finbertCounts[label] || 0),
        itemStyle: {
          color: (params) => getColor(allLabels[params.dataIndex]),
        },
        barGap: 0,
      },
      {
        name: "RoBERTa",
        type: "bar",
        data: allLabels.map((label) => robertaCounts[label] || 0),
        itemStyle: {
          color: theme === "Cyber Dark" ? "#8888ff" : "#3366ff",
        },
      },
    ],
    grid: {
      top: 80,
      left: 60,
      right: 30,
      bottom: 50,
    },
  };

  return (
    <ReactECharts
      option={option}
      style={{ height: "400px", width: "100%" }}
    />
  );
};

export default SentimentChart;

