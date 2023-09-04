import PySimpleGUI as sg
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Tk
from tkinter.filedialog import asksaveasfile
import ctypes
from vmanage.api.authentication import Authentication
from vmanage.api.central_policy import CentralPolicy
from vmanage.api.cluster import Cluster
from vmanage.api.device_templates import DeviceTemplates
from vmanage.api.device import Device
from vmanage.api.feature_templates import FeatureTemplates
from vmanage.api.local_policy import LocalPolicy
from vmanage.api.monitor_network import MonitorNetwork
from vmanage.api.policy_definitions import PolicyDefinitions
from vmanage.api.policy_lists import PolicyLists
from vmanage.api.policy_updates import PolicyUpdates
from vmanage.api.security_policy import SecurityPolicy

icon = b'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'
MAX_N_SHOW_ITEM = 1000
Authenticated = False
sg.theme('Reddit')

ctypes.windll.shcore.SetProcessDpiAwareness(True)

def collapse(layout, key):
    return sg.pin(sg.Column(layout, key=key))

collapse_authentication = [
    [
        sg.Input('devnetuser', key='user', size=(16,0)),
        sg.Input('RG!_Yw919_83', key='password', size=(27,0), password_char='*'),
        sg.Input('sandbox-sdwan-2.cisco.com', key='host', size=(40,0)),
        sg.Button('Authenticate')
    ]
]

collapse_central_policy = [
    [sg.Button('Central Policy')]
]

collapse_cluster = [
    [
        sg.Button('Cluster Connected Devices'),
        sg.Text('vmanage_cluster_ip'),
        sg.Input(key='get_cluster_connected_devices_list_ip', size=(25,0))
    ],
    [sg.Button('Cluster Health Details')],
    [sg.Button('Cluster Health Status')],
    [sg.Button('Cluster List')],
    [sg.Button('Cluster IP Addresses')],
    [sg.Button('Cluster Ready State')],
    [sg.Button('Cluster Node Properties')],
    [sg.Button('Cluster Tenancy Mode')],
    [
        sg.Button('Cluster vManage Details'),
        sg.Text('vmanage_cluster_ip'),
        sg.Input(key='get_cluster_health_details_list_ip', size=(25,0))
    ]
]

collapse_device_templates = [
    [sg.Button('Device Templates')],
    [
        sg.Button('Device Template'),
        sg.Text('template_id'),
        sg.Input(key='get_device_template_object_template_id', size=(25,0))
    ],
    [
        sg.Button('Template Attachments'),
        sg.Text('template_id'),
        sg.Input(key='get_template_attachments_template_id', size=(25,0)),
        sg.Text('key'),
        sg.Input('host-name', key='get_template_attachments_key', size=(25,0))
    ],
    [
        sg.Button('Template Input'),
        sg.Text('template_id'),
        sg.Input(key='get_template_input_template_id', size=(25,0)),
        sg.Text('device_id_list'),
        sg.Input(key='get_template_input_device_id_list', size=(25,0)),
    ],
    [
        sg.Button('Attachments'),
        sg.Text('template_id'),
        sg.Input(key='get_attachments_template_id', size=(25,0)),
        sg.Text('key'),
        sg.Input('host-name', key='get_attachments_key', size=(25,0))
    ],
    [
        sg.Button('Device Running Config'),
        sg.Text('uuid'),
        sg.Input(key='get_device_running_config_uuid', size=(25,0))
    ],

]

collapse_device = [
    [
        sg.Button('Device List'),
        sg.Text('category'),
        sg.Combo(['vedges', 'controllers'], default_value='vedges', key='device_device_type')
    ],
    [
        sg.Button('Device Status'),
        sg.Text('key'),
        sg.Combo(['deviceId', 'system-ip', 'host-name', 'reachability', 'status', 'personality', 'device-type', 'timezone', 'device-groups', 'lastupdated', 'bfdSessionsUp', 'domain-id', 'board-serial',   'certificate-validity', 'max-controllers', 'uuid', 'bfdSessions', 'controlConnections', 'device-model', 'version', 'connectedVManages', 'site-id', 'ompPeers', 'latitude', 'longitude', 'isDeviceGeoData', 'platform', 'uptime-date', 'statusOrder', 'device-os', 'validity', 'state', 'state_description', 'model_sku', 'local-system-ip', 'total_cpu_count', 'linux_cpu_count', 'testbed_mode', 'layoutLevel'], default_value='system-ip', key='device_status_key'),
        sg.Text('value'),
        sg.Input(key='device_status_value', size=(25,0))
    ],
    [
        sg.Button('Device Config'),
        sg.Text('category'),
        sg.Combo(['vedges', 'controllers'], default_value='vedges', key='device_config_device_type'),
        sg.Text('key'),
        sg.Combo(['deviceType', 'serialNumber', 'uuid', 'managementSystemIP', 'chasisNumber', 'configOperationMode', 'deviceModel', 'deviceState', 'validity', 'vedgeCertificateState', 'personality',  'lifeCycleRequired', 'expirationDate', 'hardwareCertSerialNumber', 'subjectSerialNumber', 'resourceGroup', 'id', 'tags', 'draftMode'], key='device_config_key'),
        sg.Text('value'),
        sg.Input(key='device_config_value', size=(25,0))
    ]
]

collapse_feature_templates = [
    [sg.Button('Feature Templates')],
    [
        sg.Button('Device Templates for Feature'),
        sg.Text('templateId'),
        sg.Input(key='get_device_templates_for_feature_templateId', size=(25,0))
    ]
]

collapse_local_policy = [
    [sg.Button('Local Policy')]
]

collapse_monitor_network_misc = [
    [sg.Button('Device Type'),sg.Text('system_ip'),sg.Input(key='_get_device_type_system_ip', size=(25,0))],
    [sg.Button('AAA Users'),sg.Text('system_ip'),sg.Input(key='get_aaa_users_system_ip', size=(25,0))],
    [sg.Button('ARP Table'),sg.Text('system_ip'),sg.Input(key='get_arp_table_system_ip', size=(25,0))],
    [sg.Button('Interface VPN'),sg.Text('system_ip'),sg.Input(key='get_interface_vpn_system_ip', size=(25,0))],
    [sg.Button('Security Information'),sg.Text('system_ip'),sg.Input(key='get_security_information_system_ip',  size=(25,0))],
    [sg.Button('Software'),sg.Text('system_ip'),sg.Input(key='get_software_system_ip', size=(25,0))],
    [sg.Button('VRRP'),sg.Text('system_ip'),sg.Input(key='get_vrrp_system_ip', size=(25,0))]
]

collapse_monitor_network_bfd = [
    [sg.Button('BFD History'),sg.Text('system_ip'),sg.Input(key='get_bfd_history_system_ip', size=(25,0))],
    [sg.Button('BFD Links'),sg.Text('system_ip'),sg.Input(key='get_bfd_links_system_ip', size=(25,0))],
    [sg.Button('BFD Sessions'),sg.Text('system_ip'),sg.Input(key='get_bfd_sessions_system_ip', size=(25,0))],
    [sg.Button('BFD Device State'),sg.Text('system_ip'),sg.Input(key='get_bfd_device_state_system_ip', size=(25,0))],
    [sg.Button('BFD Device State TLOC'),sg.Text('system_ip'),sg.Input(key='get_bfd_device_state_tloc_system_ip', size=(25,0))],
    [sg.Button('BFD Summary'),sg.Text('system_ip'),sg.Input(key='get_bfd_summary_system_ip', size=(25,0))],
    [sg.Button('BFD TLOC'),sg.Text('system_ip'),sg.Input(key='get_bfd_tloc_system_ip', size=(25,0))]
]

collapse_monitor_network_bgp = [
    [sg.Button('BGP Neighbors'),sg.Text('system_ip'),sg.Input(key='get_bgp_neighbors_system_ip', size=(25,0))],
    [sg.Button('BGP Routes'),sg.Text('system_ip'),sg.Input(key='get_bgp_routes_system_ip', size=(25,0))],
    [sg.Button('BGP Summary'),sg.Text('system_ip'),sg.Input(key='get_bgp_summary_system_ip', size=(25,0))]
]

collapse_monitor_network_cellular = [
    [sg.Button('Cellular Connections'),sg.Text('system_ip'),sg.Input(key='get_cellular_connections_system_ip', size=(25,0))],
    [sg.Button('Cellular Hardware'),sg.Text('system_ip'),sg.Input(key='get_cellular_hardware_system_ip', size=(25,0))],
    [sg.Button('Cellular Modems'),sg.Text('system_ip'),sg.Input(key='get_cellular_modems_system_ip', size=(25,0))],
    [sg.Button('Cellular Networks'),sg.Text('system_ip'),sg.Input(key='get_cellular_networks_system_ip', size=(25,0))],
    [sg.Button('Cellular Profiles'),sg.Text('system_ip'),sg.Input(key='get_cellular_profiles_system_ip', size=(25,0))],
    [sg.Button('Cellular Radios'),sg.Text('system_ip'),sg.Input(key='get_cellular_radios_system_ip', size=(25,0))],
    [sg.Button('Cellular Sessions'),sg.Text('system_ip'),sg.Input(key='get_cellular_sessions_system_ip', size=(25,0))],
    [sg.Button('Cellular Status'),sg.Text('system_ip'),sg.Input(key='get_cellular_status_system_ip', size=(25,0))]
]

collapse_monitor_network_control = [
    [sg.Button('Control Affinity Config'),sg.Text('system_ip'),sg.Input(key='get_control_affinity_config_system_ip', size=(25,0))],
    [sg.Button('Control Affinity Status'),sg.Text('system_ip'),sg.Input(key='get_control_affinity_status_system_ip', size=(25,0))],
    [sg.Button('Control Connections'),sg.Text('system_ip'),sg.Input(key='get_control_connections_system_ip', size=(25,0))],
    [sg.Button('Control Connections History'),sg.Text('system_ip'),sg.Input(key='get_control_connections_history_system_ip', size=(25,0))],
    [sg.Button('Control Count'),sg.Text('system_ip'),sg.Input(key='get_control_count_system_ip', size=(25,0))],
    [sg.Button('Control Links'),sg.Text('system_ip'),sg.Input(key='get_control_links_system_ip', size=(25,0))],
    [sg.Button('Control Local Properties'),sg.Text('system_ip'),sg.Input(key='get_control_local_properties_system_ip', size=(25,0))],
    [sg.Button('Control Summary'),sg.Text('system_ip'),sg.Input(key='get_control_summary_system_ip', size=(25,0))],
    [sg.Button('Control Valid Devices'),sg.Text('system_ip'),sg.Input(key='get_control_valid_devices_system_ip', size=(25,0))],
    [sg.Button('Control Valid Vsmarts'),sg.Text('system_ip'),sg.Input(key='get_control_valid_vsmarts_system_ip', size=(25,0))],
    [sg.Button('Control WAN Interface'),sg.Text('system_ip'),sg.Input(key='get_control_wan_interface_system_ip', size=(25,0))],
    [sg.Button('Control WAN Interface Color'),sg.Text('system_ip'),sg.Input(key='get_control_wan_interface_color_system_ip', size=(25,0))]
]

collapse_monitor_network_device = [
    [sg.Button('Device Status'),sg.Text('system_ip'),sg.Input(key='get_device_status_system_ip', size=(25,0))],
    [sg.Button('Device System Info'),sg.Text('system_ip'),sg.Input(key='get_device_system_info_system_ip', size=(25,0))]
]

collapse_monitor_network_dhcp = [
    [sg.Button('DHCP Clients'),sg.Text('system_ip'),sg.Input(key='get_dhcp_clients_system_ip', size=(25,0))],
    [sg.Button('DHCP Interfaces'),sg.Text('system_ip'),sg.Input(key='get_dhcp_interfaces_system_ip', size=(25,0))],
    [sg.Button('DHCP Servers'),sg.Text('system_ip'),sg.Input(key='get_dhcp_servers_system_ip', size=(25,0))]
]

collapse_monitor_network_dot1x = [
    [sg.Button('dot1x Clients'),sg.Text('system_ip'),sg.Input(key='get_dot1x_clients_system_ip', size=(25,0))],
    [sg.Button('dot1x Interfaces'),sg.Text('system_ip'),sg.Input(key='get_dot1x_interfaces_system_ip', size=(25,0))],
    [sg.Button('dot1x RADIUS'),sg.Text('system_ip'),sg.Input(key='get_dot1x_radius_system_ip', size=(25,0))]
]

collapse_monitor_network_hardware = [
    [sg.Button('Hardware Alarms'),sg.Text('system_ip'),sg.Input(key='get_hardware_alarms_system_ip', size=(25,0))],
    [sg.Button('Hardware Environment'),sg.Text('system_ip'),sg.Input(key='get_hardware_environment_system_ip', size=(25,0))],
    [sg.Button('Hardware Inventory'),sg.Text('system_ip'),sg.Input(key='get_hardware_inventory_system_ip', size=(25,0))],
    [sg.Button('Hardware Status Summary'),sg.Text('system_ip'),sg.Input(key='get_hardware_status_summary_system_ip', size=(25,0))],
    [sg.Button('Hardware System'),sg.Text('system_ip'),sg.Input(key='get_hardware_system_system_ip', size=(25,0))]
]

collapse_monitor_network_ip = [
    [sg.Button('IP FIB'),sg.Text('system_ip'),sg.Input(key='get_ip_fib_system_ip', size=(25,0))],
    [sg.Button('IP Route Table'),sg.Text('system_ip'),sg.Input(key='get_ip_route_table_system_ip', size=(25,0))],
    [sg.Button('IP NAT Translations'),sg.Text('system_ip'),sg.Input(key='get_ip_nat_translations_system_ip', size=(25,0))],
    [sg.Button('IP NAT64 Translations'),sg.Text('system_ip'),sg.Input(key='get_ip_nat64_translations_system_ip', size=(25,0))]
]

collapse_monitor_network_omp = [
    [sg.Button('OMP Peers'),sg.Text('system_ip'),sg.Input(key='get_omp_peers_system_ip', size=(25,0))],
    [sg.Button('OMP Routes Received'),sg.Text('system_ip'),sg.Input(key='get_omp_routes_received_system_ip', size=(25,0))],
    [sg.Button('OMP Routes Advertised'),sg.Text('system_ip'),sg.Input(key='get_omp_routes_advertised_system_ip', size=(25,0))],
    [sg.Button('OMP Summary'),sg.Text('system_ip'),sg.Input(key='get_omp_summary_system_ip', size=(25,0))]
]

collapse_monitor_network_orchestrator = [
    [sg.Button('Orchestrator Summary'),sg.Text('system_ip'),sg.Input(key='get_orchestrator_summary_system_ip', size=(25,0))],
    [sg.Button('Orchestrator Connections'),sg.Text('system_ip'),sg.Input(key='get_orchestrator_connections_system_ip', size=(25,0))],
    [sg.Button('Orchestrator Connections History'),sg.Text('system_ip'),sg.Input(key='get_orchestrator_connections_history_system_ip', size=(25,0))],
    [sg.Button('Orchestrator Local Properties'),sg.Text('system_ip'),sg.Input(key='get_orchestrator_local_properties_system_ip', size=(25,0))]
]

collapse_monitor_network_ospf = [
    [sg.Button('OSPF Interfaces'),sg.Text('system_ip'),sg.Input(key='get_ospf_interfaces_system_ip', size=(25,0))],
    [sg.Button('OSPF Neighbors'),sg.Text('system_ip'),sg.Input(key='get_ospf_neighbors_system_ip', size=(25,0))],
    [sg.Button('OSPF Routes'),sg.Text('system_ip'),sg.Input(key='get_ospf_routes_system_ip', size=(25,0))],
    [sg.Button('OSPF Database'),sg.Text('system_ip'),sg.Input(key='get_ospf_database_system_ip', size=(25,0))],
    [sg.Button('OSPF Database Summary'),sg.Text('system_ip'),sg.Input(key='get_ospf_database_summary_system_ip', size=(25,0))],
    [sg.Button('OSPF Process'),sg.Text('system_ip'),sg.Input(key='get_ospf_process_system_ip', size=(25,0))],
    [sg.Button('OSPF Database External'),sg.Text('system_ip'),sg.Input(key='get_ospf_database_external_system_ip', size=(25,0))]
]

collapse_monitor_network = [
    [sg.Text('Misc ' + '_'*96, enable_events=True, key='collapse_monitor_network_misc_text')],
    [collapse(collapse_monitor_network_misc, 'collapse_monitor_network_misc')],
    [sg.Text('BFD ' + '_'*97, enable_events=True, key='collapse_monitor_network_bfd_text')],
    [collapse(collapse_monitor_network_bfd, 'collapse_monitor_network_bfd')],
    [sg.Text('BGP ' + '_'*97, enable_events=True, key='collapse_monitor_network_bgp_text')],
    [collapse(collapse_monitor_network_bgp, 'collapse_monitor_network_bgp')],
    [sg.Text('Cellular ' + '_'*92, enable_events=True, key='collapse_monitor_network_cellular_text')],
    [collapse(collapse_monitor_network_cellular, 'collapse_monitor_network_cellular')],
    [sg.Text('Control ' + '_'*93, enable_events=True, key='collapse_monitor_network_control_text')],
    [collapse(collapse_monitor_network_control, 'collapse_monitor_network_control')],
    [sg.Text('Device ' + '_'*94, enable_events=True, key='collapse_monitor_network_device_text')],
    [collapse(collapse_monitor_network_device, 'collapse_monitor_network_device')],
    [sg.Text('DHCP ' + '_'*96, enable_events=True, key='collapse_monitor_network_dhcp_text')],
    [collapse(collapse_monitor_network_dhcp, 'collapse_monitor_network_dhcp')],
    [sg.Text('dot1x ' + '_'*95, enable_events=True, key='collapse_monitor_network_dot1x_text')],
    [collapse(collapse_monitor_network_dot1x, 'collapse_monitor_network_dot1x')],
    [sg.Text('Hardware ' + '_'*92, enable_events=True, key='collapse_monitor_network_hardware_text')],
    [collapse(collapse_monitor_network_hardware, 'collapse_monitor_network_hardware')],
    [sg.Text('IP ' + '_'*98, enable_events=True, key='collapse_monitor_network_ip_text')],
    [collapse(collapse_monitor_network_ip, 'collapse_monitor_network_ip')],
    [sg.Text('OMP ' + '_'*97, enable_events=True, key='collapse_monitor_network_omp_text')],
    [collapse(collapse_monitor_network_omp, 'collapse_monitor_network_omp')],
    [sg.Text('Orchestrator ' + '_'*88, enable_events=True, key='collapse_monitor_network_orchestrator_text')],
    [collapse(collapse_monitor_network_orchestrator, 'collapse_monitor_network_orchestrator')],
    [sg.Text('OSPF ' + '_'*96, enable_events=True, key='collapse_monitor_network_ospf_text')],
    [collapse(collapse_monitor_network_ospf, 'collapse_monitor_network_ospf')]
]

collapse_policy_definitions = [
    [sg.Button('Definition Types')],
    [
        sg.Button('Policy Definition'),
        sg.Text('definition_type'),
        sg.Input(key='get_policy_definition_definition_type', size=(25,0)),
        sg.Text('definition_id'),
        sg.Input(key='get_policy_definition_definition_id', size=(25,0))
    ]
]

collapse_policy_lists = [
    [sg.Button('Data Prefix List')],
    [sg.Button('Policy List All')],
    [
        sg.Button('Policy List by Name'),
        sg.Text('policy_list_name'),
        sg.Input(key='get_policy_list_by_name_policy_list_name', size=(25,0))
    ],
    [
        sg.Button('Policy List by ID'),
        sg.Text('policy_list_id'),
        sg.Input(key='get_policy_list_by_id_policy_list_id', size=(25,0))
    ]
]

collapse_policy_updates = [
    [
        sg.Button('Device IDs'),
        sg.Text('template_id'),
        sg.Input(key='get_device_ids_template_id', size=(25,0))
    ],
    [
        sg.Button('Device Inputs'),
        sg.Text('template_id'),
        sg.Input(key='get_device_inputs_template_id', size=(25,0)),
        sg.Text('device_ids'),
        sg.Input(key='get_device_inputs_device_ids', size=(25,0))
    ],
    [
        sg.Button('Policy ID'),
        sg.Text('policy_type'),
        sg.Input(key='get_policy_id_policy_type', size=(25,0)),
        sg.Text('policy_name'),
        sg.Input(key='get_policy_id_policy_name', size=(25,0))
    ],
    [
        sg.Button('Policy Definition'),
        sg.Text('policy_type'),
        sg.Input(key='get_policy_definition_policy_type', size=(25,0)),
        sg.Text('policy_id'),
        sg.Input(key='get_policy_definition_policy_id', size=(25,0))
    ]
]

collapse_security_policy = [
    [sg.Button('Get Security Policy')], 
    [
        sg.Button('Get Security Definition'),
        sg.Text('definition'),
        sg.Combo(['zonebasedfw','urlfiltering','intrusionprevention', 'advancedMalwareProtection', 'dnssecurity'], key='security_policy_defintion')
    ]
]

layout = [
    #vmanage.api.authentication
    [sg.Text('Authentication ' + '_'*88, enable_events=True, key='collapse_authentication_text')],
    [collapse(collapse_authentication, 'collapse_authentication')],

    #vmanage.api.central_policy
    [sg.Text('Central Policy ' + '_'*88, enable_events=True, key='collapse_central_policy_text', )],
    [collapse(collapse_central_policy, 'collapse_central_policy')],

    #vmanage.api.cluster
    [sg.Text('Cluster ' + '_'*95, enable_events=True, key='collapse_cluster_text')],
    [collapse(collapse_cluster, 'collapse_cluster')],

    #vmanage.api.device_templates
    [sg.Text('Device Templates ' + '_'*86, enable_events=True, key='collapse_device_templates_text')],
    [collapse(collapse_device_templates, 'collapse_device_templates')],

    #vmanage.api.device
    [sg.Text('Device ' + '_'*96, enable_events=True, key='collapse_device_text')],
    [collapse(collapse_device, 'collapse_device')],

    #vmanage.api.feature_templates
    [sg.Text('Feature Templates ' + '_'*85, enable_events=True, key='collapse_feature_templates_text')],
    [collapse(collapse_feature_templates, 'collapse_feature_templates')],

    #vmanage.api.local_policy
    [sg.Text('Local Policy ' + '_'*90, enable_events=True, key='collapse_local_policy_text')],
    [collapse(collapse_local_policy, 'collapse_local_policy')],

    #vmanage.api.monitor_network
    [sg.Text('Monitor Network ' + '_'*87, enable_events=True, key='collapse_monitor_network_text')],
    [collapse(collapse_monitor_network, 'collapse_monitor_network')],

    #vmanage.api.policy_definitions
    [sg.Text('Policy Definitions ' + '_'*84, enable_events=True, key='collapse_policy_definitions_text')],
    [collapse(collapse_policy_definitions, 'collapse_policy_definitions')],

    #vmanage.api.policy_lists
    [sg.Text('Policy Lists ' + '_'*90, enable_events=True, key='collapse_policy_lists_text')],
    [collapse(collapse_policy_lists, 'collapse_policy_lists')],

    #vmanage.api.policy_updates
    [sg.Text('Policy Updates ' + '_'*88, enable_events=True, key='collapse_policy_updates_text')],
    [collapse(collapse_policy_updates, 'collapse_policy_updates')],

    #vmanage.api.security_policy
    [sg.Text('Security Policy ' + '_'*87, enable_events=True, key='collapse_security_policy_text')],
    [collapse(collapse_security_policy, 'collapse_security_policy')]
]

def paste():
    focus_element = window.find_element_with_focus()
    try:
        focus_element.Widget.delete('sel.first', 'sel.last')
    except:
        focus_element.Widget.insert('insert', focus_element.Widget.clipboard_get())

class JSONTreeFrame(ttk.Frame):
    def __init__(self, master, json_data=None):
        super().__init__(master)
        self.master = master
        self.tree = ttk.Treeview(self, show='tree')
        self.create_widgets()
        self.set_table_data_from_json(json_data)
        self.tree.bind('<Button-3>', self.copy)
        self.tree.bind('<Button-2>', self.export)

    def copy(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            curItem = self.tree.focus()
            item_dict = self.tree.item(curItem)
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(item_dict.get('text'))
            r.update()
            r.destroy()
        else:
            pass

    def export(self, event):
        file = asksaveasfile(initialfile='Untitled.json', filetypes=[('JSON Files','*.json'),('All Files','*.*')])
        if file != None:
            file.write(str(json_data))
            file.close()

    def create_widgets(self):
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        ysb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def insert_node(self, parent, key, value):
        node = self.tree.insert(parent, 'end', text=key, open=False)
        if value is None:
            return
        if type(value) in (list, tuple):
            for index, item in enumerate(value[:MAX_N_SHOW_ITEM]):
                self.insert_node(node, index, item)
        elif isinstance(value, dict):
            for key, item in value.items():
                self.insert_node(node, key, item)
        else:
            self.tree.insert(node, 'end', text=value, open=False)

    def set_table_data_from_json(self, json_data):
        assert type(json_data) in (list, dict)
        self.delete_all_nodes()
        self.insert_nodes(json_data)

    def delete_all_nodes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def insert_nodes(self, data):
        parent = ''
        if isinstance(data, list):
            for index, value in enumerate(data):
                self.insert_node(parent, index, value)
        elif isinstance(data, dict):
            for (key, value) in data.items():
                self.insert_node(parent, key, value)

def view_data(title, json_data=None):
    root: Tk = tk.Tk()
    #style = ttk.Style(root)
    #style.configure("Treeview", background="#394A6D", foreground="#ABFFB3")
    root.geometry('1280x720')
    root.title(title + ' - vManage APy Viewer')
    root.iconbitmap(icon)
    app = JSONTreeFrame(root, json_data=json_data)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()

def move_center(window):
    screen_width, screen_height = window.get_screen_dimensions()
    win_width, win_height = window.size
    x, y = (screen_width - win_width)//2, (screen_height - win_height)//2
    window.move(x, y)

window = sg.Window('vManage APy', layout, icon=icon, finalize=True, font=('Consolas', 10))
window.bind('<Button-3>', 'B3')
collapse_authentication_state = True
collapse_central_policy_state = False
collapse_cluster_state = False
collapse_device_templates_state = False
collapse_device_state = False
collapse_feature_templates_state = False
collapse_local_policy_state = False
collapse_monitor_network_misc_state = False
collapse_monitor_network_bfd_state = False
collapse_monitor_network_bgp_state = False
collapse_monitor_network_cellular_state = False
collapse_monitor_network_control_state = False
collapse_monitor_network_device_state = False
collapse_monitor_network_dhcp_state = False
collapse_monitor_network_dot1x_state = False
collapse_monitor_network_hardware_state = False
collapse_monitor_network_ip_state = False
collapse_monitor_network_omp_state = False
collapse_monitor_network_orchestrator_state = False
collapse_monitor_network_ospf_state = False
collapse_monitor_network_state = False
collapse_policy_definitions_state = False
collapse_policy_lists_state = False
collapse_policy_updates_state = False
collapse_security_policy_state = False
window['collapse_central_policy'].update(visible=False)
window['collapse_cluster'].update(visible=False)
window['collapse_device_templates'].update(visible=False)
window['collapse_device'].update(visible=False)
window['collapse_feature_templates'].update(visible=False)
window['collapse_local_policy'].update(visible=False)
window['collapse_monitor_network_misc'].update(visible=False)
window['collapse_monitor_network_bfd'].update(visible=False)
window['collapse_monitor_network_bgp'].update(visible=False)
window['collapse_monitor_network_cellular'].update(visible=False)
window['collapse_monitor_network_control'].update(visible=False)
window['collapse_monitor_network_device'].update(visible=False)
window['collapse_monitor_network_dhcp'].update(visible=False)
window['collapse_monitor_network_dot1x'].update(visible=False)
window['collapse_monitor_network_hardware'].update(visible=False)
window['collapse_monitor_network_ip'].update(visible=False)
window['collapse_monitor_network_omp'].update(visible=False)
window['collapse_monitor_network_orchestrator'].update(visible=False)
window['collapse_monitor_network_ospf'].update(visible=False)
window['collapse_monitor_network'].update(visible=False)
window['collapse_policy_definitions'].update(visible=False)
window['collapse_policy_lists'].update(visible=False)
window['collapse_policy_updates'].update(visible=False)
window['collapse_security_policy'].update(visible=False)
move_center(window)

while True:
    event, values = window.read()
    try:
        user = values['user']
        password = values['password']
        host = values['host']
    except:
        print('')
    if event == sg.WINDOW_CLOSED:
        break
    if event.endswith('B3'):
        paste()

    if event == 'collapse_authentication_text':
        collapse_authentication_state = not collapse_authentication_state
        window['collapse_authentication'].update(visible=collapse_authentication_state)
    if event == 'collapse_central_policy_text':
        collapse_central_policy_state = not collapse_central_policy_state
        window['collapse_central_policy'].update(visible=collapse_central_policy_state)
    if event == 'collapse_cluster_text':
        collapse_cluster_state = not collapse_cluster_state
        window['collapse_cluster'].update(visible=collapse_cluster_state)
    if event == 'collapse_device_templates_text':
        collapse_device_templates_state = not collapse_device_templates_state
        window['collapse_device_templates'].update(visible=collapse_device_templates_state)
    if event == 'collapse_device_text':
        collapse_device_state = not collapse_device_state
        window['collapse_device'].update(visible=collapse_device_state)
    if event == 'collapse_feature_templates_text':
        collapse_feature_templates_state = not collapse_feature_templates_state
        window['collapse_feature_templates'].update(visible=collapse_feature_templates_state)
    if event == 'collapse_local_policy_text':
        collapse_local_policy_state = not collapse_local_policy_state
        window['collapse_local_policy'].update(visible=collapse_local_policy_state)
    if event == 'collapse_monitor_network_misc_text':
        collapse_monitor_network_misc_state = not collapse_monitor_network_misc_state
        window['collapse_monitor_network_misc'].update(visible=collapse_monitor_network_misc_state)
    if event == 'collapse_monitor_network_bfd_text':
        collapse_monitor_network_bfd_state = not collapse_monitor_network_bfd_state
        window['collapse_monitor_network_bfd'].update(visible=collapse_monitor_network_bfd_state)
    if event == 'collapse_monitor_network_bgp_text':
        collapse_monitor_network_bgp_state = not collapse_monitor_network_bgp_state
        window['collapse_monitor_network_bgp'].update(visible=collapse_monitor_network_bgp_state)
    if event == 'collapse_monitor_network_cellular_text':
        collapse_monitor_network_cellular_state = not collapse_monitor_network_cellular_state
        window['collapse_monitor_network_cellular'].update(visible=collapse_monitor_network_cellular_state)
    if event == 'collapse_monitor_network_control_text':
        collapse_monitor_network_control_state = not collapse_monitor_network_control_state
        window['collapse_monitor_network_control'].update(visible=collapse_monitor_network_control_state)
    if event == 'collapse_monitor_network_device_text':
        collapse_monitor_network_device_state = not collapse_monitor_network_device_state
        window['collapse_monitor_network_device'].update(visible=collapse_monitor_network_device_state)
    if event == 'collapse_monitor_network_dhcp_text':
        collapse_monitor_network_dhcp_state = not collapse_monitor_network_dhcp_state
        window['collapse_monitor_network_dhcp'].update(visible=collapse_monitor_network_dhcp_state)
    if event == 'collapse_monitor_network_dot1x_text':
        collapse_monitor_network_dot1x_state = not collapse_monitor_network_dot1x_state
        window['collapse_monitor_network_dot1x'].update(visible=collapse_monitor_network_dot1x_state)
    if event == 'collapse_monitor_network_hardware_text':
        collapse_monitor_network_hardware_state = not collapse_monitor_network_hardware_state
        window['collapse_monitor_network_hardware'].update(visible=collapse_monitor_network_hardware_state)
    if event == 'collapse_monitor_network_ip_text':
        collapse_monitor_network_ip_state = not collapse_monitor_network_ip_state
        window['collapse_monitor_network_ip'].update(visible=collapse_monitor_network_ip_state)
    if event == 'collapse_monitor_network_omp_text':
        collapse_monitor_network_omp_state = not collapse_monitor_network_omp_state
        window['collapse_monitor_network_omp'].update(visible=collapse_monitor_network_omp_state)
    if event == 'collapse_monitor_network_orchestrator_text':
        collapse_monitor_network_orchestrator_state = not collapse_monitor_network_orchestrator_state
        window['collapse_monitor_network_orchestrator'].update(visible=collapse_monitor_network_orchestrator_state)
    if event == 'collapse_monitor_network_ospf_text':
        collapse_monitor_network_ospf_state = not collapse_monitor_network_ospf_state
        window['collapse_monitor_network_ospf'].update(visible=collapse_monitor_network_ospf_state)
    if event == 'collapse_monitor_network_text':
        collapse_monitor_network_state = not collapse_monitor_network_state
        window['collapse_monitor_network'].update(visible=collapse_monitor_network_state)
    if event == 'collapse_policy_definitions_text':
        collapse_policy_definitions_state = not collapse_policy_definitions_state
        window['collapse_policy_definitions'].update(visible=collapse_policy_definitions_state)
    if event == 'collapse_policy_lists_text':
        collapse_policy_lists_state = not collapse_policy_lists_state
        window['collapse_policy_lists'].update(visible=collapse_policy_lists_state)
    if event == 'collapse_policy_updates_text':
        collapse_policy_updates_state = not collapse_policy_updates_state
        window['collapse_policy_updates'].update(visible=collapse_policy_updates_state)
    if event == 'collapse_security_policy_text':
        collapse_security_policy_state = not collapse_security_policy_state
        window['collapse_security_policy'].update(visible=collapse_security_policy_state)

    #vmanage.api.authentication
    if event == 'Authenticate':
        session = Authentication(host=host, user=user, password=password, validate_certs=False).login()
        if session != None:
            Authenticated = True
        collapse_authentication_state = not collapse_authentication_state
        window['collapse_authentication'].update(visible=False)
        window['collapse_authentication_text'].update(text_color='#00D000')

    try:
        #vmanage.api.central_policy
        api_central_policy = CentralPolicy(session, host=host)
        if event == 'Central Policy':
            json_data=api_central_policy.get_central_policy()
            view_data(title=event, json_data=json_data)

        #vmanage.api.cluster
        api_cluster = Cluster(session, host=host)
        if event == 'Cluster Connected Devices':
            json_data=api_cluster.get_cluster_connected_devices_list(values['get_cluster_connected_devices_list_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Cluster Health Details':
            json_data=api_cluster.get_cluster_health_details_list()
            view_data(title=event, json_data=json_data)
        if event == 'Cluster Health Status':
            json_data=api_cluster.get_cluster_health_status_list()
            view_data(title=event, json_data=json_data)
        if event == 'Cluster List':
            json_data=api_cluster.get_cluster_list()
            view_data(title=event, json_data=json_data)
        if event == 'Cluster IP Addresses':
            json_data=api_cluster.get_cluster_ip_addresses_dict()
            view_data(title=event, json_data=json_data)
        if event == 'Cluster Ready State':
            json_data=api_cluster.get_cluster_ready_state()
            view_data(title=event, json_data=json_data)
        if event == 'Cluster Node Properties':
            json_data=api_cluster.get_cluster_node_properties()
            view_data(title=event, json_data=json_data)
        if event == 'Cluster Tenancy Mode':
            json_data=api_cluster.get_cluster_tenancy_mode()
            view_data(title=event, json_data=json_data)
        if event == 'Cluster vManage Details':
            json_data=api_cluster.get_cluster_vmanage_details_list(values['get_cluster_health_details_list_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.device_templates
        api_device_templates = DeviceTemplates(session, host=host)
        if event == 'Device Templates':
            json_data=api_device_templates.get_device_templates()
            view_data(title=event, json_data=json_data)
        if event == 'Device Template List':
            json_data=api_device_templates.get_device_template_object(values['get_device_template_object_template_id'])
            view_data(title=event, json_data=json_data)
        if event == 'Template Attachments':
            json_data=api_device_templates.get_template_attachments(values['get_template_attachments_template_id'], values['get_template_attachments_key'])
            view_data(title=event, json_data=json_data)
        if event == 'Template Input':
            json_data=api_device_templates.get_template_input(values['get_template_input_template_id'], values['get_template_input_device_id_list'].split(','))
            view_data(title=event, json_data=json_data)
        if event == 'Attachments':
            json_data=api_device_templates.get_attachments(values['get_attachments_template_id'], values['get_attachments_key'])
            view_data(title=event, json_data=json_data)
        if event == 'Device Running Config':
            json_data=api_device_templates.get_device_running_config(values['get_device_running_config_uuid'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.device
        api_device = Device(session, host=host)
        if event == 'Device List':
            json_data=api_device.get_device_list(values['device_device_type'])
            view_data(title=event, json_data=json_data)
        if event == 'Device Status':
            json_data=api_device.get_device_status(values['device_status_value'], values['device_status_key'])
            view_data(title=event, json_data=json_data)
        if event == 'Device Config':
            json_data=api_device.get_device_config(values['device_config_device_type'], values['device_config_value'], values['device_config_key'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.feature_templates
        api_feature_templates = FeatureTemplates(session, host=host)
        if event == 'Feature Templates':
            json_data=api_feature_templates.get_feature_templates()
            view_data(title=event, json_data=json_data)
        if event == 'Device Templates for Feature':
            json_data=api_feature_templates.get_device_templates_for_feature(values['get_device_templates_for_feature_templateId'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.local_policy
        api_local_policy = LocalPolicy(session, host=host)
        if event == 'Local Policy':
            json_data=api_local_policy.get_local_policy()
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network
        api_monitor_network = MonitorNetwork(session, host=host)

        #vmanage.api.monitor_network.misc
        if event == 'Device Type':
            json_data=api_monitor_network._get_device_type(values['_get_device_type_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'AAA Users':
            json_data=api_monitor_network.get_aaa_users(values['get_aaa_users_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'ARP Table':
            json_data=api_monitor_network.get_arp_table(values['get_arp_table_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Interface VPN':
            json_data=api_monitor_network.get_interface_vpn(values['get_interface_vpn_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Security Information':
            json_data=api_monitor_network.get_security_information(values['get_security_information_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Software':
            json_data=api_monitor_network.get_software(values['get_software_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'VRRP':
            json_data=api_monitor_network.get_vrrp(values['get_vrrp_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.bfd
        if event == 'BFD History':
            json_data=api_monitor_network.get_bfd_history(values['get_bfd_history_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'BFD Links':
            json_data=api_monitor_network.get_bfd_links(values['get_bfd_links_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'BFD Sessions':
            json_data=api_monitor_network.get_bfd_sessions(values['get_bfd_sessions_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'BFD Device State':
            json_data=api_monitor_network.get_bfd_device_state(values['get_bfd_device_state_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'BFD Device State TLOC':
            json_data=api_monitor_network.get_bfd_device_state_tloc(values['get_bfd_device_state_tloc_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'BFD Summary':
            json_data=api_monitor_network.get_bfd_summary(values['get_bfd_summary_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'BFD TLOC':
            json_data=api_monitor_network.get_bfd_tloc(values['get_bfd_tloc_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.bgp
        if event == 'BGP Neighbors':
            json_data=api_monitor_network.get_bgp_neighbors(values['get_bgp_neighbors_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'BGP Routes':
            json_data=api_monitor_network.get_bgp_routes(values['get_bgp_routes_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'BGP Summary':
            json_data=api_monitor_network.get_bgp_summary(values['get_bgp_summary_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.cellular
        if event == 'Cellular Connections':
            json_data=api_monitor_network.get_cellular_connections(values['get_cellular_connections_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Cellular Hardware':
            json_data=api_monitor_network.get_cellular_hardware(values['get_cellular_hardware_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Cellular Modems':
            json_data=api_monitor_network.get_cellular_modems(values['get_cellular_modems_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Cellular Networks':
            json_data=api_monitor_network.get_cellular_networks(values['get_cellular_networks_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Cellular Profiles':
            json_data=api_monitor_network.get_cellular_profiles(values['get_cellular_profiles_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Cellular Radios':
            json_data=api_monitor_network.get_cellular_radios(values['get_cellular_radios_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Cellular Sessions':
            json_data=api_monitor_network.get_cellular_sessions(values['get_cellular_sessions_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Cellular Status':
            json_data=api_monitor_network.get_cellular_status(values['get_cellular_status_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.control
        if event == 'Control Affinity Config':
            json_data=api_monitor_network.get_control_affinity_config(values['get_control_affinity_config_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control Affinity Status':
            json_data=api_monitor_network.get_control_affinity_status(values['get_control_affinity_status_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control Connections':
            json_data=api_monitor_network.get_control_connections(values['get_control_connections_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control Connections History':
            json_data=api_monitor_network.get_control_connections_history(values['get_control_connections_history_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control Count':
            json_data=api_monitor_network.get_control_count(values['get_control_count_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control Links':
            json_data=api_monitor_network.get_control_links(values['get_control_links_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control Local Properties':
            json_data=api_monitor_network.get_control_local_properties(values['get_control_local_properties_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control Summary':
            json_data=api_monitor_network.get_control_summary(values['get_control_summary_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control Valid Devices':
            json_data=api_monitor_network.get_control_valid_devices(values['get_control_valid_devices_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control Valid Vsmarts':
            json_data=api_monitor_network.get_control_valid_vsmarts(values['get_control_valid_vsmarts_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control WAN Interface':
            json_data=api_monitor_network.get_control_wan_interface(values['get_control_wan_interface_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Control WAN Interface Color':
            json_data=api_monitor_network.get_control_wan_interface_color(values['get_control_wan_interface_color_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.device
        if event == 'Device Status':
            json_data=api_monitor_network.get_device_status(values['get_device_status_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Device System Info':
            json_data=api_monitor_network.get_device_system_info(values['get_device_system_info_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.dhcp
        if event == 'DHCP Clients':
            json_data=api_monitor_network.get_dhcp_clients(values['get_dhcp_clients_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'DHCP Interfaces':
            json_data=api_monitor_network.get_dhcp_interfaces(values['get_dhcp_interfaces_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'DHCP Servers':
            json_data=api_monitor_network.get_dhcp_servers(values['get_dhcp_servers_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.dot1x
        if event == 'dot1x Clients':
            json_data=api_monitor_network.get_dot1x_clients(values['get_dot1x_clients_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'dot1x Interfaces':
            json_data=api_monitor_network.get_dot1x_interfaces(values['get_dot1x_interfaces_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'dot1x RADIUS':
            json_data=api_monitor_network.get_dot1x_radius(values['get_dot1x_radius_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.hardware
        if event == 'Hardware Alarms':
            json_data=api_monitor_network.get_hardware_alarms(values['get_hardware_alarms_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Hardware Environment':
            json_data=api_monitor_network.get_hardware_environment(values['get_hardware_environment_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Hardware Inventory':
            json_data=api_monitor_network.get_hardware_inventory(values['get_hardware_inventory_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Hardware Status Summary':
            json_data=api_monitor_network.get_hardware_status_summary(values['get_hardware_status_summary_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Hardware System':
            json_data=api_monitor_network.get_hardware_system(values['get_hardware_system_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.ip
        if event == 'IP FIB':
            json_data=api_monitor_network.get_ip_fib(values['get_ip_fib_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'IP Route Table':
            json_data=api_monitor_network.get_ip_route_table(values['get_ip_route_table_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'IP NAT Translations':
            json_data=api_monitor_network.get_ip_nat_translations(values['get_ip_nat_translations_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'IP NAT64 Translations':
            json_data=api_monitor_network.get_ip_nat64_translations(values['get_ip_nat64_translations_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.omp
        if event == 'OMP Peers':
            json_data=api_monitor_network.get_omp_peers(values['get_omp_peers_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'OMP Routes Received':
            json_data=api_monitor_network.get_omp_routes_received(values['get_omp_routes_received_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'OMP Routes Advertised':
            json_data=api_monitor_network.get_omp_routes_advertised(values['get_omp_routes_advertised_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'OMP Summary':
            json_data=api_monitor_network.get_omp_summary(values['get_omp_summary_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.orchestrator
        if event == 'Orchestrator Summary':
            json_data=api_monitor_network.get_orchestrator_summary(values['get_orchestrator_summary_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Orchestrator Connections':
            json_data=api_monitor_network.get_orchestrator_connections(values['get_orchestrator_connections_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Orchestrator Connections History':
            json_data=api_monitor_network.get_orchestrator_connections_history(values['get_orchestrator_connections_history_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'Orchestrator Local Properties':
            json_data=api_monitor_network.get_orchestrator_local_properties(values['get_orchestrator_local_properties_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.monitor_network.ospf
        if event == 'OSPF Interfaces':
            json_data=api_monitor_network.get_ospf_interfaces(values['get_ospf_interfaces_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'OSPF Neighbors':
            json_data=api_monitor_network.get_ospf_neighbors(values['get_ospf_neighbors_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'OSPF Routes':
            json_data=api_monitor_network.get_ospf_routes(values['get_ospf_routes_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'OSPF Database':
            json_data=api_monitor_network.get_ospf_database(values['get_ospf_database_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'OSPF Database Summary':
            json_data=api_monitor_network.get_ospf_database_summary(values['get_ospf_database_summary_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'OSPF Process':
            json_data=api_monitor_network.get_ospf_process(values['get_ospf_process_system_ip'])
            view_data(title=event, json_data=json_data)
        if event == 'OSPF Database External':
            json_data=api_monitor_network.get_ospf_database_external(values['get_ospf_database_external_system_ip'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.policy_definitions
        api_policy_definitions = PolicyDefinitions(session, host=host)
        if event == 'Definition Types':
            json_data=api_policy_definitions.get_definition_types()
            view_data(title=event, json_data=json_data)
        if event == 'Policy Definition':    
            json_data=api_policy_definitions.get_policy_definition(values['get_policy_definition_definition_type'], values['get_policy_definition_definition_id'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.policy_lists
        api_policy_lists = PolicyLists(session, host=host)
        if event == 'Data Prefix List':
            json_data=api_policy_lists.get_data_prefix_list()
            view_data(title=event, json_data=json_data)
        if event == 'Policy List All':
            json_data=api_policy_lists.get_policy_list_all()
            view_data(title=event, json_data=json_data)
        if event == 'Policy List by Name':
            json_data=api_policy_lists.get_policy_list_by_name(values['get_policy_list_by_name_policy_list_name'])
            view_data(title=event, json_data=json_data)
        if event == 'Policy List by ID':
            json_data=api_policy_lists.get_policy_list_by_id(values['get_policy_list_by_id_policy_list_id'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.policy_updates
        api_policy_updates = PolicyUpdates(session, host=host)
        if event == 'Device IDs':
            json_data=api_policy_updates.get_device_ids(values['get_device_ids_template_id'])
            view_data(title=event, json_data=json_data)
        if event == 'Device Inputs':
            json_data=api_policy_updates.get_device_inputs(values['get_device_inputs_template_id'], values['get_device_inputs_device_ids'])
            view_data(title=event, json_data=json_data)
        if event == 'Policy ID':
            json_data=api_policy_updates.get_policy_id(values['get_policy_id_policy_type'], values['get_policy_id_policy_name'])
            view_data(title=event, json_data=json_data)
        if event == 'Policy Definition':
            json_data=api_policy_updates.get_policy_definition(values['get_policy_definition_policy_type'], values['get_policy_definition_policy_id'])
            view_data(title=event, json_data=json_data)

        #vmanage.api.security_policy
        api_security_policy = SecurityPolicy(session, host=host)
        if event == 'Get Security Policy':
            json_data=api_security_policy.get_security_policy()
            view_data(title=event, json_data=json_data)
        if event == 'Get Security Definition':
            json_data=api_security_policy.get_security_definition(values['security_policy_defintion'])
            view_data(title=event, json_data=json_data)
    except:
        session = Authentication(host=host, user=user, password=password, validate_certs=False).login()
        if session != None:
            Authenticated = True
        collapse_authentication_state = not collapse_authentication_state
        window['collapse_authentication'].update(visible=False)
        window['collapse_authentication_text'].update(text_color='#00D000')
window.close()