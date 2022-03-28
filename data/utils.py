import bpy
import json

def load_properties(filepath):
    with open(filepath) as j:
        return json.load(j)

C = bpy.context
D = bpy.data

SCALE = [1.0, 1.0, 1.0]

def setup_scene():
    select_collection('SceneElements')
    set_camera()
    set_rendering_options()
    set_background()
    add_light()


def rgb_to_rgba(rgb):
    rgba = [round(c / 255, 4) for c in rgb]
    rgba.append(1.0)
    return rgba

def get_color_material(color):
    # Get material
    mat = D.materials.get(f"{color.capitalize()} Material")
    if mat is None:
        # create material
        mat = D.materials.new(name=f"{color.capitalize()} Material")
        rgba_color = rgb_to_rgba(COLORS[color])
        mat.diffuse_color = rgba_color
    return mat

def get_shape_function(shape):
    if shape == 'cone':
        return bpy.ops.mesh.primitive_cone_add
    elif shape == 'cube':
        return bpy.ops.mesh.primitive_cube_add
    elif shape == 'cylinder':
        return bpy.ops.mesh.primitive_cylinder_add
    elif shape == 'sphere':
        return bpy.ops.mesh.primitive_uv_sphere_add
    else:
        raise NotImplementedError

def setup_scene():
    set_camera()
    set_rendering_options()
    set_background()

def set_camera():
    camera = D.objects['Camera']
    camera.location = [6, 0, 0]
    
def set_rendering_options():
    D.scenes["Scene"].render.resolution_percentage=100
    D.scenes["Scene"].render.resolution_x = 512
    D.scenes["Scene"].render.resolution_y = 512
    D.scenes['Scene'].render.image_settings.color_mode='RGB'

def set_background():
    background = D.objects['Background']
    background.location = [-5, 0, 0]
    # D.images['background.mp4'].filepath = '/blender/data/00001486.jpg'
    D.objects['Background'].scale[0] = 10
    D.objects['Background'].scale[1] = 10
    bg_mat = D.materials.get(f"background")
    rgba_color = rgb_to_rgba(BG_COLORS['dark'])
    bg_mat.diffuse_color = rgba_color

def select_objects_in_collection(name):
    for obj in D.collections[name].all_objects:
        obj.select_set(True)

def select_collection(name):
    C.view_layer.active_layer_collection =  \
        C.view_layer.layer_collection.children[name]

def add_material(obj, mat):
    # Assign it to object
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = mat
    else:
        # no slots
        obj.data.materials.append(mat)

def add_object(shape):
    add_shape_fn = get_shape_function(shape)
    add_shape_fn()
    new_shape = C.view_layer.objects.active
    new_shape.scale = SCALE
    return new_shape

def get_or_create_collection(name):
    if D.collections.get(name):
        obj_collection = D.collections[name]
    else:
        obj_collection = D.collections.new(name)
        C.scene.collection.children.link(obj_collection)
    return obj_collection

def add_light():
    bpy.ops.object.light_add(type='SUN', location=[0,0,10], rotation=[1,0,0])
    light = C.active_object.data
    light.energy = 1.5
    light.color = [1,1,1]