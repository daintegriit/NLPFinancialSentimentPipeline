import React from "react";
import { useDateFilter } from "../context/DateFilterContext";

const DateFilterBar = () => {
  const { startDate, setStartDate } = useDateFilter();

  const handleChange = (e) => setStartDate(e.target.value);

  return (
    <div className="flex items-center gap-3 mb-4">
      <label className="text-sm text-white">📅 Select Date:</label>
      <input
        type="date"
        value={startDate}
        onChange={handleChange}
        className="bg-gray-800 text-white px-2 py-1 rounded"
      />
      <button
        onClick={() => setStartDate("")}
        className="text-blue-400 underline text-sm"
      >
        Clear
      </button>
    </div>
  );
};

export default DateFilterBar;
