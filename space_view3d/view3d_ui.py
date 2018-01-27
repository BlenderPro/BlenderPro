import bpy

def clear_view3d_properties_shelf():
    if hasattr(bpy.types, 'VIEW3D_PT_grease_pencil'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_grease_pencil)
    if hasattr(bpy.types, 'VIEW3D_PT_grease_pencil_palettecolor'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_grease_pencil_palettecolor)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_properties'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_properties)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_cursor'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_cursor)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_name'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_name)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_display'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_display)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_stereo'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_stereo)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_shading'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_shading)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_motion_tracking'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_motion_tracking)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_meshdisplay'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_meshdisplay)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_meshstatvis'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_meshstatvis)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_curvedisplay'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_curvedisplay)
    if hasattr(bpy.types, 'VIEW3D_PT_background_image'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_background_image)
    if hasattr(bpy.types, 'VIEW3D_PT_transform_orientations'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_transform_orientations)
    if hasattr(bpy.types, 'VIEW3D_PT_etch_a_ton'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_etch_a_ton)
    if hasattr(bpy.types, 'VIEW3D_PT_context_properties'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_context_properties)
    if hasattr(bpy.types, 'VIEW3D_PT_tools_animation'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_animation)
    if hasattr(bpy.types, 'VIEW3D_PT_tools_relations'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_relations)        
    if hasattr(bpy.types, 'VIEW3D_PT_tools_rigid_body'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_rigid_body)   

def clear_view3d_tools_shelf():
    if hasattr(bpy.types, 'VIEW3D_PT_tools_grease_pencil_brush'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_grease_pencil_brush)          
    if hasattr(bpy.types, 'VIEW3D_PT_tools_grease_pencil_draw'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_grease_pencil_draw)      
    if hasattr(bpy.types, 'VIEW3D_PT_tools_add_object'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_add_object)  
    if hasattr(bpy.types, 'VIEW3D_PT_tools_transform'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_transform)            
    if hasattr(bpy.types, 'VIEW3D_PT_tools_object'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_object)            
    if hasattr(bpy.types, 'VIEW3D_PT_tools_history'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_history)

def clear_view3d_header():
    if hasattr(bpy.types, 'VIEW3D_HT_header'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_HT_header)   
    if hasattr(bpy.types, 'INFO_HT_header'):
        bpy.utils.unregister_class(bpy.types.INFO_HT_header)           

def clear_view3d_menus():
    if hasattr(bpy.types, 'VIEW3D_MT_view'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_MT_view)

class VIEW3D_HT_header(bpy.types.Header):
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        layout = self.layout

        obj = context.active_object

        row = layout.row(align=True)
        
        row.template_header()
        
        VIEW3D_MT_menus.draw_collapsible(context, layout)
        
        layout.template_header_3D()

class VIEW3D_MT_menus(bpy.types.Menu):
    bl_space_type = 'VIEW3D_MT_editor_menus'
    bl_label = ""

    def draw(self, context):
        self.draw_menus(self.layout, context)

    @staticmethod
    def draw_menus(layout, context):
        layout.menu("VIEW3D_MT_view",icon='VIEWZOOM',text="   View   ")
        layout.menu("VIEW3D_MT_add_object",icon='GREASEPENCIL',text="   Add   ")
        layout.menu("VIEW3D_MT_tools",icon='MODIFIER',text="   Tools   ")
        

class VIEW3D_MT_view(bpy.types.Menu):
    bl_label = "View"

    def draw(self, context):
        layout = self.layout

        layout.operator("view3d.toolshelf",icon='MENU_PANEL')
        layout.operator("view3d.properties",icon='MENU_PANEL')
        layout.separator()
        layout.operator("view3d.view_all",icon='VIEWZOOM')
        layout.operator("view3d.view_selected",text="Zoom To Selected",icon='ZOOM_SELECTED')

        layout.separator()

        layout.operator("view3d.navigate",icon='RESTRICT_VIEW_OFF',text="First Person View")
        
        layout.separator()

        layout.operator("view3d.viewnumpad", text="Camera",icon='CAMERA_DATA').type = 'CAMERA'
        layout.operator("view3d.viewnumpad", text="Top",icon='TRIA_DOWN').type = 'TOP'
        layout.operator("view3d.viewnumpad", text="Front",icon='TRIA_UP').type = 'FRONT'
        layout.operator("view3d.viewnumpad", text="Left",icon='TRIA_LEFT').type = 'LEFT'
        layout.operator("view3d.viewnumpad", text="Right",icon='TRIA_RIGHT').type = 'RIGHT'

        layout.separator()

        layout.operator("view3d.view_persportho",icon='SCENE')
        
        layout.operator_context = 'INVOKE_REGION_WIN'
        
        layout.separator()

        layout.operator("screen.area_dupli",icon='GHOST')
        layout.operator("screen.region_quadview",icon='IMGDISPLAY')
        layout.operator("screen.screen_full_area",icon='FULLSCREEN_ENTER')    
        
        layout.separator()
        
        layout.operator("space_view3d.viewport_options",text="Viewport Settings...",icon='SCRIPTPLUGINS')


class VIEW3D_MT_add_object(bpy.types.Menu):
    bl_label = "Add Object"

    def draw(self, context):
        layout = self.layout

        # note, don't use 'EXEC_SCREEN' or operators wont get the 'v3d' context.

        # Note: was EXEC_AREA, but this context does not have the 'rv3d', which prevents
        #       "align_view" to work on first call (see [#32719]).
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("view3d.draw_mesh", icon='MESH_GRID')

        layout.operator_context = 'EXEC_REGION_WIN'
        layout.separator()
        layout.menu("INFO_MT_mesh_add", icon='OUTLINER_OB_MESH')

        layout.menu("INFO_MT_curve_add", icon='OUTLINER_OB_CURVE')
        layout.operator_context = 'EXEC_REGION_WIN'
        layout.operator("object.text_add", text="Text", icon='OUTLINER_OB_FONT')
        layout.separator()

        layout.operator_menu_enum("object.empty_add", "type", text="Empty", icon='OUTLINER_OB_EMPTY')
        layout.separator()
        layout.operator("view3d.add_camera",text="Camera",icon='OUTLINER_OB_CAMERA')
        layout.menu("VIEW3D_MT_add_lamp", icon='OUTLINER_OB_LAMP')
        layout.separator()
        
        if len(bpy.data.groups) > 10:
            layout.operator_context = 'INVOKE_REGION_WIN'
            layout.operator("object.group_instance_add", text="Group Instance...", icon='OUTLINER_OB_EMPTY')
        else:
            layout.operator_menu_enum("object.group_instance_add", "group", text="Group Instance", icon='OUTLINER_OB_EMPTY')


class VIEW3D_MT_add_lamp(bpy.types.Menu):
    bl_label = "Lamp"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.lamp_add",icon='LAMP_POINT',text="Add Point Lamp").type = 'POINT'
        layout.operator("object.lamp_add",icon='LAMP_SUN',text="Add Sun Lamp").type = 'SUN'
        layout.operator("object.lamp_add",icon='LAMP_SPOT',text="Add Spot Lamp").type = 'SPOT'
        layout.operator("object.lamp_add",icon='LAMP_AREA',text="Add Area Lamp").type = 'AREA'


class VIEW3D_MT_tools(bpy.types.Menu):
    bl_context = "objectmode"
    bl_label = "Object"

    def draw(self, context):
        layout = self.layout
        layout.menu("VIEW3D_MT_objecttools",icon='OBJECT_DATA')
        layout.menu("VIEW3D_MT_cursor_tools",icon='CURSOR')
        layout.menu("VIEW3D_MT_selectiontools",icon='MAN_TRANS')
        layout.separator()
        layout.operator("view3d.snapping_options",icon='SNAP_ON')


class VIEW3D_MT_cursor_tools(bpy.types.Menu):
    bl_label = "Cursor Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator('view3d.set_cursor_location',text="Set Cursor Location...",icon='CURSOR')
        layout.separator()
        layout.operator("view3d.snap_cursor_to_selected",icon='CURSOR')
        layout.operator("view3d.snap_cursor_to_center",icon='GRID')
        layout.operator("view3d.snap_selected_to_cursor",icon='SPACE2')


class VIEW3D_MT_transformtools(bpy.types.Menu):
    bl_context = "objectmode"
    bl_label = "Transforms"

    def draw(self, context):
        layout = self.layout
        layout.operator("transform.translate",text='Grab',icon='MAN_TRANS')
        layout.operator("transform.rotate",icon='MAN_ROT')
        layout.operator("transform.resize",text="Scale",icon='MAN_SCALE')


class VIEW3D_MT_selectiontools(bpy.types.Menu):
    bl_context = "objectmode"
    bl_label = "Selection Tools"

    def draw(self, context):
        layout = self.layout
        if context.active_object:
            if context.active_object.mode == 'OBJECT':
                layout.operator("object.select_all",text='Toggle De/Select',icon='MAN_TRANS')
            else:
                layout.operator("mesh.select_all",text='Toggle De/Select',icon='MAN_TRANS')
        else:
            layout.operator("object.select_all",text='Toggle De/Select',icon='MAN_TRANS')
        layout.operator("view3d.select_border",icon='BORDER_RECT')
        layout.operator("view3d.select_circle",icon='BORDER_LASSO')
        if context.active_object and context.active_object.mode == 'EDIT':    
            layout.separator()
            layout.menu('VIEW3D_MT_mesh_selection',text="Mesh Selection",icon='MAN_TRANS')


class VIEW3D_MT_origintools(bpy.types.Menu):
    bl_context = "objectmode"
    bl_label = "Origin Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.origin_set",text="Origin to Cursor",icon='CURSOR').type = 'ORIGIN_CURSOR'
        layout.operator("object.origin_set",text="Origin to Geometry",icon='CLIPUV_HLT').type = 'ORIGIN_GEOMETRY'
        
        
class VIEW3D_MT_shadetools(bpy.types.Menu):
    bl_context = "objectmode"
    bl_label = "Object Shading"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.shade_smooth",icon='SOLID')
        layout.operator("object.shade_flat",icon='SNAP_FACE')


class VIEW3D_MT_objecttools(bpy.types.Menu):
    bl_context = "objectmode"
    bl_label = "Object Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("transform.translate",text='Grab',icon='MAN_TRANS')
        layout.operator("transform.rotate",icon='MAN_ROT')
        layout.operator("transform.resize",text="Scale",icon='MAN_SCALE')        
        layout.separator()
        layout.operator("object.duplicate_move",icon='PASTEDOWN')
        layout.operator("object.convert", text="Convert to Mesh",icon='MOD_REMESH').target = 'MESH'
        layout.operator("object.join",icon='ROTATECENTER')
        layout.separator()
        layout.menu("VIEW3D_MT_selectiontools",icon='MOD_MULTIRES')            
        layout.separator()
        layout.menu("VIEW3D_MT_origintools",icon='SPACE2')
        layout.separator()
        layout.menu("VIEW3D_MT_shadetools",icon='MOD_MULTIRES')
        layout.separator()
        layout.operator("object.delete",icon='X').use_global = False


class VIEW3D_MT_mesh_selection(bpy.types.Menu):
    bl_label = "Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.select_mode",text="Vertex Select",icon='VERTEXSEL').type='VERT'
        layout.operator("mesh.select_mode",text="Edge Select",icon='EDGESEL').type='EDGE'
        layout.operator("mesh.select_mode",text="Face Select",icon='FACESEL').type='FACE'


class VIEW3D_PT_Standard_Objects(bpy.types.Panel):
    bl_label = "Standard Objects"
    bl_idname = "TOOLS_PT_Archipack_Create"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Draw"
    bl_context = "objectmode"

    def draw(self, context):
        
        box = self.layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.label("Mesh",icon='OUTLINER_OB_MESH')
        
        row = col.row(align=True)
        row.scale_y = 1.3        
        row.operator("view3d.draw_assembly", icon='SURFACE_NCYLINDER',text="Draw Assembly")   

        row = col.row(align=True)
        row.scale_y = 1.3        
        row.operator("view3d.draw_plane", icon='MESH_PLANE',text="Draw Plane")   
        
        row = col.row(align=True)
        row.scale_y = 1.3        
        row.operator("view3d.add_text", icon='MESH_PLANE',text="Add Text")         
        
        box = self.layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.label("Curves",icon='OUTLINER_OB_CURVE')
        
        row = col.row(align=True)
        row.scale_y = 1.3        
        row.operator("view3d.draw_curve", icon='CURVE_DATA',text="Select Points To Draw")  

        row = col.row(align=True)
        row.scale_y = 1.3        
        row.operator("view3d.draw_curve", icon='CURVE_BEZCIRCLE',text="Draw Circle")  
        
        box = self.layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.label("Empties",icon='OUTLINER_OB_EMPTY')
        
        row = col.row(align=True)
        row.scale_y = 1.3
        row.operator("view3d.place_empty", icon='OUTLINER_DATA_EMPTY',text="Place Empty Object")    

        box = self.layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.label("Lamps",icon='OUTLINER_OB_LAMP')
        
        row = col.row(align=True)
        row.scale_y = 1.3
        row.operator("view3d.place_area_lamp", icon='LAMP_POINT',text="Draw Area Lamp")
        
        box = self.layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.label("Cameras",icon='OUTLINER_OB_CAMERA')
        
        row = col.row(align=True)
        row.scale_y = 1.3
        row.operator("view3d.draw_curve", icon='CAMERA_DATA',text="Place Camera")

def register():
    clear_view3d_properties_shelf()
    clear_view3d_tools_shelf()
    clear_view3d_header()
    clear_view3d_menus()
    
    bpy.utils.register_class(VIEW3D_HT_header)
    bpy.utils.register_class(VIEW3D_MT_menus)
    bpy.utils.register_class(VIEW3D_MT_view)
    bpy.utils.register_class(VIEW3D_MT_add_object)
    bpy.utils.register_class(VIEW3D_MT_add_lamp)
    bpy.utils.register_class(VIEW3D_MT_tools)
    bpy.utils.register_class(VIEW3D_MT_cursor_tools) 
    bpy.utils.register_class(VIEW3D_MT_transformtools) 
    bpy.utils.register_class(VIEW3D_MT_selectiontools) 
    bpy.utils.register_class(VIEW3D_MT_origintools) 
    bpy.utils.register_class(VIEW3D_MT_shadetools) 
    bpy.utils.register_class(VIEW3D_MT_objecttools) 
    bpy.utils.register_class(VIEW3D_MT_mesh_selection)  
    bpy.utils.register_class(VIEW3D_PT_Standard_Objects)
    
def unregister():
    pass