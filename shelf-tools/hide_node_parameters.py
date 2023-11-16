nodes = hou.selectedNodes()
for node in nodes:
    ptg = node.parmTemplateGroup()
    for parm in ptg.parmTemplates():
        ptg.hide(parm.name(), True)
    node.setParmTemplateGroup(ptg)