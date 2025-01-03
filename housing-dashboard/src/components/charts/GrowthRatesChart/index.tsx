import React from 'react';
import Plot from 'react-plotly.js';
import { Data, Layout, Config } from 'plotly.js';

interface GrowthRatesChartProps {
  data?: {
    date: string[];
    values: { [market: string]: number[] };
  };
}

const GrowthRatesChart: React.FC<GrowthRatesChartProps> = ({ data }) => {
  if (!data) return <div>Loading...</div>;

  const traces: Data[] = Object.entries(data.values).map(([market, values]) => ({
    type: 'scatter' as const,
    mode: 'lines' as const,
    name: market,
    x: data.date,
    y: values,
    hovertemplate: '%{y:.2%}<extra>%{fullData.name}</extra>'
  }));

  const layout: Partial<Layout> = {
    title: 'Year-over-Year Growth Rates',
    xaxis: {
      title: 'Date',
      showgrid: true,
      gridcolor: 'rgba(211,211,211,0.3)'
    },
    yaxis: {
      title: 'Growth Rate (Year-over-Year %)',
      showgrid: true,
      gridcolor: 'rgba(211,211,211,0.3)',
      tickformat: '.1%'
    },
    hovermode: 'closest' as const,
    showlegend: true,
    legend: {
      x: 1.05,
      y: 1,
      title: { text: 'Markets' }
    },
    margin: {
      l: 60,
      r: 50,
      t: 50,
      b: 50
    },
    plot_bgcolor: 'white',
    paper_bgcolor: 'white'
  };

  const config: Partial<Config> = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ['lasso2d', 'select2d'] as any[],
    toImageButtonOptions: {
      format: 'png',
      filename: 'growth_rates_chart'
    }
  };

  return (
    <Plot
      data={traces}
      layout={layout}
      config={config}
      style={{ width: '100%', height: '600px' }}
    />
  );
};

export default GrowthRatesChart;
