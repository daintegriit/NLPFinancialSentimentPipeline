// frontend/src/components/Tabs.jsx
import React, { useState } from "react";

const Tabs = ({ tabs }) => {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <div className="w-full">
      {/* Tab Buttons */}
      <div className="flex space-x-4 mb-4 border-b border-gray-700 pb-2">
        {tabs.map((tab, index) => (
          <button
            key={index}
            onClick={() => setActiveIndex(index)}
            className={`px-4 py-2 rounded-t-md font-semibold text-sm transition ${
              index === activeIndex
                ? "bg-gradient-to-r from-cyan-500 to-blue-500 text-black"
                : "bg-gray-800 text-gray-300 hover:bg-gray-700"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="mt-2">{tabs[activeIndex]?.component}</div>
    </div>
  );
};

export default Tabs;
