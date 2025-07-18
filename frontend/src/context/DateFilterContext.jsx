// frontend/src/context/DateFilterContext.jsx
import { createContext, useContext, useState } from "react";

const DateFilterContext = createContext();

export const DateFilterProvider = ({ children }) => {
  const today = new Date().toLocaleDateString("en-CA"); // ✅ Local timezone-safe format

  const [startDate, setStartDate] = useState(today);
  const [endDate, setEndDate] = useState(today);

  return (
    <DateFilterContext.Provider
      value={{ startDate, endDate, setStartDate, setEndDate }}
    >
      {children}
    </DateFilterContext.Provider>
  );
};

export const useDateFilter = () => useContext(DateFilterContext);
