import hou
import time

def prompt_point_select (node):
  previous_node = node.node(node.parm("node_to_preview").eval())
  previous_node.setDisplayFlag(True)
  previous_node.setRenderFlag(True)
  scene_view = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
  scene_view.setCurrentNode(previous_node)
  
  parm = node.parm("points")
  geo = scene_view.selectGeometry()
  parm.set(geo.mergedSelectionString())
  node.setDisplayFlag(True)
  node.setRenderFlag(True)
  scene_view.setCurrentNode(node)
