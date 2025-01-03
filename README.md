# Housing Market Analysis Dashboard

Interactive visualization dashboard for housing market analysis, featuring price trends, growth rates, and market comparisons across different regions.

## Features

- City Trends Chart showing historical price data
- Growth Rates Chart displaying year-over-year changes
- Market Heatmap showing current market performance
- Interactive time series visualizations
- Regional market comparisons
- Statistical insights

## Project Structure

```
housing-project/
├── housing-dashboard/     # Main application directory
│   ├── src/              # React frontend source
│   │   ├── components/   # React components
│   │   └── services/     # API services
│   ├── api/              # FastAPI backend
│   │   ├── main.py      # API endpoints
│   │   └── test_db.py   # Database tests
│   └── public/          # Static assets
├── scripts/             # Data processing scripts
├── models/             # Analysis models
├── notebooks/         # Jupyter notebooks
├── dashboards/        # Generated visualizations
├── data/             # Dataset storage
└── config/          # Configuration files
```

## Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- PostgreSQL database

## Setup

1. Clone the repository:
```bash
git clone https://github.com/[your-username]/housing-project.git
cd housing-project
```

2. Install frontend dependencies:
```bash
cd housing-dashboard
npm install
```

3. Install backend dependencies:
```bash
cd api
pip install -r requirements.txt
```

4. Configure environment variables:
Create `.env` files in both the frontend and API directories:

housing-dashboard/.env:
```
REACT_APP_API_URL=http://localhost:8002
```

housing-dashboard/api/.env:
```
DATABASE_URL=postgresql://[username]:[password]@localhost:5432/housing_db
PORT=8002
```

5. Start the development servers:

Backend:
```bash
cd housing-dashboard/api
uvicorn main:app --reload --port 8002
```

Frontend:
```bash
cd housing-dashboard
npm start
```

The application will be available at http://localhost:3000

## Recent Updates

### API Improvements
- Fixed SQL query syntax and date handling
- Implemented proper date aggregation with CTE
- Added comprehensive error handling and logging
- Configured CORS for frontend communication

### Frontend Configuration
- Updated proxy settings to connect to API port 8002
- Configured proper API base URL
- Resolved port conflicts for development server

### Data Visualization
- City Trends Chart showing historical price data
- Growth Rates Chart displaying YoY changes
- Market Heatmap showing current market performance

## Development

- Frontend: React with TypeScript
- Data Visualization: Plotly.js
- Backend: Python with FastAPI
- Database: PostgreSQL

## Scripts

- `download_dataset.py`: Downloads housing market data
- `transform_load.py`: Processes and loads data into database
- `test_db_connection.py`: Verifies database connectivity
- `run_dev.bat`: Windows script to start development servers

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
