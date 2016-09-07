from django.contrib.auth.models import User
from imaplib import IMAP4

class ImapCustomBackend:
    def authenticate(self, username=None, password=None):
        if '@' in username:
            try:
                c = IMAP4('smail100')
                c.login(username.split('@')[0], password)
                c.logout()
            except IMAP4.error as e:
                print(e)
                return None
        else:
            return None
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
