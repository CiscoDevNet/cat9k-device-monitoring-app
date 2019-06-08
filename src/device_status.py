#!/usr/bin/env python2

"""Sample Device Status Monitoring Application

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Vinay Kini <vikini@cisco.com>, "\
             "Lakshmi Jayanthi <ljayanth@cisco.com>, and "\
             "Kabiraj Sethi <kasethi@cisco.com>"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


from ncclient import manager
import xmltodict
import json
from json2html import *
import cgi;
import cgitb;

# Catalyst 9K switch hostname or IP address
HOSTNAME = "<hostname_or_ip>"

# Catalyst 9K switch Netconf port
PORT = <port_number>

# Catalyst 9K switch login credentials
USERNAME = "<username>"
PASSWORD = "<password>"

# Interface of which status is monitored
INTERFACE_NAME = "GigabitEthernet0/0"


def get_intf_state_data(host, port, user, pwd, intf):
    """Fetch state of the interface from the switch.

    Open a Netconf connection to the switch and fetch
    state of the specified interface.

    Args:
        host (str): Switch hostname or IP address.
        port (str): Switch Netconf port number.
        user (str): Switch login username.
        pwd (str) : Switch login password.
        intf (str): Interface of which state to fetch.

    Returns:
        str: The XML encoded response from the switch.
    
    """

    intf_state_xml = ""

    filter_string = "/interfaces/interface[name='" + intf + "']/state"
    with manager.connect(host=host, port=port, \
                         username=user, password=pwd, \
                         allow_agent=False, look_for_keys=False, \
                         hostkey_verify=False) as m:
        intf_state_xml = m.get(filter=("xpath", filter_string)).data_xml

    return intf_state_xml


def extract_intf_state(intf_state_xml):
    """Save interface state as Python dictionary.

    Convert interface state from XML encoded string to
    a Python dictionary object.

    Args:
        intf_state_xml (str): XML encoded interface state.

    Returns:
        dict: Interface state.
    
    """

    intf_state = xmltodict.parse(intf_state_xml)

    return intf_state


def output_intf_state(intf, intf_state):
    """Output interface state as HTML webpage.

    Generate an HTML webpage displaying interface state
    and providing a Refresh link.

    Args:
        intf (str)       : Interface name.
        intf_state (dict): Interface state dictionary.

    """

    cgitb.enable()

    print "Content-Type: text/html"
    print ""

    print "<h1>Interface " + intf + " Status</h1>"
    print "<a href=\"javascript:window.location.reload(true)\">Refresh</a>"
    print json2html.convert(json.dumps(intf_state))

    return


if __name__ == '__main__':
    intf_state_xml = get_intf_state_data(HOSTNAME, PORT, \
                                         USERNAME, PASSWORD, \
                                         INTERFACE_NAME)
    intf_state = extract_intf_state(intf_state_xml)
    output_intf_state(INTERFACE_NAME, intf_state)

