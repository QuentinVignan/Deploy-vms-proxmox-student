import os

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
