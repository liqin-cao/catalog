#!/usr/bin/env python

# OAuth helper class for user registration and authentication
from flask import session as login_session
from flask import make_response, jsonify, flash
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import random
import string


# Check to see if the user is an authorized logged in user.
def authenticated():
    if 'username' not in login_session:
        return False
    else:
        return True


# Revoke a current user's token and reset their login_session
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            google_disconnect()
            del login_session['gplus_id']
            del login_session['credentials']

        if login_session['provider'] == 'facebook':
            facebook_disconnect()
            del login_session['facebook_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']


# OAuth login via google
def google_connect(request):
    # CSRF is generically handled by csrf_protect()

    # Obtain authorization credentials
    print('Obtain authorization credentials: {}'.format(request.data))
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            '/var/www/catalog/catalog/google_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the credentials access token is valid
    print('Verify that the credentials access token is valid: {}'.format(
        credentials.access_token))
    access_token = credentials.access_token
    url = '{}?access_token={}'.format(
        'https://www.googleapis.com/oauth2/v1/tokeninfo',
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user
    print("""Verify that the access token is used for the
        intended user: {}""".format(credentials.id_token['sub']))
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match give user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    GOOGLE_CLIENT_ID = json.loads(
        open('/var/www/catalog/catalog/google_client_secrets.json', 'r').read())['web']['client_id']
    print('Verify that the access token is valid for this app: {}'.format(
        GOOGLE_CLIENT_ID))
    if result['issued_to'] != GOOGLE_CLIENT_ID:
        response = make_response(json.dumps(
            "Token's client ID doesn't match app's."), 401)
        print("Token's client ID doesn't match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    print('Check to see if user is already logged in')
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    print('Store user login credentials for later use')
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    print('Get user info')
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print("Login info: {}".format(data))

    login_session['provider'] = 'google'
    if 'email' in data:
        login_session['email'] = data['email']
    if 'picture' in data:
        login_session['picture'] = data['picture']
    if 'name' in data:
        login_session['username'] = data['name']
    else:
        login_session['username'] = data['email']

    return None


# Revoke a current goole user's token
def google_disconnect():
    # Only disconnect a connected user.
    print('Verify that the user is connected.')
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is None:
        response = make_response(json.dumps(
            'Current user is not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = json.loads(stored_credentials) 
    print('Stored credentials: {}'.format(stored_credentials))
    print('Stored gplus_id : {}'.format(stored_gplus_id))

    # Execute HTTP GET request to revoke current token.
    access_token = stored_credentials['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
        access_token)
    h = httplib2.Http()
    print('Revoke current token request: {}'.format(url))
    result = h.request(url, 'GET')[0]
    print('Revoke current token response: {}'.format(result))

    if result['status'] == '200':
        # Reset the user's session.
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the give token was invalid.
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# OAuth login via Facebook
def facebook_connect(request):
    # CSRF is generically handled by csrf_protect()

    # Verify that the access token is received
    access_token = request.data
    print('Verify that the access token is received: {}'.format(access_token))

    # Verify that the access token is valid for this app.
    FACEBOOK_APP_ID = json.loads(
        open('/var/www/catalog/catalog/fb_client_secrets.json', 'r').read())['web']['app_id']
    FACEBOOK_APP_SECRET = json.loads(
        open('/var/www/catalog/catalog/fb_client_secrets.json', 'r').read())['web']['app_secret']
    print('Verify that the access token is valid for this app: {}-{}'.format(
        FACEBOOK_APP_ID, FACEBOOK_APP_SECRET))
    url = '{}?{}&client_id={}&client_secret={}&fb_exchange_token={}'.format(
        'https://graph.facebook.com/oauth/access_token',
        'grant_type=fb_exchange_token',
        FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, access_token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we
        have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replace
        the remaining quotes with nothing so that it can be used directly in
        the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token={}&{}'.format(
        token, 'fields=name,id,email')
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    print('Use token to get user info from API: {}'.format(url))

    # Print user info
    data = json.loads(result)
    print("Login info: {}".format(data))

    login_session['provider'] = 'facebook'
    if 'email' in data:
        login_session['email'] = data['email']
    if 'id' in data:
        login_session['facebook_id'] = data['id']
    if 'name' in data:
        login_session['username'] = data['name']
    else:
        login_session['username'] = data['email']

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = '{}?access_token={}&{}'.format(
        'https://graph.facebook.com/v2.8/me/picture',
        token,
        'redirect=0&height=200&width=200')
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]
    return None


# Revoke a current facebook user's token
def facebook_disconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/{}/permissions?access_token={}'.format(
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]

    response = make_response(json.dumps('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
