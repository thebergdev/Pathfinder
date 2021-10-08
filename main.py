from map import MapObj
from visualize import MapViz

mo = MapObj(20, 20, 5)
map = mo.get_map()
mv = MapViz(map, ['green', 'white', 'yellow',  'blue', 'grey', 'black'], [1,2,4,7,8,9,10])
mv.viz()

map_with_path = mo.get_map_with_path()
print(map_with_path)

map_with_order = mo.get_map_with_order(1)
print(map_with_order)

map_with_f = mo.get_map_with_f(1)
print(map_with_f)