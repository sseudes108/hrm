import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  createColumnHelper,
  flexRender,
  type SortingState,
  type ColumnFiltersState,
} from '@tanstack/react-table';
import { useState, useMemo } from 'react';
import { Box, Typography, TextField, IconButton } from '@mui/material';
import { ArrowUpward, ArrowDownward, UnfoldMore, ChevronLeft, ChevronRight } from '@mui/icons-material';
import type { QueueRow, PeriodData, QueueTableResponse } from '../../types/queueTable';

// ── célula rica ──────────────────────────────────────────────────────────────
const Delta = ({ value, unit = '' }: { value: number; unit?: string }) => {
  if (value === 0) return null;
  const positive = value > 0;
  return (
    <Box component="span" sx={{
      display: 'inline-flex',
      alignItems: 'center',
      fontSize: '0.62rem',
      fontWeight: 600,
      color: positive ? '#5eead4' : '#f87171',
      background: positive ? 'rgba(94,234,212,0.08)' : 'rgba(248,113,113,0.08)',
      borderRadius: '4px',
      px: 0.6,
      py: 0.2,
      ml: 0.5,
    }}>
      {positive ? '▲' : '▼'} {Math.abs(value)}{unit}
    </Box>
  );
};

const PeriodCell = ({ data }: { data: PeriodData }) => (
  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.6, py: 0.5 }}>
    <Box sx={{ display: 'flex', alignItems: 'center' }}>
      <Typography sx={{ fontSize: '0.85rem', fontWeight: 700, color: 'rgba(255,255,255,0.85)' }}>
        {data.qty.toLocaleString('pt-BR')}
      </Typography>
      <Delta value={data.qtyDelta} />
    </Box>
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <Typography sx={{ fontSize: '0.68rem', color: 'rgba(255,255,255,0.35)' }}>SLA {data.sla}%</Typography>
        <Delta value={data.slaDelta} unit="%" />
      </Box>
    </Box>
    <Box sx={{ display: 'flex', alignItems: 'center' }}>
      <Typography sx={{ fontSize: '0.68rem', color: 'rgba(255,255,255,0.35)' }}>TMA {data.tma}m</Typography>
      <Delta value={data.tmaDelta} unit="m" />
    </Box>
  </Box>
);

// ── ícone de sort ─────────────────────────────────────────────────────────────
const SortIcon = ({ sorted }: { sorted: false | 'asc' | 'desc' }) => {
  if (!sorted) return <UnfoldMore sx={{ fontSize: 14, opacity: 0.3 }} />;
  return sorted === 'asc'
    ? <ArrowUpward sx={{ fontSize: 14, color: '#5eead4' }} />
    : <ArrowDownward sx={{ fontSize: 14, color: '#5eead4' }} />;
};

// ── componente principal ──────────────────────────────────────────────────────
interface QueueTableProps {
  response?: QueueTableResponse;
  isLoading?: boolean;
}

const columnHelper = createColumnHelper<QueueRow>();

export default function QueueTable({ response, isLoading = false }: QueueTableProps) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState('');

  const periods = response?.periods ?? [];
  const lastPeriod = periods[periods.length - 1];

  const columns = useMemo(() => {
    const labelCol = columnHelper.accessor('label', {
      header: 'Fila',
      enableSorting: true,
      cell: info => (
        <Typography sx={{ fontSize: '0.8rem', fontWeight: 600, color: 'rgba(255,255,255,0.7)', whiteSpace: 'nowrap' }}>
          {info.getValue()}
        </Typography>
      ),
    });

    const periodCols = periods.map(period =>
      columnHelper.accessor(row => row.periods[period], {
        id: period,
        header: period,
        enableSorting: period === lastPeriod,
        sortingFn: (a, b) => {
          const aVal = a.original.periods[period]?.qty ?? 0;
          const bVal = b.original.periods[period]?.qty ?? 0;
          return aVal - bVal;
        },
        cell: info => {
          const data = info.getValue<PeriodData>();
          return data ? <PeriodCell data={data} /> : null;
        },
      })
    );

    return [labelCol, ...periodCols];
  }, [periods, lastPeriod]);

  const table = useReactTable({
    data: response?.rows ?? [],
    columns,
    state: { sorting, columnFilters, globalFilter },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: { pagination: { pageSize: 10 } },
  });

  if (isLoading) return (
    <Box sx={{ height: 300, borderRadius: '16px', background: 'rgba(255,255,255,0.03)', opacity: 0.4 }} />
  );

  const thStyle = {
    padding: '10px 16px',
    textAlign: 'left' as const,
    fontSize: '0.62rem',
    letterSpacing: '0.12em',
    textTransform: 'uppercase' as const,
    color: 'rgba(255,255,255,0.3)',
    fontWeight: 600,
    whiteSpace: 'nowrap' as const,
    borderBottom: '1px solid rgba(255,255,255,0.06)',
    background: 'rgba(255,255,255,0.02)',
  };

  const tdStyle = {
    padding: '8px 16px',
    borderBottom: '1px solid rgba(255,255,255,0.04)',
    verticalAlign: 'top' as const,
  };

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
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography sx={{ fontSize: '0.65rem', letterSpacing: '0.15em', color: 'rgba(255,255,255,0.35)', fontWeight: 600, textTransform: 'uppercase', mb: 0.5 }}>
            Evolução por Fila
          </Typography>
          <Typography sx={{ fontSize: '1.3rem', fontWeight: 700, color: 'rgba(255,255,255,0.9)', letterSpacing: '-0.02em' }}>
            {response?.rows.length} filas
            <span style={{ fontSize: '0.9rem', fontWeight: 400, color: 'rgba(255,255,255,0.35)' }}> · {periods.length} períodos</span>
          </Typography>
        </Box>
        <TextField
          size="small"
          placeholder="Buscar fila..."
          value={globalFilter}
          onChange={e => setGlobalFilter(e.target.value)}
          sx={{
            '& .MuiOutlinedInput-root': {
              fontSize: '0.8rem',
              color: 'rgba(255,255,255,0.7)',
              borderRadius: '10px',
              background: 'rgba(255,255,255,0.04)',
              '& fieldset': { borderColor: 'rgba(255,255,255,0.08)' },
              '&:hover fieldset': { borderColor: 'rgba(255,255,255,0.15)' },
              '&.Mui-focused fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
            },
            '& .MuiInputBase-input::placeholder': { color: 'rgba(255,255,255,0.2)' },
          }}
        />
      </Box>

      {/* Table */}
      <Box sx={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map(header => (
                  <th key={header.id} style={thStyle}>
                    <Box
                      sx={{ display: 'flex', alignItems: 'center', gap: 0.5, cursor: header.column.getCanSort() ? 'pointer' : 'default' }}
                      onClick={header.column.getToggleSortingHandler()}
                    >
                      {flexRender(header.column.columnDef.header, header.getContext())}
                      {header.column.getCanSort() && (
                        <SortIcon sorted={header.column.getIsSorted()} />
                      )}
                    </Box>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row, i) => (
              <tr key={row.id} style={{ background: i % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.01)' }}>
                {row.getVisibleCells().map(cell => (
                  <td key={cell.id} style={tdStyle}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </Box>

      {/* Pagination */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
        <Typography sx={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.25)' }}>
          {table.getFilteredRowModel().rows.length} filas · página {table.getState().pagination.pageIndex + 1} de {table.getPageCount()}
        </Typography>
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <IconButton
            size="small"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
            sx={{ color: 'rgba(255,255,255,0.3)', '&:disabled': { opacity: 0.1 } }}
          >
            <ChevronLeft fontSize="small" />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
            sx={{ color: 'rgba(255,255,255,0.3)', '&:disabled': { opacity: 0.1 } }}
          >
            <ChevronRight fontSize="small" />
          </IconButton>
        </Box>
      </Box>
    </Box>
  );
}