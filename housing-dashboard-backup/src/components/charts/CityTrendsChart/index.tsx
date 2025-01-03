import React from 'react';
import Plot from 'react-plotly.js';
import { Data, Layout, Config } from 'plotly.js';

interface CityTrendsChartProps {
  data?: {
    date: string[];
    values: { [city: string]: number[] };
  };
}

const CityTrendsChart: React.FC<CityTrendsChartProps> = ({ data }) => {
  if (!data) return <div>Loading...</div>;

  const traces: Data[] = Object.entries(data.values).map(([city, values]) => ({
    type: 'scatter' as const,
    mode: 'lines' as const,
    name: city,
    x: data.date,
    y: values,
    hovertemplate: '%{y:.2f}<extra>%{fullData.name}</extra>'
  }));

  const layout: Partial<Layout> = {
    title: 'Housing Price Trends by City',
    xaxis: {
      title: 'Date',
      showgrid: true,
      gridcolor: 'rgba(211,211,211,0.3)'
    },
    yaxis: {
      title: 'Normalized Price Index',
      showgrid: true,
      gridcolor: 'rgba(211,211,211,0.3)'
    },
    hovermode: 'closest' as const,
    showlegend: true,
    legend: {
      x: 1.05,
      y: 1
    },
    margin: {
      l: 50,
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
    modeBarButtonsToRemove: ['lasso2d', 'select2d'] as any[]
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

export default CityTrendsChart;
