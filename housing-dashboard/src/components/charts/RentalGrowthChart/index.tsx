import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { Box, CircularProgress, Typography } from '@mui/material';
import { fetchRentalGrowth, RentalGrowthData } from '../../../services/api';
import { Data, Layout } from 'plotly.js';

const RentalGrowthChart: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<RentalGrowthData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchRentalGrowth();
        setData(response);
        setError(null);
      } catch (err) {
        setError('Failed to fetch rental growth data');
        console.error('Error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !data) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography color="error">{error || 'No data available'}</Typography>
      </Box>
    );
  }

  const plotData: Data[] = Object.entries(data.values).map(([city, values]) => ({
    x: data.date,
    y: values.map(v => v * 100), // Convert to percentage
    name: city,
    type: 'scatter' as const,
    mode: 'lines' as const,
  }));

  const layout: Partial<Layout> = {
    title: 'Year-over-Year Rental Growth by Metropolitan Area',
    xaxis: {
      title: 'Date',
      showgrid: true,
      gridcolor: '#E1E5EA',
    },
    yaxis: {
      title: 'Year-over-Year Growth Rate (%)',
      showgrid: true,
      gridcolor: '#E1E5EA',
      zeroline: true,
      zerolinecolor: '#666666',
      zerolinewidth: 1.5,
    },
    showlegend: true,
    legend: {
      x: 1,
      xanchor: 'right' as const,
      y: 1,
    },
    hovermode: 'x unified' as const,
    height: 600,
    margin: {
      l: 50,
      r: 50,
      t: 50,
      b: 50,
    },
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
  };

  return (
    <Box>
      <Plot
        data={plotData}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '100%' }}
      />
    </Box>
  );
};

export default RentalGrowthChart;
