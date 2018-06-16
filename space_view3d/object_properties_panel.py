import bpy
import math
from bpy.app.translations import pgettext_iface as iface_ #for decimate modifier
from ..bp_lib import unit, utils
import mathutils

enum_object_tabs = [('INFO'," ","Show the Main Information"),
                    ('MATERIAL',"","Show the materials assign to the object"),
                    ('CONSTRAINTS',"","Show the constraints assigned to the object"),
                    ('MODIFIERS',"","Show the modifiers assigned to the object")]     

def draw_texture(layout,tex):
    layout.prop(tex,'type')
    layout.separator()
    
    if tex.type == 'CLOUDS':
        layout.row().prop(tex, "cloud_type", expand=True)
        layout.label(text="Noise:")
        layout.row().prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        col.prop(tex, "noise_depth", text="Depth")

        split.prop(tex, "nabla", text="Nabla")   
           
    if tex.type == 'WOOD':
        layout.row().prop(tex, "noise_basis_2", expand=True)
        layout.row().prop(tex, "wood_type", expand=True)

        col = layout.column()
        col.active = tex.wood_type in {'RINGNOISE', 'BANDNOISE'}
        col.label(text="Noise:")
        col.row().prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()
        split.active = tex.wood_type in {'RINGNOISE', 'BANDNOISE'}

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        col.prop(tex, "turbulence")

        split.prop(tex, "nabla")
    
    if tex.type == 'MARBLE':
        layout.row().prop(tex, "marble_type", expand=True)
        layout.row().prop(tex, "noise_basis_2", expand=True)
        layout.label(text="Noise:")
        layout.row().prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        col.prop(tex, "noise_depth", text="Depth")

        col = split.column()
        col.prop(tex, "turbulence")
        col.prop(tex, "nabla")  
        
    if tex.type == 'MAGIC':      
        row = layout.row()
        row.prop(tex, "noise_depth", text="Depth")
        row.prop(tex, "turbulence")    
        
    if tex.type == 'BLEND':      
        sub = layout.row()

        sub.active = (tex.progression in {'LINEAR', 'QUADRATIC', 'EASING', 'RADIAL'})
        sub.prop(tex, "use_flip_axis", expand=True)
        
    if tex.type == 'STUCCI': 
        layout.row().prop(tex, "stucci_type", expand=True)
        layout.label(text="Noise:")
        layout.row().prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        row = layout.row()
        row.prop(tex, "noise_scale", text="Size")
        row.prop(tex, "turbulence")
        
    if tex.type == 'IMAGE':
        layout.template_image(tex, "image", tex.image_user)
        
    if tex.type == 'MUSGRAVE':
        layout.prop(tex, "musgrave_type")

        split = layout.split()

        col = split.column()
        col.prop(tex, "dimension_max", text="Dimension")
        col.prop(tex, "lacunarity")
        col.prop(tex, "octaves")

        musgrave_type = tex.musgrave_type
        col = split.column()
        if musgrave_type in {'HETERO_TERRAIN', 'RIDGED_MULTIFRACTAL', 'HYBRID_MULTIFRACTAL'}:
            col.prop(tex, "offset")
        col.prop(tex, "noise_intensity", text="Intensity")
        if musgrave_type in {'RIDGED_MULTIFRACTAL', 'HYBRID_MULTIFRACTAL'}:
            col.prop(tex, "gain")

        layout.label(text="Noise:")

        layout.prop(tex, "noise_basis", text="Basis")

        row = layout.row()
        row.prop(tex, "noise_scale", text="Size")
        row.prop(tex, "nabla")
    
    if tex.type == 'VORONOI':
        split = layout.split()

        col = split.column()
        col.label(text="Distance Metric:")
        col.prop(tex, "distance_metric", text="")
        sub = col.column()
        sub.active = tex.distance_metric == 'MINKOVSKY'
        sub.prop(tex, "minkovsky_exponent", text="Exponent")
        col.label(text="Coloring:")
        col.prop(tex, "color_mode", text="")
        col.prop(tex, "noise_intensity", text="Intensity")

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Feature Weights:")
        sub.prop(tex, "weight_1", text="1", slider=True)
        sub.prop(tex, "weight_2", text="2", slider=True)
        sub.prop(tex, "weight_3", text="3", slider=True)
        sub.prop(tex, "weight_4", text="4", slider=True)

        layout.label(text="Noise:")
        row = layout.row()
        row.prop(tex, "noise_scale", text="Size")
        row.prop(tex, "nabla")
        
    if tex.type == 'DISTORTED_NOISE':
        layout.prop(tex, "noise_distortion")
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "distortion", text="Distortion")
        col.prop(tex, "noise_scale", text="Size")

        split.prop(tex, "nabla")
    
    if tex.type == 'POINT_DENSITY':
        pd = tex.point_density

        layout.row().prop(pd, "point_source", expand=True)

        split = layout.split()

        col = split.column()
        if pd.point_source == 'PARTICLE_SYSTEM':
            col.label(text="Object:")
            col.prop(pd, "object", text="")

            sub = col.column()
            sub.enabled = bool(pd.object)
            if pd.object:
                sub.label(text="System:")
                sub.prop_search(pd, "particle_system", pd.object, "particle_systems", text="")
            sub.label(text="Cache:")
            sub.prop(pd, "particle_cache_space", text="")
        else:
            col.label(text="Object:")
            col.prop(pd, "object", text="")
            col.label(text="Cache:")
            col.prop(pd, "vertex_cache_space", text="")

        col.separator()

        col.label(text="Color Source:")
        if pd.point_source == 'PARTICLE_SYSTEM':
            col.prop(pd, "particle_color_source", text="")
            if pd.particle_color_source in {'PARTICLE_SPEED', 'PARTICLE_VELOCITY'}:
                col.prop(pd, "speed_scale")
            if pd.particle_color_source in {'PARTICLE_SPEED', 'PARTICLE_AGE'}:
                layout.template_color_ramp(pd, "color_ramp", expand=True)
        else:
            col.prop(pd, "vertex_color_source", text="")
            if pd.vertex_color_source == 'VERTEX_COLOR':
                if pd.object and pd.object.data:
                    col.prop_search(pd, "vertex_attribute_name", pd.object.data, "vertex_colors", text="")
            if pd.vertex_color_source == 'VERTEX_WEIGHT':
                if pd.object:
                    col.prop_search(pd, "vertex_attribute_name", pd.object, "vertex_groups", text="")
                layout.template_color_ramp(pd, "color_ramp", expand=True)

        col = split.column()
        col.label()
        col.prop(pd, "radius")
        col.label(text="Falloff:")
        col.prop(pd, "falloff", text="")
        if pd.falloff == 'SOFT':
            col.prop(pd, "falloff_soft")
        if pd.falloff == 'PARTICLE_VELOCITY':
            col.prop(pd, "falloff_speed_scale")

        col.prop(pd, "use_falloff_curve")

        if pd.use_falloff_curve:
            col = layout.column()
            col.label(text="Falloff Curve")
            col.template_curve_mapping(pd, "falloff_curve", brush=False)
            
    if tex.type == 'OCEAN':
        ot = tex.ocean

        col = layout.column()
        col.prop(ot, "ocean_object")
        col.prop(ot, "output")
                
def draw_modifier(mod,layout,obj):
    
    def draw_show_expanded(mod,layout):
        if mod.show_expanded:
            layout.prop(mod,'show_expanded',text="",emboss=False)
        else:
            layout.prop(mod,'show_expanded',text="",emboss=False)
    
    def draw_apply_close(layout):
        layout.operator('object.modifier_apply',text="",icon='EDIT',emboss=False).modifier = mod.name
        layout.operator('object.modifier_move_up',text="",icon='TRIA_UP',emboss=False).modifier = mod.name
        layout.operator('object.modifier_move_down',text="",icon='TRIA_DOWN',emboss=False).modifier = mod.name
        layout.operator('object.modifier_remove',text="",icon='PANEL_CLOSE',emboss=False).modifier = mod.name
    
    def draw_visibility(layout):
        layout.label("Visibility:")
        layout.prop(mod,'show_render')
        layout.prop(mod,'show_viewport')
        layout.prop(mod,'show_in_editmode')
    
    def draw_array_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_ARRAY')
        draw_apply_close(row)

        
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)            
            box = col.box()
            box.prop(mod, "fit_type")
    
            if mod.fit_type == 'FIXED_COUNT':
                box.prop(mod, "count")
            elif mod.fit_type == 'FIT_LENGTH':
                box.prop(mod, "fit_length")
            elif mod.fit_type == 'FIT_CURVE':
                box.prop(mod, "curve")
    
            box.separator()
    
            split = box.split()
    
            col = split.column()
            col.prop(mod, "use_constant_offset")
            sub = col.column()
            sub.active = mod.use_constant_offset
            sub.prop(mod, "constant_offset_displace", text="")
    
            col.separator()
    
            col.prop(mod, "use_merge_vertices", text="Merge")
            sub = col.column()
            sub.active = mod.use_merge_vertices
            sub.prop(mod, "use_merge_vertices_cap", text="First Last")
            sub.prop(mod, "merge_threshold", text="Distance")
    
            col = split.column()
            col.prop(mod, "use_relative_offset")
            sub = col.column()
            sub.active = mod.use_relative_offset
            sub.prop(mod, "relative_offset_displace", text="")
    
            col.separator()
    
            col.prop(mod, "use_object_offset")
            sub = col.column()
            sub.active = mod.use_object_offset
            sub.prop(mod, "offset_object", text="")
    
            box.separator()
    
            box.prop(mod, "start_cap")
            box.prop(mod, "end_cap")
            
    def draw_bevel_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_BEVEL')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            split = box.split()
    
            col = split.column()
            col.prop(mod, "width")
            col.prop(mod, "segments")
            col.prop(mod, "profile")
    
            col = split.column()
            col.prop(mod, "use_only_vertices")
            col.prop(mod, "use_clamp_overlap")
    
            box.label(text="Limit Method:")
            box.row().prop(mod, "limit_method", expand=True)
            if mod.limit_method == 'ANGLE':
                box.prop(mod, "angle_limit")
            elif mod.limit_method == 'VGROUP':
                box.label(text="Vertex Group:")
                box.prop_search(mod, "vertex_group", obj, "vertex_groups", text="")
    
            box.label(text="Width Method:")
            box.row().prop(mod, "offset_type", expand=True)
    
    def draw_boolean_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_BOOLEAN')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            split = box.split()
    
            col = split.column()
            col.label(text="Operation:")
            col.prop(mod, "operation", text="")
    
            col = split.column()
            col.label(text="Object:")
            col.prop(mod, "object", text="")
    
    def draw_curve_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_CURVE')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            split = box.split()
    
            col = split.column()
            col.label(text="Object:")
            col.prop(mod, "object", text="")
            col = split.column()
            col.label(text="Vertex Group:")
            col.prop_search(mod, "vertex_group", obj, "vertex_groups", text="")
            box.label(text="Deformation Axis:")
            box.row().prop(mod, "deform_axis", expand=True)
    
    def draw_decimate_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_DECIM')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            decimate_type = mod.decimate_type
    
            row = box.row()
            row.prop(mod, "decimate_type", expand=True)
    
            if decimate_type == 'COLLAPSE':
                box.prop(mod, "ratio")
    
                split = box.split()
                row = split.row(align=True)
                row.prop_search(mod, "vertex_group", obj, "vertex_groups", text="")
                row.prop(mod, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
                split.prop(mod, "use_collapse_triangulate")
            elif decimate_type == 'UNSUBDIV':
                box.prop(mod, "iterations")
            else:  # decimate_type == 'DISSOLVE':
                box.prop(mod, "angle_limit")
                box.prop(mod, "use_dissolve_boundaries")
                box.label("Delimit:")
                row = box.row()
                row.prop(mod, "delimit")
    
            box.label(text=iface_("Face Count: %d") % mod.face_count, translate=False)
    
    def draw_edge_split_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_EDGESPLIT')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            split = box.split()
    
            col = split.column()
            col.prop(mod, "use_edge_angle", text="Edge Angle")
            sub = col.column()
            sub.active = mod.use_edge_angle
            sub.prop(mod, "split_angle")
    
            split.prop(mod, "use_edge_sharp", text="Sharp Edges")
    
    def draw_hook_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='HOOK')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            split = box.split()
    
            col = split.column()
            col.label(text="Object:")
            col.prop(mod, "object", text="")
            if mod.object and mod.object.type == 'ARMATURE':
                col.label(text="Bone:")
                col.prop_search(mod, "subtarget", mod.object.data, "bones", text="")
            col = split.column()
            col.label(text="Vertex Group:")
            col.prop_search(mod, "vertex_group", obj, "vertex_groups", text="")
    
            layout.separator()
    
            split = box.split()

            col = split.column()
            col.operator("object.hook_reset", text="Reset")
            col.operator("object.hook_recenter", text="Recenter")
    
            if obj.mode == 'EDIT':
                layout.separator()
                row = layout.row()
                row.operator("object.hook_select", text="Select")
                row.operator("object.hook_assign", text="Assign")
    
    def draw_mask_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_MASK')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            split = box.split()
    
            col = split.column()
            col.label(text="Mode:")
            col.prop(mod, "mode", text="")
    
            col = split.column()
            if mod.mode == 'ARMATURE':
                col.label(text="Armature:")
                col.prop(mod, "armature", text="")
            elif mod.mode == 'VERTEX_GROUP':
                col.label(text="Vertex Group:")
                row = col.row(align=True)
                row.prop_search(mod, "vertex_group", obj, "vertex_groups", text="")
                sub = row.row(align=True)
                sub.active = bool(mod.vertex_group)
                sub.prop(mod, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
    def draw_mirror_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_MIRROR')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            split = box.split(percentage=0.25)
    
            col = split.column()
            col.label(text="Axis:")
            col.prop(mod, "use_x")
            col.prop(mod, "use_y")
            col.prop(mod, "use_z")
    
            col = split.column()
            col.label(text="Options:")
            col.prop(mod, "use_mirror_merge", text="Merge")
            col.prop(mod, "use_clip", text="Clipping")
            col.prop(mod, "use_mirror_vertex_groups", text="Vertex Groups")
    
            col = split.column()
            col.label(text="Textures:")
            col.prop(mod, "use_mirror_u", text="U")
            col.prop(mod, "use_mirror_v", text="V")
    
            col = box.column()
    
            if mod.use_mirror_merge is True:
                col.prop(mod, "merge_threshold")
            col.label(text="Mirror Object:")
            col.prop(mod, "mirror_object", text="") 
    
    def draw_solidify_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_SOLIDIFY')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            split = box.split()
    
            col = split.column()
            col.prop(mod, "thickness")
            col.prop(mod, "thickness_clamp")
    
            col.separator()
    
            row = col.row(align=True)
            row.prop_search(mod, "vertex_group", obj, "vertex_groups", text="")
            sub = row.row(align=True)
            sub.active = bool(mod.vertex_group)
            sub.prop(mod, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
    
            sub = col.row()
            sub.active = bool(mod.vertex_group)
            sub.prop(mod, "thickness_vertex_group", text="Factor")
    
            col.label(text="Crease:")
            col.prop(mod, "edge_crease_inner", text="Inner")
            col.prop(mod, "edge_crease_outer", text="Outer")
            col.prop(mod, "edge_crease_rim", text="Rim")
    
            col = split.column()
    
            col.prop(mod, "offset")
            col.prop(mod, "use_flip_normals")
    
            col.prop(mod, "use_even_offset")
            col.prop(mod, "use_quality_normals")
            col.prop(mod, "use_rim")
    
            col.separator()
    
            col.label(text="Material Index Offset:")
    
            sub = col.column()
            row = sub.split(align=True, percentage=0.4)
            row.prop(mod, "material_offset", text="")
            row = row.row(align=True)
            row.active = mod.use_rim
            row.prop(mod, "material_offset_rim", text="Rim")
    
    def draw_subsurf_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_SUBSURF')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            box.row().prop(mod, "subdivision_type", expand=True)
    
            split = box.split()
            col = split.column()
            col.label(text="Subdivisions:")
            col.prop(mod, "levels", text="View")
            col.prop(mod, "render_levels", text="Render")
    
            col = split.column()
            col.label(text="Options:")
            col.prop(mod, "use_subsurf_uv")
            col.prop(mod, "show_only_control_edges")
    
    def draw_skin_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_SKIN')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            box.operator("object.skin_armature_create", text="Create Armature")
    
            box.separator()
    
            col = box.column(align=True)
            col.prop(mod, "branch_smoothing")
            col.prop(mod, "use_smooth_shade")
    
            split = box.split()
    
            col = split.column()
            col.label(text="Selected Vertices:")
            sub = col.column(align=True)
            sub.operator("object.skin_loose_mark_clear", text="Mark Loose").action = 'MARK'
            sub.operator("object.skin_loose_mark_clear", text="Clear Loose").action = 'CLEAR'
    
            sub = col.column()
            sub.operator("object.skin_root_mark", text="Mark Root")
            sub.operator("object.skin_radii_equalize", text="Equalize Radii")
    
            col = split.column()
            col.label(text="Symmetry Axes:")
            col.prop(mod, "use_x_symmetry")
            col.prop(mod, "use_y_symmetry")
            col.prop(mod, "use_z_symmetry")
    
    def draw_triangulate_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_TRIANGULATE')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            row = box.row()
    
            col = row.column()
            col.label(text="Quad Method:")
            col.prop(mod, "quad_method", text="")
            col = row.column()
            col.label(text="Ngon Method:")
            col.prop(mod, "ngon_method", text="")  
    
    def draw_simple_deform_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_SIMPLEDEFORM')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            box.row().prop(mod, "deform_method", expand=True)
    
            split = box.split()
    
            col = split.column()
            col.label(text="Vertex Group:")
            col.prop_search(mod, "vertex_group", obj, "vertex_groups", text="")
    
            split = box.split()
    
            col = split.column()
            col.label(text="Origin:")
            col.prop(mod, "origin", text="")
    
            if mod.deform_method in {'TAPER', 'STRETCH', 'TWIST'}:
                col.label(text="Lock:")
                col.prop(mod, "lock_x")
                col.prop(mod, "lock_y")
    
            col = split.column()
            col.label(text="Deform:")
            if mod.deform_method in {'TAPER', 'STRETCH'}:
                col.prop(mod, "factor")
            else:
                col.prop(mod, "angle")
            col.prop(mod, "limits", slider=True)
    
    def draw_wireframe_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_WIREFRAME')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()
            has_vgroup = bool(mod.vertex_group)
    
            split = box.split()
    
            col = split.column()
            col.prop(mod, "thickness", text="Thickness")
    
            row = col.row(align=True)
            row.prop_search(mod, "vertex_group", obj, "vertex_groups", text="")
            sub = row.row(align=True)
            sub.active = has_vgroup
            sub.prop(mod, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
            row = col.row(align=True)
            row.active = has_vgroup
            row.prop(mod, "thickness_vertex_group", text="Factor")
    
            col.prop(mod, "use_crease", text="Crease Edges")
            col.prop(mod, "crease_weight", text="Crease Weight")
    
            col = split.column()
    
            col.prop(mod, "offset")
            col.prop(mod, "use_even_offset", text="Even Thickness")
            col.prop(mod, "use_relative_offset", text="Relative Thickness")
            col.prop(mod, "use_boundary", text="Boundary")
            col.prop(mod, "use_replace", text="Replace Original")
    
            col.prop(mod, "material_offset", text="Material Offset")                            
    
    def draw_displace_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_WIREFRAME')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()    
            
            has_texture = (mod.texture is not None)

            col = box.column(align=True)
            
            texbox = col.box()
            texbox.label(text="Texture Info:")
            texbox.template_ID(mod, "texture", new="texture.new")
    
            if has_texture:
                col.separator()
                
                draw_texture(texbox,mod.texture)
    
            split = box.split()
    
            col = split.column(align=True)
            col.label(text="Direction:")
            col.prop(mod, "direction", text="")
            col.label(text="Vertex Group:")
            col.prop_search(mod, "vertex_group", obj, "vertex_groups", text="")
    
            col = split.column(align=True)
            col.active = has_texture
            col.label(text="Texture Coordinates:")
            col.prop(mod, "texture_coords", text="")
            if mod.texture_coords == 'OBJECT':
                col.label(text="Object:")
                col.prop(mod, "texture_coords_object", text="")
            elif mod.texture_coords == 'UV' and obj.type == 'MESH':
                col.label(text="UV Map:")
                col.prop_search(mod, "uv_layer", obj.data, "uv_textures", text="")
    
            box.separator()
    
            row = box.row()
            row.prop(mod, "mid_level")
            row.prop(mod, "strength")            
    
    def draw_particle_system(layout):
        ob = bpy.context.object
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='PARTICLE_DATA')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)  
            box = col.box()
            ps = mod.particle_system
            split = box.split(percentage=0.32)

            col = split.column()
            col.label(text="Settings:")

            col = split.column()
            col.template_ID(ps, "settings", new="particle.new") 
                       
            ps_settings = ps.settings
#             box.prop(ps,'name')
            box.prop(ps_settings,'type')
            box.prop(ps_settings,'emit_from')
            box.prop(ps_settings,'distribution')
            row = box.row()
            row.label("Number of Particles:")
            row.prop(ps_settings,'count',text="")

            row = box.row()
            row.label("Hair Length:")            
            row.prop(ps_settings,'hair_length',text="")
#             row = box.row()
#             row.label("Hair Length:")            
#             row.prop(ps_settings,'normal_factor',text="")            
            
            row = box.row()
            row.label("Twist:")            
            row.prop(ps_settings,'brownian_factor',text="")            
            
            row = box.row()
            row.label("Children Type:")            
            row.prop(ps_settings,'child_type',text="") 
            
            if ps_settings.child_type != 'NONE':
                row = box.row(align=True)
                row.label("Child Quantity:")
                row.prop(ps_settings,'child_nbr',text="Display")            
                row.prop(ps_settings,'rendered_child_count',text="Render")            
                
                row = box.row()
                row.label("Random Length:")            
                row.prop(ps_settings,'length_random',text="")                   
                
                row = box.row(align=True)
                row.label("Clump Amount:")
                row.prop(ps_settings,'clump_factor',text="") 
                
                row = box.row(align=True)
                row.label("Child Size:")
                row.prop(ps_settings,'child_length',text="Length") 
                row.prop(ps_settings,'child_length_threshold',text="Threshold") 
                row = box.row(align=True)
                row.label(" ")
                row.prop(ps_settings,'child_radius',text="Radius") 
                row.prop(ps_settings,'roughness_endpoint',text="Roughness Endpoint") 
                row = box.row(align=True)
                row.label(" ")
#                 row.prop(ps_settings,'randomness',text="Random")
                row.prop(ps_settings,'roughness_2',text="Roughness 2") 

            row = box.row()
            row.label("Random Size:")            
            row.prop(ps_settings,'size_random',text="",slider=True)              
            row = box.row()
            row.label("Material:")            
            row.prop(ps_settings,'material_slot',text="")
            row = box.row()
            row.label("Rotation Mode:")            
            row.prop(ps_settings,'rotation_mode',text="")      
            row = box.row()
            row.label("Rotation Factor:")            
            row.prop(ps_settings,'rotation_factor_random',text="",slider=True)                 
            row = box.row()
            row.label("Render Type:")            
            row.prop(ps_settings,'render_type',text="")
            
            col = box.column()
            row = col.row(align=True)
            row.prop_search(ps, "vertex_group_density", ob, "vertex_groups", text="Density")
            row.prop(ps, "invert_vertex_group_density", text="", toggle=True, icon='ARROW_LEFTRIGHT')
    
            row = col.row(align=True)
            row.prop_search(ps, "vertex_group_length", ob, "vertex_groups", text="Length")
            row.prop(ps, "invert_vertex_group_length", text="", toggle=True, icon='ARROW_LEFTRIGHT')               
            
            if ps_settings.render_type == 'OBJECT':
                row = box.row()
                row.label("Object:")            
                row.prop(ps_settings,'dupli_object',text="")    
                row = box.row()          
                row.prop(ps_settings,'use_global_dupli')
                row.prop(ps_settings,'use_rotation_dupli')
                row.prop(ps_settings,'use_scale_dupli')        
                
            if ps_settings.render_type == 'GROUP':
                row = box.row()
                row.label("Group:")            
                row.prop(ps_settings,'dupli_group',text="") 
                row = box.row()          
                row.prop(ps_settings,'use_global_dupli')
                row.prop(ps_settings,'use_rotation_dupli')
                row.prop(ps_settings,'use_scale_dupli')
                row = box.row()   
                row.prop(ps_settings,'use_whole_group')
                row.prop(ps_settings,'use_group_pick_random')
                row.prop(ps_settings,'use_group_count')
                        
    def draw_ocean_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_SIMPLEDEFORM')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()    
            if not bpy.app.build_options.mod_oceansim:
                box.label("Built without OceanSim modifier")
                return
    
            box.prop(mod, "geometry_mode")
    
            if mod.geometry_mode == 'GENERATE':
                row = box.row()
                row.prop(mod, "repeat_x")
                row.prop(mod, "repeat_y")
    
            box.separator()
    
            split = box.split()
    
            col = split.column()
            col.prop(mod, "time")
            col.prop(mod, "depth")
            col.prop(mod, "random_seed")
    
            col = split.column()
            col.prop(mod, "resolution")
            col.prop(mod, "size")
            col.prop(mod, "spatial_size")
    
            box.label("Waves:")
    
            split = box.split()
    
            col = split.column()
            col.prop(mod, "choppiness")
            col.prop(mod, "wave_scale", text="Scale")
            col.prop(mod, "wave_scale_min")
            col.prop(mod, "wind_velocity")
    
            col = split.column()
            col.prop(mod, "wave_alignment", text="Alignment")
            sub = col.column()
            sub.active = (mod.wave_alignment > 0.0)
            sub.prop(mod, "wave_direction", text="Direction")
            sub.prop(mod, "damping")
    
            box.separator()
    
            box.prop(mod, "use_normals")
    
            split = box.split()
    
            col = split.column()
            col.prop(mod, "use_foam")
            sub = col.row()
            sub.active = mod.use_foam
            sub.prop(mod, "foam_coverage", text="Coverage")
    
            col = split.column()
            col.active = mod.use_foam
            col.label("Foam Data Layer Name:")
            col.prop(mod, "foam_layer_name", text="")
    
            box.separator()
    
            if mod.is_cached:
                box.operator("object.ocean_bake", text="Free Bake").free = True
            else:
                box.operator("object.ocean_bake").free = False
    
            split = box.split()
            split.enabled = not mod.is_cached
    
            col = split.column(align=True)
            col.prop(mod, "frame_start", text="Start")
            col.prop(mod, "frame_end", text="End")
    
            col = split.column(align=True)
            col.label(text="Cache path:")
            col.prop(mod, "filepath", text="")
    
            split = box.split()
            split.enabled = not mod.is_cached
    
            col = split.column()
            col.active = mod.use_foam
            col.prop(mod, "bake_foam_fade")
    
            col = split.column()
                        
    def draw_multires_modifier(layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        draw_show_expanded(mod,row)
        row.prop(mod,'name',text="",icon='MOD_MULTIRES')
        draw_apply_close(row)
        if mod.show_expanded:
            row = box.row()
            draw_visibility(row)                   
            box = col.box()    
                        
            box.row().prop(mod, "subdivision_type", expand=True)
    
            split = box.split()
            col = split.column()
            col.prop(mod, "levels", text="Preview")
            col.prop(mod, "sculpt_levels", text="Sculpt")
            col.prop(mod, "render_levels", text="Render")
    
            col = split.column()
    
            col.enabled = obj.mode != 'EDIT'
            col.operator("object.multires_subdivide", text="Subdivide")
            col.operator("object.multires_higher_levels_delete", text="Delete Higher")
            col.operator("object.multires_reshape", text="Reshape")
            col.operator("object.multires_base_apply", text="Apply Base")
            col.prop(mod, "use_subsurf_uv")
            col.prop(mod, "show_only_control_edges")
    
            box.separator()
    
            col = box.column()
            row = col.row()
            if mod.is_external:
                row.operator("object.multires_external_pack", text="Pack External")
                row.label()
                row = col.row()
                row.prop(mod, "filepath", text="")
            else:
                row.operator("object.multires_external_save", text="Save External...")
                row.label()        
                        
    if mod.type == 'ARRAY':
        draw_array_modifier(layout)
    elif mod.type == 'BEVEL':
        draw_bevel_modifier(layout)
    elif mod.type == 'BOOLEAN':
        draw_boolean_modifier(layout)
    elif mod.type == 'CURVE':
        draw_curve_modifier(layout)
    elif mod.type == 'DECIMATE':
        draw_decimate_modifier(layout)
    elif mod.type == 'EDGE_SPLIT':
        draw_edge_split_modifier(layout)
    elif mod.type == 'HOOK':
        draw_hook_modifier(layout)
    elif mod.type == 'MASK':
        draw_mask_modifier(layout)
    elif mod.type == 'MIRROR':
        draw_mirror_modifier(layout)
    elif mod.type == 'SOLIDIFY':
        draw_solidify_modifier(layout)
    elif mod.type == 'SUBSURF':
        draw_subsurf_modifier(layout)
    elif mod.type == 'SKIN':
        draw_skin_modifier(layout)
    elif mod.type == 'SIMPLE_DEFORM':
        draw_simple_deform_modifier(layout)
    elif mod.type == 'TRIANGULATE':
        draw_triangulate_modifier(layout)
    elif mod.type == 'WIREFRAME':
        draw_wireframe_modifier(layout)
    elif mod.type == 'DISPLACE':
        draw_displace_modifier(layout)        
    elif mod.type == 'OCEAN':
        draw_ocean_modifier(layout)
    elif mod.type == 'MULTIRES':
        draw_multires_modifier(layout)       
    elif mod.type == 'PARTICLE_SYSTEM':
        draw_particle_system(layout)
    else:
        row = layout.row()
        row.label(mod.name + " view ")
    
def draw_constraint(con,layout,obj):

    def draw_show_expanded(con,layout):
        if con.show_expanded:
            layout.prop(con,'show_expanded',text="",emboss=False)
        else:
            layout.prop(con,'show_expanded',text="",emboss=False)

    def space_template(layout, con, target=True, owner=True):
        if target or owner:

            split = layout.split(percentage=0.2)

            split.label(text="Space:")
            row = split.row()

            if target:
                row.prop(con, "target_space", text="")

            if target and owner:
                row.label(icon='ARROW_LEFTRIGHT')

            if owner:
                row.prop(con, "owner_space", text="")

    def target_template(layout, con, subtargets=True):
        layout.prop(con, "target")  # XXX limiting settings for only 'curves' or some type of object

        if con.target and subtargets:
            if con.target.type == 'ARMATURE':
                layout.prop_search(con, "subtarget", con.target.data, "bones", text="Bone")

                if hasattr(con, "head_tail"):
                    row = layout.row()
                    row.label(text="Head/Tail:")
                    row.prop(con, "head_tail", text="")
            elif con.target.type in {'MESH', 'LATTICE'}:
                layout.prop_search(con, "subtarget", con.target, "vertex_groups", text="Vertex Group")

    def draw_copy_location_constraint(layout):
        col = layout.column(align=True)
        box = col.template_constraint(con)

        if con.show_expanded:
            target_template(box, con)
            
            split = box.split()
    
            col = split.column()
            col.prop(con, "use_x", text="X")
            sub = col.column()
            sub.active = con.use_x
            sub.prop(con, "invert_x", text="Invert")
    
            col = split.column()
            col.prop(con, "use_y", text="Y")
            sub = col.column()
            sub.active = con.use_y
            sub.prop(con, "invert_y", text="Invert")
    
            col = split.column()
            col.prop(con, "use_z", text="Z")
            sub = col.column()
            sub.active = con.use_z
            sub.prop(con, "invert_z", text="Invert")
    
            box.prop(con, "use_offset")
    
            space_template(box, con)
            
            if con.type not in {'RIGID_BODY_JOINT', 'NULL'}:
                box.prop(con, "influence")            
     
    def draw_copy_rotation_constraint(layout):
        col = layout.column(align=True)
        box = col.template_constraint(con)

        if con.show_expanded:        
            target_template(box, con)
    
            split = box.split()
    
            col = split.column()
            col.prop(con, "use_x", text="X")
            sub = col.column()
            sub.active = con.use_x
            sub.prop(con, "invert_x", text="Invert")
    
            col = split.column()
            col.prop(con, "use_y", text="Y")
            sub = col.column()
            sub.active = con.use_y
            sub.prop(con, "invert_y", text="Invert")
    
            col = split.column()
            col.prop(con, "use_z", text="Z")
            sub = col.column()
            sub.active = con.use_z
            sub.prop(con, "invert_z", text="Invert")
    
            box.prop(con, "use_offset")
    
            space_template(box, con) 
            
            if con.type not in {'RIGID_BODY_JOINT', 'NULL'}:
                box.prop(con, "influence")            
    
    def draw_copy_scale_constraint(layout):
        col = layout.column(align=True)
        box = col.template_constraint(con)

        if con.show_expanded:        
            target_template(box, con)
    
            row = box.row(align=True)
            row.prop(con, "use_x", text="X")
            row.prop(con, "use_y", text="Y")
            row.prop(con, "use_z", text="Z")
    
            box.prop(con, "use_offset")
    
            space_template(box, con)
            
            if con.type not in {'RIGID_BODY_JOINT', 'NULL'}:
                box.prop(con, "influence")  
    
    def draw_copy_transforms_constraint(layout):
        col = layout.column(align=True)
        box = col.template_constraint(con)

        if con.show_expanded:        
            target_template(box, con)

            space_template(box, con)
            
            if con.type not in {'RIGID_BODY_JOINT', 'NULL'}:
                box.prop(con, "influence")  
    
    def draw_limit_distance_constraint(layout):
        col = layout.column(align=True)
        box = col.template_constraint(con)

        if con.show_expanded:        
            target_template(box, con)
    
            col = box.column(align=True)
            col.prop(con, "distance")
            col.operator("constraint.limitdistance_reset")
    
            row = box.row()
            row.label(text="Clamp Region:")
            row.prop(con, "limit_mode", text="")
    
            row = box.row()
            row.prop(con, "use_transform_limit")
            row.label()
    
            space_template(box, con) 
            
            if con.type not in {'RIGID_BODY_JOINT', 'NULL'}:
                box.prop(con, "influence")  
    
    def draw_limit_location_constraint(layout):
        col = layout.column(align=True)
        box = col.template_constraint(con)

        if con.show_expanded:        
            split = box.split()
    
            col = split.column()
            col.prop(con, "use_min_x")
            sub = col.column()
            sub.active = con.use_min_x
            sub.prop(con, "min_x", text="")
            col.prop(con, "use_max_x")
            sub = col.column()
            sub.active = con.use_max_x
            sub.prop(con, "max_x", text="")
    
            col = split.column()
            col.prop(con, "use_min_y")
            sub = col.column()
            sub.active = con.use_min_y
            sub.prop(con, "min_y", text="")
            col.prop(con, "use_max_y")
            sub = col.column()
            sub.active = con.use_max_y
            sub.prop(con, "max_y", text="")
    
            col = split.column()
            col.prop(con, "use_min_z")
            sub = col.column()
            sub.active = con.use_min_z
            sub.prop(con, "min_z", text="")
            col.prop(con, "use_max_z")
            sub = col.column()
            sub.active = con.use_max_z
            sub.prop(con, "max_z", text="")
    
            row = box.row()
            row.prop(con, "use_transform_limit")
            row.label()
    
            row = box.row()
            row.label(text="Convert:")
            row.prop(con, "owner_space", text="")
            
            if con.type not in {'RIGID_BODY_JOINT', 'NULL'}:
                box.prop(con, "influence")  
    
    def draw_limit_rotation_constraint(layout):
        col = layout.column(align=True)
        box = col.template_constraint(con)

        if con.show_expanded:        
            split = box.split()
    
            col = split.column(align=True)
            col.prop(con, "use_limit_x")
            sub = col.column(align=True)
            sub.active = con.use_limit_x
            sub.prop(con, "min_x", text="Min")
            sub.prop(con, "max_x", text="Max")
    
            col = split.column(align=True)
            col.prop(con, "use_limit_y")
            sub = col.column(align=True)
            sub.active = con.use_limit_y
            sub.prop(con, "min_y", text="Min")
            sub.prop(con, "max_y", text="Max")
    
            col = split.column(align=True)
            col.prop(con, "use_limit_z")
            sub = col.column(align=True)
            sub.active = con.use_limit_z
            sub.prop(con, "min_z", text="Min")
            sub.prop(con, "max_z", text="Max")
    
            box.prop(con, "use_transform_limit")
    
            row = box.row()
            row.label(text="Convert:")
            row.prop(con, "owner_space", text="")
            
            if con.type not in {'RIGID_BODY_JOINT', 'NULL'}:
                box.prop(con, "influence")   
    
    def draw_limit_scale_constraint(layout):
        col = layout.column(align=True)
        box = col.template_constraint(con)

        if con.show_expanded:        
            split = box.split()
    
            col = split.column()
            col.prop(con, "use_min_x")
            sub = col.column()
            sub.active = con.use_min_x
            sub.prop(con, "min_x", text="")
            col.prop(con, "use_max_x")
            sub = col.column()
            sub.active = con.use_max_x
            sub.prop(con, "max_x", text="")
    
            col = split.column()
            col.prop(con, "use_min_y")
            sub = col.column()
            sub.active = con.use_min_y
            sub.prop(con, "min_y", text="")
            col.prop(con, "use_max_y")
            sub = col.column()
            sub.active = con.use_max_y
            sub.prop(con, "max_y", text="")
    
            col = split.column()
            col.prop(con, "use_min_z")
            sub = col.column()
            sub.active = con.use_min_z
            sub.prop(con, "min_z", text="")
            col.prop(con, "use_max_z")
            sub = col.column()
            sub.active = con.use_max_z
            sub.prop(con, "max_z", text="")
    
            row = box.row()
            row.prop(con, "use_transform_limit")
            row.label()
    
            row = box.row()
            row.label(text="Convert:")
            row.prop(con, "owner_space", text="")
            
            if con.type not in {'RIGID_BODY_JOINT', 'NULL'}:
                box.prop(con, "influence")                     
            
    if con.type == 'COPY_LOCATION':
        draw_copy_location_constraint(layout)
    elif con.type == 'COPY_ROTATION':
        draw_copy_rotation_constraint(layout)
    elif con.type == 'COPY_SCALE':
        draw_copy_scale_constraint(layout)
    elif con.type == 'COPY_TRANSFORMS':
        draw_copy_transforms_constraint(layout)
    elif con.type == 'LIMIT_DISTANCE':
        draw_limit_distance_constraint(layout)
    elif con.type == 'LIMIT_LOCATION':
        draw_limit_location_constraint(layout)
    elif con.type == 'LIMIT_ROTATION':
        draw_limit_rotation_constraint(layout)
    elif con.type == 'LIMIT_SCALE':
        draw_limit_scale_constraint(layout)
    else:
        row = layout.row()
        row.label(con.name + " view ")            

def draw_mesh_properties(layout,obj,context):
    layout.label('Mesh Properties:',icon='OUTLINER_OB_MESH')
    layout.prop(obj,'draw_type',text="Draw Type")
    draw_uv_maps(layout,obj,context)
    draw_vertex_groups(layout, obj, context)
    draw_shape_keys(layout,obj,context)
    
    
def draw_vertex_groups(layout,obj,context):
    ob = context.object
    group = ob.vertex_groups.active

    rows = 2
    if group:
        rows = 4
    
    box = layout.box()
    row = box.row()
    row.label("Vertex Groups:",icon='GROUP_VERTEX')
    if len(obj.vertex_groups) > 0:
        pass
        row = box.row()
        row.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=rows)
    
        col = row.column(align=True)
        col.operator("object.vertex_group_add", icon='ZOOMIN', text="")
        col.operator("object.vertex_group_remove", icon='ZOOMOUT', text="").all = False
        col.menu("MESH_MT_vertex_group_specials", icon='DOWNARROW_HLT', text="")
        if group:
            col.separator()
            col.operator("object.vertex_group_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("object.vertex_group_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
    
        if ob.vertex_groups and (ob.mode == 'EDIT' or (ob.mode == 'WEIGHT_PAINT' and ob.type == 'MESH' and ob.data.use_paint_mask_vertex)):
            row = box.row()
    
            sub = row.row(align=True)
            sub.operator("object.vertex_group_assign", text="Assign")
            sub.operator("object.vertex_group_remove_from", text="Remove")
    
            sub = row.row(align=True)
            sub.operator("object.vertex_group_select", text="Select")
            sub.operator("object.vertex_group_deselect", text="Deselect")
    
            box.prop(context.tool_settings, "vertex_group_weight", text="Weight")   
    else:
         row.operator('object.vertex_group_add',icon='ZOOMIN',text="Add")
    
def draw_shape_keys(layout,obj,context):
    ob = context.object
    key = ob.data.shape_keys
    kb = ob.active_shape_key

    enable_edit = ob.mode != 'EDIT'
    enable_edit_value = False

    if ob.show_only_shape_key is False:
        if enable_edit or (ob.type == 'MESH' and ob.use_shape_key_edit_mode):
            enable_edit_value = True
            
    box = layout.box()
    row = box.row()
    row.label("Shape Keys",icon='SHAPEKEY_DATA')
    
    if key and len(key.key_blocks) > 0:
        row = box.row()
        rows = 2
        if kb:
            rows = 4
        row.template_list("MESH_UL_shape_keys", "", key, "key_blocks", ob, "active_shape_key_index", rows=rows)
    
        col = row.column()
    
        sub = col.column(align=True)
        sub.operator("object.shape_key_add", icon='ZOOMIN', text="").from_mix = False
        sub.operator("object.shape_key_remove", icon='ZOOMOUT', text="").all = False
        sub.menu("MESH_MT_shape_key_specials", icon='DOWNARROW_HLT', text="")
    
        if kb:
            col.separator()
    
            sub = col.column(align=True)
            sub.operator("object.shape_key_move", icon='TRIA_UP', text="").type = 'UP'
            sub.operator("object.shape_key_move", icon='TRIA_DOWN', text="").type = 'DOWN'
    
            split = box.split(percentage=0.4)
            row = split.row()
            row.enabled = enable_edit
            row.prop(key, "use_relative")
    
            row = split.row()
            row.alignment = 'RIGHT'
    
            sub = row.row(align=True)
            sub.label()  # XXX, for alignment only
            subsub = sub.row(align=True)
            subsub.active = enable_edit_value
            subsub.prop(ob, "show_only_shape_key", text="")
            sub.prop(ob, "use_shape_key_edit_mode", text="")
    
            sub = row.row()
            if key.use_relative:
                sub.operator("object.shape_key_clear", icon='X', text="")
            else:
                sub.operator("object.shape_key_retime", icon='RECOVER_LAST', text="")
    
            if key.use_relative:
                if ob.active_shape_key_index != 0:
                    row = box.row()
                    row.active = enable_edit_value
                    row.prop(kb, "value")
    
                    split = box.split()
    
                    col = split.column(align=True)
                    col.active = enable_edit_value
                    col.label(text="Range:")
                    col.prop(kb, "slider_min", text="Min")
                    col.prop(kb, "slider_max", text="Max")
    
                    col = split.column(align=True)
                    col.active = enable_edit_value
                    col.label(text="Blend:")
                    col.prop_search(kb, "vertex_group", ob, "vertex_groups", text="")
                    col.prop_search(kb, "relative_key", key, "key_blocks", text="")
    
            else:
                box.prop(kb, "interpolation")
                row = box.column()
                row.active = enable_edit_value
                row.prop(key, "eval_time")
    else:
        row.operator("object.shape_key_add", icon='ZOOMIN', text="Add Shape ").from_mix = False
    
def draw_uv_maps(layout,obj,context):
    me = obj.data
    box = layout.box()
    row = box.row()
    row.label("UV Maps",icon='GROUP_UVS')
    

                            
    if len(me.uv_textures) > 0:
        row.operator('object_props.open_texture_editor',
                        text="Show UV Map",
                        icon='IMAGE_COL')    
                                    
        row = box.row()
        col = row.column()
    
        col.template_list("MESH_UL_uvmaps_vcols", "uvmaps", me, "uv_textures", me.uv_textures, "active_index", rows=1)
    
        col = row.column(align=True)
        col.operator("mesh.uv_texture_add", icon='ZOOMIN', text="")
        col.operator("mesh.uv_texture_remove", icon='ZOOMOUT', text="")    
    else:
        row.operator('uv.smart_project',icon='ZOOMIN',text="Unwrap Mesh")
        
def draw_empty_properties(layout,obj,context):
    layout.label('Empty Properties:',icon='OUTLINER_OB_EMPTY')
    layout.prop(obj,'empty_draw_type',text='Draw Type')
    layout.prop(obj,'empty_draw_size')
        
def draw_text_properties(layout,obj,context):
    layout.label('Text Properties:',icon='OUTLINER_OB_FONT')
    text = obj.data
    box = layout.box()
    row = box.row()
    row.label("Font Data:")
    row.operator('view3d.update_selected_text_with_active_font',text='',icon='FILE_REFRESH')
    row = box.row()
    row.template_ID(text, "font", open="font.open", unlink="font.unlink")
    row = box.row()
    row.label("Text Size:")
    row.prop(text,"size",text="")
    row = box.row()
    row.label("Horizontal Alignment")
    row.prop(text,"align_x",text="")
    row = box.row()
    row.label("Vertical Alignment")
    row.prop(text,"align_y",text="")
        
    box = layout.box()
    row = box.row()
    row.label("3D Font:")
    row = box.row()
    row.prop(text,"extrude")
    row = box.row()
    row.prop(text,"bevel_depth")
        
def draw_curve_properties(layout,obj,context):
    layout.label('Curve Properties:',icon='OUTLINER_OB_CURVE')
    curve = obj.data
    layout.prop(curve,"dimensions",text="Curve Type")
    layout.prop(curve,"fill_mode")
    layout.prop(curve,"bevel_object")
    if curve.bevel_object:
        layout.prop(curve,"use_fill_caps")
    row = layout.row(align=True)
    row.label("Curve Resolution:")
    row.prop(curve,"resolution_u",text="Preview")   
    row.prop(curve,"render_resolution_u",text="Render")      
    
    row = layout.row(align=True)
    row.prop(curve.splines[0],"use_cyclic_u",text="Close Curve")       
    
    if curve.bevel_object is None:
        row = layout.row(align=True)
        row.label("Extrude Amount:")
        row.prop(curve,"extrude")
        row = layout.row(align=True)
        row.label("Bevel Depth:")        
        row.prop(curve,"bevel_depth")

    if curve.bevel_depth > 0:
        layout.prop(curve,"bevel_resolution")  
            
    if curve.bevel_depth > 0 or curve.extrude > 0 or curve.bevel_object is not None:
        layout.prop(curve,"offset")  
        row = layout.row(align=True)
        row.label("Change Start/End:")   
        row.prop(curve,"bevel_factor_start",text="Start")  
        row.prop(curve,"bevel_factor_end",text="End")  
        
#     layout.prop(curve.splines[0],"resolution_u") # JUST USE MAIN resolution_u PROPERTY
#     layout.prop(curve.splines[0],"use_smooth") # JUST USE OPERATOR

def draw_camera_properties(layout,obj,context):
    layout.label('Camera Properties:',icon='OUTLINER_OB_CAMERA')

    cam = obj.data
    ccam = cam.cycles
    scene = bpy.context.scene
    rd = scene.render

    row = layout.row(align=True)
    row.label(text="Render Size:",icon='STICKY_UVS_VERT')        
    row.prop(rd, "resolution_x", text="X")
    row.prop(rd, "resolution_y", text="Y")
    row = layout.row(align=True)
    row.label("Clipping")
    row.prop(cam, "clip_start", text="Start")
    row.prop(cam, "clip_end", text="End")          
    
    layout.prop(cam, "type", expand=False, text="Camera Type")
    split = layout.split()
    col = split.column()
    if cam.type == 'PERSP':
        row = col.row()
        if cam.lens_unit == 'MILLIMETERS':
            row.prop(cam, "lens")
        elif cam.lens_unit == 'FOV':
            row.prop(cam, "angle")
        row.prop(cam, "lens_unit", text="")

    if cam.type == 'ORTHO':
        col.prop(cam, "ortho_scale")

    if cam.type == 'PANO':
        engine = bpy.context.scene.render.engine
        if engine == 'CYCLES':
            ccam = cam.cycles
            col.prop(ccam, "panorama_type", text="Panorama Type")
            if ccam.panorama_type == 'FISHEYE_EQUIDISTANT':
                col.prop(ccam, "fisheye_fov")
            elif ccam.panorama_type == 'FISHEYE_EQUISOLID':
                row = col.row()
                row.prop(ccam, "fisheye_lens", text="Lens")
                row.prop(ccam, "fisheye_fov")
        elif engine == 'BLENDER_RENDER':
            row = col.row()
            if cam.lens_unit == 'MILLIMETERS':
                row.prop(cam, "lens")
            elif cam.lens_unit == 'FOV':
                row.prop(cam, "angle")
            row.prop(cam, "lens_unit", text="")
    
    row = layout.row()
#         row.menu("CAMERA_MT_presets", text=bpy.types.CAMERA_MT_presets.bl_label)         
    row.prop_menu_enum(cam, "show_guide")            
    row = layout.row()         
    row.prop(bpy.context.scene.cycles,"film_transparent",text="Transparent Film")   
    row.prop(context.space_data,"lock_camera",text="Lock Camera to View")
    
    layout.label(text="Depth of Field:")
    row = layout.row(align=True)
    row.prop(cam, "dof_object", text="")
    col = row.column()
    sub = col.row()
    sub.active = cam.dof_object is None
    sub.prop(cam, "dof_distance", text="Distance")

def draw_light_properties(layout,obj,context):
    layout.label('Light Properties:',icon='OUTLINER_OB_LAMP')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    
    lamp = obj.data
    clamp = lamp.cycles
    cscene = bpy.context.scene.cycles  
    
    emissionNode = None
    mathNode = None
    
    if "Emission" in lamp.node_tree.nodes:
        emissionNode = lamp.node_tree.nodes["Emission"]
    if "Math" in lamp.node_tree.nodes:
        mathNode = lamp.node_tree.nodes["Math"]

    row = layout.row()
    row.label("Type:")     
    row.prop(lamp, "type", expand=True)
    
    if lamp.type in {'POINT', 'SUN', 'SPOT'}:
        layout.prop(lamp, "shadow_soft_size", text="Shadow Size")
    elif lamp.type == 'AREA':
        layout.prop(lamp, "shape", text="")
        sub = layout.column(align=True)

        if lamp.shape == 'SQUARE':
            sub.prop(lamp, "size")
        elif lamp.shape == 'RECTANGLE':
            sub.prop(lamp, "size", text="Size X")
            sub.prop(lamp, "size_y", text="Size Y")

    if cscene.progressive == 'BRANCHED_PATH':
        layout.prop(clamp, "samples")

    if lamp.type == 'HEMI':
        layout.label(text="Not supported, interpreted as sun lamp")         

    if emissionNode:
        row = layout.row()
        split = row.split(percentage=0.3)
        split.label("Lamp Color:")
        split.prop(emissionNode.inputs[0],"default_value",text="")  
        
    row = layout.row()
    split = row.split(percentage=0.3)
    split.label("Lamp Strength:")            
    if mathNode:   
        split.prop(mathNode.inputs[0],"default_value",text="") 
    else:          
        split.prop(emissionNode.inputs[1], "default_value",text="")
        
    row = layout.row()        
    split = row.split(percentage=0.4)     
    split.prop(clamp, "cast_shadow",text="Cast Shadows")
    split.prop(clamp, "use_multiple_importance_sampling")
    
    if lamp.type == 'AREA':
        layout.prop(lamp.cycles,'is_portal')
        
def draw_object_properties(layout,obj,context):
    props = get_scene_props(bpy.context.scene)
    main_col = layout.column(align=True)
    row = main_col.row(align=True)
    draw_object_tabs(row,obj)
    box = main_col.box()
    col = box.column()
    if props.tabs == 'INFO':
        draw_object_info(col,obj,context)
        
        if obj.type == 'MESH':
            box = main_col.box()
            draw_mesh_properties(box, obj, context)
        if obj.type == 'CURVE':
            box = main_col.box()
            draw_curve_properties(box, obj, context)
        if obj.type == 'FONT':
            box = main_col.box()
            draw_text_properties(box, obj, context)
        if obj.type == 'EMPTY':
            box = main_col.box()
            draw_empty_properties(box, obj, context)
        if obj.type == 'LAMP':
            box = main_col.box()
            draw_light_properties(box, obj, context)
        if obj.type == 'CAMERA':
            box = main_col.box()
            draw_camera_properties(box, obj, context)        

    if props.tabs == 'MATERIAL':
        draw_object_materials(col,obj,context)
        
    if props.tabs == 'CONSTRAINTS':
        row = col.row()
        row.operator_menu_enum("object.constraint_add", "type", text="Add Constraint",icon='CONSTRAINT_DATA')
        row.operator('object_props.collapse_all_constraints',text="",icon='FULLSCREEN_EXIT')
        for con in obj.constraints:
            draw_constraint(con,col,obj)
            
    if props.tabs == 'MODIFIERS':
        row = col.row()
        row.operator_menu_enum("object.modifier_add", "type",icon='MODIFIER')
        row.operator('object_props.collapse_all_modifiers',text="",icon='FULLSCREEN_EXIT')
        for mod in obj.modifiers:
            draw_modifier(mod,col,obj)

def draw_object_tabs(layout,obj):
    props = get_scene_props(bpy.context.scene)
    layout.scale_y = 1.3
    layout.scale_x = 1.5
    layout.prop_enum(props, "tabs", 'INFO',icon="INFO", text="Main") 
    if obj.type in {'MESH','CURVE','FONT'}:
        layout.prop_enum(props, "tabs", 'MATERIAL', icon="MATERIAL", text="Materials") 
        layout.prop_enum(props, "tabs", 'MODIFIERS', icon="MODIFIER", text="Modifiers") 
        layout.prop_enum(props, "tabs", 'CONSTRAINTS', icon="CONSTRAINT", text="Constraints")
    if obj.type in {'EMPTY','LAMP','CAMERA'}:
        layout.prop_enum(props, "tabs", 'CONSTRAINTS', icon='CONSTRAINT', text="Constraints") 

def draw_object_info(layout,obj,context):

    layout.label("Main Object Properties:",icon='OBJECT_DATA')

    row = layout.row()
    row.prop(obj,'name')
    row = layout.row()
    row.prop(obj, "parent", text="Parent")
    has_hook_modifier = False
    for mod in obj.modifiers:
        if mod.type == 'HOOK':
            has_hook_modifier =  True
            break
    
    has_shape_keys = False
    if obj.type == 'MESH':
        if obj.data.shape_keys:
            if len(obj.data.shape_keys.key_blocks) > 0:
                has_shape_keys = True
    
    if has_hook_modifier or has_shape_keys:
        row = layout.row()
        col = row.column(align=True)
        col.label("Dimension")
        col.label("X: " + str(obj.dimensions.x))
        col.label("Y: " + str(obj.dimensions.y))
        col.label("Z: " + str(obj.dimensions.z))
        col = row.column(align=True)
        col.label("Location")
        col.label("X: " + str(obj.location.x))
        col.label("Y: " + str(obj.location.y))
        col.label("Z: " + str(obj.location.z))
        col = row.column(align=True)
        col.label("Rotation")
        col.label("X: " + str(round(math.degrees(obj.rotation_euler.x),4)))
        col.label("Y: " + str(round(math.degrees(obj.rotation_euler.y),4)))
        col.label("Z: " + str(round(math.degrees(obj.rotation_euler.z),4)))
    else:
        if obj.type not in {'EMPTY','CAMERA','LAMP'}:
            col = layout.column(align=True)   
            
            row = col.row()
            row.label('Dimensions:')

#             vec = mathutils.Vector((1.0, 1.0, 1.0))            
            if obj.scale != mathutils.Vector((1.0, 1.0, 1.0)):
                props = row.operator('object.transform_apply',text="Apply Scale")
                props.location = False
                props.rotation = False
                props.scale = True

            #X
            row = col.row(align=True)
            row.prop(obj,"lock_scale",index=0,text="")
            if obj.lock_scale[0]:
                row.label("X: " + str(obj.dimensions.x))
            else:
                row.prop(obj,"dimensions",index=0,text="X")
            #Y
            row = col.row(align=True)
            row.prop(obj,"lock_scale",index=1,text="")
            if obj.lock_scale[1]:
                row.label("Y: " + str(obj.dimensions.y))
            else:
                row.prop(obj,"dimensions",index=1,text="Y")
            #Z
            row = col.row(align=True)
            row.prop(obj,"lock_scale",index=2,text="")
            if obj.lock_scale[2]:
                row.label("Z: " + str(obj.dimensions.z))
            else:
                row.prop(obj,"dimensions",index=2,text="Z")
                
        col1 = layout.row()
        if obj:
            col2 = col1.split()
            col = col2.column(align=True)
            col.label('Location:')
            #X
            row = col.row(align=True)
            row.prop(obj,"lock_location",index=0,text="")
            if obj.lock_location[0]:
                row.label("X: " + str(obj.location.x))
            else:
                row.prop(obj,"location",index=0,text="X")
            #Y    
            row = col.row(align=True)
            row.prop(obj,"lock_location",index=1,text="")
            if obj.lock_location[1]:
                row.label("Y: " + str(obj.location.y))
            else:
                row.prop(obj,"location",index=1,text="Y")
            #Z    
            row = col.row(align=True)
            row.prop(obj,"lock_location",index=2,text="")
            if obj.lock_location[2]:
                row.label("Z: " + str(obj.location.z))
            else:
                row.prop(obj,"location",index=2,text="Z")
                
            col2 = col1.split()
            col = col2.column(align=True)
            col.label('Rotation:')
            #X
            row = col.row(align=True)
            row.prop(obj,"lock_rotation",index=0,text="")
            if obj.lock_rotation[0]:
                row.label("X: " + str(round(math.degrees(obj.rotation_euler.x),4)))
            else:
                row.prop(obj,"rotation_euler",index=0,text="X")
            #Y    
            row = col.row(align=True)
            row.prop(obj,"lock_rotation",index=1,text="")
            if obj.lock_rotation[1]:
                row.label("Y: " + str(round(math.degrees(obj.rotation_euler.y),4)))
            else:
                row.prop(obj,"rotation_euler",index=1,text="Y")
            #Z    
            row = col.row(align=True)
            row.prop(obj,"lock_rotation",index=2,text="")
            if obj.lock_rotation[2]:
                row.label("Y: " + str(round(math.degrees(obj.rotation_euler.z),4)))
            else:
                row.prop(obj,"rotation_euler",index=2,text="Z")
                


def draw_object_materials(layout,obj,context):

    mat = None
    ob = context.object
    slot = None
    space = context.space_data
    
    if ob:
        mat = ob.active_material
    
    if ob:
        is_sortable = len(ob.material_slots) > 1
        rows = 1
        if (is_sortable):
            rows = 4

        row = layout.row()

        row.template_list("MATERIAL_UL_matslots", "", ob, 
                          "material_slots", ob, "active_material_index", rows=rows)

        col = row.column(align=True)
        col.operator("object.material_slot_add", icon='ZOOMIN', text="")
        col.operator("object.material_slot_remove", icon='ZOOMOUT', text="")

        col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")

        if is_sortable:
            col.separator()

            col.operator("object.material_slot_move", 
                         icon='TRIA_UP', text="").direction = 'UP'
            col.operator("object.material_slot_move", 
                         icon='TRIA_DOWN', text="").direction = 'DOWN'

        if ob.mode == 'EDIT':
            row = layout.row(align=True)
            row.operator("object.material_slot_assign", text="Assign")
            row.operator("object.material_slot_select", text="Select")
            row.operator("object.material_slot_deselect", text="Deselect")

    if ob:
        layout.template_ID(ob, "active_material", new="material.new")
        row = layout.row()

    if mat:
        layout.template_preview(mat)
        layout.operator('object_props.open_new_window',
                        text="Open Material Editor",
                        icon='NODETREE').space_type = 'NODE_EDITOR' 

class PANEL_object_properties(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = " "
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        if context.object:
            return True
        else:
            return False

    def draw_header(self, context):
        layout = self.layout
        obj = context.object
        layout.label(text="Object: " + obj.name,icon='OBJECT_DATA')

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj:
            draw_object_properties(layout,obj,context)
            
class OPS_open_new_window(bpy.types.Operator):
    bl_idname = "object_props.open_new_window"
    bl_label = "Open New Window"

    space_type = bpy.props.StringProperty(name="Space Type")
    
    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        for window in context.window_manager.windows:
            if len(window.screen.areas) == 1 and window.screen.areas[0].type == 'USER_PREFERENCES':
                window.screen.areas[0].type = self.space_type
        return {'FINISHED'}            
            
class OPS_collapse_all_modifiers(bpy.types.Operator):
    bl_idname = "object_props.collapse_all_modifiers"
    bl_label = "Collapse All Modifiers"

    def execute(self, context):
        for mod in context.active_object.modifiers:
            mod.show_expanded = False
        return {'FINISHED'}                        
            
class OPS_collapse_all_constraints(bpy.types.Operator):
    bl_idname = "object_props.collapse_all_constraints"
    bl_label = "Collapse All Constraints"

    def execute(self, context):
        for mod in context.active_object.constraints:
            mod.show_expanded = False
        return {'FINISHED'}                          
            
def get_scene_props(scene):
    return scene.obj_panel
            
class scene_props(bpy.types.PropertyGroup):

    tabs = bpy.props.EnumProperty(name="type",
        items=enum_object_tabs,
        description="Select the Object Type.",
        default='INFO')       

def register():
    bpy.utils.register_class(PANEL_object_properties)
    bpy.utils.register_class(scene_props)
    bpy.utils.register_class(OPS_open_new_window)
    bpy.utils.register_class(OPS_collapse_all_modifiers)
    bpy.utils.register_class(OPS_collapse_all_constraints)
    bpy.types.Scene.obj_panel = bpy.props.PointerProperty(type = scene_props)
    
def unregister():
    pass            