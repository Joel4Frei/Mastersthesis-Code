import matplotlib.pyplot as plt
import skimage
import math
import cv2
import pandas as pd
from cellpose import models
import numpy as np


def centroid(p0,p1,p2):
    a = 0.35 #centroid
    b = 1 #extent
    x = (a*p0[0]+b*p1[0]+b*p2[0])/(a+2*b)
    y = (a*p0[1]+b*p1[1]+b*p2[1])/(a+2*b)
    return x,y

def middle(p0,p1,axis_loc):
    a = 1 #centroid
    b = axis_loc #extent
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


def spot_mask_from_labels_bottom(labels, spot_size_b, axis_loc):
    '''Creates four spots for every cell in a segmentation image. Returns a binary image for the DMD.
    Returns a datatable that contains data for every spot: Cell label, cell size, cell centroid, spot centroid, spot size.'''
    df = pd.DataFrame()
    props = skimage.measure.regionprops(labels)

    plt.figure(figsize = (10,10),dpi = 200)
    plt.imshow(labels%13,cmap = 'Pastel2')

    
    spot_mask = np.zeros_like(labels)

    for prop in props[:]:
        print(prop.bbox)

        y = prop.centroid[0]
        x = prop.centroid[1]

        ax = plt.gca()

        x0 = x
        y0 = y
        
        orientation = prop.orientation

        x1 = x0 + math.cos(orientation) * 0.5 * prop.minor_axis_length
        y1 = y0 - math.sin(orientation) * 0.5 * prop.minor_axis_length
        x2 = x0 - math.sin(orientation) * 0.5 * prop.major_axis_length
        y2 = y0 - math.cos(orientation) * 0.5 * prop.major_axis_length


        x3 = x0 - math.cos(orientation) * 0.5 * prop.minor_axis_length
        y3 = y0 + math.sin(orientation) * 0.5 * prop.minor_axis_length
        x4 = x0 + math.sin(orientation) * 0.5 * prop.major_axis_length
        y4 = y0 + math.cos(orientation) * 0.5 * prop.major_axis_length


        x5,y5 = middle((x4,y4),(x0,y0),axis_loc)
        plt.scatter(x5,y5, c = 'darkgreen',s = 80)
        spot_mask = draw_circle((x5,y5),spot_size_b,spot_mask)
        df_spot = pd.DataFrame({'cell_label': [prop.label],'cell_x': [x], 'cell_y': [y], 'cell_area': [prop.area],'spot_radius': [10], 'spot_x': [x5], 'spot_y': [y5]})
        df = pd.concat([df, df_spot])
        

        
        ax.plot((x0, x3), (y0, y3), '-k', linewidth=1.)
        ax.plot((x0, x4), (y0, y4), '-k', linewidth=1.)
        ax.plot((x0, x1), (y0, y1), '-k', linewidth=1.)
        ax.plot((x0, x2), (y0, y2), '-k', linewidth=1.)

        
    plt.show()
    return spot_mask.astype('uint8'), df


def spot_mask_from_labels_top(labels, spot_size_a ,axis_loc):
    '''Creates four spots for every cell in a segmentation image. Returns a binary image for the DMD.
    Returns a datatable that contains data for every spot: Cell label, cell size, cell centroid, spot centroid, spot size.'''
    df = pd.DataFrame()
    props = skimage.measure.regionprops(labels)

    plt.figure(figsize = (10,10),dpi = 200)
    plt.imshow(labels%13,cmap = 'Pastel2')

    
    spot_mask = np.zeros_like(labels)

    for prop in props[:]:
        print(prop.bbox)

        y = prop.centroid[0]
        x = prop.centroid[1]

        ax = plt.gca()

        x0 = x
        y0 = y
        
        orientation = prop.orientation

        # Inside spot_mask_from_labels_top function
        x2 = x0 + math.cos(orientation) * 0.5 * prop.major_axis_length
        y2 = y0 + math.sin(orientation) * 0.5 * prop.major_axis_length
        x4 = x0 - math.cos(orientation) * 0.5 * prop.major_axis_length
        y4 = y0 - math.sin(orientation) * 0.5 * prop.major_axis_length
        x3 = x0 - math.cos(orientation) * 0.5 * prop.minor_axis_length
        y3 = y0 + math.sin(orientation) * 0.5 * prop.minor_axis_length


        x5,y5 = middle((x0,y0),(x2,y2),axis_loc)
        plt.scatter(x5,y5, c = 'darkgreen',s = 80)
        spot_mask = draw_circle((x5,y5),spot_size_a,spot_mask)
        df_spot = pd.DataFrame({'cell_label': [prop.label],'cell_x': [x], 'cell_y': [y], 'cell_area': [prop.area],'spot_radius': [6], 'spot_x': [x5], 'spot_y': [y5]})
        df = pd.concat([df, df_spot])
        

        
        ax.plot((x0, x3), (y0, y3), '-k', linewidth=1.)
        ax.plot((x0, x4), (y0, y4), '-k', linewidth=1.)
        ax.plot((x0, x1), (y0, y1), '-k', linewidth=1.)
        ax.plot((x0, x2), (y0, y2), '-k', linewidth=1.)

        
    plt.show()
    return spot_mask.astype('uint8'), df


def anch_masking(spot, spot_size, frame, axis_loc):

    model = models.Cellpose(gpu=True, model_type='cyto2')
    mask, flows, styles, diams = model.eval(frame, diameter=80)

    if spot == 'top':
        spot_mask,df = spot_mask_from_labels_top(mask,spot_size,axis_loc)
    elif spot == 'bottom':
        spot_mask,df = spot_mask_from_labels_bottom(mask,spot_size,axis_loc)

    return spot_mask,mask


