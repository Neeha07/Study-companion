/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#6C63FF",
        secondary: "#48BB78",
        dark: "#1A1A2E",
        card: "#16213E",
        surface: "#0F3460",
      },
    },
  },
  plugins: [],
};