import bpy
import math
from mathutils import Vector

scene = bpy.context.scene

# clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def make_mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = color
    return m

# drone root
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 5))
drone_root = bpy.context.active_object
drone_root.name = "DroneRoot"

def add_child(obj):
    obj.parent = drone_root
    obj.matrix_parent_inverse = drone_root.matrix_world.inverted()

# drone body
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 5))
body = bpy.context.active_object
body.scale = (0.35, 0.35, 0.12)
bpy.ops.object.transform_apply(scale=True)
body.data.materials.append(make_mat("mat_body", (0.9, 0.2, 0.05, 1)))
add_child(body)

# sensor
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(0, 0, 4.86))
sensor = bpy.context.active_object
sensor.data.materials.append(make_mat("mat_sensor", (0.1, 0.6, 1.0, 1)))
add_child(sensor)

arm_positions = [(0.55,0.55), (-0.55,0.55), (-0.55,-0.55), (0.55,-0.55)]
prop_objects = []

for i, (ax, ay) in enumerate(arm_positions):

    bpy.ops.mesh.primitive_cube_add(location=(ax*0.5, ay*0.5, 5))
    arm = bpy.context.active_object
    arm.scale = (0.06, 0.06, 0.42)
    arm.rotation_euler = (math.pi/2, 0, math.atan2(ay, ax))
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    arm.data.materials.append(make_mat(f"mat_arm_{i}", (1.0, 0.75, 0.0, 1)))
    add_child(arm)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=0.08, location=(ax, ay, 5.04))
    motor = bpy.context.active_object
    motor.data.materials.append(make_mat(f"mat_motor_{i}", (0.6, 0.05, 0.05, 1)))
    add_child(motor)

    for angle_offset in (0, math.pi/2):
        bpy.ops.mesh.primitive_cube_add(location=(ax, ay, 5.10))
        blade = bpy.context.active_object
        blade.scale = (0.40, 0.04, 0.01)
        blade.rotation_euler = (0, 0, angle_offset)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        blade.data.materials.append(make_mat(f"mat_blade_{i}", (0.95, 0.95, 0.95, 1)))
        add_child(blade)
        prop_objects.append(blade)

# sky
bpy.ops.mesh.primitive_uv_sphere_add(radius=60, location=(0, 0, 0))
sky = bpy.context.active_object
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.flip_normals()
bpy.ops.object.mode_set(mode='OBJECT')
sky.data.materials.append(make_mat("mat_sky", (0.3, 0.6, 1.0, 1)))

# ground
bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
ground = bpy.context.active_object
ground.dimensions = (80, 80, 0)
ground.data.materials.append(make_mat("mat_ground", (0.12, 0.40, 0.10, 1)))

# road
bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0.01))
road = bpy.context.active_object
road.dimensions = (4, 80, 0)
road.data.materials.append(make_mat("mat_road", (0.25, 0.25, 0.25, 1)))

# line
bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0.02))
line = bpy.context.active_object
line.dimensions = (0.2, 80, 0)
line.data.materials.append(make_mat("mat_line", (1.0, 1.0, 0.0, 1)))

# buildings
building_data = [
    (8,8,2.5,2.5,6,0.8,0.5,0.2),
    (-9,7,2,2,8,0.2,0.4,0.8),
    (9,-8,3,2,5,0.6,0.2,0.6),
    (-8,-9,2.5,3,7,0.2,0.65,0.35),
    (5,12,1.8,1.8,9,0.85,0.2,0.2),
    (-6,-12,2,2,6,0.9,0.8,0.1),
    (13,3,2.2,2.2,5,0.3,0.7,0.7),
    (-13,-3,2,3,8,0.75,0.45,0.2)
]

for bx, by, bw, bd, bh, r, g, b in building_data:
    bpy.ops.mesh.primitive_cube_add(location=(bx, by, bh/2))
    bld = bpy.context.active_object
    bld.dimensions = (bw, bd, bh)
    bpy.ops.object.transform_apply(scale=True)
    bld.data.materials.append(make_mat(f"mat_bld_{bx}", (r, g, b, 1)))

# tower
bpy.ops.mesh.primitive_cylinder_add(radius=1.2, depth=10, location=(0,0,5))
tower = bpy.context.active_object
tower.data.materials.append(make_mat("mat_tower", (0.75,0.75,0.8,1)))

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=3, location=(0,0,11.5))
antenna = bpy.context.active_object
antenna.data.materials.append(make_mat("mat_antenna", (0.9,0.1,0.1,1)))

# lighting
sun = bpy.data.lights.new(name="Sun", type='SUN')
sun.energy = 5
sun_obj = bpy.data.objects.new("Sun", sun)
bpy.context.collection.objects.link(sun_obj)
sun_obj.location = (8,-8,15)
sun_obj.rotation_euler = (0.6,0,0.8)

fill = bpy.data.lights.new(name="Fill", type='POINT')
fill.energy = 800
fill_obj = bpy.data.objects.new("Fill", fill)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (-6,6,8)

# camera
cam = bpy.data.cameras.new(name="cam")
cam_obj = bpy.data.objects.new("Camera", cam)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (14,-12,8)

# animation
scene.frame_start = 0
scene.frame_end = 200

for frame in range(scene.frame_start, scene.frame_end+1):
    scene.frame_set(frame)

    angle = frame * 0.05

    drone_root.location = Vector((
        8*math.cos(angle),
        6*math.sin(angle),
        5 + math.sin(frame*0.08)*1.5
    ))

    drone_root.rotation_euler = (0, math.sin(angle)*0.15, angle + math.pi/2)

    drone_root.keyframe_insert("location", index=-1)
    drone_root.keyframe_insert("rotation_euler", index=-1)

    spin = (frame/4)*(2*math.pi)
    for blade in prop_objects:
        blade.rotation_euler = (0,0,spin)
        blade.keyframe_insert("rotation_euler", index=-1)

    direction = drone_root.location - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat('-Z','Y').to_euler()
    cam_obj.keyframe_insert("rotation_euler", index=-1)

# render
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.fps = 24
scene.render.filepath = "//drone_animation_output"
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'

print("Done - press Ctrl+F12")