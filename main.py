from lib.shell import list_yaml_in_folder , setup_argparse_global_var , setup_argparse_parameters
from lib.get_project_info import display_info , get_project_info_yaml
from lib.generate_template import create_template , create_template_file
from lib.create_delete_vm import create_vm , delete_vm
import argparse

parser = argparse.ArgumentParser(
    prog="Creator of vm Proxmox",
    description="This tool allows you to create batches of vm"
)

setup_argparse_parameters(parser)
result = setup_argparse_global_var(parser)

if result is None:
    print("ERROR aucun argument est ok")
elif result[0] == "list_config":
    list_file = list_yaml_in_folder('./config')
    info = []
    for path in list_file:
        info.append(get_project_info_yaml(path))
    if len(info) < 1:
        print("No config file found indise folder -> ./config")
    else:
        display_info(info)
elif result[0] == "create":
    user_proxmox = input("Enter user : ")
    password_proxmox = input("Enter password " + user_proxmox + " : ")
    create_vm(result[1] , user_proxmox , password_proxmox)
elif result[0] == "delete":
    user_proxmox = input("Enter user for proxmox : ")
    password_proxmox = input("Enter password " + user_proxmox + " : ")
    delete_vm(result[1] , user_proxmox , password_proxmox)
elif result[0] == "interactive_config":
    create_template_file(create_template())
elif result[0] == "ERROR":
    print("ERROR aucun argument est ok")


