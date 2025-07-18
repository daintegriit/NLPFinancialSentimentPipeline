import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles/tailwind.css";

import { ThemeProvider } from "./context/ThemeContext";
import { DateFilterProvider } from "./context/DateFilterContext";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider>
      <DateFilterProvider>
        <App />
      </DateFilterProvider>
    </ThemeProvider>
  </React.StrictMode>
);
