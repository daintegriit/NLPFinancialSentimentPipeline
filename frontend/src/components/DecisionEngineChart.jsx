import React, { useEffect } from "react";
import ReactECharts from "echarts-for-react";
import usePipelineData from "../hooks/usePipelineData";

const DecisionEngineChart = () => {
  const { data, loading, error } = usePipelineData();

  useEffect(() => {
    if (error) console.error("Graph fetch error:", error);
  }, [error]);

  if (loading)
    return <div className="text-center text-white">Loading graph...</div>;
  if (error)
    return (
      <div className="text-red-500">Error loading graph: {error.message}</div>
    );
  if (!data || !data.series) return <div>No data available</div>;

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold text-white mb-4">
        Decision Engine Graph
      </h2>
      <ReactECharts
        option={data}
        style={{ height: "600px", width: "100%" }}
        theme="dark"
        notMerge={true}
        lazyUpdate={true}
      />
    </div>
  );
};

export default DecisionEngineChart;
