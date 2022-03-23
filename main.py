import bpy
import random
from utils import *

Y_RANGE = 3
Z_RANGE = 3.5

C = bpy.context
D = bpy.data
    
def main():
    scene_graphs = []
    name = 'SG_Objects'
    obj_collection = get_or_create_collection(name)
    for i in range(2):
        select_objects_in_collection(name)
        bpy.ops.object.delete()
        object_classes = ['cube', 'cylinder', 'cone', 'sphere']
        n_objs = 4
        objects = [random.choice(object_classes) for i in range(n_objs)]
        relationships = [
            [0, 'left to', 1],
            [2, 'left to', 3],
    #        [0, 'left to', 3],
    #        [2, 'left to', 1],
            [2, 'below', 0],
            [3, 'below', 1],
    #        [2, 'below', 3],
    #        [1, 'below', 0]
        ]
        scene_graph = {'objects': objects, 'relationships': relationships}
        
        

        select_collection(name)
            
        for obj in scene_graph['objects']:
            if len(D.collections['SG_Objects'].all_objects) == len(scene_graph['objects']):
                break
            # Object
            # shape = random.choice(['cone', 'cube', 'cylinder', 'sphere'])
            new_obj = add_object(obj)

            color = random.choice(list(COLORS.keys()))
            mat = get_color_material(color)
            add_material(new_obj, mat)
            
        for rel in scene_graph['relationships']:
            s,p,o = rel
            
            subj = list(D.collections['SG_Objects'].all_objects)[s]
            obj = list(D.collections['SG_Objects'].all_objects)[o]

            if p == 'left to':
                x_loc = -4.5
                y_loc = round(random.gauss(-Y_RANGE / 2, Y_RANGE / 4))
                z_loc = subj.location.z
                # z_loc = round(random.gauss(0, 0.5), 2)
                subj.location = [x_loc, y_loc, z_loc]
                
                y_loc = round(random.gauss(y_loc + 3, Y_RANGE / 8), 2)
                # z_loc = round(random.gauss(0, 0.5), 2)
                z_loc = subj.location.z
                obj.location = [x_loc, y_loc, z_loc]

            elif p == 'below':
                x_loc = -4.5
                # y_loc = round(random.gauss(0, 0.5), 2)
                y_loc = subj.location.y
                z_loc = round(random.gauss(-Z_RANGE / 2, Z_RANGE / 4))
                subj.location = [x_loc, y_loc, z_loc]
                
                # y_loc = round(random.gauss(0, 0.5), 2)
                y_loc = subj.location.y
                z_loc = round(random.gauss(z_loc + 3, Z_RANGE / 8), 2)
                obj.location = [x_loc, y_loc, z_loc]  
                
        
        scene_graphs.append(scene_graph)