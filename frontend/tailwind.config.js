/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./node_modules/@tremor/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Sugestão: Cores para o seu tema de Fraude/Segurança
        brand: {
          primary: "#ff0000", // Vermelho Alerta
          secondary: "#00ff88", // Verde Aprovação
          dark: "#0a0a0a",
        }
      }
    },
  },
  plugins: [],
}