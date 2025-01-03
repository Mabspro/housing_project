import React from 'react';
import { Box, Link, Typography } from '@mui/material';

const Footer: React.FC = () => {
  return (
    <Box
      component="footer"
      sx={{
        width: '100%',
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: 'background.paper',
        borderTop: '1px solid',
        borderColor: 'divider',
        textAlign: 'center',
        marginTop: 'auto'
      }}
    >
      <Typography variant="body2" color="text.secondary">
        Data Source:{' '}
        <Link
          href="https://www.kaggle.com/datasets/praveenchandran2006/u-s-housing-prices-regional-trends-2000-2023"
          target="_blank"
          rel="noopener noreferrer"
          color="primary"
          sx={{ 
            textDecoration: 'none',
            '&:hover': {
              textDecoration: 'underline'
            }
          }}
        >
          U.S. Housing Prices Regional Trends (2000-2023)
        </Link>
        {' '}(Kaggle)
      </Typography>
    </Box>
  );
};

export default Footer;
