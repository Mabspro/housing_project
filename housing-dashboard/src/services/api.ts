const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8002/api';

// Interfaces for historical data
export interface HistoricalTrendsData {
  date: string[];
  values: { [city: string]: number[] };
}

export interface HistoricalGrowthData {
  date: string[];
  values: { [city: string]: number[] };
}

// Interfaces for current market data
export interface MarketTrendsData {
  date: string[];
  values: { [city: string]: number[] };
}

export interface MarketGrowthData {
  date: string[];
  values: { [market: string]: number[] };
}

export interface MarketHeatmapData {
  markets: string[];
  growthRates: number[];
}

// Historical data API calls (Dashboard)
export const fetchHistoricalTrends = async (): Promise<HistoricalTrendsData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/city-trends`);
    if (!response.ok) {
      throw new Error('Failed to fetch historical trends data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching historical trends:', error);
    throw error;
  }
};

export const fetchHistoricalGrowth = async (): Promise<HistoricalGrowthData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/growth-rates`);
    if (!response.ok) {
      throw new Error('Failed to fetch historical growth data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching historical growth:', error);
    throw error;
  }
};

// Current market data API calls (Market Trends)
export const fetchMarketTrends = async (): Promise<MarketTrendsData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/market-trends`);
    if (!response.ok) {
      throw new Error('Failed to fetch market trends data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching market trends:', error);
    throw error;
  }
};

export const fetchMarketGrowth = async (): Promise<MarketGrowthData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/market-growth`);
    if (!response.ok) {
      throw new Error('Failed to fetch market growth data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching market growth:', error);
    throw error;
  }
};

export const fetchMarketHeatmap = async (): Promise<MarketHeatmapData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/market-heatmap`);
    if (!response.ok) {
      throw new Error('Failed to fetch market heatmap data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching market heatmap:', error);
    throw error;
  }
};

export const api = {
  // Historical data (Dashboard)
  fetchHistoricalTrends,
  fetchHistoricalGrowth,
  // Current market data (Market Trends)
  fetchMarketTrends,
  fetchMarketGrowth,
  fetchMarketHeatmap,
};

export default api;
