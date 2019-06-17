#!/usr/bin/env python

from gimpfu import *

def stretchLayer( img, drawable, *args ):

    pdb.gimp_context_push()

    layers = img.layers
    layer = pdb.gimp_layer_new_from_visible( img, img, "Auto_levels" )

    pdb.gimp_image_undo_group_start(img)

    pdb.gimp_image_insert_layer( img, layer, None, 0 )
    pdb.gimp_layer_set_mode( layer, LAYER_MODE_HSV_VALUE )
    pdb.gimp_drawable_levels_stretch( layer )

    pdb.gimp_image_undo_group_end(img)

    pdb.gimp_context_pop()


def warmupLayer( img, drawable, *args ):

    pdb.gimp_context_push()

    layers = img.layers
    layer = pdb.gimp_layer_new_from_visible( img, img, "Warm-up filter" )

    pdb.gimp_image_undo_group_start(img)

    pdb.gimp_image_insert_layer( img, layer, None, 0 )
    pdb.gimp_layer_set_mode( layer,  LAYER_MODE_LCH_COLOR )
    pdb.gimp_curves_spline( layer, 1, 6, [0, 0, 104, 152, 255, 255])
    pdb.gimp_curves_spline( layer, 2, 6, [0, 0, 116, 140, 255, 255])
    pdb.gimp_layer_set_opacity( layer, 33 )
    # pdb.gimp_layer_add_mask( layer, False )

    pdb.gimp_image_undo_group_end(img)

    pdb.gimp_context_pop()

def yellowFilterLayer( img, drawable, *args ):

    pdb.gimp_context_push()

    layers = img.layers
    layer = pdb.gimp_layer_new_from_visible( img, img, "Warm-up filter" )

    pdb.gimp_image_undo_group_start(img)

    pdb.gimp_image_insert_layer( img, layer, None, 0 )
    pdb.gimp_layer_set_mode( layer,  LAYER_MODE_LUMINANCE )

    channels = pdb.gimp_image_get_channels( img )
    pdb.plug_in_colors_channel_mixer( img, layer, False, 1, 0, 0, 0, 1, 0, 0, 0, 0 )

    pdb.gimp_image_undo_group_end(img)

    pdb.gimp_context_pop()

def blurSelFilterLayer( img, drawable, *args ):

    pdb.gimp_context_push()

    layers = img.layers
    layer = pdb.gimp_layer_new_from_visible( img, img, "Blur selection layer" )

    pdb.gimp_image_undo_group_start(img)

    pdb.gimp_image_insert_layer( img, layer, None, 0 )

    mask = layer.create_mask( ADD_SELECTION_MASK )
    layer.add_mask( mask )
	
    layer_position = pdb.gimp_image_get_item_position( img, layer )

    for l in layers:
        l.visible = False
		
    layer.visible = True

    layerBlur = pdb.gimp_layer_new_from_visible( img, img, "Blur Layer" )
    pdb.gimp_image_insert_layer( img, layerBlur, None, 0 )
    pdb.gimp_selection_clear( img )
    pdb.plug_in_gauss_rle2( img, layerBlur, 64.0, 64.0 )

    maskBlur = layerBlur.create_mask( ADD_SELECTION_MASK )
    layerBlur.add_mask( maskBlur )

    pdb.gimp_edit_copy( mask )
    sel = pdb.gimp_edit_paste( maskBlur, True )
    pdb.gimp_floating_sel_anchor( sel )
	
    pdb.gimp_image_set_active_layer( img, layerBlur )
    pdb.gimp_image_remove_layer( img, layer )
	
    for l in layers:
        l.visible = True
	
    pdb.gimp_image_undo_group_end(img)
    pdb.gimp_context_pop()

def combinedLayerOps( img, drawable, *args ):
    yellowFilterLayer( img, drawable, *args )
    warmupLayer( img, drawable, *args )
    stretchLayer( img, drawable, *args )

def saveAsTif( img, drawable, *args ):
    pdb.file_tiff_save( img, drawable, "dsd_004301.tif", "dsd_004301.tif", 0 )

register(
    "python-fu-add-stretch-layer",
    "Add a layer with the histogram automatically stretched",
    "Add a layer with the histogram automatically stretched",
    "Elliott Bignell",
    "Elliott Bignell",
    "2018",
    "Add Stretch (Py)",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None)
    ],
    [],
    stretchLayer,
    menu="<Image>/Layer/Custom"
    )

register(
    "python-fu-add-yellow_filter-layer",
    "Add a yellow filter layer",
    "Add a yellow filter layer",
    "Elliott Bignell",
    "Elliott Bignell",
    "2018",
    "Add yellow filter Py)",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None)
    ],
    [],
    yellowFilterLayer,
    menu="<Image>/Layer/Custom"
    )

register(
    "python-fu-add-warmup-layer",
    "Add a layer with the curves biased to red/green",
    "Add a layer with the curves biased to red/green",
    "Elliott Bignell",
    "Elliott Bignell",
    "2018",
    "Add Warm-Up Layer (Py)",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None)
    ],
    [],
    warmupLayer,
    menu="<Image>/Layer/Custom"
    )

register(
    "python-fu-add-combined-layer",
    "Standards set of layers",
    "Standards set of layers",
    "Elliott Bignell",
    "Elliott Bignell",
    "2019",
    "Apply standard set of layer ops",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None)
    ],
    [],
    combinedLayerOps,
    menu="<Image>/Layer/Custom"
    )
	
register(
    "python-fu-add-blursel-layer",
    "Add a layer with the selection blurred",
    "Add a layer with the selection blurred",
    "Elliott Bignell",
    "Elliott Bignell",
    "2019",
    "Blur selection",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None)
    ],
    [],
    blurSelFilterLayer,
    menu="<Image>/Layer/Custom"
    )
	
register(
    "python-fu-save-as-tif",
    "Save the current file as a TIF",
    "Save the current file as a TIF",
    "Elliott Bignell",
    "Elliott Bignell",
    "2019",
    "Save as TIF",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None)
    ],
    [],
    saveAsTif,
    menu="<File>/Custom"
    )

main()
