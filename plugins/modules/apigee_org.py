from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''

'''

EXAMPLES = r'''

'''

from ansible.module_utils.basic import AnsibleModule
import pyapigee

def run_module():
    
    
    module_args = dict(
        method=dict(type='str', choices=['http','https'],required=True),
        mode=dict(type='str', required=False, default='create'),
        adminuser=dict(type='str', required=True),
        adminpwd=dict(type='str', required=True),
        mgmtserver=dict(type='str', required=True),
        orgadmin=dict(type='str', required=True),
        org=dict(type='str', required=True),
        env=dict(type='str', required=True),
        mgmtport=dict(type='str', required=False, default='8080')

    )

    result = dict(
        changed=False,
        org='',
        env='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)
    
    # local variables
    method = module.params['method']
    mode = module.params['mode']
    mgmtserver = module.params['mgmtserver']
    mgmtport = module.params['mgmtport']
    adminuser = module.params['adminuser']
    adminpwd = module.params['adminpwd']
    org = module.params['org']
    env = module.params['env']
    orgadmin = module.params['orgadmin']

    # init apigee object

    apigee = pyapigee.apigee(method,mgmtserver,mgmtport,adminuser,adminpwd)

    if mode == 'create':
        apigee.createOrg(org)
        apigee.associateOrg(org,'gateway')
        apigee.addEnv(org,env)
        apigee.addAdmin(org,orgadmin)
        apigee.addAnalytics(org,env)

    if mode == 'delete':
        envs = apigee.getEnv(org)
        response = apigee.disassociateOrg(org,'gateway')
        for env in envs:
            apigee.deleteEnv(org,env)
        apigee.deleteOrg(org)

    result['message'] = response.text
    result['org'] = org
    result['env'] = env

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
