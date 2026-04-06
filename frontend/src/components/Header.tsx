import { Title, Text } from "@tremor/react";
import { COLORS, THEMES } from "../constants/colors"; // Mantendo a centralização de cores

interface HeaderProps {
  theme: typeof THEMES.FRAUDE; // ou use a tipagem que preferir
}
export function Header({ theme }: HeaderProps) {
  return (
    <header 
      className="flex items-center justify-between px-10 py-3 border-b sticky top-0 z-50 backdrop-blur-xl"
      style={{ 
        backgroundColor: "rgba(10, 15, 26, 0.4)", // Vidro sutil
        borderBottomColor: COLORS.borderWhite 
      }}
    >
      {/* LADO ESQUERDO: LOGO E TÍTULO */}
      <div className="flex items-center gap-6">
        
        {/* LOGO: O Orbe Central do Sharingan */}
        <div 
          className="relative flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all duration-700"
          style={{ 
            borderColor: theme.primary,
            boxShadow: `0 0 15px ${theme.primary}80` // Brilho de 50% de opacidade
          }}
        >
          <div 
            className="w-4 h-4 rounded-full animate-pulse"
            style={{ backgroundColor: theme.primary }}
          ></div>
          
          {/* Detalhe estético: Anel de luz externo */}
          <div className="absolute inset-[-4px] border border-white/5 rounded-full"></div>
        </div>
        
        <div>
          <Title className="text-white text-3xl font-black tracking-[0.2em] uppercase leading-none">
            SHARINGAN
          </Title>
          <div className="flex items-center gap-2 mt-1">
            <div className="h-[1px] w-4 bg-rose-900/50"></div>
            <Text className="text-[10px] text-slate-500 font-black tracking-[0.3em] uppercase">
              Fraud Monitoring System
            </Text>
          </div>
        </div>

        {/* PALAVRAS EM SÂNSCRITO (Substituindo os Kanjis) */}
        <div className="ml-14 hidden md:flex gap-8 text-slate-500 font-serif text-base tracking-widest opacity-40 italic">
          <div className="flex flex-col items-center">
            <span className="text-xl">सत्य</span>
            <span className="text-[8px] uppercase tracking-tighter">Satya</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-xl">ज्ञान</span>
            <span className="text-[8px] uppercase tracking-tighter">Jnana</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-xl">दृष्टि</span>
            <span className="text-[8px] uppercase tracking-tighter">Drishti</span>
          </div>
        </div>
        
      </div>

      {/* LADO DIREITO (Opcional: Pode colocar um relógio ou user status aqui) */}
      <div className="flex items-center gap-4">
         <div className="text-[10px] text-slate-500 font-mono tracking-widest uppercase">
            System Protocol: <span style={{ color: theme.primary }}>Veda-01</span>
         </div>
      </div>
    </header>
  );
}