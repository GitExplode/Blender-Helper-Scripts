bl_info = {
    "name": "Keep Basis and Active Shape Key",
    "author": "GitExplode",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "description": "Deletes all shape keys except Basis and the active one",
    "category": "Object",
}

import bpy


class KeepBasisAndActiveShapeKey(bpy.types.Operator):
    """Delete all shape keys except Basis and the active one"""
    bl_idname = "object.keep_basis_active_shapekey"
    bl_label = "Keep Basis and Active Shape Key"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ob = context.object

        if not ob or ob.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected")
            return {'CANCELLED'}

        if not ob.data.shape_keys:
            self.report({'WARNING'}, "Object has no shape keys")
            return {'CANCELLED'}

        if context.mode != 'OBJECT':
            self.report({'WARNING'}, "Must be in Object Mode")
            return {'CANCELLED'}

        sk_data = ob.data.shape_keys
        kbs = sk_data.key_blocks

        if len(kbs) == 0:
            return {'CANCELLED'}

        basis_name = kbs[0].name  # robust: Basis is always index 0
        active = ob.active_shape_key

        if not active:
            self.report({'WARNING'}, "No active shape key")
            return {'CANCELLED'}

        active_name = active.name

        # If active is already Basis, just keep Basis
        keep = {basis_name, active_name}

        # --- REMOVE DRIVERS referencing keys to be deleted ---
        if sk_data.animation_data:
            for d in list(sk_data.animation_data.drivers):
                path = d.data_path
                if 'key_blocks["' in path:
                    name = path.split('"')[1]
                    if name not in keep:
                        sk_data.animation_data.drivers.remove(d)

        # --- DELETE ALL EXCEPT KEEP SET ---
        for kb in reversed(kbs):
            if kb.name not in keep:
                ob.shape_key_remove(kb)

        # Restore active index (prefer active if still present)
        if active_name in kbs:
            ob.active_shape_key_index = kbs.find(active_name)
        else:
            ob.active_shape_key_index = kbs.find(basis_name)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(KeepBasisAndActiveShapeKey.bl_idname)


def register():
    bpy.utils.register_class(KeepBasisAndActiveShapeKey)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(KeepBasisAndActiveShapeKey)


if __name__ == "__main__":
    register()