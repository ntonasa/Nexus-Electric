import base64
import binascii
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions, HTTP_HEADER_ENCODING
from rest_framework.authtoken.models import Token

def get_authorization_header(request):
    auth = request.META.get('HTTP_X_OBSERVATORY_AUTH', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth

class NexusTokenAuthentication(authentication.BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "X-OBERVATORY-AUTH"
    HTTP header.  For example:

        X-OBERVATORY-AUTH: 401f7ac837da42b97f613d789819ff93537bee6a
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).strip()

        if not auth:
            return None

        try:
            token = auth.decode()
        except UnicodeError:
            msg = _('Invalid token. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)