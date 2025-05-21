from rest_framework import authentication, exceptions
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials
from .models import FirebaseUser

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            id_token = auth_header.split(' ').pop()
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user, created = FirebaseUser.objects.get_or_create(uid=uid, defaults={
            'email': decoded_token.get('email'),
            'display_name': decoded_token.get('name')}),
            return (user, None)
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid Firebase token')
