import React, { useContext } from "react";
import { ThemeContext } from "../context/ThemeContext";
import {
  BrainCircuit,
  ActivitySquare,
  CalendarClock,
  Infinity,
  Settings2,
} from "lucide-react";

const modelBlocks = [
  {
    color: "pink",
    icon: <BrainCircuit size={28} strokeWidth={2} />,
    title: "Central Node",
    items: [
      {
        label: "Decision Engine",
        desc: "Fusion point of all intelligence: executes trades, updates weights, learns from outcome",
      },
    ],
  },
  {
    color: "cyan",
    icon: <ActivitySquare size={28} />,
    title: "Short-Term Alpha Models",
    items: [
      {
        label: "FinBERT",
        desc: "Financial sentiment classification from news and tweets",
      },
      { label: "LSTM", desc: "Sequential price movement prediction" },
      {
        label: "XGBoost",
        desc: "Price/sentiment regression from structured inputs",
      },
      {
        label: "CatBoost",
        desc: "Handles categorical features like sectors or tickers",
      },
    ],
  },
  {
    color: "yellow",
    icon: <CalendarClock size={28} strokeWidth={2} />,
    title: "Medium-Term Forecast Models",
    items: [
      { label: "Prophet", desc: "Detects seasonality and macro patterns" },
      { label: "ARIMA / SARIMA", desc: "Classical time series forecasting" },
      {
        label: "TimesNet / Informer",
        desc: "Transformer-based multi-day prediction",
      },
    ],
  },
  {
    color: "purple",
    icon: <Infinity size={28} strokeWidth={2} />,
    title: "Long-Term Intelligence Models",
    items: [
      {
        label: "RLlib / DQN / PPO",
        desc: "Reinforcement Learning for optimal trade decisions",
      },
      {
        label: "Markowitz Optimizer",
        desc: "Classical risk-return capital allocation",
      },
      {
        label: "HRP",
        desc: "Hierarchical diversification for asset clusters",
      },
    ],
  },
  {
    color: "pink",
    icon: <Settings2 size={28} strokeWidth={2} />,
    title: "Meta / Decision Core Models",
    items: [
      {
        label: "Model Ensembler",
        desc: "Combines signals from all models (stacking/blending)",
      },
      {
        label: "Bayesian Net",
        desc: "Probabilistic decision logic with uncertainty quantification",
      },
      {
        label: "AutoML / TPOT",
        desc: "Auto-selects the best pipeline per region",
      },
      {
        label: "LLM Agent (GPT-based)",
        desc: "Reads charts, reacts to changes, commands strategies",
      },
    ],
  },
];

const ModelLegend = () => {
  const { theme } = useContext(ThemeContext);

  return (
    <section className={`font-body mt-8 ${theme.textColor}`}>
      <h2 className={`text-3xl font-bold mb-6 ${theme.titleFont}`}>
        🧠 <span className="underline underline-offset-4">Model Legend</span>
      </h2>

      <div className="space-y-6">
        {modelBlocks.map((block, idx) => (
          <div
            key={idx}
            className={`rounded-lg shadow-md border ${theme.borderColor} ${theme.rowBackground1}`}
          >
            {/* Header with gradient background and aligned icon + title */}
            <div
              className={`flex items-center gap-3 px-4 py-3 rounded-t-md text-white font-header font-bold text-lg bg-gradient-to-r ${theme.primaryBg}`}
            >
              <span className="drop-shadow-[1.5px_1.5px_2px_rgba(0,0,0,0.8)]">
                {block.icon}
              </span>
              <span className="text-xl md:text-2xl font-extrabold uppercase tracking-wide drop-shadow-[1.5px_1.5px_2px_rgba(0,0,0,0.8)]">
                {block.title}
              </span>
            </div>

            {/* Model items */}
            <div className="p-4">
              <ul className="space-y-1 pl-2">
                {block.items.map((item, i) => (
                  <li key={i}>
                    <span className="text-[15px] font-body text-white subpixel-antialiased shadow-textGlow">
                      {item.label}
                    </span>{" "}
                    —{" "}
                    <span className="text-[15px] tracking-[0.05em] font-body subpixel-antialiased text-white shadow-textGlow">
                      {item.desc}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ModelLegend;
