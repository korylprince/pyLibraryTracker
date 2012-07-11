# coding: utf8
#Fix authentication paths
auth.settings.controller = 'check'
auth.settings.login_url = URL('check','user')
auth.settings.login_next = URL('check','index')
auth.settings.logout_next = URL('check','user')

#Only let staff log in
auth.settings.login_methods = [ldap_auth(mode='ad',
    allowed_groups = ['Domain Staff'], #group name 
    bind_dn = 'CN=Admin,OU=Technology Staff,OU=root,DC=example,DC=com',
    bind_pw = 'supersecret',
    group_dn = 'OU=Domain Groups,OU=root,DC=example,DC=com',
    group_name_attrib = 'cn',
    group_member_attrib = 'member',
    group_filterstr = 'objectClass=Group',
    server='example.com',
    base_dn='OU=root,DC=example,DC=com')]

response.title = "Library Logins"

@auth.requires_login()
def index():
    #get last id then select 10 before
    try:
        lastid = db(db.logins).select().last().id
    except AttributeError:
        # no logins yet                                                                                                                      
        return dict(form=DIV("No Records"))
    query = db.logins.id > lastid-10
    form = rowTable(query)
    return dict(form=form)

def user():
    if auth.is_logged_in() and len(request.args) == 0:
        redirect(URL('index'))
    response.subtitle = "Please Log In"
    return dict(form=auth())

@auth.requires_login()
def search():
    form = SQLFORM.factory(Field('name'),Field('start_time','datetime'),Field('end_time','datetime'),Field('type'))
    if form.process().accepted:
        #we don't want blank entries
        for k,v in request.post_vars.items():
            if v == '' or v is None:
                del request.post_vars[k]
        if len(request.post_vars.values()) == 2:
            response.flash = 'You must specify at least one parameter'
        else:
            response.flash = ''
            session.gridvars = {}
            if 'name' in request.post_vars.keys():
                session.gridvars['name'] = form.vars.name
            if 'type' in request.post_vars.keys():
                session.gridvars['type'] = form.vars.type
            if 'start_time' in request.post_vars.keys():
                session.gridvars['start_time'] = form.vars.start_time
            if 'end_time' in request.post_vars.keys():
                session.gridvars['end_time'] = form.vars.end_time
            redirect(URL('result'))
    return dict(form=form)
    
@auth.requires_login()
def result():
    if session.gridvars is not None:
        return dict(grid=rowTable(makeQuery()))
    else:
        redirect(URL('search'))
