bl_info = {
    "name": "Reset Shape Keys to Zero",
    "author": "GitExplode",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Object > Set Shapekeys to Zero",
    "description": "Sets all shape keys except Basis of the active object to zero",
    "category": "Object",
}

import bpy


class OBJECT_OT_reset_shapekeys_zero(bpy.types.Operator):
    bl_idname = "object.reset_shapekeys_zero"
    bl_label = "Set Shape Keys to Zero"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object

        if not obj:
            self.report({'WARNING'}, "No active object")
            return {'CANCELLED'}

        if obj.type != 'MESH':
            self.report({'WARNING'}, "Active object is not a mesh")
            return {'CANCELLED'}

        if not obj.data.shape_keys:
            self.report({'WARNING'}, "Object has no shape keys")
            return {'CANCELLED'}

        for key in obj.data.shape_keys.key_blocks:
            if key.name != "Basis":
                key.value = 0.0

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_reset_shapekeys_zero.bl_idname, icon='SHAPEKEY_DATA')


def register():
    bpy.utils.register_class(OBJECT_OT_reset_shapekeys_zero)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_reset_shapekeys_zero)


if __name__ == "__main__":
    register()