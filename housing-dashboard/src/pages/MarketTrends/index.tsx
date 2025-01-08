import React from 'react';
import { Container, Typography, Box, Grid, Paper } from '@mui/material';
import GrowthRatesChart from '../../components/charts/GrowthRatesChart';
import MarketHeatmap from '../../components/charts/MarketHeatmap';
import RentalTrendsChart from '../../components/charts/RentalTrendsChart';
import RentalGrowthChart from '../../components/charts/RentalGrowthChart';
import RentalHeatmap from '../../components/charts/RentalHeatmap';

const MarketTrends: React.FC = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Market Trends Analysis
        </Typography>

        {/* Housing Price Trends Section */}
        <Box mb={6}>
          <Typography variant="h5" gutterBottom color="primary">
            Housing Price Trends
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Price Growth Rates
                </Typography>
                <GrowthRatesChart />
              </Paper>
            </Grid>

            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Market Performance
                </Typography>
                <MarketHeatmap />
              </Paper>
            </Grid>
          </Grid>
        </Box>

        {/* Rental Market Section */}
        <Box>
          <Typography variant="h5" gutterBottom color="primary">
            Rental Market Analysis
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Rental Price Trends
                </Typography>
                <RentalTrendsChart />
              </Paper>
            </Grid>

            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Rental Growth Rates
                </Typography>
                <RentalGrowthChart />
              </Paper>
            </Grid>

            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Current Rental Market Performance
                </Typography>
                <RentalHeatmap />
              </Paper>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};

export default MarketTrends;
