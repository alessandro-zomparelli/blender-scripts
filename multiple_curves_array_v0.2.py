#--------------------- MULTIPLE CURVES ARRAY -------------------#
#------------------------------ v0.2 ---------------------------#
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

scn = bpy.context.scene
ob = bpy.context.object
try:
    for m in ob.modifiers:
        if m.type == 'ARRAY':
            curve = m.curve
except:
    pass

curves = []
objects = []
bpy.ops.object.select_all(action='DESELECT')
bpy.context.scene.objects.active = curve
curve.select = True
bpy.ops.object.mode_set(mode = 'EDIT')

print("split curves")

n_splines = len(curve.data.splines)
next = curve
for i in range(n_splines):
    new_crv = next.copy()
    new_crv.data = next.data.copy()
    if i > 0: new_crv.data.splines.remove(new_crv.data.splines[0])
    next = new_crv.copy()
    next.data = new_crv.data.copy()
    curves.append(new_crv)
    delete = False
    for s in new_crv.data.splines:
        if delete: new_crv.data.splines.remove(s)
        delete = True
    scn.objects.link(new_crv)

bpy.ops.object.mode_set(mode = 'OBJECT')

bpy.ops.object.select_all(action='DESELECT')

print("copy objects")

for c in curves:
    new_ob = ob.copy()
    if merge:
        new_ob.data = ob.data.copy()
        objects.append(new_ob)
    scn.objects.link(new_ob)
    for m in new_ob.modifiers:
        if m.type == 'CURVE': m.object = c
        if m.type == 'ARRAY': m.curve = c

bpy.context.scene.update()

if merge:
    print("merge objects")
    for o in objects:
        o.data = o.to_mesh(scn, apply_modifiers=True, settings = 'PREVIEW')
        o.modifiers.clear()
        o.select = True
        scn.objects.active = o
    bpy.ops.object.join()
    for c in curves: bpy.data.objects.remove(c)
