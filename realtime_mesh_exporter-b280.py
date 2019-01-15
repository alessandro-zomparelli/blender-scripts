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

bl_info = {
    "name": "Realtime Mesh Exporter",
    "author": "Alessandro Zomparelli (Co-de-iT)",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Save mesh data to external files",
    "warning": "",
    "wiki_url": "https://wiki.blender.org/index.php/Extensions:2.6/"
                "Py/Scripts/Mesh/Tissue",
    "tracker_url": "https://plus.google.com/u/0/+AlessandroZomparelli/",
    "category": "Mesh"}

import bpy

class OBJECT_PT_realtime_export(bpy.types.Panel):
    bl_idname = "OBJECT_PT_realtime_export"
    bl_label = "Real-time Mesh Exporter"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        try:
            ob = context.object
            return ob.type == 'MESH'
        except: return False

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.prop(obj, 'prop_record')
        row.operator('object.export_mesh_data', icon='EXPORT')
        row = layout.row()
        row.prop(obj, 'RT_apply_modifiers')
        row.prop(obj, 'RT_export_weight')
        layout.label(text="File Path:")
        layout.prop(obj, 'RT_prop_path', icon='FILE_FOLDER')

        if obj.prop_record: simple_export(obj, obj.RT_prop_path)


def simple_export(obj, rec_path):

    if obj.RT_apply_modifiers: mesh = obj.to_mesh(bpy.context.depsgraph, True)
    else: mesh = obj.data

    # save VERTICES
    v_list = []
    for v in mesh.vertices:
        v_list.append(v.co)

    lines = []
    rec_path = bpy.path.abspath(rec_path)
    obj_text = open(rec_path + '_vertices.txt', 'w+')

    lines.append(str(len(v_list)) + '\n')
    for i in range(0, len(v_list)):
        #open mesh
        co_1 = str(v_list[i][0])
        co_2 = str(v_list[i][1])
        co_3 = str(v_list[i][2])
        co = co_1 + ', ' + co_2 + ', ' + co_3 + '\n'
        lines.append(co)

    obj_text.writelines(lines)
    obj_text.close()

    # save FACES
    obj_text = open(rec_path + '_faces.txt', 'w+')
    obj_text.write(str(len(mesh.polygons)) + '\n')
    for f in mesh.polygons:
        for i in range(0,len(f.vertices)):
            a=str(f.vertices[i])
            if i != len(f.vertices) - 1:
                a += ' '
            obj_text.write(a)
        obj_text.write('\n')
    obj_text.close()

    # save WEIGHT
    if obj.RT_export_weight and obj.vertex_groups.active:
        obj_text = open(rec_path + '_weight.txt', 'w+')
        obj_text.write(str(len(mesh.vertices)) + '\n')
        group_id = obj.vertex_groups.active_index
        for v in mesh.vertices:
            weight = 0
            for w in v.groups:
                if w.group == group_id:
                    weight = w.weight
            obj_text.write(str(weight) + '\n')
        obj_text.close()


class export_mesh_data(bpy.types.Operator):
    bl_idname = "object.export_mesh_data"
    bl_label = "Export Mesh Data"
    bl_description = ("")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.object
        simple_export(obj, obj.RT_prop_path)
        return {'FINISHED'}

classes = (
    OBJECT_PT_realtime_export,
    export_mesh_data
    )

def register():
    from bpy.utils import register_class
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.prop_record = bpy.props.BoolProperty(name = "Active Real-time", description = "Active realtime recording", default = False)
    bpy.types.Object.RT_apply_modifiers = bpy.props.BoolProperty(name = "Modifiers", description = "Apply Modifiers", default = False)
    bpy.types.Object.RT_export_weight = bpy.props.BoolProperty(name = "Export Weight", description = "Export Active Weight", default = False)
    bpy.types.Object.RT_prop_path = bpy.props.StringProperty(name="", description="Recording Folder", subtype='FILE_PATH')

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        bpy.utils.unregister_class(cls)
