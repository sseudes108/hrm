import { Title, Text } from "@tremor/react";
import { COLORS, THEMES } from "../../constants/colors";

interface HeaderProps {
  theme: typeof THEMES.FRAUDE;
}

export function Header({ theme }: HeaderProps) {
  return (
    <header 
      className="flex items-center justify-between px-10 py-4 relative z-50 backdrop-blur-[1px] !bg-transparent"
      style={{ 
        // 1. O FADE: Replicando a lógica da Sidebar (mesmas cores e intensidades)
        // O radial-gradient cria o ponto de luz no canto inferior esquerdo (bottom left)
        // O linear-gradient faz a transição do vidro escuro
        backgroundImage: `
          linear-gradient(15deg, rgba(16, 22, 36, 0.1) 0%, rgba(16, 22, 36, 0.05) 50%, ${COLORS.glassBase} 100%),
          radial-gradient(circle at bottom left, ${COLORS.whiteGlow} 0%, rgba(255, 255, 255, 0) 40%)
        `,

        // 2. A BORDA: Usando sua variável centralizada
        // borderBottom: `1px solid ${COLORS.borderWhite}`,
        backgroundColor: "rgba(10, 15, 26, 0.00)", 
      }}
    >
      {/* LADO ESQUERDO: LOGO E TÍTULO */}
      <div className="flex items-center gap-6">
        
        {/* LOGO: Sharingan Orb */}
        <div 
          className="relative flex items-center justify-center w-8 h-8 rounded-full border-2 transition-all duration-700"
          style={{ 
            borderColor: theme.primary,
            boxShadow: `0 0 15px ${theme.primary}60` 
          }}
        >
          <div 
            className="w-3 h-3 rounded-full animate-pulse"
            style={{ backgroundColor: theme.primary }}
          />
          <div className="absolute inset-[-3px] border border-white/5 rounded-full" />
        </div>
        
        <div>
          <Title className="text-white text-2xl font-black tracking-[0.2em] uppercase leading-none">
            SHARINGAN
          </Title>
          <div className="flex items-center gap-2 mt-0.5">
            <div className="h-[1px] w-3 bg-rose-900/50" />
            <Text className="text-[8px] text-slate-500 font-black tracking-[0.3em] uppercase">
              Fraud Monitoring System
            </Text>
          </div>
        </div>

        {/* SÂNSCRITO: Aumentamos a opacidade de 40% para 70% e o tamanho sutilmente */}
        <div className="ml-14 hidden md:flex gap-8 text-slate-300 font-serif text-base tracking-widest opacity-70 italic">
          <div className="flex flex-col items-center">
            <span className="text-xl">सत्य</span>
            <span className="text-[7px] uppercase tracking-[0.2em] text-slate-500">Satya</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-xl">ज्ञान</span>
            <span className="text-[7px] uppercase tracking-[0.2em] text-slate-500">Jnana</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-xl">दृष्टि</span>
            <span className="text-[7px] uppercase tracking-[0.2em] text-slate-500">Drishti</span>
          </div>
        </div>
      </div>

      {/* LADO DIREITO */}
      <div className="flex items-center gap-4">
         <div className="text-[9px] text-slate-500 font-mono tracking-widest uppercase">
            System Protocol: <span style={{ color: theme.primary }} className="font-bold">Veda-01</span>
         </div>
      </div>
    </header>
  );
}