import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { Box, CircularProgress, Typography } from '@mui/material';
import { fetchRentalHeatmap, RentalHeatmapData } from '../../../services/api';
import { Data, Layout } from 'plotly.js';

const RentalHeatmap: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<RentalHeatmapData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchRentalHeatmap();
        setData(response);
        setError(null);
      } catch (err) {
        setError('Failed to fetch rental heatmap data');
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

  // Convert growth rates to percentages
  const growthRatesPercentage = data.growthRates.map(rate => rate * 100);

  // Create color scale based on growth rates
  const getColor = (value: number) => {
    if (value > 5) return '#2E7D32'; // Strong growth (dark green)
    if (value > 2) return '#4CAF50'; // Moderate growth (medium green)
    if (value > 0) return '#81C784'; // Slight growth (light green)
    if (value > -2) return '#FFCDD2'; // Slight decline (light red)
    if (value > -5) return '#E57373'; // Moderate decline (medium red)
    return '#C62828'; // Strong decline (dark red)
  };

  const plotData: Data[] = [{
    type: 'bar' as const,
    x: data.markets,
    y: growthRatesPercentage,
    marker: {
      color: growthRatesPercentage.map(getColor),
    },
    text: growthRatesPercentage.map(value => value.toFixed(1) + '%'),
    textposition: 'auto' as const,
  }];

  const layout: Partial<Layout> = {
    title: 'Current Rental Market Performance by Metropolitan Area',
    xaxis: {
      title: 'Metropolitan Area',
      tickangle: -45,
    },
    yaxis: {
      title: 'Year-over-Year Growth Rate (%)',
      zeroline: true,
      zerolinecolor: '#666666',
      zerolinewidth: 1.5,
    },
    height: 500,
    margin: {
      l: 50,
      r: 50,
      t: 50,
      b: 100, // Increased bottom margin for rotated labels
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
      <Box mt={2}>
        <Typography variant="body2" color="textSecondary">
          * Growth rates represent year-over-year changes in average rental prices
        </Typography>
      </Box>
    </Box>
  );
};

export default RentalHeatmap;
