from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
import json
import urllib2, urllib

OAUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
OAUTH_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
OAUTH_RESPONSE_TYPE = 'code'
OAUTH_SCOPE = 'https://www.googleapis.com/auth/userinfo.profile+https://www.googleapis.com/auth/userinfo.email'
OAUTH_STATE = '/profile'

URL = "{0}?response_type={1}&client_id={2}&redirect_uri={3}&scope={4}&state={5}".format(
    OAUTH_ENDPOINT,
    OAUTH_RESPONSE_TYPE,
    settings.YADAL_CLIENT_ID,
    settings.YADAL_CALLBACK_URL,
    OAUTH_SCOPE,
    OAUTH_STATE
)

def _get_access_token(request, code):
    post_data = {
        'code': code,
        'client_id': settings.YADAL_CLIENT_ID,
        'client_secret': settings.YADAL_CLIENT_SECRET,
        'redirect_uri': settings.YADAL_CALLBACK_URL,
        'grant_type': 'authorization_code',
        }
    req = urllib2.Request(OAUTH_TOKEN_ENDPOINT, urllib.urlencode(post_data))
    result = urllib2.urlopen(req)
    content = result.read()
    content = json.loads(content)
    if not content.has_key('access_token'):
        # TODO: handle error
        pass
    return _get_user_info(request, content['access_token'])

def _get_user_info(request, token):
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
    URL = "{0}?access_token={1}".format(
        USER_INFO_URL,
        token
    )
    req = urllib2.Request(URL)
    result = urllib2.urlopen(req)
    content = result.read()
    content = json.loads(content)
    return _handle_user_login(request, content)

def _handle_user_login(request, user_data):
    """Handles a user login that happened via oAuth

    TODO: Based on settings: allow creating of new users via oAuth login
        See if we already have a user with a similar email address, otherwise create a user

    TODO: send signal to allow catching of user data by other code
    """
    try:
        # TODO: only handle users with verified_email: True
        u = User.objects.get(email__exact=user_data['email'])
        authenticate()
    except ObjectDoesNotExist:
        if settings.YADAL_USER_REQUIRED:
            return HttpResponseRedirect(settings.YADAL_LOGIN_NOT_ALLOWED)
        else:
            # Registration of new users through oAuth is allowed, create a suitable user object
            u = User(username=user_data['email'], email=user_data['email'])
            u.save()

    if settings.YADAL_UPDATE_PROFILE:
        # Update profile based on values
        u.first_name = user_data['given_name']
        u.last_name = user_data['family_name']
        u.save()

    u.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, u)

    # Redirect to YADAL_LOGIN_SUCCESS
    return HttpResponseRedirect(settings.YADAL_LOGIN_SUCCESS)

def oauth(request):
    """Handle a request to login via an oAuth2 provider

    TODO: dynamic handling of oAuth2 provider via url parameter
        /login/google/          oauth(request, 'google')
        /login/twitter/         oauth(request, 'twitter')
            Should be possible if no provider fucked up responses too much....
    """
    return HttpResponseRedirect(URL)

def oauth_callback(request):
    error = request.GET.get('error', None)
    code = request.GET.get('code', None)
    token = request.GET.get('access_token', None)
    if error:
        return HttpResponseRedirect(settings.YADAL_ACCESS_DENIED)
    elif code:
        return _get_access_token(request, code)