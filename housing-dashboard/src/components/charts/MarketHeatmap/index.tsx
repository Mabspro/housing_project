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
    y: ['Average Growth'],
    x: data.markets,
    colorscale: 'RdBu',
    reversescale: true,
    zmin: -0.1,
    zmax: 0.1,
    text: [formattedText] as any,
    texttemplate: '%{text}',
    textfont: {
      size: isMobile ? 8 : isTablet ? 9 : 10,
      family: 'Arial, sans-serif'
    } as any,
    hoverongaps: false,
    showscale: true,
    colorbar: {
      title: 'Growth Rate',
      titlefont: {
        size: isMobile ? 10 : 12,
        family: 'Arial, sans-serif'
      } as any,
      tickformat: '.1%',
      len: isMobile ? 0.8 : 1,
      thickness: isMobile ? 15 : 20
    }
  }];

  const layout: Partial<Layout> = {
    title: {
      text: 'Market Growth Rate Analysis',
      font: {
        size: isMobile ? 14 : isTablet ? 16 : 18,
        family: 'Arial, sans-serif'
      } as any
    },
    xaxis: {
      title: {
        text: 'Markets',
        font: {
          size: isMobile ? 10 : 12,
          family: 'Arial, sans-serif'
        } as any,
        standoff: 25
      },
      tickangle: isMobile ? 60 : 45,
      showgrid: false,
      tickfont: {
        size: isMobile ? 8 : 10,
        family: 'Arial, sans-serif'
      } as any,
      automargin: true
    },
    yaxis: {
      showgrid: false,
      ticksuffix: '  ',
      tickfont: {
        size: isMobile ? 8 : 10,
        family: 'Arial, sans-serif'
      } as any,
      automargin: true
    },
    margin: {
      l: isMobile ? 60 : 100,
      r: isMobile ? 30 : 50,
      t: isMobile ? 40 : 50,
      b: isMobile ? 120 : 140,
      pad: isMobile ? 0 : 4
    },
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    annotations: [{
      xref: 'paper',
      yref: 'paper',
      x: 0.5,
      xanchor: 'center',
      y: -0.35,
      yanchor: 'top',
      text: 'Red indicates higher growth rates while blue shows lower growth.<br>Markets are sorted by Average Growth Rate.',
      showarrow: false,
      align: 'center',
      font: {
        size: isMobile ? 8 : isTablet ? 9 : 10,
        family: 'Arial, sans-serif'
      } as any,
      bgcolor: 'rgba(255, 255, 255, 0.95)',
      borderpad: 4
    }]
  };

  const config: Partial<Config> = {
    responsive: true,
    displayModeBar: !isMobile,
    modeBarButtonsToRemove: ['lasso2d', 'select2d', 'zoom2d', 'pan2d'] as any[],
    toImageButtonOptions: {
      format: 'png',
      filename: 'market_heatmap'
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
        height: isMobile ? '300px' : isTablet ? '350px' : '400px',
        minHeight: '250px'
      }}
    />
  );
};

export default MarketHeatmap;
