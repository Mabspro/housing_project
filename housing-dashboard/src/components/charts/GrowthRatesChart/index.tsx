import React from 'react';
import Plot from 'react-plotly.js';
import { Data, Layout, Config } from 'plotly.js';
import { useTheme, useMediaQuery } from '@mui/material';

interface GrowthRatesChartProps {
  data?: {
    date: string[];
    values: { [market: string]: number[] };
  };
}

const GrowthRatesChart: React.FC<GrowthRatesChartProps> = ({ data }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));

  if (!data) return <div>Loading...</div>;

  const traces: Data[] = Object.entries(data.values).map(([market, values]) => ({
    type: 'scatter' as const,
    mode: 'lines' as const,
    name: market,
    x: data.date,
    y: values,
    hovertemplate: '%{y:.2%}<extra>%{fullData.name}</extra>',
    line: {
      width: isMobile ? 1.5 : 2
    }
  }));

  const layout: Partial<Layout> = {
    title: {
      text: 'Year-over-Year Growth Rates',
      font: {
        size: isMobile ? 14 : isTablet ? 16 : 18,
        family: 'Arial, sans-serif'
      } as any
    },
    xaxis: {
      title: {
        text: 'Date',
        font: {
          size: isMobile ? 10 : 12,
          family: 'Arial, sans-serif'
        } as any,
        standoff: 10
      },
      showgrid: true,
      gridcolor: 'rgba(211,211,211,0.3)',
      tickfont: {
        size: isMobile ? 8 : 10,
        family: 'Arial, sans-serif'
      } as any,
      automargin: true
    },
    yaxis: {
      title: {
        text: 'Growth Rate (Year-over-Year %)',
        font: {
          size: isMobile ? 10 : 12,
          family: 'Arial, sans-serif'
        } as any,
        standoff: 20
      },
      showgrid: true,
      gridcolor: 'rgba(211,211,211,0.3)',
      tickformat: '.1%',
      tickfont: {
        size: isMobile ? 8 : 10,
        family: 'Arial, sans-serif'
      } as any,
      automargin: true,
      fixedrange: isMobile,
      range: [-0.3, 0.3],
      dtick: 0.1
    },
    hovermode: 'closest' as const,
    showlegend: true,
    legend: {
      x: isMobile ? 0 : 1.05,
      y: isMobile ? -0.2 : 1,
      orientation: isMobile ? 'h' as const : 'v' as const,
      xanchor: isMobile ? 'center' : 'left',
      yanchor: isMobile ? 'top' : 'top',
      font: {
        size: isMobile ? 8 : 10,
        family: 'Arial, sans-serif'
      } as any,
      title: { 
        text: 'Markets',
        font: {
          size: isMobile ? 9 : 11,
          family: 'Arial, sans-serif'
        } as any
      }
    },
    margin: {
      l: isMobile ? 65 : 95,
      r: isMobile ? 20 : 50,
      t: isMobile ? 40 : 50,
      b: isMobile ? 100 : 50,
      pad: 0
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
      filename: 'growth_rates_chart'
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
        height: isMobile ? '250px' : isTablet ? '350px' : '400px',
        minHeight: '200px'
      }}
    />
  );
};

export default GrowthRatesChart;
