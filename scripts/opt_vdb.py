import hou

def set_file_path(path):
  hou.parm('/obj/geo/file/file').set(path)
  return

def set_size(value):
  hou.parmTuple('/obj/geo/resize/size').set(value)
  return

def calculate_voxel_count(point_separation):
  print('Point separation: ' + str(point_separation))
  hou.parm('/obj/geo/pfv/particlesep').set(point_separation)
  vdb = hou.node('/obj/geo/vdb')
  vdb.cook()
  return vdb.geometry().prims()[0].activeVoxelCount()

def find_optimal_point_separation(min_value, max_value, delta):
  best_point_separation = min_value
  lowest_voxel_count = float('inf')

  point_separation = min_value

  while point_separation <= max_value:
    voxel_count = calculate_voxel_count(point_separation)
    print('Voxel count: ' + str(voxel_count))
    if voxel_count < lowest_voxel_count:
        lowest_voxel_count = voxel_count
        best_point_separation = point_separation

    point_separation += delta

  optimization_percentage = 100 * (1 - (abs(best_point_separation - min_value) / (max_value - min_value)))
  print('\nLowest Voxel Count: ' + str(lowest_voxel_count) + '\nBest point separation: ' + str(best_point_separation)[:4] + '\nOptimization percentage: ' + str(optimization_percentage)[:4] + '%')
  return best_point_separation
