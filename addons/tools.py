from skimage.io import imread
from skimage.io.collection import alphanumeric_key
from dask import delayed
import dask.array as da
from glob import glob
import os
import numpy as np
from dask_image.imread import imread
from glob import glob
import math
import matplotlib.pyplot as plt
import skimage
import cv2
import pandas as pd
from skimage.morphology import binary_erosion
from skimage.segmentation import expand_labels
from skimage.measure import regionprops_table
from skimage.measure import label
from cellpose import models




def tiff_to_lazy_da(path,folder,fov):
    '''Read in all tiff files form the same FOV in a folder and load them lazily with dask. '''
    file_name_pattern = str(fov).zfill(2)+"_*.tiff"
#     filenames = os.listdir(path + os.path.join(str(folder))
    filenames = sorted(glob(os.path.join(path,folder, file_name_pattern)), key=alphanumeric_key)
    # read the first file to get the shape and dtype
    # ASSUMES THAT ALL FILES SHARE THE SAME SHAPE and TYPE
    print(filenames)

    sample = imread(filenames[0])
    
    lazy_imread = delayed(imread)  # lazy reader
    lazy_arrays = [lazy_imread(fn) for fn in filenames]
    dask_arrays = [
        da.from_delayed(delayed_reader, shape=sample.shape, dtype=sample.dtype)
        for delayed_reader in lazy_arrays
    ]
    # Stack into one large dask.array
    stack = da.stack(dask_arrays, axis=0)
    stack = np.squeeze(stack)
    return stack

'''Get next Experiment number of folder'''

def get_next_experiment_number(parent_folder):
    import os
    experiment_folders = [folder for folder in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))]
    
    # Extract numbers from folder names and sort them
    folder_numbers = [int(folder.split('_')[-1]) for folder in experiment_folders]
    folder_numbers.sort()
    
    # Find the last number and return the next number
    if folder_numbers:
        last_number = folder_numbers[-1]
        next_number = last_number + 1
        return next_number
    else:
        # If no folders exist, return 1
        return "Error"
    


'''Cell pose to light Mask'''    

def centroid(p0,p1,p2):
    a = 0.35 #centroid
    b = 1 #extent
    x = (a*p0[0]+b*p1[0]+b*p2[0])/(a+2*b)
    y = (a*p0[1]+b*p1[1]+b*p2[1])/(a+2*b)
    return x,y

def middle(p0,p1):
    a = 1 #centroid
    b = 1 #extent
    divisor = a+b
    x = (a*p0[0]+b*p1[0])/(divisor)
    y = (a*p0[1]+b*p1[1])/(divisor)
    return x,y

def draw_circle(xy, size, spot_mask):
    '''Takes a list of coordinates [(y,x),(y,x),...] and draws an ellipse on a mask for every point. '''
    #Elipse properties
    axesLength = (size,size) #20, 5 for horizontally stretched ellipse 
    angle = 0
    startAngle = 0
    endAngle = 360
    color = (1) 
    thickness = -1

    center_coordinates = (int(xy[0]),int(xy[1]))
    spot_mask = cv2.ellipse(spot_mask, center_coordinates, axesLength, angle, startAngle, endAngle, color, thickness) 
    return spot_mask


def spot_mask_from_labels(labels, spot_size_a = 6, spot_size_b = 10):
    '''Creates four spots for every cell in a segmentation image. Returns a binary image for the DMD.
    Returns a datatable that contains data for every spot: Cell label, cell size, cell centroid, spot centroid, spot size.'''
    df = pd.DataFrame()
    props = skimage.measure.regionprops(labels)

    plt.figure(figsize = (10,10),dpi = 200)
    plt.imshow(labels%13,cmap = 'Pastel2')

    an_size = 40
    cutouts = []
    
    spot_mask = np.zeros_like(labels)

    for prop in props[:]:
        print(prop.bbox)
        bbox = prop.bbox
        bbox_top = bbox[0]
        bbox_left = bbox[1]

        bbox_bottom = bbox[2]
        bbox_right = bbox[3]

        y = prop.centroid[0]
        x = prop.centroid[1]

        stim_top_x = (x+x)/2
        stim_top_y = (bbox_top +y)/2

        stim_right_y = (y+y)/2
        stim_right_x = (bbox_right+x)/2

        stim_bottom_x = (x+x)/2
        stim_bottom_y = (y+bbox_bottom)/2

        stim_left_x = (x+bbox_left)/2
        stim_left_y = (y+y)/2

        ax = plt.gca()

        x0 = x
        y0 = y
        
        orientation = prop.orientation

        x1 = x0 + math.cos(orientation) * 0.5 * prop.minor_axis_length
        y1 = y0 - math.sin(orientation) * 0.5 * prop.minor_axis_length
        x2 = x0 - math.sin(orientation) * 0.5 * prop.major_axis_length
        y2 = y0 - math.cos(orientation) * 0.5 * prop.major_axis_length


        minr, minc, maxr, maxc = prop.bbox
        bx = (minc, maxc, maxc, minc, minc)
        by = (minr, minr, maxr, maxr, minr)


        x3 = x0 - math.cos(orientation) * 0.5 * prop.minor_axis_length
        y3 = y0 + math.sin(orientation) * 0.5 * prop.minor_axis_length
        x4 = x0 + math.sin(orientation) * 0.5 * prop.major_axis_length
        y4 = y0 + math.cos(orientation) * 0.5 * prop.major_axis_length



        minr, minc, maxr, maxc = prop.bbox
        bx = (minc, maxc, maxc, minc, minc)
        by = (minr, minr, maxr, maxr, minr)

        x5,y5 = middle((x0,y0),(x2,y2))
        plt.scatter(x5,y5, c = 'darkgreen',s = 80)
        spot_mask = draw_circle((x5,y5),spot_size_a,spot_mask)
        df_spot = pd.DataFrame({'cell_label': [prop.label],'cell_x': [x], 'cell_y': [y], 'cell_area': [prop.area],'spot_radius': [6], 'spot_x': [x5], 'spot_y': [y5]})
        df = df.append(df_spot)
        
        x5,y5 = middle((x4,y4),(x0,y0))
        plt.scatter(x5,y5, c = 'darkgreen',s = 80)
        spot_mask = draw_circle((x5,y5),spot_size_b,spot_mask)
        df_spot = pd.DataFrame({'cell_label': [prop.label],'cell_x': [x], 'cell_y': [y], 'cell_area': [prop.area],'spot_radius': [10], 'spot_x': [x5], 'spot_y': [y5]})
        df = df.append(df_spot)
        
        ax.plot((x0, x3), (y0, y3), '-k', linewidth=1.)
        ax.plot((x0, x4), (y0, y4), '-k', linewidth=1.)
        ax.plot((x0, x1), (y0, y1), '-k', linewidth=1.)
        ax.plot((x0, x2), (y0, y2), '-k', linewidth=1.)

        
    plt.show()
    return spot_mask.astype('uint8'), df





''' Light Mask for migration or area of cell stimulation '''

def above_line(i,j,x2,y2,x3,y3):
    '''Check if point (i,j) is above the line given py points (x2,y2) and (x3,y3)'''
    v1 = (x2-x3, y2-y3)   #vector along line
    v2 = (x2-i, y2-j)     #vector petween line point and point to check
    xp = v1[0]*v2[1] - v1[1]*v2[0]  #cross product
    return xp>0

def beneath_line(i,j,x2,y2,x3,y3):
    '''Check if point (i,j) is above the line given py points (x2,y2) and (x3,y3)'''
    v1 = (x2-x3, y2-y3)   #vector along line
    v2 = (x2-i, y2-j)     #vector petween line point and point to check
    xp = v1[0]*v2[1] - v1[1]*v2[0]  #cross product
    return xp<0

def spot_mask_from_labels_y(labels, percentage,current_direction,current_width,current_type):
    '''Stim certain percentage of cell along major axis.
    50%: stim one half of the cell with border lying on minor axis.'''
    
    light_map = np.zeros_like(labels)
    props = skimage.measure.regionprops(labels)

    scaler = (percentage-50)/50*-1/2

    for prop in props:
        label = prop.label
        single_label = (labels == label)

        y0, x0 = prop.centroid

        min_point_height, min_point_width, max_point_height, max_point_width = prop.bbox

        move_factor = (max_point_height - min_point_height) * scaler
        
        if current_type == 'surface':
            outline_label = single_label
        
        elif current_type == 'outline':
            # Erode the cell mask
            eroded_label = binary_erosion(single_label)

            # Subtract the eroded mask from the original mask to get the outline
            outline_label = np.logical_xor(single_label, eroded_label)

        if current_direction == 'up-right':
            # Find point where cutoff line and major axis intersect
            x2 = x0 
            y2 = y0 - move_factor
            # Find second point on line
            length = 0.5 * prop.minor_axis_length
            x3 = x2 + length
            y3 = y2 

            # Make mask where all pixels above line are TRUE
            cutoff_mask = np.fromfunction(lambda i, j: above_line(j, i, x3, y3, x2, y2), np.shape(labels), dtype=int)
        
        elif current_direction == 'down-left':
            # Find point where cutoff line and major axis intersect
            x2 = x0 
            y2 = y0 + move_factor
            # Find second point on line
            length = 0.5 * prop.minor_axis_length
            x3 = x2 + length
            y3 = y2 

            # Make mask where all pixels above line are TRUE
            cutoff_mask = np.fromfunction(lambda i, j: beneath_line(j, i, x3, y3, x2, y2), np.shape(labels), dtype=int)

        # Intersect with cell mask
        frame_labeled_expanded = expand_labels(outline_label, current_width)
        stim_mask = np.logical_and(cutoff_mask, frame_labeled_expanded)

        light_map = np.logical_or(light_map, stim_mask)
        light_map = light_map.astype('uint8')


    return light_map

def spot_mask_from_labels_x(labels, percentage, current_direction,current_width,current_type):
    '''Stim certain percentage of cell along major axis.
    50%: stim one half of the cell with border lying on minor axis.'''
    
    light_map = np.zeros_like(labels)
    props = skimage.measure.regionprops(labels)

    scaler = (percentage-50)/50*-1/2

    for prop in props:
        label = prop.label
        single_label = (labels == label)

        y0, x0 = prop.centroid

        min_point_height, min_point_width, max_point_height, max_point_width = prop.bbox

        move_factor = (max_point_width - min_point_width) * scaler
        
        if current_type == 'surface':
            outline_label = single_label
        
        elif current_type == 'outline':
            # Erode the cell mask
            eroded_label = binary_erosion(single_label)

            # Subtract the eroded mask from the original mask to get the outline
            outline_label = np.logical_xor(single_label, eroded_label)

        # Find point where cutoff line and major axis intersect

        if current_direction == 'up-right':
            x2 = x0 - move_factor
            y2 = y0 
            # Find second point on line
            length = 0.5 * prop.minor_axis_length
            x3 = x2 
            y3 = y2 + length

            # Make mask where all pixels above line are TRUE
            cutoff_mask = np.fromfunction(lambda i, j: above_line(j, i, x3, y3, x2, y2), np.shape(labels), dtype=int)
        
        elif current_direction == 'down-left':
            print("O")
            x2 = x0 + move_factor
            y2 = y0 
            # Find second point on line
            length = 0.5 * prop.minor_axis_length
            x3 = x2 
            y3 = y2 + length  # change this line

            # Make mask where all pixels above line are TRUE
            cutoff_mask = np.fromfunction(lambda i, j: beneath_line(j, i, x3, y3, x2, y2), np.shape(labels), dtype=int)
            

        # Intersect with cell mask
        frame_labeled_expanded = expand_labels(outline_label, current_width)
        stim_mask = np.logical_and(cutoff_mask, frame_labeled_expanded)

        light_map = np.logical_or(light_map, stim_mask)
        light_map = light_map.astype('uint8')


    return light_map


def migration_mask(frame, current_axis, current_percentage, current_width, current_type, current_direction):
    
    model = models.Cellpose(gpu=True, model_type='cyto2')
    mask, flows, styles, diams = model.eval(frame, diameter=80)
    

    if current_axis == 'x-axis':
        light_map = spot_mask_from_labels_x(mask, current_percentage, current_direction, current_width, current_type)

    elif current_axis == 'y-axis':
        light_map = spot_mask_from_labels_y(mask, current_percentage, current_direction, current_width, current_type)

    return light_map , mask




