# -*- coding: utf-8 -*-
import ldap

db = DAL('sqlite://storage.sqlite')
from gluon.tools import Crud
crud = Crud(db)

#Generate Grade levels
import datetime                                                                                                                              
year = datetime.datetime.now().year
month = datetime.datetime.now().month
if month > 6:
    year +=1 

grades = ['Pre-K','1st','2nd','3rd','4th','5th','6th','7th','8th','Freshman','Sophomore','Junior','Senior']
i = 12
years = {}
for year in xrange(year,year+13):
    years[str(year)] = grades[i] 
    i -= 1

def findGrade(val, *args):
    if val in years:
        return years[val]
    return val
    
def formatTime(val, *args):
    return val.strftime('%a, %b %d, %Y %I:%M:%S %p')

db.define_table('logins',Field('name'),Field('date','datetime', represent=formatTime),Field('type', represent=findGrade))

# General Auth settings
from gluon.tools import Auth
auth = Auth(db, hmac_key=Auth.get_or_create_key())
auth.define_tables(username=True)
auth.settings.create_user_groups=False
# all we need is login
auth.settings.actions_disabled=['register','change_password','request_reset_password','retrieve_username','profile']
# you don't have to remember me
auth.settings.remember_me_form = False
# ldap authentication and not save password on web2py
from gluon.contrib.login_methods.ldap_auth import ldap_auth

#returns user and parent OU name
def findUserAttr(user):
    server = 'example.com'
    base = 'OU=root,dc=example,dc=com'
    strfilter = '(&(objectClass=person)(sAMAccountName={0}))'.format(user)
    dnuser = 'admin@example.com'
    passwd = 'super secret'
    
    l = ldap.open(server)
    l.simple_bind(dnuser,passwd)
    scope = ldap.SCOPE_SUBTREE
    retrieve_attributes = None
    
    timeout = 0
    result_id = l.search(base, scope, strfilter, retrieve_attributes)
    
    result_set = []
    while 1:
        result_type, result_data = l.result(result_id, timeout)
        if (result_data == []):
            break
        else:
            if result_type == ldap.RES_SEARCH_ENTRY:
                result_set.append(result_data)
    cn = result_set[0][0][0].split(',')
    return cn[0][3:],cn[1][3:]

#wrapper for noneditable grid
def rowTable(query):
    return SQLFORM.grid(query,fields=[db.logins.name,db.logins.date,db.logins.type],searchable=False,search_widget=False,deletable=False,editable=False,create=False,csv=False,details=False,orderby=~db.logins.date)

#creates query from session
def makeQuery():
    query = db.logins.id >0
    if 'name' in session.gridvars.keys():
        query = query & (db.logins.name.contains(session.gridvars['name']))
    if 'type' in session.gridvars.keys():
        query = query & (db.logins.type.contains(session.gridvars['type']))
    if 'start_time' in session.gridvars.keys():
        query = query & (db.logins.date > session.gridvars['start_time'])
    if 'end_time' in session.gridvars.keys():
        query = query & (db.logins.date < session.gridvars['end_time'])
    return query
