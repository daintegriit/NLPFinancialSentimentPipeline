import React from "react";
import ReactECharts from "echarts-for-react";

const SentimentOverTimeChart = ({ timeline }) => {
  if (!timeline || timeline.length === 0) {
    return (
      <div className="text-yellow-400 px-4 py-2">
        ⚠️ No sentiment data available.
      </div>
    );
  }

  const dates = timeline.map((item) => item.date);
  const sentimentScores = timeline.map((item) => item.score_finbert);
  const close = timeline.map((item) => item.close);

  const option = {
    title: {
      text: "Sentiment vs. Price Timeline (Smoothed)",
      left: "center",
      textStyle: { color: "#00eaff", fontSize: 16 }
    },
    tooltip: {
      trigger: "axis"
    },
    legend: {
      data: ["Smoothed Sentiment", "Close"],
      bottom: 0,
      textStyle: { color: "#fff" }
    },
    xAxis: {
      type: "category",
      data: dates,
      axisLabel: { color: "#ccc" }
    },
    yAxis: [
      {
        type: "value",
        name: "Sentiment Score",
        min: 0,
        max: 1,
        position: "left",
        axisLabel: { color: "#ccc" }
      },
      {
        type: "value",
        name: "Close",
        position: "right",
        axisLabel: { color: "#ccc" }
      }
    ],
    series: [
      {
        name: "Smoothed Sentiment",
        type: "line",
        data: sentimentScores,
        smooth: true,
        lineStyle: { width: 3 }
      },
      {
        name: "Close",
        type: "line",
        yAxisIndex: 1,
        data: close,
        smooth: true,
        lineStyle: { width: 3, type: "dashed" }
      }
    ]
  };

  return (
    <div className="px-4">
      <ReactECharts option={option} style={{ height: "400px" }} />
    </div>
  );
};

export default SentimentOverTimeChart;
