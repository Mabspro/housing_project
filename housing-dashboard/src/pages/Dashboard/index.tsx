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

// Helper function to format percentage
const formatPercentage = (value: number): string => {
  return `${(value * 100).toFixed(1)}%`;
};

// Helper function to get stats from data
const getStats = (data: CityTrendsData | null) => {
  if (!data) return { hpiGrowth: 'N/A', totalCities: 0 };
  const cities = Object.keys(data.values).filter(city => city !== 'U.S. National');
  const lastIndex = data.date.length - 1;
  const firstIndex = 0;
  const nationalStart = data.values['U.S. National']?.[firstIndex] || 0;
  const nationalEnd = data.values['U.S. National']?.[lastIndex] || 0;
  const growthRate = (nationalEnd / nationalStart) - 1;
  return {
    hpiGrowth: formatPercentage(growthRate),
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
    <Container maxWidth="xl" sx={{ px: { xs: 2, sm: 3 } }}>
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
            mb: { xs: 1, sm: 2 },
            fontWeight: 'bold',
            color: 'primary.main'
          }}
        >
          Real Estate Market Analytics
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
            lineHeight: 1.5
          }}
        >
          Explore comprehensive insights into real estate market trends, growth patterns, and regional performance metrics across major metropolitan areas.
        </Typography>

        <Grid container spacing={{ xs: 2, sm: 3 }} sx={{ mb: { xs: 3, sm: 4 } }}>
          <Grid item xs={6} sm={6} md={3}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: { xs: 1.5, sm: 2 }, 
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
                Highest Growth City
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
          <Grid item xs={6} sm={6} md={3}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: { xs: 1.5, sm: 2 }, 
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
                Lowest Growth City
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
          <Grid item xs={6} sm={6} md={3}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: { xs: 1.5, sm: 2 }, 
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
                  HPI Growth Since 2000
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
                    title="Housing Price Index (HPI) growth from base year 2000 (index=100) to present"
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
          <Grid item xs={6} sm={6} md={3}>
            <Paper 
              elevation={0} 
              sx={{ 
                p: { xs: 1.5, sm: 2 }, 
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
                  fontSize: { xs: '0.9rem', sm: '1.1rem', md: '1.25rem' },
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
              <Typography 
                variant="h6" 
                gutterBottom 
                sx={{ 
                  fontWeight: 'bold',
                  fontSize: { xs: '1.1rem', sm: '1.25rem' },
                  mb: 2
                }}
              >
                Price Index Trends by Metropolitan Area (2000-2023)
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ 
                  color: 'text.secondary',
                  mb: 3,
                  fontSize: { xs: '0.875rem', sm: '1rem' },
                  maxWidth: '800px',
                  lineHeight: 1.5
                }}
              >
                Track historical price index evolution across major metropolitan areas, normalized to a base year for comparative analysis.
              </Typography>
              <Box sx={{ 
                mt: 2,
                overflowX: 'auto',
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
              <Typography 
                variant="h6" 
                gutterBottom 
                sx={{ 
                  fontWeight: 'bold',
                  fontSize: { xs: '1.1rem', sm: '1.25rem' },
                  mb: 2
                }}
              >
                Annual Growth Rate Analysis
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ 
                  color: 'text.secondary',
                  mb: 3,
                  fontSize: { xs: '0.875rem', sm: '1rem' },
                  maxWidth: '800px',
                  lineHeight: 1.5
                }}
              >
                Compare year-over-year growth rates across metropolitan areas to identify emerging market opportunities and trends.
              </Typography>
              <Box sx={{ 
                mt: 2,
                overflowX: 'auto',
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
              <Typography 
                variant="h6" 
                gutterBottom 
                sx={{ 
                  fontWeight: 'bold',
                  fontSize: { xs: '1.1rem', sm: '1.25rem' },
                  mb: 2
                }}
              >
                Regional Market Performance
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ 
                  color: 'text.secondary',
                  mb: 3,
                  fontSize: { xs: '0.875rem', sm: '1rem' },
                  maxWidth: '800px',
                  lineHeight: 1.5
                }}
              >
                Visualize current market performance across regions with an intuitive heatmap highlighting growth variations.
              </Typography>
              <Box sx={{ 
                mt: 2,
                overflowX: 'auto',
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
