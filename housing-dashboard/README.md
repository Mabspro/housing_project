# Housing Market Analytics Dashboard

A real-time analytics dashboard for tracking U.S. housing market trends and statistics.

## Data Source

This project uses the [U.S. Housing Prices Regional Trends (2000-2023)](https://www.kaggle.com/datasets/praveenchandran2006/u-s-housing-prices-regional-trends-2000-2023) dataset from Kaggle. The dataset provides housing price indices for major metropolitan areas in the United States, with data normalized to a base year (2000 = 100) for comparative analysis.

## Features

- Real-time housing price trend analysis
- Metropolitan area comparisons
- Growth rate visualization
- Market performance heatmaps
- Mobile-responsive design

## Architecture

- Frontend: Deployed on GitHub Pages
- Backend API: Deployed on Vercel (housing-dashboard-api.vercel.app)
- Database: PostgreSQL hosted on Supabase

## Getting Started

1. Clone the repository
```bash
git clone https://github.com/Mabspro/housing_project.git
```

2. Install dependencies
```bash
cd housing-dashboard
npm install
```

3. Start the development server
```bash
npm start
```

## API Documentation

The API documentation is available at:
- Development: http://localhost:8002/docs
- Production: https://housing-dashboard-api.vercel.app/docs

## Built With

- React
- TypeScript
- Material-UI
- Python (FastAPI backend)
- PostgreSQL
