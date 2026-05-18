// src/components/NivoBarChart.tsx
import { ResponsiveBar } from '@nivo/bar';
import { Box, Typography } from '@mui/material';
import type { DataPoint } from '../../../types/volumePropostas';

interface NivoBarChartProps {
  data?: DataPoint[];
  indexBy?: string;
  valueKey?: string;
  title?: string;
  subtitle?: string;
  total?: number;
  media?: number;
  refLineH?: number;
  refLineHLabel?: string;
  refLineV?: string;
  refLineVLabel?: string;
  isLoading?: boolean;
}

export default function NivoBarChart({
  data = [],
  total = 0,
  media = 0,
  isLoading = false,
  indexBy = 'xAxis',
  valueKey = 'yAxis',
  title = 'Volume Diário',
  subtitle = 'Março 2025',
  refLineH = 80,
  refLineHLabel = 'Forecast',
  refLineV = '13',
  refLineVLabel = 'Hoje',
}: NivoBarChartProps) {

  if (isLoading) return (
    <Box sx={{opacity: 0.4, height: 400, borderRadius: '16px', background: 'rgba(255,255,255,0.03)' }} />
  );

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
            {title} — {subtitle}
          </Typography>
          <Typography sx={{
            fontSize: '1.6rem', fontWeight: 700,
            color: 'rgba(255,255,255,0.9)', letterSpacing: '-0.02em',
          }}>
            {total.toLocaleString('pt-BR')}
            <span style={{ fontSize: '1rem', fontWeight: 400, color: 'rgba(255,255,255,0.35)' }}> ocorrências</span>
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
      <Box sx={{ height: 280 }}>
        <ResponsiveBar
          data={data}
          keys={[valueKey]}
          indexBy={indexBy}
          margin={{ top: 20, right: 20, bottom: 40, left: 40 }}
          padding={0.35}
          valueScale={{ type: 'linear' }}
          colors="#5eead4"
          borderRadius={4}
          axisBottom={{
            tickSize: 0,
            tickPadding: 10,
            tickRotation: 0,
            tickValues: data.map(d => d[indexBy as keyof DataPoint]),
          }}
          axisLeft={{
            tickSize: 0,
            tickPadding: 10,
          }}
          gridYValues={5}
          enableLabel={false}
          tooltip={({ indexValue, value }) => (
            <Box sx={{
              background: 'rgba(10,10,15,0.92)',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: '10px',
              padding: '10px 16px',
              backdropFilter: 'blur(12px)',
            }}>
              <Typography sx={{ fontSize: '0.65rem', letterSpacing: '0.1em', color: 'rgba(255,255,255,0.35)', mb: 0.5 }}>
                Dia {indexValue}
              </Typography>
              <Typography sx={{ fontSize: '1rem', fontWeight: 700, color: '#5eead4' }}>
                {value} ocorrências
              </Typography>
            </Box>
          )}
          theme={{
            grid: { line: { stroke: 'rgba(255,255,255,0.04)', strokeWidth: 1 } },
            axis: {
              ticks: { text: { fill: 'rgba(255,255,255,0.25)', fontSize: 11 } },
            },
            tooltip: { container: { background: 'transparent', boxShadow: 'none', padding: 0 } },
          }}
          markers={[
            {
              axis: 'y',
              value: refLineH,
              lineStyle: { stroke: 'rgba(255,100,100,0.6)', strokeWidth: 1.5, strokeDasharray: '4 4' },
              legend: refLineHLabel,
              legendPosition: 'top-right',
              legendOffsetY: -8,
              textStyle: { fill: 'rgba(255,100,100,0.6)', fontSize: 11 },
            },
            {
              axis: 'x',
              value: refLineV,
              lineStyle: { stroke: 'rgba(255,255,255,0.15)', strokeWidth: 1.5, strokeDasharray: '4 4' },
              legend: refLineVLabel,
              legendPosition: 'top-right',
              legendOffsetX: 8,
              textStyle: { fill: 'rgba(255,255,255,0.3)', fontSize: 11 },
            },
          ]}
        />
      </Box>

      {/* Legend */}
      <Box sx={{ display: 'flex', gap: 3, mt: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ width: 16, height: 2, background: 'rgba(255,100,100,0.6)', borderRadius: 1 }} />
          <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.3)' }}>{refLineHLabel}</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ width: 16, height: 2, background: 'rgba(255,255,255,0.2)', borderRadius: 1 }} />
          <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.3)' }}>{refLineVLabel}</Typography>
        </Box>
      </Box>
    </Box>
  );
}