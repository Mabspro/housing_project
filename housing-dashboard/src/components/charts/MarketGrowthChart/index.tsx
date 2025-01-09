import React from 'react';
import Plot from 'react-plotly.js';
import { Box, Typography } from '@mui/material';
import { HistoricalGrowthData, MarketGrowthData } from '../../../services/api';
import { Data, Layout } from 'plotly.js';

interface MarketGrowthChartProps {
  data: HistoricalGrowthData | MarketGrowthData | null;
}

const MarketGrowthChart: React.FC<MarketGrowthChartProps> = ({ data }) => {
  if (!data) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography color="error">No data available</Typography>
      </Box>
    );
  }

  const plotData: Data[] = Object.entries(data.values).map(([city, values]) => ({
    x: data.date,
    y: values as number[],
    name: city,
    type: 'scatter' as const,
    mode: 'lines' as const,
  }));

  const layout: Partial<Layout> = {
    title: 'Growth Rates by Metropolitan Area',
    xaxis: {
      title: 'Date',
      showgrid: true,
      gridcolor: '#E1E5EA',
    },
    yaxis: {
      title: 'Growth Rate (%)',
      showgrid: true,
      gridcolor: '#E1E5EA',
      tickformat: '.1f',
      hoverformat: '.2f',
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

export default MarketGrowthChart;
