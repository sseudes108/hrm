import { THEMES } from "../../constants/colors";

// O Card agora recebe o 'theme' que vem do Dashboard
interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  theme?: typeof THEMES.FRAUDE;
}

export function GlassCard({ children, className = "", theme }: GlassCardProps) {
  // Se não houver tema (fallback), usa o FRAUDE
  const activeTheme = theme || THEMES.FRAUDE;

  const dynamicGlassStyle = {
    // 1. O SEU GRADIENTE ORIGINAL (Agora com a cor do tema no final)
    backgroundImage: `
      linear-gradient(135deg, rgba(40, 47, 60, 0.1) 0%, rgba(16, 22, 36, 0.05) 50%, rgba(16, 22, 36, 0.1) 100%),
      radial-gradient(circle at top left, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0) 35%),
      radial-gradient(circle at bottom right, ${activeTheme.glow} 0%, rgba(225, 29, 72, 0) 45%)
    `,
    
    // 2. A SUA BORDA (Podemos usar a cor do tema para dar o "match" com o mapa)
    border: `2px solid ${activeTheme.primary}22`, // O '22' no final adiciona transparência à borda
    
    // 3. O SEU BLUR E FUNDO
    backdropFilter: 'blur(1px)',
    backgroundColor: 'rgba(10, 15, 26, 0.01)',
    
    // 4. EXTRA: Um brilho externo sutil para combinar com o "mood" do sistema
    boxShadow: `0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 0 1px 1px ${activeTheme.primary}11`,
    
    transition: "all 0.5s ease-in-out" // Suave na troca de cores
  };

  return (
    <div style={dynamicGlassStyle} className={`rounded-2xl p-6 ${className}`}>
      {children}
    </div>
  );
}