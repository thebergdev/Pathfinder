import map
from a_star import a_star

mo = map.Map_Obj(15, 15, 2)
map = mo.get_map()
key_loc = mo.get_key_loc()
print(map)
print(key_loc)
cost, path, node_path, map = a_star(map, key_loc[0], key_loc[1])
if(cost > -1):
    print(map)
    print(cost)
    print(path)
else:
    print("No path")

