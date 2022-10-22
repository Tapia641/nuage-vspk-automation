"""
author: luis.e.hernande.ext@nokia.com
version: 0.1
date: 10/22/2022
"""

import argparse
import csv
import time
import logging
import yaml



try:
    # YOUR VSD RELEASE
    from vspk import v6 as vsdk # <------------------------- VSD RELEASE
    from vspk.utils import set_log_level

    # CHOSE THE LOG LEVEL
    # set_log_level(logging.INFO)
    set_log_level(logging.WARNING)
    # set_log_level(logging.DEBUG)
    # set_log_level(logging.ERROR)

except ImportError:
    logging.error(f'Verify your Nuage Release or install the vspk packet [pip install vspk or pip3 install vspk].')
    logging.error(f'For more information, check \'https://pypi.org/project/vspk/\'')
    exit(-1)

class API():

    #SLOTS FOR THE CLASS
    __slots__ = ['nusession', 'enterprises']

    def nuage_login(self):

        #READ KEYS
        stream = open(r'keys.yml', 'r')
        yaml_info = yaml.load(stream, Loader=yaml.FullLoader)
        nuage = yaml_info['nuage']

        #DO THE LOGIN
        session = vsdk.NUVSDSession(
            username=nuage['user'],
            password=nuage['password'],
            enterprise=nuage['organization'],
            api_url=f"https://{nuage['vsd']}" 
        )

        #USE THE REST API
        try:
            logging.info('Establishing session to VSD %s as User %s', vsdhost, user)
            session.start()
            logging.info('Logged to VSD successfully')
        except:
            logging.error('Failed to start a Session to VSD')
            exit(-1)
        nusession = session.user

    def get_enterprises(self):
        logging.info('Getting list of Enterprises')
        # enterprises = self.nusession.enterprises.get()

        # GET TOTAL ENTEPRISES WITHOUT LIMIT (ONLY MEMORY)
        page_number = -1
        enterprises_collected = []
        while True:
            page_number += 1
            enterprieses_tmp = self.nusession.bgp_neighbors.get(page=page_number, page_size=100)
            if len(enterprieses_tmp) == 0:
                break
            else:
                enterprises_collected += enterprieses_tmp  
        
        logging.info(f"Enterprises' total: {len(enterprises_collected)}")

        # for enterprise in enterprises:

nuage = API()
nuage.nuage_login()
nuage.get_enterprises()

# def configure_log(log_level=logging.INFO):
#     # Logging settings
#     configuration = {}
#     configuration['log_file'] = None
#     # log_level = logging.DEBUG
#     # log_level = logging.INFO
#     # log_level = logging.WARNING

#     logging.basicConfig(
#         filename=configuration['log_file'], format='%(asctime)s %(levelname)s %(message)s', level=log_level)
#     logger = logging.getLogger(__name__)

# def login():
#     # COLOMBIA
#     nc = vsdk.NUVSDSession(username='csproot', password='TqHe38cJEuhjfnY',
#                            enterprise='csp', api_url="https://localhost:8443")
#     # ARGENTINA
#     # nc = vsdk.NUVSDSession(username='csproot', password='20TelCO20ClouD', enterprise='csp', api_url="https://nvsd.cbamosp.claro.amx:8443")
#     nc.start()
#     return nc.user


# def compare_l2(nuage_user, domain_name):

#     # L2 VPORTS -----------------------------------------------------------------------------------------------
#     enterprise = nuage_user.enterprises.get_first(filter='name is "NFV-C-VNF"')
#     domain = enterprise.domains.get_first(
#         filter=f'name is "{domain_name}"')
    
#     #L3 VPORTS -----------------------------------------------------------------------------------------------
#     l3_info = {
#     'ldap_authorization_enabled' : domain.ldap_authorization_enabled ,
#     'ldap_enabled' : domain.ldap_enabled ,
#     'bgp_enabled' : domain.bgp_enabled ,
#     'dhcp_lease_interval' : domain.dhcp_lease_interval ,
#     'vnf_management_enabled' : domain.vnf_management_enabled ,
#     'name' : domain.name ,
#     'last_updated_by' : domain.last_updated_by,
#     'last_updated_date' : domain.last_updated_date ,
#     'web_filter_enabled' : domain.web_filter_enabled,
#     'receive_multi_cast_list_id' : domain.receive_multi_cast_list_id,
#     'send_multi_cast_list_id' : domain.send_multi_cast_list_id ,
#     'description' : domain.description ,
#     'shared_enterprise' : domain.shared_enterprise ,
#     'threat_intelligence_enabled' : domain.threat_intelligence_enabled ,
#     'threat_prevention_management_enabled' : domain.threat_prevention_management_enabled ,
#     'dictionary_version' : domain.dictionary_version,
#     'virtual_firewall_rules_enabled' : domain.virtual_firewall_rules_enabled ,
#     'allow_advanced_qos_configuration' : domain.allow_advanced_qos_configuration ,
#     'allow_gateway_management' : domain.allow_gateway_management,
#     'allow_trusted_forwarding_class' : domain.allow_trusted_forwarding_class,
#     'allowed_forwarding_classes' : domain.allowed_forwarding_classes ,
#     'allowed_forwarding_mode' : domain.allowed_forwarding_mode,
#     'floating_ips_quota' : domain.floating_ips_quota ,
#     'floating_ips_used' : domain.floating_ips_used ,
#     'blocked_page_text' : domain.blocked_page_text,
#     'flow_collection_enabled' : domain.flow_collection_enabled,
#     'embedded_metadata' : domain.embedded_metadata ,
#     'enable_application_performance_management' : domain.enable_application_performance_management ,
#     'encryption_management_mode' : domain.encryption_management_mode ,
#     'enterprise_profile_id' : domain.enterprise_profile_id,
#     'enterprise_type' : domain.enterprise_type,
#     'entity_scope' : domain.entity_scope,
#     'local_as' : domain.local_as ,
#     'forwarding_class' : domain.forwarding_class ,
#     'creation_date' : domain.creation_date ,
#     'use_global_mac' : domain.use_global_mac,
#     'associated_enterprise_security_id' : domain.associated_enterprise_security_id ,
#     'associated_group_key_encryption_profile_id' : domain.associated_group_key_encryption_profile_id ,
#     'associated_key_server_monitor_id' : domain.associated_key_server_monitor_id,
#     'customer_id' : domain.customer_id,
#     'avatar_data' : domain.avatar_data,
#     'avatar_type' : domain.avatar_type,
#     'owner' : domain.owner ,
#     'external_id' : domain.external_id,
#     }
#     dump = yaml.dump(l3_info, default_flow_style=False,
#                      allow_unicode=True, encoding=None)
#     print(dump)

# configure_log()
# nuage_user = login()
# compare_l3(nuage_user, "EPDG02MEG_dataSwitchFabric_2_SubNet")