// src/components/DailyVolumeChart.tsx
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { Box, Typography } from '@mui/material';

const hoje = 13;
const mes = 'Março';

const rawValues = [
  45, 62, 38, 71, 55, 80, 43, 67, 90, 52,
  48, 76, 61, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
];

const data = Array.from({ length: 31 }, (_, i) => {
  const dia = i + 1;
  const isFuturo = dia > hoje;
  return {
    dia: `${dia}`,
    valor: !isFuturo ? rawValues[i] : null,
    placeholder: isFuturo ? 50 : null,
  };
});

const total = rawValues.slice(0, hoje).reduce((a, b) => a + b, 0);
const media = Math.round(total / hoje);

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  const isFuturo = payload[0]?.dataKey === 'placeholder';

  return (
    <Box sx={{
      background: 'rgba(10,10,15,0.92)',
      border: '1px solid rgba(255,255,255,0.08)',
      borderRadius: '10px',
      padding: '10px 16px',
      backdropFilter: 'blur(12px)',
    }}>
      <Typography sx={{ fontSize: '0.65rem', letterSpacing: '0.1em', color: 'rgba(255,255,255,0.35)', mb: 0.5 }}>
        Dia {label} — {mes}
      </Typography>
      {isFuturo ? (
        <Typography sx={{ fontSize: '0.85rem', color: 'rgba(255,255,255,0.25)', fontStyle: 'italic' }}>
          sem dados
        </Typography>
      ) : (
        <Typography sx={{ fontSize: '1rem', fontWeight: 700, color: '#5eead4' }}>
          {payload[0].value} atendimentos
        </Typography>
      )}
    </Box>
  );
};

export default function DailyVolumeChart() {
  return (
    <Box sx={{
      padding: '28px 32px',
      borderRadius: '16px',
      background: 'rgba(255,255,255,0.03)',
      border: '1px solid rgba(255,255,255,0.07)',
      backdropFilter: 'blur(12px)',
      boxShadow: '0 4px 40px rgba(0,0,0,0.25)',
    }}>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Box>
          <Typography sx={{
            fontSize: '0.65rem', letterSpacing: '0.15em',
            color: 'rgba(255,255,255,0.35)', fontWeight: 600,
            textTransform: 'uppercase', mb: 0.5,
          }}>
            Volume Diário — {mes}
          </Typography>
          <Typography sx={{
            fontSize: '1.6rem', fontWeight: 700,
            color: 'rgba(255,255,255,0.9)', letterSpacing: '-0.02em',
          }}>
            {total.toLocaleString('pt-BR')}
            <span style={{ fontSize: '1rem', fontWeight: 400, color: 'rgba(255,255,255,0.35)' }}> atendimentos</span>
          </Typography>
        </Box>
        <Box sx={{ textAlign: 'right' }}>
          <Typography sx={{ fontSize: '0.65rem', letterSpacing: '0.1em', color: 'rgba(255,255,255,0.25)', textTransform: 'uppercase' }}>
            Média/dia
          </Typography>
          <Typography sx={{ fontSize: '1.1rem', fontWeight: 600, color: 'rgba(255,255,255,0.5)' }}>
            {media}
          </Typography>
        </Box>
      </Box>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} margin={{ top: 8, right: 4, left: -28, bottom: 0 }} barSize={10}>
          <XAxis
            dataKey="dia"
            tick={{ fill: 'rgba(255,255,255,0.2)', fontSize: 10 }}
            axisLine={false}
            tickLine={false}
            interval={1}
          />
          <YAxis
            tick={{ fill: 'rgba(255,255,255,0.2)', fontSize: 10 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            content={<CustomTooltip />}
            cursor={{ fill: 'rgba(255,255,255,0.03)' }}
          />

          <ReferenceLine
            x={`${hoje}`}
            stroke="rgba(255,255,255,0.1)"
            strokeDasharray="4 4"
          />

            <ReferenceLine
            y={80}
            stroke="rgba(255,100,100,0.5)"
            strokeWidth={3}
            strokeDasharray="4 4"
            label={{
                value: 'Forecast: 80%',
                fill: 'rgba(255,100,100,0.5)',
                fontSize: 11,
                position: 'insideBottomRight',
            }}
            />
          <Bar dataKey="valor" fill="#5eead4" radius={[4, 4, 0, 0]} />
          <Bar dataKey="placeholder" fill="rgba(255,255,255,0.05)" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>

      {/* Legend */}
      <Box sx={{ display: 'flex', gap: 3, mt: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ width: 8, height: 8, borderRadius: '2px', background: '#5eead4' }} />
          <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.3)' }}>Realizado</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ width: 8, height: 8, borderRadius: '2px', background: 'rgba(255,255,255,0.1)' }} />
          <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.3)' }}>Projetado</Typography>
        </Box>
      </Box>
    </Box>
  );
} 