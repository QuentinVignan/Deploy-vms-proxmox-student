from rich.console import Console
from rich.table import Table

import os
import yaml

def get_project_info_yaml(filename):
    tmp_arr = []
    with open(filename , 'r') as file:
        load_yaml = yaml.safe_load(file)
        tmp_arr.append(str(load_yaml['project_name']))
        tmp_arr.append(str(load_yaml['time_start']))
        tmp_arr.append(str(load_yaml['time_end']))
        tmp_arr.append(str(load_yaml['time_delete']))
        tmp_arr.append(str(load_yaml['proxmox_ip']))
        tmp_arr.append(str(load_yaml['template_id']))
    return tmp_arr


def display_info(arr):
    console = Console()
    table = Table(show_header=True, header_style="bold white")
    table.add_column("Project Name")
    table.add_column("Project Start")
    table.add_column("Project End")
    table.add_column("Project Delete")
    table.add_column("Proxmox IP")
    table.add_column("Template ID")
    for line in arr:
        table.add_row("[bright_blue]" + line[0] + "[/bright_blue]", "[green]" + line[1] + "[/green]" , "[orange4]" + line[2] + "[/orange4]" , "[red]" + line[3] + "[/red]" , line[4] , line[5])
    console.print(table)