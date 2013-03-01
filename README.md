django-yadal
==
Yet Another Django oAuth Library

After a night and a morning of messing with various oAuth2 libraries and trying too get stuff working with a Django
application, sleep deprivation led me to create django-yadal.

version 0.0.1
Working Google oAuth2 authentication and profile update

License: MIT license

Settings
--
Make sure you define all these in your settings.py or you risk implosion...

*   DECPRECATED: YADAL_LOGIN_SUCCESS use LOGIN_REDIRECT_URL instead!
    Redirect to this URL when login is succesfull
*   YADAL_USER_REQUIRED
    True or False, when True oAuth authentication only works if a user with the correct email addres
    already exists.
*   YADAL_LOGIN_NOT_ALLOWED
    Redirect to this page when login is not allowed because of YADAL_USER_REQUIRED
*   YADAL_ACCESS_DENIED
    Redirect to this page when the user denies access to login via oAuth
*   YADAL_CLIENT_ID
    oAuth2 client ID
*   YADAL_CLIENT_SECRET
    oAuth2 client secreat
*   YADAL_CALLBACK_URL
    Callback URL when returning from oAuth2 provider. For example: http://127.0.0.1:8000/oauth/callback'
*   YADAL_UPDATE_PROFILE
    Update user profile after oAuth login succesful

Easy to copy/paste settings.py template:
    YADAL_CLIENT_ID = '46954009.apps.googleusercontent.com'
    YADAL_CLIENT_SECRET = 'zcLf9IIkYn9vUOYUFt3uU2'
    YADAL_CALLBACK_URL = 'http://127.0.0.1:8000/oauth/callback'
    YADAL_LOGIN_SUCCESS = ''
    YADAL_UPDATE_PROFILE = True
