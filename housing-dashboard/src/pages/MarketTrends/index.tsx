import React from 'react';
import { Container, Typography, Box, Grid, Paper } from '@mui/material';
import RentalTrendsChart from '../../components/charts/RentalTrendsChart';
import RentalGrowthChart from '../../components/charts/RentalGrowthChart';
import RentalHeatmap from '../../components/charts/RentalHeatmap';

const MarketTrends: React.FC = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 3 }}>
          Rental Market Analysis
        </Typography>
        
        <Typography variant="h6" align="center" color="text.secondary" sx={{ mb: 6, maxWidth: '800px', mx: 'auto' }}>
          Comprehensive analysis of rental market dynamics, including price trends, growth patterns, and regional performance across major metropolitan areas.
        </Typography>

        <Grid container spacing={4}>
          {/* Rental Price Trends Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom color="primary.main">
                Monthly Rental Price Trends
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Track average monthly rental prices across different metropolitan areas over time, revealing long-term market patterns and regional variations.
              </Typography>
              <RentalTrendsChart />
            </Paper>
          </Grid>

          {/* Rental Growth Rates Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom color="primary.main">
                Year-over-Year Rental Growth
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Analyze annual rental price changes by region, highlighting markets with significant growth or decline in rental rates.
              </Typography>
              <RentalGrowthChart />
            </Paper>
          </Grid>

          {/* Market Performance Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom color="primary.main">
                Current Rental Market Performance
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Compare current rental market conditions across regions with a visual representation of relative market strength and growth rates.
              </Typography>
              <RentalHeatmap />
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
                      Analysis of rental price movements and their implications for different metropolitan areas, helping identify emerging trends and market shifts.
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                    <Typography variant="h6" gutterBottom>
                      Regional Comparisons
                    </Typography>
                    <Typography variant="body2">
                      Comparative analysis of rental markets across different regions, highlighting variations in growth rates and market conditions.
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                    <Typography variant="h6" gutterBottom>
                      Growth Patterns
                    </Typography>
                    <Typography variant="body2">
                      Identification of rental growth patterns and trends, providing insights into market momentum and potential future directions.
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
