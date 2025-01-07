import React, { useState, useEffect } from 'react';
import { Container, Grid, Paper, Typography, Box, CircularProgress } from '@mui/material';
import CityTrendsChart from '../../components/charts/CityTrendsChart';
import GrowthRatesChart from '../../components/charts/GrowthRatesChart';
import MarketHeatmap from '../../components/charts/MarketHeatmap';
import api, { CityTrendsData, GrowthRatesData, MarketHeatmapData } from '../../services/api';

interface DashboardData {
  cityTrends: CityTrendsData | null;
  growthRates: GrowthRatesData | null;
  marketHeatmap: MarketHeatmapData | null;
}

// Helper function to format percentage
const formatPercentage = (value: number): string => {
  return `${(value * 100).toFixed(1)}%`;
};

// Helper function to get stats from data
const getStats = (data: CityTrendsData | null) => {
  if (!data) return { hpiGrowth: 'N/A', totalCities: 0 };
  const cities = Object.keys(data.values);
  const lastIndex = data.date.length - 1;
  const firstIndex = 0;

  // Calculate average growth across all cities
  let totalGrowth = 0;
  let validCityCount = 0;

  cities.forEach(city => {
    const startValue = data.values[city][firstIndex];
    const endValue = data.values[city][lastIndex];
    if (startValue && endValue) {
      const growth = (endValue / startValue) - 1;
      totalGrowth += growth;
      validCityCount++;
    }
  });

  const averageGrowth = validCityCount > 0 ? totalGrowth / validCityCount : 0;

  return {
    hpiGrowth: formatPercentage(averageGrowth),
    totalCities: cities.length
  };
};

// Helper function to get growth stats
const getGrowthStats = (data: GrowthRatesData | null) => {
  if (!data) return { highestGrowth: 'N/A', lowestGrowth: 'N/A' };
  const lastIndex = data.date.length - 1;
  let highest = -Infinity;
  let lowest = Infinity;
  let highestCity = '';
  let lowestCity = '';

  Object.entries(data.values).forEach(([city, values]) => {
    const value = values[lastIndex];
    if (value > highest) {
      highest = value;
      highestCity = city;
    }
    if (value < lowest) {
      lowest = value;
      lowestCity = city;
    }
  });

  return {
    highestGrowth: `${highestCity} (${formatPercentage(highest)})`,
    lowestGrowth: `${lowestCity} (${formatPercentage(lowest)})`
  };
};

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
    <Container 
      maxWidth="xl"
      sx={{ 
        px: { xs: 1, sm: 2, md: 3 },
        mx: 'auto',
        width: '100%',
        maxWidth: {
          xs: '100%',
          sm: '600px',
          md: '900px',
          lg: '1200px',
          xl: '1536px'
        }
      }}
    >
      <Box 
        sx={{ 
          my: { xs: 3, sm: 4 },
          background: 'linear-gradient(180deg, rgba(25,118,210,0.05) 0%, rgba(25,118,210,0) 100%)',
          borderRadius: 2,
          p: { xs: 2, sm: 3, md: 4 }
        }}
      >
        <Typography 
          variant="h3" 
          component="h1" 
          gutterBottom 
          align="center"
          sx={{
            fontSize: { xs: '1.75rem', sm: '2.25rem', md: '2.75rem' },
            mb: { xs: 2, sm: 3 },
            fontWeight: 'bold',
            color: 'primary.main'
          }}
        >
          Rental Market Trends and Statistics
        </Typography>
        
        <Typography 
          variant="h6" 
          align="center"
          sx={{ 
            color: 'text.secondary',
            mb: { xs: 3, sm: 4 },
            fontSize: { xs: '1rem', sm: '1.1rem' },
            maxWidth: '800px',
            mx: 'auto',
            lineHeight: 1.6
          }}
        >
          Explore comprehensive insights into rental market trends, growth patterns, and regional performance metrics across major metropolitan areas.
        </Typography>

        <Grid container spacing={{ xs: 2, sm: 3 }} sx={{ mb: { xs: 3, sm: 4 } }}>
          <Grid item xs={12} sm={6} md={3}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: { xs: 2, sm: 2 }, 
                bgcolor: 'background.paper', 
                borderRadius: 2,
                height: '100%',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
                }
              }}
            >
              <Typography 
                variant="subtitle2" 
                color="text.secondary"
                sx={{ 
                  fontSize: { xs: '0.75rem', sm: '0.875rem' },
                  mb: { xs: 0.5, sm: 1 }
                }}
              >
                Highest Rental Growth
              </Typography>
              <Typography 
                variant="h6" 
                sx={{ 
                  fontWeight: 'bold', 
                  color: 'success.main',
                  fontSize: { xs: '0.9rem', sm: '1.1rem', md: '1.25rem' },
                  lineHeight: 1.2
                }}
              >
                {getGrowthStats(data.growthRates).highestGrowth}
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: { xs: 2, sm: 2 }, 
                bgcolor: 'background.paper', 
                borderRadius: 2,
                height: '100%',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
                }
              }}
            >
              <Typography 
                variant="subtitle2" 
                color="text.secondary"
                sx={{ 
                  fontSize: { xs: '0.75rem', sm: '0.875rem' },
                  mb: { xs: 0.5, sm: 1 }
                }}
              >
                Lowest Rental Growth
              </Typography>
              <Typography 
                variant="h6" 
                sx={{ 
                  fontWeight: 'bold', 
                  color: 'error.main',
                  fontSize: { xs: '0.9rem', sm: '1.1rem', md: '1.25rem' },
                  lineHeight: 1.2
                }}
              >
                {getGrowthStats(data.growthRates).lowestGrowth}
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: { xs: 2, sm: 2 }, 
                bgcolor: 'background.paper', 
                borderRadius: 2,
                height: '100%',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
                }
              }}
            >
              <Box>
                <Typography 
                  variant="subtitle2" 
                  color="text.secondary"
                  sx={{ 
                    fontSize: { xs: '0.75rem', sm: '0.875rem' },
                    mb: { xs: 0.5, sm: 1 },
                    display: 'flex',
                    alignItems: 'center'
                  }}
                >
                  Rental Growth Since 2010
                  <Typography
                    component="span"
                    sx={{
                      display: 'inline-block',
                      ml: 0.5,
                      color: 'text.secondary',
                      cursor: 'help',
                      '&:hover': {
                        color: 'primary.main'
                      }
                    }}
                    title="Average rental price growth across all cities from 2010 to present"
                  >
                    ⓘ
                  </Typography>
                </Typography>
                <Typography 
                  variant="h6" 
                  sx={{ 
                    fontWeight: 'bold',
                    fontSize: { xs: '0.9rem', sm: '1.1rem', md: '1.25rem' },
                    lineHeight: 1.2
                  }}
                >
                  {getStats(data.cityTrends).hpiGrowth}
                </Typography>
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: { xs: 2, sm: 2 }, 
                bgcolor: 'background.paper', 
                borderRadius: 2,
                height: '100%',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
                }
              }}
            >
              <Typography 
                variant="subtitle2" 
                color="text.secondary"
                sx={{ 
                  fontSize: { xs: '0.75rem', sm: '0.875rem' },
                  mb: { xs: 0.5, sm: 1 }
                }}
              >
                Cities Analyzed
              </Typography>
              <Typography 
                variant="h6" 
                sx={{ 
                  fontWeight: 'bold',
                  fontSize: { xs: '1rem', sm: '1.1rem', md: '1.25rem' },
                  lineHeight: 1.2
                }}
              >
                {getStats(data.cityTrends).totalCities}
              </Typography>
            </Paper>
          </Grid>
        </Grid>
        
        <Grid container spacing={{ xs: 3, sm: 4 }}>
          <Grid item xs={12}>
            <Paper 
              elevation={2} 
              sx={{ 
                p: { xs: 2, sm: 3 },
                borderRadius: 2,
                bgcolor: 'background.default',
                transition: 'all 0.3s ease',
                '&:hover': {
                  bgcolor: '#fafafa',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
                },
                overflow: 'hidden'
              }}
            >
              <Box sx={{ 
                mt: 2,
                overflowX: 'auto',
                position: 'relative',
                '&::after': {
                  content: '""',
                  position: 'absolute',
                  right: 0,
                  top: 0,
                  bottom: 0,
                  width: '40px',
                  background: 'linear-gradient(to right, transparent, rgba(255,255,255,0.9))',
                  pointerEvents: 'none',
                  display: { xs: 'block', md: 'none' }
                },
                '& > div': {
                  minWidth: { xs: '600px', md: '100%' }
                }
              }}>
                {data.cityTrends && <CityTrendsChart data={data.cityTrends} />}
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper 
              elevation={2} 
              sx={{ 
                p: { xs: 2, sm: 3 },
                borderRadius: 2,
                bgcolor: 'background.default',
                transition: 'all 0.3s ease',
                '&:hover': {
                  bgcolor: '#fafafa',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
                },
                overflow: 'hidden'
              }}
            >
              <Box sx={{ 
                mt: 2,
                overflowX: 'auto',
                position: 'relative',
                '&::after': {
                  content: '""',
                  position: 'absolute',
                  right: 0,
                  top: 0,
                  bottom: 0,
                  width: '40px',
                  background: 'linear-gradient(to right, transparent, rgba(255,255,255,0.9))',
                  pointerEvents: 'none',
                  display: { xs: 'block', md: 'none' }
                },
                '& > div': {
                  minWidth: { xs: '600px', md: '100%' }
                }
              }}>
                {data.growthRates && <GrowthRatesChart data={data.growthRates} />}
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper 
              elevation={2} 
              sx={{ 
                p: { xs: 2, sm: 3 },
                borderRadius: 2,
                bgcolor: 'background.default',
                transition: 'all 0.3s ease',
                '&:hover': {
                  bgcolor: '#fafafa',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
                },
                overflow: 'hidden'
              }}
            >
              <Box sx={{ 
                mt: 2,
                overflowX: 'auto',
                position: 'relative',
                '&::after': {
                  content: '""',
                  position: 'absolute',
                  right: 0,
                  top: 0,
                  bottom: 0,
                  width: '40px',
                  background: 'linear-gradient(to right, transparent, rgba(255,255,255,0.9))',
                  pointerEvents: 'none',
                  display: { xs: 'block', md: 'none' }
                },
                '& > div': {
                  minWidth: { xs: '600px', md: '100%' }
                }
              }}>
                {data.marketHeatmap && <MarketHeatmap data={data.marketHeatmap} />}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default DashboardPage;
