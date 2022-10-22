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
    __slots__ = ['nuage_user', 'enterprises']

    def nuage_login(self):

        #READ KEYS
        stream = open(r'keys.yml', 'r')
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

nuage = API()
nuage.nuage_login()
nuage.get_enterprises()