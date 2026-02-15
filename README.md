# flask-react-boilerplate

A full-stack web application built with Flask (backend) and React (frontend) for managing cybersecurity insurance-related operations.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Database Setup](#database-setup)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [Development Guidelines](#development-guidelines)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.9 or higher) - [Download](https://www.python.org/)
- **PostgreSQL** (v12 or higher) - [Download](https://www.postgresql.org/)
- **Git** - [Download](https://git-scm.com/)

### Verify Installation

```bash
# Check Node.js version
node --version
npm --version

# Check Python version
python --version

# Check PostgreSQL version
psql --version
```

## Project Structure

```
flask-react-boilerplate/
├── backend/
│   ├── .venv/                 # Virtual environment (auto-created)
│   ├── public/                # Frontend build output & static files
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration settings
│   ├── .env                   # Environment variables
│   ├── requirements.txt       # Python dependencies
│   ├── migrations/            # Alembic migrations
│   └── ...
├── frontend/
│   ├── src/
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── .env                   # Frontend environment variables (optional)
│   └── ...
└── README.md                  # This file
```

## Database Setup

### Create PostgreSQL Database

1. **Open PostgreSQL command line (psql)**

   On Windows:
   ```bash
   psql -U postgres
   ```

2. **Create the database and user**

   ```sql
   -- Create the database
   CREATE DATABASE flask-react-boilerplate;

   -- Create the user/role
   CREATE USER flask-react-boilerplate WITH PASSWORD 'flask-react-boilerplate_pass';

   -- Grant privileges
   ALTER ROLE flask-react-boilerplate SET client_encoding TO 'utf8';
   ALTER ROLE flask-react-boilerplate SET default_transaction_isolation TO 'read committed';
   ALTER ROLE flask-react-boilerplate SET default_transaction_deferrable TO on;
   ALTER ROLE flask-react-boilerplate SET default_transaction_read_only TO off;
   GRANT ALL PRIVILEGES ON DATABASE flask-react-boilerplate TO flask-react-boilerplate;

   -- Exit psql
   \q
   ```

3. **Verify the connection**

   ```bash
   psql -U flask-react-boilerplate -d flask-react-boilerplate -h localhost -W
   # Enter password: flask-react-boilerplate_pass
   ```

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Create .env File

Create a `.env` file in the `backend/` directory with the following content:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
DATABASE_URL=postgresql://flask-react-boilerplate:flask-react-boilerplate_pass@localhost:5432/flask-react-boilerplate

# PostgreSQL Connection Details
DB_HOST=localhost
DB_PORT=5432
DB_NAME=flask-react-boilerplate
DB_USER=flask-react-boilerplate
DB_PASSWORD=flask-react-boilerplate_pass
```

### Step 5: Initialize Database (First Time)

```bash
# Create Alembic migrations directory (if not already present)
alembic init -t async migrations

# Create an initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations to the database
alembic upgrade head
```

### Step 6: Install Backend Dependencies (if requirements.txt not yet created)

Create `backend/requirements.txt`:

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.0
alembic==1.13.1
psycopg2-binary==2.9.9
```

Then install:

```bash
pip install -r requirements.txt
```

### Step 7: Run Backend Server

```bash
# Make sure virtual environment is activated
flask run

# Server will run on http://localhost:5000
```

## Frontend Setup

### Step 1: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Create .env File (Optional)

Create a `.env` file in the `frontend/` directory if needed:

```env
VITE_API_URL=http://localhost:5000
VITE_APP_TITLE=Cyberitance
```

### Step 4: Configure Vite for Backend Integration

The Vite configuration (`vite.config.js`) should be set to build into the backend's public folder:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../backend/public',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
```

### Step 5: Run Frontend Development Server

```bash
npm run dev

# Server will run on http://localhost:5173 (or another port if 5173 is busy)
```

### Step 6: Build Frontend for Production

```bash
npm run build

# Output will be generated in backend/static/
```

## Running the Application

### Development Mode (Two Terminals)

#### Terminal 1 - Backend:

```bash
cd backend
.venv\Scripts\activate   # (on Windows)
# source .venv/bin/activate  # (on macOS/Linux)
flask run
```

#### Terminal 2 - Frontend:

```bash
cd frontend
npm run dev
```

Visit:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

### Production Mode

1. **Build the frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Run the backend** (it will serve the built frontend from `backend/public`)
   ```bash
   cd backend
   .venv\Scripts\activate   # (on Windows)
   flask run
   ```

3. Visit: http://localhost:5000

## Technology Stack

### Backend
- **Framework**: Flask 3.0+
- **ORM**: SQLAlchemy 3.1+
- **Migrations**: Alembic 1.13+
- **Database**: PostgreSQL 12+
- **Environment Management**: python-dotenv

### Frontend
- **Framework**: React
- **State Management**: Redux
- **Routing**: React Router DOM
- **Build Tool**: Vite
- **UI Library**: Chakra UI v3
- **Package Manager**: npm

## Development Guidelines

### Backend Development

1. **Database Migrations**
   ```bash
   # Create a new migration
   alembic revision --autogenerate -m "Description of changes"

   # Apply migrations
   alembic upgrade head

   # Revert last migration
   alembic downgrade -1
   ```

2. **Install Python Packages**
   ```bash
   # Activate virtual environment first
   pip install package-name
   pip freeze > requirements.txt  # Update requirements file
   ```

3. **Virtual Environment Management**
   ```bash
   # Activate
   .venv\Scripts\activate       # Windows
   source .venv/bin/activate    # macOS/Linux

   # Deactivate
   deactivate
   ```

### Frontend Development
0. **Creating the vite react app**
   ```bash
   npm create vite@latest frontend -- --template react
   #follow the onscreen instructions
   
   #install dependecies
   npm install redux react-redux @reduxjs/toolkit react-router-dom @chakra-ui/react @emotion/react @emotion/styled framer-motion

   

   ```
   

1. **Install JavaScript Packages**
   ```bash
   npm install package-name
   ```

2. **Update Dependencies**
   ```bash
   npm update
   npm outdated  # Check for outdated packages
   ```

3. **Code Quality**
   ```bash
   npm run lint      # If configured
   npm run format    # If configured
   ```

### Common Commands Summary

```bash
# Backend - Setup and run
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask run

# Frontend - Setup and run
cd frontend
npm install
npm run dev

# Frontend - Build
npm run build

# Frontend - Preview production build
npm run preview
```

## Troubleshooting

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -U cyberitance -d cyberitance -h localhost -W

# If port 5432 is in use, check PostgreSQL service status on Windows:
# - Check Services (services.msc) for PostgreSQL entry
# - Or reinstall PostgreSQL with a different port
```

### Virtual Environment Issues

```bash
# Remove and recreate virtual environment
rmdir /s .venv          # Windows: Remove directory
python -m venv .venv    # Recreate
.venv\Scripts\activate  # Activate
pip install -r requirements.txt
```

### Port Already in Use

- Flask default: 5000 → Change with: `flask run --port 8000`
- Vite default: 5173 → Will automatically use next available port

### npm/pip Issues

```bash
# Clear cache and reinstall
npm cache clean --force && npm install
pip cache purge && pip install -r requirements.txt
```

## License

MIT License - Modify as needed

## Support

For issues or questions, please refer to the official documentation:
- Flask: https://flask.palletsprojects.com/
- React: https://react.dev/
- Vite: https://vitejs.dev/
- Redux: https://redux.js.org/
- Chakra UI: https://v3.chakra-ui.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Alembic: https://alembic.sqlalchemy.org/
