import { ResponsiveLine } from '@nivo/line';
import { Box, Typography } from '@mui/material';
import type { SlaDataPoint } from '../../../types/sla';

interface NivoLineChartProps {
  data?: SlaDataPoint[];
  indexBy?: string;
  valueKey?: string;
  title?: string;
  subtitle?: string;
  total?: number;
  totalLabel?: string;
  refLineH?: number;
  refLineHLabel?: string;
  refLineV?: string;
  refLineVLabel?: string;
  isLoading?: boolean;
  unit?: string;
}

export default function NivoLineChart({
  data = [],
  indexBy = 'dia',
  valueKey = 'sla',
  title = 'SLA Diário',
  subtitle = '',
  total = 0,
  totalLabel = 'média no período',
  refLineH = 80,
  refLineHLabel = 'Meta',
  refLineV = '',
  refLineVLabel = 'Hoje',
  isLoading = false,
  unit = '%',
}: NivoLineChartProps) {
  if (isLoading) return (
    <Box sx={{
      height: 400, borderRadius: '16px',
      background: 'rgba(255,255,255,0.03)',
      border: '1px solid rgba(255,255,255,0.07)',
      opacity: 0.4,
    }} />
  );

  // formato que o nivo/line espera
  const nivoData = [
    {
      id: valueKey,
      data: data.map(d => ({
        x: d[indexBy as keyof SlaDataPoint],
        y: d[valueKey as keyof SlaDataPoint],
      })),
    },
  ];

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
            {total}{unit}
            <span style={{ fontSize: '1rem', fontWeight: 400, color: 'rgba(255,255,255,0.35)' }}> {totalLabel}</span>
          </Typography>
        </Box>
        <Box sx={{ textAlign: 'right' }}>
          <Typography sx={{ fontSize: '0.65rem', letterSpacing: '0.1em', color: 'rgba(255,255,255,0.25)', textTransform: 'uppercase' }}>
            Meta
          </Typography>
          <Typography sx={{ fontSize: '1.1rem', fontWeight: 600, color: total >= refLineH ? '#5eead4' : '#f87171' }}>
            {refLineH}{unit}
          </Typography>
        </Box>
      </Box>

      {/* Chart */}
      <Box sx={{ height: 280 }}>
        <ResponsiveLine
          data={nivoData}
          margin={{ top: 20, right: 20, bottom: 40, left: 40 }}
          xScale={{ type: 'point' }}
          yScale={{ type: 'linear', min: 0, max: 100 }}
          curve="monotoneX"
          colors={['#5eead4']}
          lineWidth={2}
          pointSize={0}
          enableArea
          areaOpacity={0.06}
          axisBottom={{
            tickSize: 0,
            tickPadding: 10,
          }}
          axisLeft={{
            tickSize: 0,
            tickPadding: 10,
            tickValues: [0, 25, 50, 75, 100],
            format: v => `${v}%`,
          }}
          gridYValues={[0, 25, 50, 75, 100]}
          enableGridX={false}
          useMesh
          tooltip={({ point }) => (
            <Box sx={{
              background: 'rgba(10,10,15,0.92)',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: '10px',
              padding: '10px 16px',
              backdropFilter: 'blur(12px)',
            }}>
              <Typography sx={{ fontSize: '0.65rem', letterSpacing: '0.1em', color: 'rgba(255,255,255,0.35)', mb: 0.5 }}>
                Dia {point.data.x}
              </Typography>
              <Typography sx={{ fontSize: '1rem', fontWeight: 700, color: '#5eead4' }}>
                {point.data.y}{unit}
              </Typography>
            </Box>
          )}
          theme={{
            grid: { line: { stroke: 'rgba(255,255,255,0.04)', strokeWidth: 1 } },
            axis: { ticks: { text: { fill: 'rgba(255,255,255,0.25)', fontSize: 11 } } },
            tooltip: { container: { background: 'transparent', boxShadow: 'none', padding: 0 } },
          }}
          markers={[
            {
              axis: 'y',
              value: refLineH,
              lineStyle: { stroke: 'rgba(255,100,100,0.5)', strokeWidth: 1.5, strokeDasharray: '4 4' },
              legend: refLineHLabel,
              legendPosition: 'top-right',
              legendOffsetY: -8,
              textStyle: { fill: 'rgba(255,100,100,0.5)', fontSize: 11 },
            },
            ...(refLineV ? [{
              axis: 'x' as const,
              value: refLineV,
              lineStyle: { stroke: 'rgba(255,255,255,0.15)', strokeWidth: 1.5, strokeDasharray: '4 4' },
              legend: refLineVLabel,
              legendPosition: 'top-right' as const,
              legendOffsetX: 8,
              textStyle: { fill: 'rgba(255,255,255,0.3)', fontSize: 11 },
            }] : []),
          ]}
        />
      </Box>

      {/* Legend */}
      <Box sx={{ display: 'flex', gap: 3, mt: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ width: 16, height: 2, background: '#5eead4', borderRadius: 1 }} />
          <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.3)' }}>SLA</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ width: 16, height: 2, background: 'rgba(255,100,100,0.5)', borderRadius: 1, borderStyle: 'dashed' }} />
          <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.3)' }}>{refLineHLabel}</Typography>
        </Box>
      </Box>
    </Box>
  );
}