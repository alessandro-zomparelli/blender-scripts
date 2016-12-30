#------------------- export gcode G1 movements -----------------#
#                                                               #
# Simple script for exporting selected curves as G1 lines for   #
# generating a gcode from curves. XYZ coordinates are correctly #
# generated accordingly to model size and position.             #
# E for extruding filament need to be fixed.                    #
#                                                               #
#                      Alessandro Zomparelli                    #
#                             (2016)                            #
#                                                               #
#                                                               #
# Creative Commons                                              #
# CC BY-SA 3.0                                                  #
# http://creativecommons.org/licenses/by-sa/3.0/                #


# SETTINGS

extrusion_parameter = 10     # adjust the amount of extruded filament



import bpy

obj = bpy.context.active_object
rec_path = bpy.path.abspath("//" + obj.name)


def simple_curves_export():    
    
    crvs = obj.data.splines
    
    # sort curves in Z
    sorted_curves = {}
    for i in range(len(crvs)):
        sorted_curves[crvs[i].points[0].co[2]] = i
        
    print(sorted_curves)
    
    pts_list = []
    for id in sorted_curves:
        for pt in crvs[sorted_curves[id]].points:
            pts_list.append(pt.co)
    
    lines = []
    obj_text = open(rec_path + '.gcode', 'w')
    
    #lines.append(str(len(pts_list)) + '\n')    
    for i in range(0, len(pts_list)):
        pt1 = pts_list[i]
        if i>0:
            distVec = pt0 - pt1
            extrusion = distVec.length*extrusion_parameter
        else: extrusion = 0
        
        # open mesh
        co_1 = str(pts_list[i][0])
        co_2 = str(pts_list[i][1])
        co_3 = str(pts_list[i][2])
        extrusion_string = "%.1f" % extrusion
        co = 'G1 ' + 'X' + co_1 + ' Y' + co_2 + ' Z' + co_3 + ' E' + extrusion_string + '\n'
        lines.append(co)
        
        pt0 = pt1
    
    obj_text.writelines(lines)
    obj_text.close()
    
    '''
    obj_text = open(rec_path + '.curves', 'w')
    #obj_text.write(str(len(crvs)) + '\n')    
    for crv in crvs:
        obj_text.write(str(len(crv.points)))
        obj_text.write('\n')
    obj_text.close()
    '''
    
if(obj.type == 'CURVE'): simple_curves_export()