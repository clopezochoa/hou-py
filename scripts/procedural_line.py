import hou


def _create_xform(node, xform_number, length):
  floats = node.parent().parmsInFolder(('Handlers', ))
  current_node = node
  inc = length / xform_number

  for idx in range(xform_number):
    xform = current_node.createOutputNode("xform", "xform_" + str(idx + 1))
    xform.parm("group").set(str(idx + 1))
    xform.parm("grouptype").set(3)

    if idx < xform_number -1:
      path = floats[idx].path()
      xform.parm("ty").setExpression('ch(\'' + path  + '\')')
      xform.parm("ty").set(inc*(idx+1))
      
      current_node = xform
    else:
      xform.parm("ty").set(length)
      xform.createOutputNode("output", "output")

def _create_float_parm(idx, length):
  parm = hou.FloatParmTemplate('hhandle_' + str(idx + 1), 'Handler ' + str(idx + 1), 1)
  parm.setMinValue(0.0)
  parm.setMaxValue(length)
  return parm

def on_length_changed(node):
  length = float(node.parm("length").eval())
  floats = node.parmsInFolder(('Handlers', ))
  ptg = node.parmTemplateGroup()
  for parm in floats:
    parm_template = ptg.find(parm.name())
    parm_template.setMaxValue(length)
    ptg.replace(parm.name(), parm_template)
  node.setParmTemplateGroup(ptg)
  _update_last_pt(node, length)

def _update_last_pt(node, length):
  py = node.node('python_sop')
  if py is None:
      py = node.createNode('python', 'python_sop')
      output_node = node.node('output')
      last_xform = output_node.inputConnectors()[0][0].inputNode()
      py.insertInput(0, last_xform)
      output_node.insertInput(0, py)

  py.parm('python').set(
'''import hou

node = hou.pwd()
geo = node.geometry()
length = {}

pt = geo.points()[-1]
pt.setPosition((0,length,0))'''.format(length))

def _create_resample(segs, line):
  resample = line.createOutputNode("resample", "resample")
  resample.parm("dolength").set(False)
  resample.parm("dosegs").set(True)
  resample.parm("segs").set(segs)
  return resample

def reset(node):
  floats = node.parmsInFolder(('Handlers', ))
  length = float(node.parm('length').eval())
  inc = length / (len(floats) +1)

  for idx in range(len(floats)):
    parm = floats[idx]
    parm.set(inc*(idx + 1))
    
def create_divisions(node):
  clean(node)
  segs = int(node.parm("segs").eval())
  length = float(node.parm("length").eval())
  parm_templates = [_create_float_parm(idx, length) for idx in range(segs - 1)]
  folder = hou.FolderParmTemplate("hhandle", "Handlers", parm_templates = parm_templates, folder_type = hou.folderType.Simple)
  ptg = node.parmTemplateGroup()
  ptg.append(folder)
  node.setParmTemplateGroup(ptg)

  line = node.createNode("line", "line")
  line.parm("dist").set(length)
  resample = _create_resample(segs, line)
  set_height_to_zero = resample.createOutputNode("attribadjustfloat", "set_height_to_zero")
  set_height_to_zero.parm('attrib').set("P")
  set_height_to_zero.parm('operation').set(4)

  _create_xform(set_height_to_zero, segs, length)

def clean(node):
  node.deleteItems(node.children())
  ptg = node.parmTemplateGroup()
  previous_folder = ptg.findFolder('Handlers')
  if previous_folder:
    ptg.remove(previous_folder)
    node.setParmTemplateGroup(ptg)

def clean_extrusion(node):
  wrangler = node.node("wrangler")
  if wrangler: wrangler.destroy()
  extrude = node.node("extrude")
  if extrude: extrude.destroy()

  ptg = node.parmTemplateGroup()
  previous_folder = ptg.findFolder('Handlers')
  if previous_folder:
    ptg.remove(previous_folder)
    node.setParmTemplateGroup(ptg)


def dynamic_min_max(node, parm):
  pass

def preset_extrusion(node):
  clean_extrusion(node)
  prims = node.geometry().prims()
  parm_templates = tuple([_create_float_parm(idx, 1.0) for idx in range(len(prims))])
  folder = hou.FolderParmTemplate("hhandle", "Handlers", parm_templates = parm_templates, folder_type = hou.folderType.Simple)
  ptg = node.parmTemplateGroup()
  ptg.append(folder)
  node.setParmTemplateGroup(ptg)

  item = node.node("skin")
  wrangler = item.createOutputNode("attribwrangle", "wrangler")
  wrangler.parm('class').set(1)
  wrangler.parm('snippet').set(
'''string channel = "../hhandle_";
channel = concat(channel, itoa(@primnum + 1));
float handler = ch(channel);
f@zscale = handler;''')
  
def extrude(node):
  isExtrusion = False
  extrusion = node.node("extrude")
  if not extrusion:
    wrangler = node.node("wrangler")
    if wrangler:
      extrusion = wrangler.createOutputNode("polyextrude::2.0", "extrude")
      extrusion.parm("dist").setExpression('ch(\"../../depth\")')
      extrusion.parm("uselocalzscaleattrib").set(True)
      extrusion.parm("splittype").set(0)
      isExtrusion = True
    else:
      hou.ui.displayMessage("You must preset the node before cooking it!")

  else:
    isExtrusion = True
  if isExtrusion:
    extrusion.setDisplayFlag(True)
    extrusion.setRenderFlag(True)
    extrusion.cook()

def update_cross_section_parms(node):
  node.parm("cook").pressButton()
  node.parm("preset").pressButton()
  node.parm("cook2").pressButton()

  ptg = node.parmTemplateGroup()
  
  line_node = node.node("procedural_line")
  line_folder = ptg.findFolder('Handlers Line')
  if line_folder:
    line_parms = line_folder.parmTemplates()
    if line_parms:
      ptg.remove(line_folder)

  extrusion_node = node.node("extrude_line")
  extrusion_folder = ptg.findFolder('Handlers Extrusion')
  if extrusion_folder:
    extrusion_parms = extrusion_folder.parmTemplates()
    if extrusion_parms:
      ptg.remove(extrusion_folder)

  line_folder = line_node.parmTemplateGroup().findFolder('Handlers')
  line_parm_templates = [_clone_parm_template(parm, line_node, '_l') for parm in line_folder.parmTemplates()]

  extrusion_folder = extrusion_node.parmTemplateGroup().findFolder('Handlers')
  extrusion_parm_templates = [_clone_parm_template(parm, extrusion_node, "_e") for parm in extrusion_folder.parmTemplates()]
  
  new_line_folder = hou.FolderParmTemplate("l_handle_line", "Handlers Line", parm_templates = line_parm_templates, folder_type = hou.folderType.Collapsible)
  new_extrusion_folder = hou.FolderParmTemplate("e_handle_extrusion", "Handlers Extrusion", parm_templates = extrusion_parm_templates, folder_type = hou.folderType.Collapsible)
  
  ptg.append(new_line_folder)
  ptg.append(new_extrusion_folder)
  node.setParmTemplateGroup(ptg)

def _clone_parm_template(parm_template, node, suffix):
  new_parm_template = parm_template.clone()
  new_parm_template.setName(new_parm_template.name() + suffix)
  node.parm(parm_template.name()).setExpression('ch("../' + parm_template.name() + suffix + '")')
  return new_parm_template