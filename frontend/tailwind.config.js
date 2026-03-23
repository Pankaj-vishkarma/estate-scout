/** @type {import('tailwindcss').Config} */
const config = {
  content: [
    "./app/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      boxShadow: {
        glow: "0 0 24px rgba(59, 130, 246, 0.35)",
      },
      backgroundImage: {
        "hero-gradient":
          "radial-gradient(1000px 500px at 20% 0%, rgba(56, 189, 248, 0.35) 0%, rgba(56, 189, 248, 0) 60%), radial-gradient(900px 400px at 80% 10%, rgba(99, 102, 241, 0.35) 0%, rgba(99, 102, 241, 0) 60%), linear-gradient(180deg, rgba(2,6,23,1) 0%, rgba(2,6,23,0.9) 50%, rgba(2,6,23,1) 100%)",
      },
    },
  },
  plugins: [],
};

export default config;

