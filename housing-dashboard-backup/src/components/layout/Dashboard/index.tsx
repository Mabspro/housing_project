import React, { useState, useEffect } from 'react';
import { Container, Grid, Paper, Typography, Box, CircularProgress } from '@mui/material';
import CityTrendsChart from '../../charts/CityTrendsChart/index.tsx';
import GrowthRatesChart from '../../charts/GrowthRatesChart/index.tsx';
import MarketHeatmap from '../../charts/MarketHeatmap/index.tsx';
import api, { CityTrendsData, GrowthRatesData, MarketHeatmapData } from '../../../services/api.ts';

interface DashboardData {
  cityTrends: CityTrendsData | null;
  growthRates: GrowthRatesData | null;
  marketHeatmap: MarketHeatmapData | null;
}

const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData>({
    cityTrends: null,
    growthRates: null,
    marketHeatmap: null
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [cityTrends, growthRates, marketHeatmap] = await Promise.all([
          api.fetchCityTrends(),
          api.fetchGrowthRates(),
          api.fetchMarketHeatmap()
        ]);

        setData({
          cityTrends,
          growthRates,
          marketHeatmap
        });
        setLoading(false);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }
  
  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <Typography color="error" variant="h6">{error}</Typography>
      </Box>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Housing Market Analysis Dashboard
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                City Housing Price Trends
              </Typography>
              {data.cityTrends && <CityTrendsChart data={data.cityTrends} />}
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Growth Rate Analysis
              </Typography>
              {data.growthRates && <GrowthRatesChart data={data.growthRates} />}
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Market Performance Heatmap
              </Typography>
              {data.marketHeatmap && <MarketHeatmap data={data.marketHeatmap} />}
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard;
