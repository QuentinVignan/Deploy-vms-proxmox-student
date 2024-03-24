from lib.shell import list_yaml_in_folder , setup_argparse_global_var , setup_argparse_parameters
from lib.get_project_info import display_info , get_project_info_yaml
from lib.generate_template import create_template , create_template_file
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
    print("je crées des vms")
elif result[0] == "delete":
    print("je delete les vm et le project")
elif result[0] == "interactive_config":
    create_template_file(create_template())
elif result[0] == "ERROR":
    print("ERROR aucun argument est ok")


#console = Console()
#tasks = [f"task {n}" for n in range(1, 11)]
#with console.status("[bold green]Working on tasks...") as status:
#    while tasks:
#        task = tasks.pop(0)
#        sleep(5)
#        console.log(f"{task} complete")