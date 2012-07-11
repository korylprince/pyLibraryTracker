# -*- coding: utf-8 -*-
#Let everyone log in
auth.settings.login_methods = [ldap_auth(mode='ad',
    bind_dn = 'CN=Admin,OU=Technology Staff,OU=root,DC=example,DC=com',
    bind_pw = 'supersecret',
    server='example.com',
    base_dn='OU=root,DC=example,DC=com')]

def index():
    redirect(URL('user'))

def user():
    response.view = 'default/index.html'
    response.menu = None
    return dict(form=auth.login(next=URL('success')))
    
@auth.requires_login()
def success():
    u,g = findUserAttr(auth.user.username)
    import datetime
    db.logins.insert(name=u,date=datetime.datetime.now(),type=g)
    response.menu = None
    session.auth = None
    response.flash = None
    return dict()
