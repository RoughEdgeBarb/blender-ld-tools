
bl_info = {
    "name": "LDTools",
    "category": "Level Design",
    "author": "RoughEdgeBarb",
    "description": "Level Design tools to improve workflow",
    "blender": (4, 0, 0),
    "version": (0, 1),
    "location": "View3D -> Tool Shelf",
    "warning" : "",
    "wiki_url": "burning-barb.itch.io/gltf-level-importer"
}


import bpy


class LDToolsPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_LDTools"
    bl_label = "LDTools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LDTools'
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("export_scene.gltf")
        
        row = layout.row()
        # one "grid unit" is 1/32nd of a meter, approx 3cm
        grid_scale = bpy.context.space_data.overlay.grid_scale
        grid_units = grid_scale * 32.0
        row.label(text = "Grid Scale " + str(grid_units) + " units   " + str(grid_scale) + "m")
        row = layout.row()
        row.operator("ld.divide_grid")
        row.operator("ld.multiply_grid")
        
        row = layout.row()
        row.operator("mesh.extrude_and_rotate")
        
        
        row = layout.row()
        row.prop(context.tool_settings, "use_transform_correct_face_attributes", text = "Correct Face Attributes")
        row = layout.row()
        row.prop(context.space_data.region_3d, "lock_rotation", text = "Lock View Rotation")
        
        
        



class multiply_grid_scale(bpy.types.Operator):
    bl_idname = 'ld.multiply_grid'
    bl_label = "x2"
    def execute(self, context):
        
        bpy.context.space_data.overlay.grid_scale = 2 * bpy.context.space_data.overlay.grid_scale
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)


class divide_grid_scale(bpy.types.Operator):
    bl_idname = 'ld.divide_grid'
    bl_label = "/2"
    def execute(self, context):
        
        bpy.context.space_data.overlay.grid_scale = bpy.context.space_data.overlay.grid_scale / 2
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)



class MESH_OT_extrude_and_rotate(bpy.types.Operator):
    "Extrude the Mesh and Rotate + Offset around pivot point, around Z axis"
    bl_idname = 'mesh.extrude_and_rotate'
    bl_label = "Extrude and Rotate"
    bl_options = {"REGISTER", "UNDO"}
    
    rot_degrees: bpy.props.FloatProperty(
        name = "Rotation",
        default = 15.0,
        description = "How much to rotate by",
    )
    v_offset: bpy.props.FloatProperty(
        name = "Vertical Offset",
        default = 0.0,
        description = "Increase height by this much",
    )
    
    def execute(self, context):
        rot_rad = self.rot_degrees * 0.0174532925
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 1), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "alt_navigation":False, "use_automerge_and_split":False})
        bpy.ops.transform.rotate(value=rot_rad, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)




def register():
    bpy.utils.register_class(LDToolsPanel)
    bpy.utils.register_class(divide_grid_scale)
    bpy.utils.register_class(multiply_grid_scale)
    bpy.utils.register_class(MESH_OT_extrude_and_rotate)


        
def unregister():
    bpy.utils.unregister_class(LDToolsPanel)
    bpy.utils.unregister_class(divide_grid_scale)
    bpy.utils.unregister_class(multiply_grid_scale)
    bpy.utils.unregister_class(MESH_OT_extrude_and_rotate)


if __name__== "__main__":
    register()