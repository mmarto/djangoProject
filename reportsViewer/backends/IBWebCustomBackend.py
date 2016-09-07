from django.contrib.auth.models import User
import requests
import base64
import xml.etree.ElementTree as ET

class IBWebCustomBackend:
    def authenticate(self, username=None, password=None):
        
        roleList = list()
        errors = list()

        authUrl = 'http://ibop2/ibcs/tools/ums/ums_auth_app2.php'

        usermne = base64.b64encode(username.encode('utf-8')).decode('utf-8')
        passwd = base64.b64encode(password.encode('utf-8')).decode('utf-8')

        credentials = {'usermnemonic': usermne, 'password': passwd, 'appmnemonic': 'SkillMgmt'}
        r = requests.get(authUrl, params=credentials)

        try:
            root = ET.fromstring(r.text)
            app = root.find('app')
            if app:
                for roleid in app.findall('approleid'):
                    roleList.append(roleid.attrib['id'])
            for error in root.findall('error'):
                errors.append(error.attrib['text'])
        except ET.ParseError as e:
            print('Not an xml document or not well formed xml: '.format(r.text))
            print('{}'.format(e))
            return None
        
        if len(errors) > 0:
            print(','.join(errors))
            return None
        
        if len(roleList) == 0:
            print('No permission to access')
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
