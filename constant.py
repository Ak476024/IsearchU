# In production environment we should not hard code secrets.

CLIENT_ID = '64326874349-an10pavlelh1nvpumb4ghpkjrhjk4vqt.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'http://localhost:5001/integrations/drive/callback'
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/drive.file']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'
PROJECT_ID= "metrics-324905"
INTEGERATION_NAME= "google-drive"
TOKEN_URI="https://oauth2.googleapis.com/token"
CONFIG={ 
    "web": {
        "client_id": CLIENT_ID,
        "project_id": PROJECT_ID,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": CLIENT_SECRET,
        "redirect_uris": [REDIRECT_URI],
        "javascript_origins": ["http://localhost:8000"]
    }
}