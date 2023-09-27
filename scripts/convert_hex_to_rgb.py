# Converts the updated value of the parameter from hexadecimal web color code to rgb float values.
# Please remember to set Gamma to 1.0 if using web colors
def hex_to_rgb(node, parm):
    parms = node.parmsInFolder(parm.containingFolders())[1:]
    hex = parm.eval()
    if len(hex) != 6:
        raise ValueError("Input HEX color must be 6 characters long")

    r = int(hex[0:2], 16) / 255.0
    g = int(hex[2:4], 16) / 255.0
    b = int(hex[4:6], 16) / 255.0

    parms[0].set(r)
    parms[1].set(g)
    parms[2].set(b)
    