import React from 'react';
import { Container, Typography, Box, Grid, Paper } from '@mui/material';
import GrowthRatesChart from '../../components/charts/GrowthRatesChart';
import MarketHeatmap from '../../components/charts/MarketHeatmap';
import HousingAffordabilityChart from '../../components/charts/HousingAffordabilityChart';

const MarketTrends: React.FC = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Market Trends
        </Typography>
        
        <Grid container spacing={3}>
          {/* Growth Rates Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Year-over-Year Growth Rates
              </Typography>
              <GrowthRatesChart />
            </Paper>
          </Grid>

          {/* Housing Affordability Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Housing Affordability Analysis
              </Typography>
              <HousingAffordabilityChart />
            </Paper>
          </Grid>

          {/* Market Heatmap Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Current Market Performance
              </Typography>
              <MarketHeatmap />
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default MarketTrends;
