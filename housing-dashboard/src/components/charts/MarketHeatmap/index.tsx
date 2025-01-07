import React from 'react';
import Plot from 'react-plotly.js';
import { Data, Layout, Config } from 'plotly.js';
import { useTheme, useMediaQuery } from '@mui/material';

interface MarketHeatmapProps {
  data?: {
    markets: string[];
    growthRates: number[];
  };
}

const MarketHeatmap: React.FC<MarketHeatmapProps> = ({ data }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));

  if (!data) return <div>Loading...</div>;

  const formattedText = data.growthRates.map(v => `${(v * 100).toFixed(2)}%`);

  const traces: Data[] = [{
    type: 'heatmap' as const,
    z: [data.growthRates],
    y: ['Current Growth'],
    x: data.markets,
    colorscale: 'RdBu',
    reversescale: true,
    zmin: -0.1,
    zmax: 0.1,
    text: [formattedText] as any,
    texttemplate: '%{text}',
    textfont: {
      size: isMobile ? 10 : isTablet ? 11 : 12,
      family: 'Arial, sans-serif'
    } as any,
    hoverongaps: false,
    showscale: true,
    colorbar: {
      title: 'Annual Rental Growth',
      titlefont: {
        size: isMobile ? 12 : 14,
        family: 'Arial, sans-serif'
      } as any,
      tickformat: '.0%',
      len: 0.8,
      thickness: isMobile ? 15 : 20,
      x: 1,
      xpad: 10,
      nticks: isMobile ? 2 : 5, // Show only extreme values on mobile
      tickvals: isMobile ? [-0.1, 0.1] : undefined, // -10% and 10% on mobile
      ticktext: isMobile ? ['-10%', '10%'] : undefined
    }
  }];

  const layout: Partial<Layout> = {
    title: {
      text: 'Current Rental Growth by Metropolitan Area',
      font: {
        size: isMobile ? 14 : isTablet ? 16 : 18,
        family: 'Arial, sans-serif'
      } as any
    },
    xaxis: {
      title: {
        text: 'Metropolitan Areas',
        font: {
          size: isMobile ? 12 : 14,
          family: 'Arial, sans-serif'
        } as any,
        standoff: isMobile ? 30 : 25
      },
      tickangle: 45,
      showgrid: false,
      tickfont: {
        size: isMobile ? 10 : 12,
        family: 'Arial, sans-serif'
      } as any,
      automargin: true,
      tickmode: 'auto',
      nticks: isMobile ? 5 : undefined
    },
    yaxis: {
      showgrid: false,
      ticksuffix: '  ',
      tickfont: {
        size: isMobile ? 10 : 12,
        family: 'Arial, sans-serif'
      } as any,
      automargin: true
    },
    margin: {
      l: isMobile ? 40 : 80,
      r: isMobile ? 60 : 80,
      t: isMobile ? 40 : 50,
      b: isMobile ? 100 : 80,
      pad: 4
    },
    plot_bgcolor: 'white',
    paper_bgcolor: 'white'
  };

  const config: Partial<Config> = {
    responsive: true,
    displayModeBar: !isMobile,
    modeBarButtonsToRemove: ['lasso2d', 'select2d', 'zoom2d', 'pan2d'] as any[],
    toImageButtonOptions: {
      format: 'png',
      filename: 'rental_market_heatmap'
    },
    scrollZoom: false
  };

  return (
    <Plot
      data={traces}
      layout={layout}
      config={config}
      style={{ 
        width: '100%', 
        height: isMobile ? '250px' : isTablet ? '300px' : '350px',
        minHeight: '200px'
      }}
    />
  );
};

export default MarketHeatmap;
