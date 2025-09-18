# Keyword Generator Backend

FastAPI backend for generating SEM keywords using Cohere AI.

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Setup environment variables:
```bash
# Create .env file and add your Cohere API key
echo "COHERE_API_KEY=your_cohere_api_key_here" > .env
# Get your API key from: https://dashboard.cohere.com/api-keys
```

4. Run the server:
```bash
python main.py
```

The API will be available at: http://localhost:8000

## API Endpoints

- `GET /` - Health check
- `POST /api/keyword-list` - Generate keywords

## Documentation

Interactive API documentation available at: http://localhost:8000/docs
