from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
import os, sys
import cx_Oracle
sys.path.append(os.path.join(os.environ['HOME'], 'python_lib'))
from utilities import getDbCredentials

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

def rowsToDictList(cursor):
    columns = [i[0] for i in cursor.description]
    return [dict(zip(columns,row)) for row in cursor]

class Command(BaseCommand):
    def handle(self, *args, **options):
        cred = getDbCredentials('ORAUMS')
        conn = cx_Oracle.connect(cred)
        cur = conn.cursor()

        sqlUsers = '''
            SELECT usermnemonic,
              userfirstname,
              userlastname,
              emailidin,
              emailserverin,
              emailidext,
              emailserverext
            FROM ums_user_account
            WHERE status = :status
            and emailidin is not null
            and usermnemonic != 'mhristov'
        '''
        #get all active users
        activeUsersDict = dict()
        cur.execute(sqlUsers, {'status': 1})
        activeUsers = rowsToDictList(cur)
        for user_ in activeUsers:
            activeUsersDict[user_['USERMNEMONIC']] = user_
            user = User.objects.create_user(user_['USERMNEMONIC'], email=user_['EMAILIDIN'] + '@' + user_['EMAILSERVERIN'], password='-', first_name=user_['USERFIRSTNAME'], last_name=user_['USERLASTNAME'])
            user.is_active = True
            user.is_superuser = False
            user.save()
            print('saved {}'.format(user_['USERMNEMONIC']))
            
        #print(len(activeUsersDict))

        #get all inactive users
        inactiveUsersSet = set()
        cur.execute(sqlUsers, {'status': 0})
        inactiveUsers = rowsToDictList(cur)
        for user in inactiveUsers:
            inactiveUsersSet.add(user['USERMNEMONIC'])
        #print(len(inactiveUsersSet))

        #get users in reports viewer

        #remove inactive users
        removedUsersCnt = 0
        reportsViewerUsers = User.objects.all()
        for user in reportsViewerUsers:
            if user.is_superuser: continue
            
            if user.username in inactiveUsersSet:
                print('{} to be removed'.format(user.username))
                removedUsersCnt += 1
                ret = user.delete()
                print(ret)

        print('{} users to be removed'.format(removedUsersCnt))
            
