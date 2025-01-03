import React from 'react';
import { Container, Typography, Box, Paper, List, ListItem, ListItemText, Switch } from '@mui/material';

const SettingsPage: React.FC = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Settings
        </Typography>
        
        <Paper elevation={3} sx={{ p: 2 }}>
          <List>
            <ListItem>
              <ListItemText 
                primary="Dark Mode" 
                secondary="Toggle dark/light theme"
              />
              <Switch edge="end" />
            </ListItem>
            <ListItem>
              <ListItemText 
                primary="Data Auto-Refresh" 
                secondary="Automatically refresh data every hour"
              />
              <Switch edge="end" />
            </ListItem>
            <ListItem>
              <ListItemText 
                primary="Email Notifications" 
                secondary="Receive email alerts for significant market changes"
              />
              <Switch edge="end" />
            </ListItem>
          </List>
        </Paper>
      </Box>
    </Container>
  );
};

export default SettingsPage;
