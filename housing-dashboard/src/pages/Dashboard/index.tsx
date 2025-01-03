import React, { useState, useEffect } from 'react';
import { Container, Grid, Paper, Typography, Box, CircularProgress } from '@mui/material';
import CityTrendsChart from '../../components/charts/CityTrendsChart/index.tsx';
import GrowthRatesChart from '../../components/charts/GrowthRatesChart/index.tsx';
import MarketHeatmap from '../../components/charts/MarketHeatmap/index.tsx';
import api, { CityTrendsData, GrowthRatesData, MarketHeatmapData } from '../../services/api.ts';

interface DashboardData {
  cityTrends: CityTrendsData | null;
  growthRates: GrowthRatesData | null;
  marketHeatmap: MarketHeatmapData | null;
}

const DashboardPage: React.FC = () => {
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
    <Container maxWidth="xl" sx={{ px: { xs: 2, sm: 3 } }}>
      <Box sx={{ my: { xs: 3, sm: 4 } }}>
        <Typography 
          variant="h4" 
          component="h1" 
          gutterBottom 
          sx={{
            fontSize: { xs: '1.5rem', sm: '2rem', md: '2.5rem' },
            mb: { xs: 2, sm: 3 }
          }}
        >
          Market Analysis
        </Typography>
        
        <Grid container spacing={{ xs: 2.5, sm: 3, md: 4 }}>
          <Grid item xs={12}>
            <Paper elevation={2} sx={{ 
              p: { xs: 2, sm: 2.5, md: 3 },
              borderRadius: { xs: 1, sm: 2 },
              bgcolor: 'background.default',
              transition: 'all 0.3s ease',
              '&:hover': {
                bgcolor: '#fafafa',
                boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
              }
            }}>
              <Typography 
                variant="h6" 
                gutterBottom 
                sx={{ 
                  fontWeight: 'bold',
                  fontSize: { xs: '1rem', sm: '1.25rem' }
                }}
              >
                City Price Trends
              </Typography>
              {data.cityTrends && <CityTrendsChart data={data.cityTrends} />}
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={2} sx={{ 
              p: { xs: 2, sm: 2.5, md: 3 },
              borderRadius: { xs: 1, sm: 2 },
              bgcolor: 'background.default',
              transition: 'all 0.3s ease',
              '&:hover': {
                bgcolor: '#fafafa',
                boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
              }
            }}>
              <Typography 
                variant="h6" 
                gutterBottom 
                sx={{ 
                  fontWeight: 'bold',
                  fontSize: { xs: '1rem', sm: '1.25rem' }
                }}
              >
                Growth Rates
              </Typography>
              {data.growthRates && <GrowthRatesChart data={data.growthRates} />}
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={2} sx={{ 
              p: { xs: 2, sm: 2.5, md: 3 },
              borderRadius: { xs: 1, sm: 2 },
              bgcolor: 'background.default',
              transition: 'all 0.3s ease',
              '&:hover': {
                bgcolor: '#fafafa',
                boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
              }
            }}>
              <Typography 
                variant="h6" 
                gutterBottom 
                sx={{ 
                  fontWeight: 'bold',
                  fontSize: { xs: '1rem', sm: '1.25rem' }
                }}
              >
                Performance Heatmap
              </Typography>
              {data.marketHeatmap && <MarketHeatmap data={data.marketHeatmap} />}
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default DashboardPage;
