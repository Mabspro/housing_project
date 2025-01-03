import React from 'react';
import Plot from 'react-plotly.js';
import { Data, Layout, Config } from 'plotly.js';

interface MarketHeatmapProps {
  data?: {
    markets: string[];
    growthRates: number[];
  };
}

const MarketHeatmap: React.FC<MarketHeatmapProps> = ({ data }) => {
  if (!data) return <div>Loading...</div>;

  const formattedText = data.growthRates.map(v => `${(v * 100).toFixed(2)}%`);

  const traces: Data[] = [{
    type: 'heatmap' as const,
    z: [data.growthRates],
    y: ['Average Growth'],
    x: data.markets,
    colorscale: 'RdBu',
    reversescale: true,
    zmin: -0.1, // -10%
    zmax: 0.1,  // +10%
    text: [formattedText] as any, // Cast to any to resolve typing issue with Plotly
    texttemplate: '%{text}',
    textfont: { size: 10 },
    hoverongaps: false,
    showscale: true,
    colorbar: {
      title: 'Growth Rate',
      tickformat: '.1%'
    }
  }];

  const layout: Partial<Layout> = {
    title: 'Market Growth Rate Analysis',
    xaxis: {
      title: 'Markets',
      tickangle: 45,
      showgrid: false
    },
    yaxis: {
      showgrid: false,
      ticksuffix: '  '  // Add some padding
    },
    margin: {
      l: 100,
      r: 50,
      t: 50,
      b: 100
    },
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    annotations: [{
      xref: 'paper',
      yref: 'paper',
      x: 0,
      xanchor: 'right',
      y: -0.3,
      yanchor: 'top',
      text: 'Red indicates higher growth rates while blue shows lower growth. Markets are sorted by average growth rate.',
      showarrow: false,
      font: {
        size: 10
      }
    }]
  };

  const config: Partial<Config> = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ['lasso2d', 'select2d'] as any[],
    toImageButtonOptions: {
      format: 'png',
      filename: 'market_heatmap'
    }
  };

  return (
    <Plot
      data={traces}
      layout={layout}
      config={config}
      style={{ width: '100%', height: '400px' }}
    />
  );
};

export default MarketHeatmap;
