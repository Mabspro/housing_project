import React from 'react';
import Plot from 'react-plotly.js';
import { Box, Typography } from '@mui/material';
import { MarketHeatmapData } from '../../../services/api';
import { Data, Layout } from 'plotly.js';

interface MarketHeatmapProps {
  data: MarketHeatmapData | null;
}

const MarketHeatmap: React.FC<MarketHeatmapProps> = ({ data }) => {
  if (!data) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography color="error">No data available</Typography>
      </Box>
    );
  }

  const plotData: Data[] = [{
    type: 'bar' as const,
    x: data.markets,
    y: data.growthRates,
    marker: {
      color: data.growthRates.map((rate: number) => 
        rate >= 0 ? 'rgb(0, 128, 0)' : 'rgb(255, 0, 0)'
      ),
    },
  }];

  const layout: Partial<Layout> = {
    title: 'Current Market Growth Rates by Metropolitan Area',
    xaxis: {
      title: 'Metropolitan Area',
      showgrid: false,
    },
    yaxis: {
      title: 'Year-over-Year Growth Rate (%)',
      showgrid: true,
      gridcolor: '#E1E5EA',
      tickformat: '.1f',
      hoverformat: '.2f',
    },
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

export default MarketHeatmap;
