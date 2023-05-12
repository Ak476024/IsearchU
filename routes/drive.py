import os
from flask import  request, redirect, session, jsonify, url_for, Blueprint
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import urllib.parse
from extensions import db
import constant
from models import Integrations

drive_bp = Blueprint('drive', __name__)

@drive_bp.post('/integrations/drive')
def create_integration():
    integration = Integrations(name=constant.INTEGERATION_NAME,access_token='',refresh_token='')
    db.session.add(integration)
    db.session.commit()
    return {}

@drive_bp.get('/integrations/drive')
def get_integration():
    integration= db.session.query(Integrations).filter(Integrations.name == constant.INTEGERATION_NAME).first()
    try:
        credentials = Credentials(**{'token': integration.access_token,
            'refresh_token': integration.refresh_token,
            'token_uri': constant.TOKEN_URI,
            'client_id': constant.CLIENT_ID,
            'client_secret': constant.CLIENT_SECRET,
            'scopes': constant.SCOPES}
            )
        drive = build(
            constant.API_SERVICE_NAME, constant.API_VERSION, credentials=credentials)
        files = drive.files().list(
            pageSize=1,
            fields="nextPageToken, files(id, name, webContentLink, size, iconLink)").execute()
    except Exception as err:
        return {"status": False}
    return {"status": True}

@drive_bp.get('/integrations/drive/authorize')
def authorize():
    # redirect to the OAuth2 consent screen
    flow = Flow.from_client_config(constant.CONFIG,
                                    scopes=constant.SCOPES,
                                    )
    flow.redirect_uri = url_for('drive.oauth2callback', _external=True)
    auth_url, state = flow.authorization_url(prompt="consent", access_type='offline',include_granted_scopes='true')
    session['state'] = state
    return {'url':auth_url}

@drive_bp.get('/integrations/drive/callback')
def oauth2callback():
    # exchange the authorization code for access and refresh tokens
    parsed_url = urllib.parse.urlparse(request.url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    code = query_params['code'][0]

    flow = Flow.from_client_config(constant.CONFIG,
                                    scopes=constant.SCOPES,
                                    state = session['state'])
    flow.redirect_uri = url_for('drive.oauth2callback', _external=True)
    flow.fetch_token(code=code)
    credentials = flow.credentials

    integration= db.session.query(Integrations).filter(Integrations.name == constant.INTEGERATION_NAME).first()
    integration.access_token = credentials.token
    integration.refresh_token = credentials.refresh_token
    db.session.merge(integration)
    db.session.commit()

    # build the Google Drive API client
    service = build( constant.API_SERVICE_NAME, constant.API_VERSION, credentials=credentials)
    # make a request to the Google Drive API
    service.files().list(
        pageSize=10,
        orderBy='modifiedTime',
        fields="nextPageToken, files(id, name, webContentLink, size)"
    ).execute()
    return redirect('http://localhost:3000')


@drive_bp.get('/integrations/drive/files')
def get_files():
    args = request.args
    q = args.get("q", default="", type=str)
    integration= db.session.query(Integrations).filter(Integrations.name == constant.INTEGERATION_NAME).first()

    credentials = Credentials(**{'token': integration.access_token,
            'refresh_token': integration.refresh_token,
            'token_uri': constant.TOKEN_URI,
            'client_id': constant.CLIENT_ID,
            'client_secret': constant.CLIENT_SECRET,
            'scopes': constant.SCOPES}
            )
    drive = build(
        constant.API_SERVICE_NAME, constant.API_VERSION, credentials=credentials)
    files = drive.files().list(
        q=f"name contains '{q}'", 
        pageSize=30,
        fields="nextPageToken, files(id, name, webContentLink, size, iconLink)").execute()
    return jsonify(**files)
    
@drive_bp.post('/integrations/drive/upload')
def upload_file():
    try:
        file = request.files['file']
        filename = file.filename
        mimetype = file.mimetype

        # Save the file to a temporary location on the server
        file_path = os.path.join('./upload', filename)
        file.save(file_path)
        

        # Load credentials from the session.
        integration= db.session.query(Integrations).filter(Integrations.name == constant.INTEGERATION_NAME).first()

        credentials = Credentials(**{'token': integration.access_token,
            'refresh_token': integration.refresh_token,
            'token_uri': constant.TOKEN_URI,
            'client_id': constant.CLIENT_ID,
            'client_secret': constant.CLIENT_SECRET,
            'scopes': constant.SCOPES}
            )
        drive = build(
        constant.API_SERVICE_NAME, constant.API_VERSION, credentials=credentials)
        # Upload the file to Google Drive
        file_metadata = {'name': filename, 'parents': ''}
        media = MediaFileUpload(file_path, mimetype=mimetype)
        file = drive.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return {'status': True}

    except HttpError as error:
        print(f'An error occurred: {error}')
        return {'status': False}