// src/components/TopCategoriesChart.tsx
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer, Cell,
} from 'recharts';
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

const data = [
  ...top5,
  { name: 'Outros', value: outrosTotal, isOthers: true },
];

const MiniChart = ({ items }: { items: typeof outrosItems }) => (
  <Box sx={{ width: 260, pt: 1 }}>
    <Typography sx={{ fontSize: '0.6rem', letterSpacing: '0.12em', color: 'rgba(255,255,255,0.35)', mb: 1, textTransform: 'uppercase' }}>
      Composição
    </Typography>
    {items.map((item) => (
      <Box key={item.name} sx={{ mb: 0.8 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.3 }}>
          <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.55)' }}>
            {item.name}
          </Typography>
          <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.4)' }}>
            {item.value}
          </Typography>
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

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  const isOthers = payload[0]?.payload?.isOthers;

  return (
    <Box sx={{
      background: 'rgba(10,10,15,0.92)',
      border: '1px solid rgba(255,255,255,0.08)',
      borderRadius: '12px',
      padding: '14px 18px',
      backdropFilter: 'blur(12px)',
      boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
      zIndex:100
    }}>
      <Typography sx={{ fontSize: '0.65rem', letterSpacing: '0.1em', color: 'rgba(255,255,255,0.35)', mb: 0.5 }}>
        {label}
      </Typography>
      <Typography sx={{ fontSize: '1.1rem', fontWeight: 700, color: isOthers ? '#94a3b8' : '#5eead4', mb: isOthers ? 1.5 : 0 }}>
        {payload[0].value} atendimentos
      </Typography>
      {isOthers && <MiniChart items={outrosItems} />}
    </Box>
  );
};

const CustomLabel = ({ x, y, width, height, value }: any) => {
  const total = data.reduce((acc, d) => acc + d.value, 0);
  const pct = ((value / total) * 100).toFixed(1);

  return (
    <text
      x={x + width + 8}
      y={y + height / 2}
      fill="rgba(255,255,255,0.35)"
      fontSize={11}
      dominantBaseline="middle"
    >
      {value} · {pct}%
    </text>
  );
};

export default function TopCategoriesChart() {
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
          Top 5 <span style={{ fontSize: '1rem', fontWeight: 400, color: 'rgba(255,255,255,0.35)' }}>+ outros {outrosItems.length}</span>
        </Typography>
      </Box>

      <ResponsiveContainer width="100%" height={280}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 0, right: 16, left: 8, bottom: 0 }}
          barSize={10}
        >
          <XAxis type="number" hide />
          <YAxis
            type="category"
            dataKey="name"
            width={120}
            tick={{ fill: 'rgba(255,255,255,0.45)', fontSize: 12 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            content={<CustomTooltip />}
            cursor={{ fill: 'rgba(255,255,255,0.03)' }}
          />
          <Bar dataKey="value" radius={[0, 6, 6, 0]} label={<CustomLabel />}>
            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={entry.isOthers ? 'rgba(148,163,184,0.35)' : '#5eead4'}
                opacity={entry.isOthers ? 1 : 1 - index * 0.12}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
}