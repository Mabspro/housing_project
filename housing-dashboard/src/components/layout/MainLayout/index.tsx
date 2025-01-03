import React, { useState } from 'react';
import {
  AppBar,
  Box,
  CssBaseline,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  TrendingUp as TrendingUpIcon,
  Map as MapIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import Footer from '../Footer';

const drawerWidth = 240;

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();
  const location = useLocation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
    { text: 'Market Trends', icon: <TrendingUpIcon />, path: '/market-trends' },
    { text: 'Regional Analysis', icon: <MapIcon />, path: '/regional-analysis' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' }
  ];

  const drawer = (
    <Box sx={{ height: '100%', bgcolor: 'background.paper' }}>
      <Toolbar sx={{ 
        borderBottom: '1px solid',
        borderColor: 'divider',
        mb: 1
      }}>
        <Typography variant="h6" noWrap component="div" sx={{ 
          fontWeight: 'bold',
          fontSize: { xs: '1.1rem', sm: '1.25rem' },
          color: 'primary.main'
        }}>
          RISE DATA INC
        </Typography>
      </Toolbar>
      <List>
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <ListItem
              button
              key={item.text}
              onClick={() => {
                navigate(item.path);
                if (isMobile) {
                  setMobileOpen(false);
                }
              }}
              selected={isActive}
              sx={{
                mb: 0.5,
                mx: 1,
                borderRadius: 1,
                transition: 'all 0.2s ease',
                '&.Mui-selected': {
                  bgcolor: 'primary.main',
                  color: 'primary.contrastText',
                  '& .MuiListItemIcon-root': {
                    color: 'inherit'
                  },
                  '&:hover': {
                    bgcolor: 'primary.dark'
                  }
                },
                '&:hover': {
                  bgcolor: isActive ? 'primary.dark' : 'action.hover',
                  borderRadius: 1
                }
              }}
            >
              <ListItemIcon sx={{ 
                minWidth: 40,
                color: isActive ? 'inherit' : 'primary.main',
                transition: 'color 0.2s ease'
              }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.text} 
                primaryTypographyProps={{
                  fontSize: '0.95rem',
                  fontWeight: isActive ? 'bold' : 'normal'
                }}
              />
            </ListItem>
          );
        })}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          bgcolor: 'background.paper',
          color: 'text.primary',
          boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
          backdropFilter: 'blur(8px)',
          borderBottom: '1px solid',
          borderColor: 'divider'
        }}
      >
        <Toolbar sx={{ display: 'flex', justifyContent: 'center' }}>
          <IconButton
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ 
              mr: 2,
              position: 'absolute',
              left: 16,
              display: { sm: 'none' },
              color: 'primary.main',
              '&:hover': {
                bgcolor: 'primary.main',
                color: 'primary.contrastText'
              },
              transition: 'all 0.2s ease'
            }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ 
            fontWeight: 'bold',
            fontSize: { xs: '1.1rem', sm: '1.25rem' },
            color: 'primary.main',
            textAlign: 'center'
          }}>
            Market Trends and Statistics
          </Typography>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { 
              boxSizing: 'border-box', 
              width: drawerWidth,
              boxShadow: 3,
              border: 'none'
            },
            '& .MuiBackdrop-root': {
              backdropFilter: 'blur(4px)'
            }
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { 
              boxSizing: 'border-box', 
              width: drawerWidth,
              borderRight: '1px solid',
              borderColor: 'divider',
              boxShadow: 'none'
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          display: 'flex',
          flexDirection: 'column',
          minHeight: '100vh',
          pt: '64px'
        }}
      >
        <Box sx={{ flex: 1, p: { xs: 2, sm: 3 } }}>
          {children}
        </Box>
        <Footer />
      </Box>
    </Box>
  );
};

export default MainLayout;
