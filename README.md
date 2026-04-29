# Research Paper Tracker

A modern, full-stack web application for managing academic research papers, authors, and topics. Built with Flask, SQLAlchemy, and Azure SQL Database, featuring a professional dark dashboard UI with glassmorphism effects.

## Features

- **Authentication System**: Login/Register with role-based access (admin/viewer)
- **Dashboard**: Interactive charts showing statistics, top authors, and publication trends
- **Papers Management**: CRUD operations, search, filtering, pagination, and CSV export
- **Authors Management**: Card-based grid layout with detailed author profiles
- **Topics Management**: Tag cloud interface for browsing research topics
- **REST API**: JSON endpoints for programmatic access
- **Modern UI**: Dark theme with glassmorphism, responsive design, and smooth animations
- **Bonus Features**: Dark/Light mode toggle, live search, health check endpoint

## Tech Stack

- **Backend**: Python 3.9+, Flask
- **Database**: Azure SQL Database
- **ORM**: SQLAlchemy with pyodbc driver
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Charts**: Chart.js
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Deployment**: Azure App Service compatible

## Project Structure

```
cloud-project/
├── app.py                      # Main application entry point
├── config.py                   # Configuration and environment variables
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .gitignore                  # Git ignore rules
├── models/                     # SQLAlchemy models
│   ├── __init__.py
│   ├── author.py
│   ├── paper.py
│   ├── topic.py
│   └── user.py
├── routes/                     # Flask route blueprints
│   ├── __init__.py
│   ├── auth.py
│   ├── dashboard.py
│   ├── papers.py
│   ├── authors.py
│   ├── topics.py
│   └── api.py
├── templates/                  # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── papers.html
│   ├── paper_detail.html
│   ├── authors.html
│   └── topics.html
└── static/                     # Static assets
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Local Development Setup

### Prerequisites

- Python 3.9 or higher
- Azure SQL Database (or local SQL Server for testing)
- ODBC Driver 18 for SQL Server

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cloud-project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy `.env` file and fill in your Azure SQL Database credentials:
   ```env
   DB_SERVER=your-server.database.windows.net
   DB_NAME=your-database-name
   DB_USER=your-admin-username
   DB_PASSWORD=your-password
   SECRET_KEY=your-secret-key-here
   ```

   Generate a secure SECRET_KEY:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   
   Open your browser and navigate to: `http://localhost:5000`
   
   Default login credentials:
   - **Admin**: username=`admin`, password=`admin123`
   - **Viewer**: username=`viewer`, password=`viewer123`

## Azure Deployment Guide

### Step 1: Create Azure SQL Database

1. Log in to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → Search "SQL Database"
3. Fill in the required fields:
   - **Resource group**: Create or select existing
   - **Database name**: e.g., `research-tracker-db`
   - **Server**: Create new server
     - **Server name**: e.g., `research-tracker-server`
     - **Server admin login**: Your admin username
     - **Password**: Strong password (save this!)
     - **Location**: Choose nearest region
   - **Compute + storage**: Select appropriate tier (Basic/Standard for testing)
4. Click "Review + create" → "Create"
5. Wait for deployment to complete

### Step 2: Configure Firewall Rules

1. Navigate to your SQL Database in Azure Portal
2. Click "Set server firewall" under Security
3. Add your current IP address (or use "Allow Azure services" for testing)
4. Click "Save"

### Step 3: Get Connection String

1. In your SQL Database overview, click "Connection strings"
2. Copy the "ODBC" connection string
3. Extract the server name, database name, username, and password

### Step 4: Create Azure App Service

1. In Azure Portal, click "Create a resource" → Search "Web App"
2. Fill in the required fields:
   - **Resource group**: Same as database
   - **App name**: e.g., `research-tracker-app` (must be unique)
   - **Runtime stack**: Python 3.9 or 3.10
   - **Region**: Same as database
   - **Pricing tier**: Free F1 or Basic B1 for testing
3. Click "Review + create" → "Create"

### Step 5: Deploy Application

#### Option A: Using Azure CLI (Recommended)

1. Install Azure CLI and login:
   ```bash
   az login
   ```

2. Create a deployment user (if not exists):
   ```bash
   az webapp deployment user set --user-name <username> --password <password>
   ```

3. Initialize git in your project:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. Deploy to Azure:
   ```bash
   az webapp up --name research-tracker-app --resource-group <resource-group-name> --runtime "PYTHON:3.9"
   ```

#### Option B: Using Visual Studio Code

1. Install "Azure App Service" extension
2. Right-click your project folder → "Deploy to Web App"
3. Follow the prompts to select your subscription and app
4. Click "Deploy"

#### Option C: Using Local Git

1. In Azure Portal, navigate to your App Service
2. Click "Deployment Center" → "Local Git"
3. Copy the Git clone URL
4. In your project:
   ```bash
   git remote add azure <git-clone-url>
   git push azure master
   ```

### Step 6: Configure Environment Variables

1. In Azure Portal, navigate to your App Service
2. Click "Configuration" → "Application settings"
3. Add the following settings:
   - `DB_SERVER`: your Azure SQL server name
   - `DB_NAME`: your database name
   - `DB_USER`: your SQL admin username
   - `DB_PASSWORD`: your SQL admin password
   - `SECRET_KEY`: generate a secure random key
4. Click "Save"

### Step 7: Configure Startup Command

1. In App Service, click "Configuration" → "General settings"
2. Set "Startup command" to:
   ```
   gunicorn --bind=0.0.0.0 --timeout 600 app:app
   ```
3. Click "Save"

### Step 8: Monitor Deployment

1. In App Service, click "Log Stream" to view real-time logs
2. Navigate to your app URL to verify it's working
3. Check that database tables are created and seeded

### Step 9: Enable HTTPS (Optional but Recommended)

1. In App Service, click "TLS/SSL settings"
2. Click "Add certificate" → "Create free App Service Managed Certificate"
3. Enable "HTTPS Only" in TLS/SSL settings

## Database Schema

### Authors
- `author_id` (Primary Key)
- `name`
- `email` (Unique)
- `university`
- `country`
- `created_at`

### Papers
- `paper_id` (Primary Key)
- `title`
- `abstract`
- `journal_name`
- `publication_date`
- `citations`
- `status` (Published, Under Review, Draft)
- `author_id` (Foreign Key)
- `created_at`

### Topics
- `topic_id` (Primary Key)
- `topic_name` (Unique)

### Paper_Topics (Many-to-Many)
- `paper_id` (Foreign Key)
- `topic_id` (Foreign Key)

### Users
- `user_id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `role` (admin, viewer)
- `created_at`

## API Endpoints

### Papers
- `GET /api/papers` - Get all papers
- `GET /api/papers/<id>` - Get single paper

### Authors
- `GET /api/authors` - Get all authors

### Statistics
- `GET /api/stats` - Get dashboard statistics

### Health Check
- `GET /health` - Check database connectivity

## Development Notes

### Database Migrations

The application uses `db.create_all()` for simplicity. For production, consider using Flask-Migrate:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Adding New Features

1. Add models in `models/` directory
2. Create routes in `routes/` directory
3. Register blueprint in `app.py`
4. Add templates in `templates/` directory
5. Add styles in `static/css/style.css`

### Testing

To run tests (if you add them):
```bash
pytest
```

## Troubleshooting

### Database Connection Issues

- Verify firewall rules allow your IP
- Check ODBC driver is installed (ODBC Driver 18 for SQL Server)
- Ensure connection string format is correct
- Check SQL server is running

### Deployment Issues

- Check App Service logs in Log Stream
- Verify environment variables are set correctly
- Ensure startup command is configured
- Check Python version compatibility

### Common Errors

**"Login timeout expired"**: Check firewall rules and network connectivity

**"Cannot open server"**: Verify server name and credentials in connection string

**"Module not found"**: Ensure all dependencies are in requirements.txt

## Security Considerations

- Change default admin password immediately after deployment
- Use strong SECRET_KEY in production
- Enable HTTPS only in production
- Restrict database access to Azure services only
- Regularly update dependencies
- Implement rate limiting for API endpoints

## Performance Optimization

- Add database indexes on frequently queried columns
- Implement caching for dashboard statistics
- Use connection pooling for database connections
- Optimize SQL queries with proper joins
- Consider CDN for static assets in production

## License

This project is created for academic purposes. Please use responsibly.

## Support

For issues or questions, please contact the development team or check the Azure documentation:
- [Azure App Service Documentation](https://docs.microsoft.com/azure/app-service/)
- [Azure SQL Database Documentation](https://docs.microsoft.com/azure/sql-database/)

## Acknowledgments

- Flask Framework
- SQLAlchemy ORM
- Chart.js for data visualization
- Azure Cloud Services
