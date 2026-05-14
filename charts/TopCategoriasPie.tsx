// src/components/TopCategoriesPieChart.tsx
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import { Box, Typography } from '@mui/material';

const rawData = [
  { name: 'Suporte Técnico', value: 340 },
  { name: 'Financeiro', value: 280 },
  { name: 'Comercial', value: 210 },
  { name: 'Logística', value: 195 },
  { name: 'RH', value: 160 },
  { name: 'Jurídico', value: 98 },
  { name: 'Marketing', value: 87 },
  { name: 'TI Interna', value: 74 },
  { name: 'Facilities', value: 61 },
  { name: 'Compliance', value: 45 },
  { name: 'Importação', value: 38 },
  { name: 'Exportação', value: 29 },
];

const sorted = [...rawData].sort((a, b) => b.value - a.value);
const top5 = sorted.slice(0, 5);
const outrosItems = sorted.slice(5);
const outrosTotal = outrosItems.reduce((acc, d) => acc + d.value, 0);
const total = rawData.reduce((acc, d) => acc + d.value, 0);

interface ChartEntry {
  name: string;
  value: number;
  isOthers?: boolean;
}

const data: ChartEntry[] = [
  ...top5,
  { name: 'Outros', value: outrosTotal, isOthers: true },
];

const COLORS = [
  '#5eead4',
  '#5eead4cc',
  '#5eead4aa',
  '#5eead488',
  '#5eead466',
  'rgba(148,163,184,0.45)',
];

const MiniChart = ({ items }: { items: typeof outrosItems }) => (
  <Box sx={{ width: 200, pt: 1 }}>
    <Typography sx={{ fontSize: '0.6rem', letterSpacing: '0.12em', color: 'rgba(255,255,255,0.35)', mb: 1, textTransform: 'uppercase' }}>
      Composição
    </Typography>
    {items.map((item) => (
      <Box key={item.name} sx={{ mb: 0.8 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.3 }}>
          <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.55)' }}>{item.name}</Typography>
          <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.4)' }}>{item.value}</Typography>
        </Box>
        <Box sx={{ height: '3px', borderRadius: '2px', background: 'rgba(255,255,255,0.06)', overflow: 'hidden' }}>
          <Box sx={{
            height: '100%',
            width: `${(item.value / outrosItems[0].value) * 100}%`,
            background: 'rgba(148,163,184,0.5)',
            borderRadius: '2px',
          }} />
        </Box>
      </Box>
    ))}
  </Box>
);

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  const entry: ChartEntry = payload[0].payload;
  const pct = ((entry.value / total) * 100).toFixed(1);

  return (
    <Box sx={{
      background: 'rgba(10,10,15,0.92)',
      border: '1px solid rgba(255,255,255,0.08)',
      borderRadius: '12px',
      padding: '14px 18px',
      backdropFilter: 'blur(12px)',
      boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
    }}>
      <Typography sx={{ fontSize: '0.65rem', letterSpacing: '0.1em', color: 'rgba(255,255,255,0.35)', mb: 0.5 }}>
        {entry.name}
      </Typography>
      <Typography sx={{ fontSize: '1.1rem', fontWeight: 700, color: entry.isOthers ? '#94a3b8' : '#5eead4', mb: entry.isOthers ? 1.5 : 0 }}>
        {entry.value} · {pct}%
      </Typography>
      {entry.isOthers && <MiniChart items={outrosItems} />}
    </Box>
  );
};

export default function TopCategoriesPieChart() {
  return (
    <Box sx={{
      padding: '28px 32px',
      borderRadius: '16px',
      background: 'rgba(255,255,255,0.03)',
      border: '1px solid rgba(255,255,255,0.07)',
      backdropFilter: 'blur(12px)',
      boxShadow: '0 4px 40px rgba(0,0,0,0.25)',
    }}>
      <Box sx={{ mb: 4 }}>
        <Typography sx={{
          fontSize: '0.65rem', letterSpacing: '0.15em',
          color: 'rgba(255,255,255,0.35)', fontWeight: 600,
          textTransform: 'uppercase', mb: 0.5,
        }}>
          Atendimentos por Categoria
        </Typography>
        <Typography sx={{
          fontSize: '1.6rem', fontWeight: 700,
          color: 'rgba(255,255,255,0.9)', letterSpacing: '-0.02em',
        }}>
          {total.toLocaleString('pt-BR')}
          <span style={{ fontSize: '1rem', fontWeight: 400, color: 'rgba(255,255,255,0.35)' }}> atendimentos</span>
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', alignItems: 'center', gap: 4 }}>
        {/* Pie */}
        <ResponsiveContainer width={220} height={220}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={100}
              paddingAngle={2}
              dataKey="value"
            >
              {data.map((_, index) => (
                <Cell key={index} fill={COLORS[index]} stroke="transparent" />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>

        {/* Legenda */}
        <Box sx={{ flex: 1 }}>
          {data.map((entry, index) => (
            <Box key={entry.name} sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1.2 }}>
              <Box sx={{ width: 8, height: 8, borderRadius: '2px', background: COLORS[index], flexShrink: 0 }} />
              <Typography sx={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.5)', flex: 1 }}>
                {entry.name}
              </Typography>
                <Typography sx={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.3)' }}>
                  {entry.value} - {((entry.value / total) * 100).toFixed(1)}%
                </Typography>
            </Box>
          ))}
        </Box>
      </Box>
    </Box>
  );
}