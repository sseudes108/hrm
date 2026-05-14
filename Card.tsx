// src/components/GenericCard.tsx
import { Box, Typography } from '@mui/material';

interface LabCardProps {
  title?: string;
  children: React.ReactNode;
  padding?: number | string;
  margin?: number | string;
}

export default function LabCard({
  title,
  children,
  padding = '28px 32px',
  margin = 0,
}: LabCardProps) {
  return (
    <Box
      sx={{
        margin,
        padding,
        borderRadius: '16px',
        background: 'rgba(255,255,255,0.03)',
        border: '1px solid rgba(255,255,255,0.07)',
        backdropFilter: 'blur(12px)',
        boxShadow: '0 4px 40px rgba(0,0,0,0.25)',
        transition: 'box-shadow 0.3s ease, border-color 0.3s ease',
        '&:hover': {
          border: '1px solid rgba(255,255,255,0.13)',
          boxShadow: '0 8px 48px rgba(0,0,0,0.35)',
        },
      }}
    >
      {title && (
        <Typography
          variant="overline"
          sx={{
            display: 'block',
            fontSize: '0.65rem',
            letterSpacing: '0.15em',
            color: 'rgba(255,255,255,0.35)',
            marginBottom: '16px',
            fontWeight: 600,
          }}
        >
          {title}
        </Typography>
      )}
      {children}
    </Box>
  );
}