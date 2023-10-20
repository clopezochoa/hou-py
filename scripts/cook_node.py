import os
import json

# When a parameter is set through python and not manually, Houdini does not run the callback script.
# This function runs all the parameters in the same folder (except the cook button).
def cook_all_parms_in_folder(node, parm):
    parms = node.parmsInFolder(parm.containingFolders())
    for p in parms:
        if p.name() != parm.name():
          p.pressButton()
    node.cook()

def save_folder_to_json(node, parm):
    data = {}
    parms = node.parmsInFolder(parm.containingFolders())
    file_path = parms[-3].evalAsString()
    file_name = parms[-2].evalAsString()
    mode = parms[-1].eval().split("@")
    suffix = mode[0]
    file_name += suffix
    folder_name = mode[1]
    parms = node.parmsInFolder((folder_name, ))
  
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_path += "/" + file_name

    for parm in parms:
        data[parm.name()] = parm.evalAsString()
    with open(file_path, 'w') as file:
        json.dump(data, file)

def load_data_from_json(node, parm):
    parms = node.parmsInFolder(parm.containingFolders())
    file_path = parms[-3].evalAsString()
    file_name = parms[-2].evalAsString()
    mode = parms[-1].eval().split("@")
    suffix = mode[0]
    file_name += suffix
    folder_name = mode[1]    
    parms = node.parmsInFolder((folder_name, ))

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_path += "/" + file_name

    with open(file_path, 'r') as file:
        data = json.load(file).items()
    for key, value in data:
        node.parm(key).set(value)