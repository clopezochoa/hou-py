import time

def execute_nodes_in_sequence(nodes, delay):
    if not nodes:
        return
    
    node = nodes.pop(0)
    
    try:
        # Execute the current node
        node.cookWorkItems()
    except Exception as e:
        print(f"An error occurred while cooking {node}: {str(e)}")
    
    if nodes:
        time.sleep(delay)
        execute_nodes_in_sequence(nodes, delay)

def main(node):
  delay = float(node.parm("./delay").eval())
  if node.errors():
      node.bypass(True)
      time.sleep(delay/2.0)
      node.bypass(False)
  else:
    node.bypass(False)

  children = node.children()

  nodes = children[0:2] + children[3:]
  nodes[0].dirtyAllWorkItems(True)
  time.sleep(delay/2.0)
  
  nodes = list(nodes)

  try:
      # nodes[0].dirtyAllWorkItems(True)
      nodes[0].generateStaticWorkItems()
      execute_nodes_in_sequence(nodes, delay)
      
  except Exception as e:
      print(f"An error occurred: {str(e)}")
