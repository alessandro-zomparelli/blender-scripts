#-------------------- REALTIME MESH EXPORTER -------------------#
#-------------------------(basic version)-----------------------#
#                                                               #
# Realtime Mesh Exporter is a script that allows you to save    #
# the mesh in real time for immediate reading from external     #
# applications. You can set exporting options for different     #
# objects in "Object Data" menu.                                #
#                                                               #
#                      Alessandro Zomparelli                    #
#                             (2013)                            #
#                                                               #
# http://sketchesofcode.wordpress.com/                          #
#                                                               #
# Creative Commons                                              #
# CC BY-SA 3.0                                                  #
# http://creativecommons.org/licenses/by-sa/3.0/                #

import bpy
        
class ObjectButtonsPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_realtime_export"
    bl_label = "Select"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"    

class OBJECT_PT_realtime_export(ObjectButtonsPanel):
    bl_label = "Real-time Mesh Exporter"
    
    
    def draw(self, context):        
        layout = self.layout
        obj = context.object
        
        row = layout.row()
        row.prop(obj, 'prop_record')
        row.prop(obj, 'apply_modifiers')
        layout.label("File Path:")
        layout.prop(obj, 'prop_path', icon='FILE_FOLDER')
            
        if obj.prop_record: simple_export(obj, obj.prop_path)


def simple_export(obj, rec_path):    
    
    if obj.apply_modifiers: mesh = obj.to_mesh(bpy.context.scene, apply_modifiers=True, settings = 'RENDER')
    else: mesh = obj.data
    
    v_list = []
    for v in mesh.vertices:
        v_list.append(v.co)
    
    lines = []
    obj_text = open(rec_path + '.vertices', 'w')
    
    lines.append(str(len(v_list)) + '\n')    
    for i in range(0, len(v_list)):
        #open mesh
        co_1 = str(v_list[i][0])
        co_2 = str(v_list[i][1])
        co_3 = str(v_list[i][2])
        co = co_1 + ' ' + co_2 + ' ' + co_3 + '\n'
        lines.append(co)
    
    obj_text.writelines(lines)
    obj_text.close()
    
    obj_text = open(rec_path + '.faces', 'w')
    obj_text.write(str(len(mesh.polygons)) + '\n')    
    for f in mesh.polygons:
        for i in range(0,len(f.vertices)):
            a=str(f.vertices[i])
            if i != len(f.vertices) - 1:
                a += ' '
            obj_text.write(a)
        obj_text.write('\n')
    obj_text.close()
    
def initialize():
    bpy.types.Object.prop_record = bpy.props.BoolProperty(name = "Active Real-time", description = "Active realtime recording", default = False)
    bpy.types.Object.apply_modifiers = bpy.props.BoolProperty(name = "Modifiers", description = "Apply Modifiers", default = False)
    bpy.types.Object.prop_path = bpy.props.StringProperty(name="", description="Recording Folder", subtype='FILE_PATH')
    
initialize()
bpy.utils.register_class(OBJECT_PT_realtime_export)
