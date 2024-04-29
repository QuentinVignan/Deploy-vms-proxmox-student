import random
import string

import paramiko
from rich.console import Console
from rich.table import Table
from lib.shell import shell_exec, sed_template, write_csv_export
from paramiko import SSHClient
from scp import SCPClient
import os
import yaml
from time import sleep


def define_vmid(ip, id):
    """define vmid with vlan + id"""
    ip_split = ip.split('/')
    ip_split_another = ip_split[0].split('.')
    result = str(ip_split_another[2])
    if int(id) < 10:
        result += "00" + str(id)
    elif int(id) < 100:
        result += "0" + str(id)
    else:
        result += str(id)
    return result


def define_gateway(ip):
    """define gateway with network"""
    ip_split = ip.split('/')
    ip_split_another = ip_split[0].split('.')
    ip_split_another[len(ip_split_another) - 1] = "254"
    result = ""
    index = 1
    for i in ip_split_another:
        result += i
        if index < len(ip_split_another):
            result += '.'
        index += 1
    return result


def generate_password(length):
    """Generates a password of the given length without special characters or uppercase letters."""
    all_characters = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password


def define_ip(ip, id):
    """define ip of vm with id"""
    ip_split = ip.split('/')
    ip_split_another = ip_split[0].split('.')
    ip_split_another[len(ip_split_another) - 1] = str(id)
    result = ""
    index = 1
    for i in ip_split_another:
        result += i
        if index < len(ip_split_another):
            result += '.'
        index += 1
    result += '/'
    result += ip_split[len(ip_split) - 1]
    return result


def create_vm(config_file_path, user_proxmox, password_proxmox):
    proxmox_ip = ""
    project_name = ""
    template_id = ""
    instances = []
    student_creds = []
    console = Console()
    with console.status("[bold green]Working on tasks...") as status:
        with open(config_file_path, 'r') as file:
            load_yaml = yaml.safe_load(file)
            proxmox_ip = load_yaml['proxmox_ip']
            project_name = load_yaml['project_name']
            template_id = load_yaml['template_id']
            instances = load_yaml['instances']
        for instance in instances:
            i = instance['start_at']
            while i < (int(instance['count']) + int(instance['start_at'])):
                lot_name = instance['vm_lot_name'].replace(' ', '')
                ip_vm = define_ip(instance['network'], i)
                gateway_vm = define_gateway(ip_vm)
                vmid_vm = define_vmid(ip_vm, i)
                vm_name = lot_name + '-' + str(vmid_vm) + ".etna.local"
                password_student = generate_password(7)
                disk = instance['spec']['disk']
                memory = instance['spec']['memory']
                vcpu = instance['spec']['vcpu']
                vlan = instance['vlan']
                shell_exec("cp ./lib/template/template.sh ./" + vm_name + ".sh")
                path_file = "./" + vm_name + ".sh"
                sed_template("VMID=1001", "VMID=" + vmid_vm, path_file)
                sed_template("VLAN=1001", "VLAN=" + str(vlan), path_file)
                sed_template("TEMPLATE_ID=9000", "TEMPLATE_ID=" + str(template_id), path_file)
                sed_template("NAME=0", 'NAME="' + vm_name + '"', path_file)
                sed_template("DISK=0", 'DISK="' + str(disk) + 'G"', path_file)
                sed_template("IP=0", 'IP="' + str(ip_vm) + '"', path_file)
                sed_template("GW=0", 'GW="' + str(gateway_vm) + '"', path_file)
                sed_template("PASSWORD=0", 'PASSWORD="' + password_student + '"', path_file)
                sed_template("VCPU=1", "VCPU=" + str(vcpu), path_file)
                sed_template("MEMORY=0", "MEMORY=" + str(memory), path_file)
                export_str = ip_vm.replace("/24" , "") + ":student:" + password_student
                student_creds.append(export_str)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh_client.connect(hostname=str(proxmox_ip), port=22, username=user_proxmox,
                                       password=password_proxmox)
                except:
                    print("Error connect to ssh with paramiko")
                    exit()
                stdin, stdout, stderr = ssh_client.exec_command("mkdir -p " + project_name)
                scp = SCPClient(ssh_client.get_transport())
                scp.put(path_file, "./" + project_name + "/" + vm_name + ".sh")
                scp.close()
                stdin, stdout, stderr = ssh_client.exec_command("chmod +x ./" + project_name + "/" + vm_name + ".sh")
                stdin, stdout, stderr = ssh_client.exec_command("./" + project_name + "/" + vm_name + ".sh create")
                exit_status = stdout.channel.recv_exit_status()
                console.log("Create vm : " + vm_name + " complete")
                shell_exec("rm ./" + vm_name + ".sh")
                ssh_client.close()
                sleep(1)
                i += 1
    write_csv_export(student_creds, "./" + project_name + "_creds")
    return


def delete_vm(config_file_path, user_proxmox, password_proxmox):
    proxmox_ip = ""
    project_name = ""
    console = Console()
    with console.status("[bold green]Working on tasks...") as status:
        with open(config_file_path, 'r') as file_load:
            load_yaml = yaml.safe_load(file_load)
            proxmox_ip = load_yaml['proxmox_ip']
            project_name = load_yaml['project_name']
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh_client.connect(hostname=str(proxmox_ip), port=22, username=user_proxmox, password=password_proxmox)
            except:
                print("Error connect to ssh with paramiko")
                exit()
            stdin, stdout, stderr = ssh_client.exec_command("ls ./" + project_name)
            result = stdout.readlines()
            for file in result:
                filename = file.replace('\n', '')
                stdin, stdout, stderr = ssh_client.exec_command("./" + project_name + "/" + filename + " delete")
                exit_status = stdout.channel.recv_exit_status()
                filename = filename.replace('.sh', '')
                console.log("Vm " + filename + " deleted complete")
            stdin, stdout, stderr = ssh_client.exec_command("rm -rf ./" + project_name)
            exit_status = stdout.channel.recv_exit_status()
            ssh_client.close()
    return
