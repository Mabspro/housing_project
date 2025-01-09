import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Grid, Paper, CircularProgress } from '@mui/material';
import MarketTrendsChart from '../../components/charts/MarketTrendsChart';
import MarketGrowthChart from '../../components/charts/MarketGrowthChart';
import MarketHeatmap from '../../components/charts/MarketHeatmap';
import api, { MarketTrendsData, MarketGrowthData, MarketHeatmapData } from '../../services/api';

const MarketTrends: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<{
    trends: MarketTrendsData | null;
    growth: MarketGrowthData | null;
    heatmap: MarketHeatmapData | null;
  }>({
    trends: null,
    growth: null,
    heatmap: null
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [trends, growth, heatmap] = await Promise.all([
          api.fetchMarketTrends(),
          api.fetchMarketGrowth(),
          api.fetchMarketHeatmap()
        ]);

        setData({
          trends,
          growth,
          heatmap
        });
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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
        <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 3 }}>
          Market Growth Analysis
        </Typography>
        
        <Typography variant="h6" align="center" color="text.secondary" sx={{ mb: 6, maxWidth: '800px', mx: 'auto' }}>
          Comprehensive analysis of housing market dynamics, including monthly changes, growth patterns, and regional performance metrics across major metropolitan areas.
        </Typography>

        <Grid container spacing={4}>
          {/* Monthly Price Changes Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom color="primary.main">
                Monthly Price Changes
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Track month-over-month price changes across different metropolitan areas, revealing short-term market dynamics and regional variations.
              </Typography>
              <MarketTrendsChart data={data.trends} />
            </Paper>
          </Grid>

          {/* Annual Growth Rates Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom color="primary.main">
                Year-over-Year Growth
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Analyze annual price changes by region, highlighting markets with significant growth or decline in housing values.
              </Typography>
              <MarketGrowthChart data={data.growth} />
            </Paper>
          </Grid>

          {/* Market Performance Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom color="primary.main">
                Current Market Performance
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Compare current market conditions across regions with a visual representation of relative market strength and growth rates.
              </Typography>
              <MarketHeatmap data={data.heatmap} />
            </Paper>
          </Grid>

          {/* Market Insights Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3, bgcolor: 'primary.main', color: 'white' }}>
              <Typography variant="h5" gutterBottom>
                Key Market Insights
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                    <Typography variant="h6" gutterBottom>
                      Market Dynamics
                    </Typography>
                    <Typography variant="body2">
                      Analysis of price movements and their implications for different metropolitan areas, helping identify emerging trends and market shifts.
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                    <Typography variant="h6" gutterBottom>
                      Regional Comparisons
                    </Typography>
                    <Typography variant="body2">
                      Comparative analysis of housing markets across different regions, highlighting variations in growth rates and market conditions.
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                    <Typography variant="h6" gutterBottom>
                      Growth Patterns
                    </Typography>
                    <Typography variant="body2">
                      Identification of price growth patterns and trends, providing insights into market momentum and potential future directions.
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default MarketTrends;
