import yaml


def create_template():
    name_project = input("Name project : ")
    time_start = input("Time start ( ex : 12/04/2024 ) : ")
    time_end = input("Time end ( ex : 12/04/2024 ) : ")
    time_delete = input("Time delete ( ex : 12/04/2024 ) : ")
    proxmox_ip = input("Proxmox IP : ")
    template_id = input("Template ID ( ex : 9000 ) : ")
    add_instance = 1
    id = 1
    instance = []
    while add_instance > 0:
        network = input("Network ( ex : 172.16.232.0/24 ) : ")
        vlan = input("Vlan : ")
        count = input("Number of VMs : ")
        start_at = input("Start At : ")
        memory = input("Memory ( ex : 8192 ) : ")
        vcpu = input("Vcpu : ")
        disk = input("Disk ( ex : 60 for 60Gb ) : ")
        reAdd = input("Add new instance [Y/n] : ")
        result = {'id': id, 'vm_lot_name': name_project + "-" + str(id), 'network': network, 'vlan': int(vlan),
                  'count': int(count), 'start_at': int(start_at), 'spec': {'memory': int(memory), 'vcpu': int(vcpu), 'disk': int(disk)}}
        instance.append(result)
        if reAdd == "n":
            add_instance = 0
        id += 1
    final_result = {'instances': instance, 'template_id': int(template_id), 'proxmox_ip': proxmox_ip,
                    'time_delete': time_delete, 'time_end': time_end, 'time_start': time_start,
                    'project_name': str(name_project)}
    return final_result


def create_template_file(info_template):
    path = './config/' + info_template['project_name'] + '.yaml'
    with open(path, 'w+') as fichier_yaml:
        yaml.dump(info_template, fichier_yaml)
    print("File  '" + path + "' was created")
    return
