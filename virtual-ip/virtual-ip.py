"""
author: luis.e.hernande.ext@nokia.com
version: 0.1
date: 10/22/2022

comments:

"""

import argparse
from array import array
import csv,sys
import time
import logging
import yaml



try:
    # YOUR VSD RELEASE
    from vspk import v6 as vsdk # <------------------------- VSD RELEASE

    # CHOSE THE LOG LEVEL
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO,
                        datefmt="%H:%M:%S")
    # logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.WARNING,
    #                     datefmt="%H:%M:%S")
    # logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.DEBUG,
    #                     datefmt="%H:%M:%S")
    # logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.ERROR,
    #                     datefmt="%H:%M:%S")

except ImportError:
    logging.error(f'Verify your Nuage Release or install the vspk packet [pip install vspk or pip3 install vspk].')
    logging.error(f'For more information, check \'https://pypi.org/project/vspk/\'')
    exit(-1)

class API():

    #SLOTS FOR THE CLASS
    __slots__ = ['nuage_user', 'enterprises', 'csv_info']

    def nuage_login(self):

        #READ KEYS
        stream = open(r'../keys.yml', 'r')
        yaml_info = yaml.load(stream, Loader=yaml.FullLoader)
        nuage = yaml_info['nuage']

        #DO THE LOGIN
        logging.info(f"https://{nuage['vsd']}" )
        session = vsdk.NUVSDSession(
            username=nuage['user'],
            password=nuage['password'],
            enterprise=nuage['organization'],
            api_url=f"https://{nuage['vsd']}" 
        )
        #USE THE REST API
        try:
            logging.info(f"Establishing session to VSD {nuage['vsd']} as {nuage['user']}")
            session.start()
            logging.info('Logged to VSD successfully')
        except:
            logging.error('Failed to start a Session to VSD')
            exit(-1)
        self.nuage_user = session.user

    def get_enterprises(self):
        logging.info('Getting list of Enterprises')

        # GET TOTAL ENTEPRISES WITHOUT LIMIT (ONLY MEMORY)
        page_number = -1
        enterprises_collected = []
        while True:
            page_number += 1
            enterprieses_tmp = self.nuage_user.enterprises.get(page=page_number, page_size=100)
            if enterprieses_tmp is None:
                break
            else:
                enterprises_collected += enterprieses_tmp  
        
        logging.info(f"Enterprises' total: {len(enterprises_collected)}")
        self.enterprises = enterprises_collected

    @staticmethod
    def find_by_name(name:str, elements:list):
        for element in elements:
            if name == element.name:
                return element
        return None

    def read_csv(self):

        #READ THE FILE NAME
        filename = 'virtual-ip.csv'

        try:
            with open(filename, newline='', mode='r', encoding='utf-8-sig') as f:

                #WITH DICTREADER WE HAVE ROWS WITH COLUMNS
                reader = csv.DictReader(f)
                self.csv_info = reader

                for row in self.csv_info:
                    if row['VSD Managed'] == 'YES':

                        #GET ENTERPRISE BY NAME
                        enterprise_name = 'NFV-C-VNF'
                        enterprise = self.nuage_user.enterprises.get_first(filter='name is "'+enterprise_name+'"')
                        
                        #GET DOMAIN BY NAME
                        domain_name = row['Domain Name']
                        domain_l3 = enterprise.domains.get_first(filter='name is "'+domain_name+'"')
                        logging.info(f'WORKING OVER THE DOMAIN: {domain_name}')
                     
                        #GET SUBNET BY NAME
                        subnet_name = row['Subnet Name']
                        subnet = domain_l3.subnets.get_first(filter='name is "'+subnet_name+'"')
                        logging.info(f'WITH SUBNET: {subnet_name}')
                        
                        #GET VPORTS BY SUBNET
                        if subnet is not None:
                            print(f"------------------------{domain_name}:{subnet_name}---------------------------")
                            vports = subnet.vports.get()
                            if len(vports) > 0:
                                for vport in vports:
                                    virtual_ips = vport.virtual_ips.get()
                                    if len(virtual_ips) > 0: 
                                        print(f"------------------------VPORT INFORMATION:---------------------------")
                                        vm = vport.vms.get_first()

                                        print(f"NAME:{vport.name} Address_Spoofing:{vport.address_spoofing}")
                                        print(f"VM NAME: {vm.name}")
                                        for item, interfaz in enumerate(vm.interfaces):
                                            if interfaz['VPortName'] == vport.name:
                                                print(f"IP: {vm.interfaces[item]['IPAddress']} GATEWAY: {vm.interfaces[item]['gateway']} MAC:{vm.interfaces[item]['MAC']} STATUS:{vm.status}")
                                        print(f"vIPS:")
                                        for virtual_ip in virtual_ips:
                                            print(virtual_ip.virtual_ip,  virtual_ip.mac, virtual_ip.subnet_id)
                                        print('')
                                    else:
                                        print("SUBNET {subnet_name} WITHOUT vIPs.")
                                print(f"------------------------{domain_name}:{subnet_name}---------------------------")
                            else:
                                print("SUBNET {subnet_name} WITHOUT VPORTS.")
                        else:
                            logging.info(f'WE DONT HAVE VPORTS IN {subnet_name}')  
        except csv.Error as e:
            logging.error(f"Error with {filename} while trying to open.")
            sys.exit(-1)


if __name__ == '__main__':
    nuage = API()
    nuage.nuage_login()
    nuage.read_csv()