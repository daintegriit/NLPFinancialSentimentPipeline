import React, { createContext, useState, useEffect } from "react";

// Tailwind-based theme definitions
export const themes = {
  "Cyber Dark": {
    name: "Cyber Dark",
    primaryColor: "text-cyan-400",
    primaryBg: "bg-cyan-500",
    gradientFrom: "from-cyan-500",
    gradientTo: "to-cyan-700",
    backgroundColor: "bg-[#0d1117]",
    secondaryBackgroundColor: "bg-[#161b22]",
    textColor: "text-gray-300",
    rowBackground1: "bg-gray-900",
    rowBackground2: "bg-gray-800",
    borderColor: "border-cyan-500",
    font: "font-mono",
    fontFamily: "font-['PixeloidMono']",
    titleFont: "font-['BulletSmallcaps']",
  },

  Matrix: {
    name: "Matrix",
    primaryColor: "text-[#00ff41]", // Classic Matrix green
    primaryBg: "bg-[#00ff41]",
    gradientFrom: "from-[#00ff41]",
    gradientTo: "to-[#02c935]",
    backgroundColor: "bg-black",
    secondaryBackgroundColor: "bg-[#111111]",
    textColor: "text-[#00ff41]",
    rowBackground1: "bg-[#0a0a0a]",
    rowBackground2: "bg-[#111111]",
    borderColor: "border-[#00ff41]",
    font: "font-mono",
    fontFamily: "font-['PixeloidMono']",
    titleFont: "font-['BulletSmallcaps']",
  },

  Bloomberg: {
    name: "Bloomberg",
    primaryColor: "text-amber-600", // Bloomberg deep amber-orange
    primaryBg: "bg-amber-600",
    gradientFrom: "from-amber-600",
    gradientTo: "to-orange-800",
    backgroundColor: "bg-[#1b1b1b]",
    secondaryBackgroundColor: "bg-[#2b2b2b]",
    textColor: "text-white",
    rowBackground1: "bg-[#2a2a2a]",
    rowBackground2: "bg-[#1f1f1f]",
    borderColor: "border-amber-600",
    font: "font-mono",
    fontFamily: "font-['PixeloidMono']",
    titleFont: "font-['BulletSmallcaps']",
  },
};

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [themeChoice, setThemeChoice] = useState("Cyber Dark");
  const theme = themes[themeChoice];

  // Apply body-level theme styles on mount/update
  useEffect(() => {
    document.body.className = ""; // Reset any tailwind classes
    document.body.classList.add(
      theme.backgroundColor.replace("bg-", ""),
      theme.textColor.replace("text-", ""),
      theme.fontFamily.replace("font-", "")
    );
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ themeChoice, setThemeChoice, theme }}>
      {children}
    </ThemeContext.Provider>
  );
};
