
z = {
    'url':'', # the CKAN url visible to this script
    'key':'', # the CKAN API key of an admin user
    'orgs':{ # organizations
            'my-org': { # slugified name
                'id':'my-org', # slugified name again
                    'name':'my-org', # slugified name again
                    'title':'My Organization', # display name
                    'description':'Short description of my organization', # description
                    'image_url':'' # see Alias in apache.conf
    },
    'groups': {
        'my-group': {
            'id':'my-group',
            'name':'my-group',
            'title':'My Group',
            'description':'Description of my group',
            'image_url':''
        },
    },
    'users': {
        # admins
        'johndoe-admin': {                            # username
            'name': 'johndoe-admin',                  # username
            'display_name': 'John Doe (Admin)',    # full name
            'fullname': 'John Doe (Admin)',        # full name
            'about': 'Sysadmin', # role
            'email': 'John.Doe@example.com', # DPaW email
            'password': 'reallysecretpassword',  # default
            'sysadmin': True
        },

        # users
        'janedoe': {                            # username
            'name': 'janedoe',                  # username
            'display_name': 'Jane Doe',    # full name
            'fullname': 'Jane Doe',        # full name
            'about': '', # role
            'email': 'Jane.Doe@example.com', # DPaW email
            'password': 'reallysecretpassword',  # default
        },

    },
    'datasets':{
    },
}
