# When a parameter is set through python and not manually, Houdini does not run the callback script.
# This function runs all the parameters in the same folder (except the cook button).
def cook_all_parms_in_folder(node, parm):
    parms = node.parmsInFolder(parm.containingFolders())
    for p in parms:
        if p.name() != parm.name():
          p.pressButton()
    node.cook()