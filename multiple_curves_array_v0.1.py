#--------------------- MULTIPLE CURVES ARRAY -------------------#
#------------------------------ v0.1 ---------------------------#
#                                                               #
# The aim of this script is to allow the creation of arrays     #
# along multiple curves. By default, using an array modifier    #
# that fits a curve, and then a curve modifier along the same   #
# curve makes the object following only a single curve.         #
# Also if your curve object has multiple splines, it will       #
# follow just one of them. With this script you can select your #
# object and make it working along all the splines of the curve #
# object.                                                       #
#                                                               #
# The option "merge" will allow to automatically merge the      #
# resulting object. This will apply all the modifiers.          #
# If "merge" is False, then all the generated object will be    #
# linked copies.                                                #
#                                                               #
#                      Alessandro Zomparelli                    #
#                             (2018)                            #
#                                                               #
# http://www.alessandrozomparelli.com/                          #
#                                                               #
# Creative Commons                                              #
# CC BY-SA 3.0                                                  #
# http://creativecommons.org/licenses/by-sa/3.0/                #

import bpy

merge = False

ob = bpy.context.object
try:
    for m in ob.modifiers:
        if m.type == 'ARRAY':
            curve = m.curve
except:
    pass

curves = []
objects = [ob]
bpy.ops.object.select_all(action='DESELECT')
bpy.context.scene.objects.active = curve
curve.select = True
bpy.ops.object.mode_set(mode = 'EDIT')

while len(curve.data.splines)>1:
    bpy.ops.curve.select_all(action='DESELECT')
    spl = curve.data.splines[0]
    if spl.type == 'BEZIER': spl.bezier_points[0].select_control_point = True
    else: spl.points[0].select = True
    bpy.ops.curve.select_linked()
    bpy.ops.curve.separate()

bpy.ops.object.mode_set(mode = 'OBJECT')


curves = bpy.context.selected_objects
bpy.ops.object.select_all(action='DESELECT')

bpy.context.scene.objects.active = ob
ob.select = True

for c in curves:
    if merge: 
        bpy.ops.object.duplicate_move()
        objects.append(bpy.context.object)
    else: bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True})
    print(c.name)
    for m in bpy.context.object.modifiers:
        if m.type == 'CURVE': m.object = c
        if m.type == 'ARRAY': m.curve = c

if merge:
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects: 
        o.select = True
        bpy.context.scene.objects.active = o
        for m in o.modifiers:
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier=m.name)

    bpy.context.scene.objects.active = ob
    bpy.ops.object.join()
