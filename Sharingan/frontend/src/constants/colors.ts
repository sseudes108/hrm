// export const COLORS = {
//   anbuRed: "#e41e1e",
//   anbuRedGlow: "rgba(241, 14, 14, 0.27)",
//   glassBase: "rgba(16, 22, 36, 0.1)",
//   glassGray: "rgba(40, 47, 60, 0.1)",
//   whiteGlow: "rgba(255, 255, 255, 0.15)",
//   borderWhite: "rgba(255, 255, 255, 0.05)",
// } as const;

// export const THEMES = {
//   NEGADA: {
//     primary: "#1e74e4",
//     glow: "rgba(14, 105, 241, 0.27)",
//     label: "SISTEMA SHARINGAN: NEGADAS",
//   },
//   FRAUDE: {
//     primary: "#9b0707",
//     glow: "rgba(241, 14, 14, 0.27)",
//     label: "SISTEMA SHARINGAN: FRAUDES DETECTADAS",
//   },
//   APROVADA: {
//     primary: "#00b31e",
//     glow: "rgba(0, 255, 136, 0.27)",
//     label: "SISTEMA SHARINGAN: FLUXO LIMPO",
//   },
//   PENDENTE: {
//     primary: "#b89300",
//     glow: "rgba(201, 161, 0, 0.27)",
//     label: "SISTEMA SHARINGAN: EM ANÁLISE",
//   },
//   TODOS: {
//     primary: "#e2e8f0",
//     glow: "rgba(226, 232, 240, 0.2)",
//     label: "SISTEMA SHARINGAN: TODOS OS EVENTOS",
//   },
// } as const;

// export type ThemeMode = keyof typeof THEMES;
// export type Theme = (typeof THEMES)[ThemeMode];

export const COLORS = {
  anbuRed: "#ce1414", // Vermelho mais suave (coral/carmesim) em vez de vermelho puro
  anbuRedGlow: "rgba(216, 92, 92, 0.15)", // Opacidade reduzida para diminuir a poluição visual
  glassBase: "rgba(15, 23, 42, 0.4)", // Base ligeiramente mais densa para melhorar o contraste do texto
  glassGray: "rgba(30, 41, 59, 0.4)",
  whiteGlow: "rgba(255, 255, 255, 0.08)", // Brilho branco reduzido para não ofuscar
  borderWhite: "rgba(255, 255, 255, 0.08)", // Bordas mais elegantes e integradas
} as const;

export const THEMES = {
  NEGADA: {
    primary: "#5c93e6", // Azul aço/suave em vez de azul caneta
    glow: "rgba(92, 147, 230, 0.15)",
    label: "SISTEMA SHARINGAN: NEGADAS",
  },
  FRAUDE: {
    primary: "#ce1414", // Carmesim/Rosa escuro, alerta sem gritar
    glow: "rgba(216, 76, 99, 0.15)",
    label: "SISTEMA SHARINGAN: FRAUDES DETECTADAS",
  },
  APROVADA: {
    primary: "#4ade80", // Verde menta/esmeralda, relaxante para os olhos
    glow: "rgba(74, 222, 128, 0.15)",
    label: "SISTEMA SHARINGAN: FLUXO LIMPO",
  },
  PENDENTE: {
    primary: "#d4a742", // Dourado suave em vez de amarelo mostarda fechado
    glow: "rgba(212, 167, 66, 0.15)",
    label: "SISTEMA SHARINGAN: EM ANÁLISE",
  },
  TODOS: {
    primary: "#94a3b8", // Cinza-azulado (slate), excelente para leitura neutra
    glow: "rgba(148, 163, 184, 0.15)",
    label: "SISTEMA SHARINGAN: TODOS OS EVENTOS",
  },
} as const;

export type ThemeMode = keyof typeof THEMES;
export type Theme = (typeof THEMES)[ThemeMode];