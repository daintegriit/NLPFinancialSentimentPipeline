// frontend/src/components/Sidebar.jsx
import React, { useContext, useState, useEffect } from "react";
import { ThemeContext, themes } from "../context/ThemeContext";
import useTickers from "../hooks/useTickers";
import { useDateFilter } from "../context/DateFilterContext";

const Sidebar = ({ ticker, setTicker }) => {
  const { theme, setThemeChoice } = useContext(ThemeContext);
  const { tickers, loading } = useTickers();
  const { startDate, endDate, setStartDate, setEndDate } = useDateFilter();
  const [pickerMode, setPickerMode] = useState("single");

  const today = new Date().toISOString().split("T")[0];

  // ⏳ Initialize default to today's date on mount
  useEffect(() => {
    if (!startDate) setStartDate(today);
    if (!endDate) setEndDate(today);
  }, []);

  const downloadCSV = () => {
    window.open(`http://localhost:8000/download/${ticker}`, "_blank");
  };

  return (
    <aside
      className="w-64 p-4 mt-2 h-screen overflow-y-auto fixed left-0 top-0 border-r"
      style={{ backgroundColor: theme.secondaryBackgroundColor, borderColor: theme.borderColor }}
    >
      <h2 className="text-3xl font-header font-bold mb-4" style={{ color: theme.textColor }}>
        Navigation
      </h2>

      {/* 🌈 Theme Selector */}
      <div className="text-sm mb-4" style={{ color: theme.textColor, fontFamily: theme.fontFamily }}>
        <label className="block font-bold text-sm mb-1">Theme</label>
        <select
          value={theme.name}
          onChange={(e) => setThemeChoice(e.target.value)}
          className="w-full p-2 rounded bg-gray-800 text-white"
        >
          {Object.keys(themes).map((key) => (
            <option key={key} value={key}>
              {key}
            </option>
          ))}
        </select>
      </div>

      {/* 📈 Ticker Selector */}
      <div className="text-sm mb-4" style={{ color: theme.textColor, fontFamily: theme.fontFamily }}>
        <label className="block font-bold text-sm mb-1">Ticker</label>
        {loading ? (
          <p className="text-gray-400">Loading tickers...</p>
        ) : (
          <select
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            className="w-full p-2 rounded bg-gray-800 text-white"
          >
            {tickers.map((t) => (
              <option key={t.ticker} value={t.ticker}>
                {t.ticker} | {t.query}
              </option>
            ))}
          </select>
        )}
      </div>

      {/* 🗓️ Smart Date Picker */}
      <div className="text-sm mb-4" style={{ color: theme.textColor, fontFamily: theme.fontFamily }}>
        <label className="block font-bold text-sm mb-1">Date Picker Mode</label>
        <select
          value={pickerMode}
          onChange={(e) => setPickerMode(e.target.value)}
          className="w-full p-2 rounded bg-gray-800 text-white mb-2"
        >
          <option value="single">Single Day</option>
          <option value="range">Date Range</option>
        </select>

        {/* 🟢 Single Mode */}
        {pickerMode === "single" && (
          <div>
            <label className="block font-bold text-sm mb-1">Date</label>
            <input
              type="date"
              value={startDate || today}
              onChange={(e) => {
                setStartDate(e.target.value);
                setEndDate(e.target.value); // mirror
              }}
              className="w-full p-2 rounded bg-gray-800 text-white"
            />
          </div>
        )}

        {/* 🔵 Range Mode */}
        {pickerMode === "range" && (
          <>
            <label className="block font-bold text-sm mb-1 mt-2">Start Date</label>
            <input
              type="date"
              value={startDate || today}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full p-2 rounded bg-gray-800 text-white mb-2"
            />

            <label className="block font-bold text-sm mb-1">End Date</label>
            <input
              type="date"
              value={endDate || today}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full p-2 rounded bg-gray-800 text-white"
            />
          </>
        )}
      </div>

      <p className="text-xs text-gray-400 mt-1 italic">🎯 Filters all charts and tables globally</p>

      {/* 📥 Download CSV Button */}
      <button
        onClick={downloadCSV}
        className={`w-full mt-4 ${theme.primaryBg} ${theme.fontFamily} text-gray-900 p-2 rounded hover:opacity-90`}
      >
        📁 Download CSV
      </button>
    </aside>
  );
};

export default Sidebar;
