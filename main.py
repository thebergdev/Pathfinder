from map import MapObj, MapSearchObjG, MapSearchObjOrder
from a_star import a_star
from visualize import MapViz
import numpy as np

mo = MapObj(20, 20, 5)
map = mo.get_map()
key_loc = mo.get_key_loc()
print(map)

print(key_loc)
cost, path, node_path, node_list = a_star(map, key_loc[0], key_loc[1])
if(cost > -1):
    print(cost)
    print(path)
    
else:
    print("No path")

mv = MapViz(map, ['green', 'white', 'yellow',  'blue', 'grey', 'black'], [1,2,4,7,8,9,10])
mv.viz()