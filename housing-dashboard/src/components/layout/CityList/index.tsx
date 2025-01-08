import React from 'react';
import { Paper, Typography, Box, Grid } from '@mui/material';

const CityList: React.FC = () => {
  const cityCategories = [
    {
      title: 'Top 20 Cities Composite',
      cities: [
        'Atlanta', 'Boston', 'Charlotte', 'Chicago', 'Cleveland',
        'Dallas', 'Denver', 'Detroit', 'Las Vegas', 'Los Angeles',
        'Miami', 'Minneapolis', 'New York', 'Phoenix', 'Portland',
        'San Diego', 'San Francisco', 'Seattle', 'Tampa', 'Washington DC'
      ]
    },
    {
      title: 'Top 10 Cities Composite',
      cities: [
        'Boston', 'Chicago', 'Denver', 'Las Vegas', 'Los Angeles',
        'Miami', 'New York', 'San Diego', 'San Francisco', 'Washington DC'
      ]
    },
    {
      title: 'Current Market Analysis',
      cities: [
        'New York', 'Los Angeles', 'Chicago', 'Dallas', 'Miami'
      ]
    }
  ];

  return (
    <Paper 
      elevation={0}
      sx={{ 
        p: { xs: 2, sm: 3 },
        bgcolor: 'background.paper',
        borderRadius: 2,
        mt: 4
      }}
    >
      <Typography 
        variant="h6" 
        gutterBottom
        sx={{ 
          fontWeight: 'bold',
          color: 'text.primary',
          mb: 3
        }}
      >
        Cities Analyzed
      </Typography>
      
      <Grid container spacing={4}>
        {cityCategories.map((category, idx) => (
          <Grid item xs={12} sm={6} md={4} key={idx}>
            <Box sx={{ 
              bgcolor: 'background.default',
              p: 2,
              borderRadius: 1,
              height: '100%'
            }}>
              <Typography 
                variant="subtitle1" 
                sx={{ 
                  fontWeight: 'bold',
                  color: 'primary.main',
                  mb: 2,
                  pb: 1,
                  borderBottom: '2px solid',
                  borderColor: 'primary.light'
                }}
              >
                {category.title}
              </Typography>
              <Box 
                component="ul" 
                sx={{ 
                  pl: 2, 
                  m: 0,
                  columnCount: { xs: 1, sm: category.cities.length > 10 ? 2 : 1 },
                  columnGap: 2
                }}
              >
                {category.cities.map((city, cityIdx) => (
                  <Typography 
                    component="li" 
                    key={cityIdx}
                    sx={{ 
                      fontSize: '0.875rem',
                      color: 'text.secondary',
                      mb: 0.5
                    }}
                  >
                    {city}
                  </Typography>
                ))}
              </Box>
            </Box>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
};

export default CityList;
