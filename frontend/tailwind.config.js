/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        yulda: {
          yellow: "#FFD600",
          gold: "#F2B500",
          black: "#121212",
          charcoal: "#1E1E1E",
          gray: {
            50: "#FAFAFA",
            100: "#F4F4F5",
            200: "#E4E4E7",
            300: "#D4D4D8",
            400: "#A1A1AA",
            500: "#71717A",
            600: "#52525B",
            700: "#3F3F46",
            800: "#27272A",
            900: "#18181B",
          },
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "Segoe UI", "Roboto", "sans-serif"],
      },
      borderRadius: {
        xl: "1rem",
        "2xl": "1.25rem",
        "3xl": "1.75rem",
      },
      boxShadow: {
        card: "0 1px 2px rgba(18, 18, 18, 0.04), 0 4px 16px rgba(18, 18, 18, 0.06)",
        "card-hover": "0 2px 4px rgba(18, 18, 18, 0.06), 0 8px 24px rgba(18, 18, 18, 0.10)",
      },
    },
  },
  plugins: [],
};
