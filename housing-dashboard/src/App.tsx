// Trigger rebuild with new API URL
import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Dashboard from './pages/Dashboard';
import MarketTrends from './pages/MarketTrends';
import RegionalAnalysis from './pages/RegionalAnalysis';
import Settings from './pages/Settings';
import './App.css';

function App() {
  return (
    <Router>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/market-trends" element={<MarketTrends />} />
          <Route path="/regional-analysis" element={<RegionalAnalysis />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </MainLayout>
    </Router>
  );
}

export default App;
