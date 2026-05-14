import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { Box, Typography } from '@mui/material';

const rawData = [
  { date: '01/03', sla: 42, meta: 80},
  { date: '02/03', sla: 51, meta: 80},
  { date: '03/03', sla: 38, meta: 80},
  { date: '04/03', sla: 64, meta: 80},
  { date: '05/03', sla: 72, meta: 80},
  { date: '06/03', sla: 59, meta: 80},
  { date: '07/03', sla: 45, meta: 80},
  { date: '08/03', sla: 81, meta: 80},
  { date: '09/03', sla: 67, meta: 80},
  { date: '10/03', sla: 53, meta: 80},
  { date: '11/03', sla: 90, meta: 80},
  { date: '12/03', sla: 78, meta: 80},
  { date: '13/03', sla: 61, meta: 80},
  { date: '14/03', sla: 49, meta: 80},
  { date: '15/03', sla: 55, meta: 80},
  { date: '16/03', sla: 73, meta: 80},
  { date: '17/03', sla: 86, meta: 80},
  { date: '18/03', sla: 62, meta: 80},
  { date: '19/03', sla: 50, meta: 80},
  { date: '20/03', sla: 44, meta: 80},
  { date: '21/03', sla: 68, meta: 80},
  { date: '22/03', sla: 75, meta: 80},
];

function calcEMA(values: number[], period: number): number[] {
  const k = 2 / (period + 1);
  const ema: number[] = [];
  values.forEach((val, i) => {
    if (i === 0) {
      ema.push(val);
    } else {
      ema.push(val * k + ema[i - 1] * (1 - k));
    }
  });
  return ema;
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <Box
        sx={{
          background: 'rgba(10,10,15,0.85)',
          border: '1px solid rgba(255,255,255,0.08)',
          borderRadius: '10px',
          padding: '10px 16px',
          backdropFilter: 'blur(10px)',
        }}
      >
        <Typography sx={{ fontSize: '0.65rem', letterSpacing: '0.1em', color: 'rgba(255,255,255,0.4)', mb: 0.5 }}>
          {label}
        </Typography>
        <Typography sx={{ fontSize: '1rem', fontWeight: 600, color: '#5eead4' }}>
          {payload[0].value} %
        </Typography>
      </Box>
    );
  }
  return null;
};

export default function SlaChart() {
  const emaValues = calcEMA(rawData.map(d => d.sla), 30); // período 7 dias
  const data = rawData.map((d, i) => ({
    ...d,
    ema: Math.round(emaValues[i]),
  }));

  return (
    <Box
      sx={{
        padding: '28px 32px',
        borderRadius: '16px',
        background: 'rgba(255,255,255,0.03)',
        border: '1px solid rgba(255,255,255,0.07)',
        backdropFilter: 'blur(12px)',
        boxShadow: '0 4px 40px rgba(0,0,0,0.25)',
      }}
    >
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography
          sx={{
            fontSize: '0.65rem',
            letterSpacing: '0.15em',
            color: 'rgba(255,255,255,0.35)',
            fontWeight: 600,
            textTransform: 'uppercase',
            mb: 0.5,
          }}
        >
          SLA
        </Typography>
        <Typography
          sx={{
            fontSize: '1.6rem',
            fontWeight: 700,
            color: 'rgba(255,255,255,0.9)',
            letterSpacing: '-0.02em',
          }}
        >
          38 <span style={{ fontSize: '1rem', fontWeight: 400, color: 'rgba(255,255,255,0.35)' }}>% / média</span>
        </Typography>
      </Box>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={260}>
        <AreaChart data={data} margin={{ top: 10, right: 4, left: -20, bottom: 0 }}>
          <defs>

            <linearGradient id="tmaGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#5eead4" stopOpacity={0.2} />
              <stop offset="95%" stopColor="#5eead4" stopOpacity={0} />
            </linearGradient>

            <linearGradient id="metaGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#60a5fa" stopOpacity={0.7} />
              <stop offset="95%" stopColor="#60a5fa" stopOpacity={0} />
            </linearGradient>

            <linearGradient id="emaGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#facc15" stopOpacity={0.08} />
              <stop offset="95%" stopColor="#facc15" stopOpacity={0} />
            </linearGradient>

          </defs>

          <CartesianGrid
            strokeDasharray="3 3"
            stroke="rgba(255,255,255,0.04)"
            vertical={false}
          />

          <XAxis
            dataKey="date"
            tick={{ fill: 'rgba(255,255,255,0.25)', fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />

          <YAxis
            tick={{ fill: 'rgba(255,255,255,0.25)', fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(v) => `${v}m`}
          />

          <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'rgba(255,255,255,0.08)', strokeWidth: 1 }} />

          <Area
            type="monotone"
            dataKey="sla"
            stroke="#5eead4"
            strokeWidth={2}
            fill="url(#tmaGradient)"
            dot={false}
            activeDot={{ r: 4, fill: '#5eead4', strokeWidth: 0 }}
          />

          <Area
            type="monotone"
            dataKey="meta"
            stroke="#60a5fa"
            strokeWidth={1.5}
            strokeDasharray="4 4"
            fill="url(#metaGradient)"
            dot={false}
            activeDot={false}
          />

          <Area
            type="monotone"
            dataKey="ema"
            stroke="#facc15"
            strokeWidth={1.5}
            fill="url(#emaGradient)"
            dot={false}
            activeDot={false}
          />

        </AreaChart>
      </ResponsiveContainer>
    </Box>
  );
}