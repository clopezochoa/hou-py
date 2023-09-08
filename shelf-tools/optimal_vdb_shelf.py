import hou
import opt_vdb

def prompt_user_parameters():
    input = hou.ui.readMultiInput(
        "Set parameters", ("File Path", "Largest Axis", "Minimum Point Separation", "Maximum Point Separation", "Increment"),
        initial_contents=("path", "1", "0.5", "1.0", "0.01"),
        title="Parameters",
        buttons=("OK", "Cancel"),
        default_choice=0, close_choice=1,
    )
    if input[0] == 0:
        file_path = input[1][0]
        size = float(input[1][1])
        min_value = float(input[1][2])
        max_value = float(input[1][3])
        delta = float(input[1][4])
    
        return file_path, size, min_value, max_value, delta
    else:
        return None

def create_nodes():
    obj_network = hou.node("/obj")

    geo_node = obj_network.createNode("geo", "geo")
    file_node = geo_node.createNode("file", "file")
    resize_node = geo_node.createNode("matchsize", "resize")
    pfv_node = geo_node.createNode("pointsfromvolume", "pfv")
    vdb_node = geo_node.createNode("vdbfromparticles", "vdb")
    output_node = geo_node.createNode("output", "output")

    resize_node.setInput(0, file_node)
    pfv_node.setInput(0, resize_node)
    vdb_node.setInput(0, pfv_node)
    output_node.setInput(0, vdb_node)
        
    geo_node.layoutChildren()
    geo_node.setCurrent(geo_node,True)
    
    active_pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.NetworkEditor)
    if active_pane:
        active_pane.homeToSelection()
    return output_node

def set_parameters():
    hou.parm('/obj/geo/resize/doscale').set(True)
    hou.parm('/obj/geo/pfv/iso').set(0.25)
    exp = "ch('" + '/obj/geo/pfv/particlesep' + "')"
    hou.parm('/obj/geo/vdb/voxelsize').setExpression(exp)
    exp = exp + " / 2"
    hou.parm('/obj/geo/vdb/radiusscale').setExpression(exp)
    hou.parm('/obj/geo/vdb/minvoxelradius').setExpression(exp)
    
def execute_solver(file_path, output_node, size, min_value, max_value, delta):
    opt_vdb.set_file_path(file_path)
    opt_vdb.set_size((size, size, size))
    optimal_value = opt_vdb.find_optimal_point_separation(min_value, max_value, delta)
    hou.parm('/obj/geo/pfv/particlesep').set(optimal_value)
    output_node.setDisplayFlag(True)
    output_node.setRenderFlag(True)
    
def main():
    parameters = prompt_user_parameters()
    if (parameters != None):
        file_path, size, min_value, max_value, delta = parameters
        output_node = create_nodes()
        set_parameters()
        execute_solver(file_path, output_node, size, min_value, max_value, delta)
    
main()
