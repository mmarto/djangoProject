from django.contrib.auth.models import User
import requests
import base64
import json

class IBWebCustomBackend:
    def authenticate(self, username=None, password=None):
        """twiki: http://websrv3/twiki/bin/view/CustOps/IBCSProgAuthUnification"""
        
        #authUrl = 'http://ibop2/ibcs/tools/ums/ums_auth_app2.php'
        authUrl = 'http://{host}:{port}/LoginApp'.format(host='ibop102', port=9009)

        # usermne = base64.b64encode(username.encode('utf-8')).decode('utf-8')
        # passwd = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        usermne = username
        passwd = password

        credentials = {'user': usermne,  # userMnemonic
                        'password': passwd,   
                        'application': 'SkillMgmt', # applicationMnemonic
                        'mode': None}

        r = requests.post(authUrl, params=credentials)

        res = json.loads(r.text)

        if 'Error' in res:
            print(res['Error'])
            return None
        
        if 'LoginApp' in res:
            if not res['LoginApp']['userAuthenticated']:
                print("User {} doesn't exist.".format(credentials['user']))
                return None        

            if not res['LoginApp']['applicationAuthenticated']:
                print("User {} doesn't have permissions to access {}".format(credentials['application']))
                return None
        else:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
