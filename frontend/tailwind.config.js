/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        pixeloid: ["PixeloidMono", "monospace"],
        bullet: ["BulletSmallcaps", "monospace"],
        VGA437: ["Perfect DOS VGA 437 Win", "monospace"],

        // ✅ ADD THESE MAPPINGS BELOW:
        //body: ["PixeloidMono", "monospace"], // <--- maps to font-body
        body: ["Perfect DOS VGA 437 Win", "monospace"],
        header: ["BulletSmallcaps", "monospace"], // <--- maps to font-header
      },
      boxShadow: {
        headerGlow: "0 1px 3px rgba(255,255,255,0.12)",
      },
      dropShadow: {
        textGlow: "0 0 3px rgba(255,255,255,0.2)",
      },
    },
  },
  plugins: [],
};
