import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { Box, CircularProgress, Typography } from '@mui/material';
import { fetchHousingAffordability } from '../../../services/api';

const HousingAffordabilityChart: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchHousingAffordability();
        setData(response);
        setError(null);
      } catch (err) {
        setError('Failed to fetch housing affordability data');
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

  // Prepare data for plotting
  const plotData = [
    // Price to Income Ratio traces
    ...data.regions.map((region: string) => ({
      x: data.dates,
      y: data.metrics.priceToIncomeRatios[region],
      name: `${region} - Price/Income Ratio`,
      type: 'scatter',
      mode: 'lines',
      yaxis: 'y1',
    })),
    // Interest Rate traces
    ...data.regions.map((region: string) => ({
      x: data.dates,
      y: data.metrics.interestRates[region],
      name: `${region} - Interest Rate`,
      type: 'scatter',
      mode: 'lines',
      yaxis: 'y2',
      line: { dash: 'dot' },
    })),
  ];

  const layout: Partial<Plotly.Layout> = {
    title: 'Housing Affordability Analysis',
    xaxis: { title: 'Date' },
    yaxis: {
      title: 'Price to Income Ratio',
      side: 'left' as const,
      showgrid: false,
    },
    yaxis2: {
      title: 'Interest Rate (%)',
      side: 'right' as const,
      overlaying: 'y',
      showgrid: false,
    },
    height: 600,
    showlegend: true,
    legend: {
      x: 1.1,
      y: 1,
    },
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
      <Box mt={2}>
        <Typography variant="body2" color="textSecondary">
          * Price to Income Ratio represents the ratio of median home price to annual median wage (Bachelor's degree)
        </Typography>
        <Typography variant="body2" color="textSecondary">
          * Interest rates shown are effective federal funds rates
        </Typography>
      </Box>
    </Box>
  );
};

export default HousingAffordabilityChart;
