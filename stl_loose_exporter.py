bl_info = {
    "name": "STL Loose Exporter",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (1, 0),
    "description": "Separates loose parts of an object and exports them as individual STL files",
    "author": "Your Name",
    "location": "View3D > Tool Shelf > STL Loose Exporter",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

import bpy
import os

class WM_OT_report_error(bpy.types.Operator):
    bl_idname = "wm.report_error"
    bl_label = "Report Error"
    message: bpy.props.StringProperty()

    def execute(self, context):
        self.report({'ERROR'}, self.message)
        return {'FINISHED'}

class OBJECT_OT_export_separated_parts(bpy.types.Operator):
    bl_idname = "object.export_separated_parts"
    bl_label = "Export Separated Parts"
    bl_options = {'REGISTER', 'UNDO'}

    export_path: bpy.props.StringProperty(
        name="Export Path",
        description="Path to export separated parts",
        default="/tmp",
        subtype='DIR_PATH'
    )

    scale_factor: bpy.props.FloatProperty(
        name="Scale Factor",
        description="Scaling factor for the exported STL files",
        default=1000.0,
    )

    def ensure_directory_exists(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            # Check if the directory is writable
            if not os.access(path, os.W_OK):
                raise PermissionError(f"The directory {path} is not writable.")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
            return False
        return True

    def duplicate_object(self, obj):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.duplicate()
        return bpy.context.active_object

    def apply_modifiers(self, obj):
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.convert(target='MESH')

    def separate_loose_parts(self, obj):
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')

    def rename_parts(self, objects, base_name):
        for i, obj in enumerate(objects):
            obj.name = f'{base_name}_{i+1}'

    def export_to_stl(self, objects, export_path, scale_factor):
        exported_files = []
        for obj in objects:
            export_file = os.path.join(export_path, f"{obj.name}.stl")
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.export_mesh.stl(filepath=export_file, use_selection=True, global_scale=scale_factor)
            exported_files.append(export_file)
        return exported_files

    def delete_objects(self, objects):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.select_set(True)
        bpy.ops.object.delete()

    def execute(self, context):
        if not self.ensure_directory_exists(self.export_path):
            self.report({'ERROR'}, "Script execution stopped due to directory issues.")
            return {'CANCELLED'}

        if bpy.context.active_object and bpy.context.active_object.type == 'MESH':
            active_obj = bpy.context.active_object
            original_name = active_obj.name
            duplicated_obj = self.duplicate_object(active_obj)
            
            self.apply_modifiers(duplicated_obj)
            self.separate_loose_parts(duplicated_obj)
            
            separated_objects = bpy.context.selected_objects
            self.rename_parts(separated_objects, original_name)
            
            exported_files = self.export_to_stl(separated_objects, self.export_path, self.scale_factor)
            
            self.delete_objects(separated_objects)
            
            # Log the exported files
            for file in exported_files:
                self.report({'INFO'}, f"Exported: {file}")
            
            # Reselect the original object
            bpy.ops.object.select_all(action='DESELECT')
            active_obj.select_set(True)
            bpy.context.view_layer.objects.active = active_obj
            
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Error: Please select a mesh object.")
            return {'CANCELLED'}

class OBJECT_PT_export_separated_parts_panel(bpy.types.Panel):
    bl_label = "STL Loose Exporter"
    bl_idname = "OBJECT_PT_export_separated_parts"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_export_separated_parts.bl_idname)
        layout.prop(context.scene, "export_separated_parts_path")
        layout.prop(context.scene, "export_separated_parts_scale")

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_export_separated_parts.bl_idname)

def register():
    bpy.utils.register_class(WM_OT_report_error)
    bpy.utils.register_class(OBJECT_OT_export_separated_parts)
    bpy.utils.register_class(OBJECT_PT_export_separated_parts_panel)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    bpy.types.Scene.export_separated_parts_path = bpy.props.StringProperty(
        name="Export Path",
        description="Path to export separated parts",
        default="/tmp",
        subtype='DIR_PATH'
    )
    bpy.types.Scene.export_separated_parts_scale = bpy.props.FloatProperty(
        name="Scale Factor",
        description="Scaling factor for the exported STL files",
        default=1000.0,
    )

def unregister():
    bpy.utils.unregister_class(WM_OT_report_error)
    bpy.utils.unregister_class(OBJECT_OT_export_separated_parts)
    bpy.utils.unregister_class(OBJECT_PT_export_separated_parts_panel)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    del bpy.types.Scene.export_separated_parts_path
    del bpy.types.Scene.export_separated_parts_scale

if __name__ == "__main__":
    register()

