bl_info = {
    "name": "Remove Shape Key Drivers",
    "author": "GitExplode",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Shape Keys Tools",
    "description": "Bulk remove drivers from shape keys",
    "category": "Animation",
}

import bpy


class OBJECT_OT_remove_shape_key_drivers(bpy.types.Operator):
    bl_idname = "object.remove_shape_key_drivers"
    bl_label = "Remove Shape Key Drivers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        # Enforce Object Mode
        if obj.mode != 'OBJECT':
            self.report({'ERROR'}, "Must be in Object Mode")
            return {'CANCELLED'}

        # Validate shape keys exist
        if not obj.data.shape_keys or not obj.data.shape_keys.key_blocks:
            self.report({'WARNING'}, "No shape keys found")
            return {'CANCELLED'}

        key_blocks = obj.data.shape_keys.key_blocks

        # Your original logic (expanded safely)
        for b in key_blocks:
            try:
                b.driver_remove("value")
            except TypeError:
                # Some keys may not have drivers; ignore safely
                pass

        self.report({'INFO'}, "Shape key drivers removed")
        return {'FINISHED'}


class VIEW3D_PT_shape_key_driver_tools(bpy.types.Panel):
    bl_label = "Shape Keys Tools"
    bl_idname = "VIEW3D_PT_shape_key_driver_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shape Keys Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.remove_shape_key_drivers", icon='DRIVER')


def register():
    bpy.utils.register_class(OBJECT_OT_remove_shape_key_drivers)
    bpy.utils.register_class(VIEW3D_PT_shape_key_driver_tools)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_shape_key_driver_tools)
    bpy.utils.unregister_class(OBJECT_OT_remove_shape_key_drivers)


if __name__ == "__main__":
    register()