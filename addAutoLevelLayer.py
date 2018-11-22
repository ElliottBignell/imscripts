#!/usr/bin/env python

from gimpfu import *

def stretchLayer( img, drawable, *args ):

    pdb.gimp_context_push()

    layers = img.layers
    layer = pdb.gimp_layer_new_from_visible( img, img, "Auto_levels" )

    pdb.gimp_image_undo_group_start(img)

    pdb.gimp_image_insert_layer( img, layer, None, 0 )
    pdb.gimp_layer_set_mode( layer, LAYER_MODE_LUMINANCE )
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
    # pdb.gimp_layer_add_mask( layer, False )

    pdb.gimp_image_undo_group_end(img)

    pdb.gimp_context_pop()

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

main()
