#--------------------------- z slicer --------------------------#
#                                                               #
# Simple script for mesh slicing through planes moving along    #
# the z-axis.                                                   #
#                                                               #
#                      Alessandro Zomparelli                    #
#                             (2016)                            #
#                                                               #
#                                                               #
# Creative Commons                                              #
# CC BY-SA 3.0                                                  #
# http://creativecommons.org/licenses/by-sa/3.0/                #

# SETTINGS

apply_modifiers = True      # set True if you want to consider the Modified object
join_slices= False          # set True if you want to join together all generated slices
convert_to_curve = True     # set True if you want to convert the final result to curves
z_step = 0.05               # set the distance between each slice


import bpy

ob = bpy.context.active_object
bpy.ops.object.select_all(action='TOGGLE')

# create clone
me = ob.to_mesh(scene=bpy.context.scene, apply_modifiers=apply_modifiers, settings='PREVIEW')
me.transform(ob.matrix_world)
ob1 = bpy.data.objects.new('clone', me)
bpy.context.scene.objects.link(ob1)
z_min = ob1.bound_box[0][2]
z_max = ob1.bound_box[1][2]

# delete clone
ob1.select = True
bpy.context.scene.objects.active = ob1
bpy.ops.object.delete()

i = 0
while True:
    ob_new = bpy.data.objects.new(str(i), me.copy())
    bpy.context.scene.objects.link(ob_new)
    #ob_new.scale = ob.scale
    #ob_new.location = ob.location
    #bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    #if(i == 0):
    #    z_min = ob_new.bound_box[0][2]
    #    z_max = ob_new.bound_box[1][2]
    ob_new.select = True
    bpy.context.scene.objects.active = ob_new
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.bisect(plane_co=(0, 0, z_min + z_step*i), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, clear_outer=True, threshold=0.0001, xstart=0, xend=0, ystart=0, yend=0)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    i+=1
    if(z_min + i*z_step > z_max):
        break

if(join_slices):
    bpy.ops.object.join()
    if(convert_to_curve):
        bpy.ops.object.convert(target='CURVE')


