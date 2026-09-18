bl_info = {
    "name": "Move Skeletons & Empties to Collections",
    "author": "GitExplode",
    "version": (1, 2),
    "blender": (3, 0, 0),
    "location": "View3D > Object Menu / Search",
    "description": "Moves all selected armatures/empties and their child objects into individual collections named after each root object.",
    "category": "Object",
}

import bpy

def get_all_children(obj):
    """Recursively fetch all children and sub-children of an object."""
    children = []
    for child in obj.children:
        children.append(child)
        children.extend(get_all_children(child))
    return children

class OBJECT_OT_isolate_roots_to_collections(bpy.types.Operator):
    """Move each selected armature/empty and its child hierarchy to a dedicated collection"""
    bl_idname = "object.isolate_roots_to_collections"
    bl_label = "Move Selected Skeletons & Empties to Collections"
    bl_options = {'REGISTER', 'UNDO'}

    # Target types that act as roots for hierarchy isolation
    TARGET_TYPES = {'ARMATURE', 'EMPTY'}

    @classmethod
    def poll(cls, context):
        # Enables operator if at least one selected object is an Armature or Empty in Object Mode
        return (
            context.mode == 'OBJECT'
            and any(obj.type in cls.TARGET_TYPES for obj in context.selected_objects)
        )

    def execute(self, context):
        # Collect all selected armature and empty objects
        selected_roots = [
            obj for obj in context.selected_objects 
            if obj.type in self.TARGET_TYPES
        ]
        
        if not selected_roots:
            self.report({'WARNING'}, "No armatures or empties selected.")
            return {'CANCELLED'}

        moved_count = 0

        for root in selected_roots:
            collection_name = root.name
            
            # Create collection if it doesn't exist, otherwise reuse it
            if collection_name in bpy.data.collections:
                target_collection = bpy.data.collections[collection_name]
            else:
                target_collection = bpy.data.collections.new(collection_name)
                context.scene.collection.children.link(target_collection)

            # Gather this root object and all its recursive children
            objects_to_move = [root] + get_all_children(root)

            for obj in objects_to_move:
                # Link to target collection if not already linked
                if obj.name not in target_collection.objects:
                    target_collection.objects.link(obj)
                
                # Unlink from all other collections to keep scene clean
                for col in list(obj.users_collection):
                    if col != target_collection:
                        col.objects.unlink(obj)

            moved_count += 1

        self.report({'INFO'}, f"Moved {moved_count} hierarchy(ies) into separate collection(s).")
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_isolate_roots_to_collections.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_isolate_roots_to_collections)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_isolate_roots_to_collections)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()