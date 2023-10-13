import hou
import time

def prompt_point_select (node, target):
  previous_node = node.node(target)
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
