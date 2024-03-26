import os
import argparse
import platform


def f_or_d_exists(path):
    if os.path.isdir(path):
        return True
    elif os.path.isfile(path):
        return True
    else:
        return False


def list_yaml_in_folder(path):
    list_file = os.listdir(path)
    tmp_arr = []
    for filename in list_file:
        if ".yaml" in filename:
            tmp_arr.append(path + '/' + filename)
        elif ".yml" in filename:
            tmp_arr.append(path + '/' + filename)
    return tmp_arr


def setup_argparse_parameters(parser):
    parser.add_argument("-l", "--list_config", help="List project info from config folder", nargs='?', const=1,
                        type=int)
    parser.add_argument("-c", "--create", help="Create project from config file", nargs='?', const=1, type=int)
    parser.add_argument("-d", "--delete", help="Delete project from config file", nargs='?', const=1, type=int)
    parser.add_argument("-con", "--config", help="Path of config file", type=str)
    parser.add_argument("-it", "--interactive_config", help="Create config file with interactive shell", nargs='?',
                        const=1, type=int)


def setup_argparse_global_var(parser):
    args = parser.parse_args()
    tmp_arr_arguments = []
    if args.list_config is not None:
        tmp_arr_arguments.append("list_config")
        return tmp_arr_arguments
    elif args.interactive_config is not None:
        tmp_arr_arguments.append("interactive_config")
        return tmp_arr_arguments
    elif args.create is not None:
        if args.config is not None:
            tmp_arr_arguments.append("create")
            tmp_arr_arguments.append(args.config)
            return tmp_arr_arguments
        else:
            tmp_arr_arguments.append("ERROR")
            return tmp_arr_arguments
    elif args.delete is not None:
        if args.config is not None:
            tmp_arr_arguments.append("delete")
            tmp_arr_arguments.append(args.config)
            return tmp_arr_arguments
        else:
            tmp_arr_arguments.append("ERROR")
            return tmp_arr_arguments
    else:
        tmp_arr_arguments.append("ERROR")
        return tmp_arr_arguments


def sed_template(old_content, new_content, filename):
    if platform.system() == "Darwin":
        shell_exec("gsed -i 's|" + old_content + "|" + new_content + "|g' " + filename)
    else:
        shell_exec("gsed -i 's|" + old_content + "|" + new_content + "|g' " + filename)
    return

def shell_exec(command):
    status = os.system(command)
    return

def write_csv_export(arr_to_csv , name):
    f = open("./" + name + ".csv", "a")
    for i in arr_to_csv:
        f.write(i + '\n')
    f.close()
