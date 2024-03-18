from stardist.models import StarDist2D
import skimage
import numpy as np
import matplotlib.pyplot as plt
from csbdeep.utils import normalize
from skimage.morphology import remove_small_objects
from matplotlib.patches import Patch

def offset_moving(xy, stim_offset):
    x_offset = 0
    y_offset = 0
    x_offset = stim_offset[1]
    y_offset = stim_offset[0]
    offset_coordinate = (xy[1]+y_offset, xy[0]+x_offset)
    return offset_coordinate

def offset_moving_global(xy, stim_offset):
    x_offset = 0
    y_offset = 0

    x_offset = -abs(stim_offset[1])
    y_offset = -abs(stim_offset[0])

    offset_coordinate = (xy[1]+y_offset, xy[0]+x_offset)

    return offset_coordinate


def offset_plot(centroids,stim_offset,diameter,frame_to_plot,ax):
    for xy in centroids:
        x = xy[0]
        y = xy[1]
        if y > 800 or x < 150:
            pass
        else:
            y_off, x_off = offset_moving(xy,stim_offset)
            print(y,y_off)
            if y == y_off and x == x_off:
                non_off_color = "green"
                off_color = "darkgreen"
            else:
                non_off_color = "yellow"
                off_color = "blue"

            circle = plt.Circle((x,y), radius = diameter / 2, fill = False, color = non_off_color, linewidth = 2)
            offset_circle = plt.Circle((x_off,y_off), radius = diameter / 2, fill = False, color = off_color, linewidth = 2)
            ax.add_patch(circle)
            ax.add_patch(offset_circle)

    ax.imshow(frame_to_plot)


def stardist_h2b(h2b_frame):

    norm_min = 1
    norm_max = 99
    stardist_model = StarDist2D.from_pretrained('2D_versatile_fluo')

    ## PREPROCESSING ##   
    #scale the h2b channel for so StarDist
    f_h2b = h2b_frame.copy()
    #plt.imshow(frame)
    f_h2b_scaled = normalize(f_h2b,norm_min,norm_max) #30 95
    labels = np.array([])
    ##Instance segmentation
    #https://github.com/stardist/stardist/blob/master/stardist/models/base.py
    labels, details = stardist_model.predict_instances(f_h2b_scaled)
    # remove small objects:
    labels = remove_small_objects(labels, min_size=100, connectivity=1)
    plt.imshow(labels)
    plt.savefig("seg.png")
    plt.show()

    plt.imshow(f_h2b)
    plt.show()
    print(len(labels))
    
    return labels

def centroid_of_labels(labels):
    #unique_labels = np.unique(labels)
    #print(f'unique labels: {unique_labels}')
    centroids = []
    table_props = skimage.measure.regionprops_table(labels,properties=('label', 'centroid'))
    centroids = [(y,x) for x,y in zip(table_props["centroid-0"], table_props["centroid-1"])]
    
    print(len(centroids))
    return centroids


def calc_row_col(stim_regimes):
    # Initialize variables to store the factors and the smallest difference
    number = len(stim_regimes)
    factors = None
    min_difference = float('inf')  # Initialize with positive infinity

    # Loop from 1 to the square root of the number
    for i in range(1, int(number**0.5) + 1):
        # Check if 'i' is a factor of 'number'
        if number % i == 0:
            # Calculate the other factor
            j = number // i
            
            # Calculate the absolute difference between factors
            difference = abs(i - j)
            
            # Update if the difference is smaller
            if difference < min_difference:
                min_difference = difference
                factors = (i, j)

    return factors



def offsetting(stim_regimes,frame_type="erk"):

    channels_to_acq = [mCherry,miRFP]
    frame = acq_multi(channels_to_acq,dmd)

    if frame_type == "h2b":
        frame_to_plot = np.array(frame[0,:,:]) #frame[0,:,:]
    elif frame_type == "erk":
        frame_to_plot = np.array(frame[1,:,:]) #frame[1,:,:]
    else:
        frame_to_plot = frame[1,:,:]
    
    h2b_frame = np.array(frame[0,:,:])

    labels = stardist_h2b(h2b_frame)
    centroids = centroid_of_labels(labels)

    nb_row,nb_col = calc_row_col(stim_regimes)

    fig, axes = plt.subplots(nrows=nb_row,ncols=nb_col, figsize=(18,12), dpi = 400)

    for stim_regime,ax in zip(stim_regimes[:],axes.flatten()):
        stim_offset = stim_regime[2]
        stim_diameter = stim_regime[3]

        offset_plot(centroids, stim_offset, stim_diameter, frame_to_plot,ax)

        #ax.set_xticks([])
        #ax.set_yticks([])

        ax.set_title(f"Stim Regime: {stim_regime}", fontsize=8)

    legend_labels = ["Color green: No offset","Color yellow: Original stim","Color Blue: Offset stim"]
    legend_colors = ["green","yellow","blue"]
    proxy_artists = [Patch(color=color) for color in legend_colors]

    fig.legend(proxy_artists, legend_labels, loc='lower center', fontsize=12)

    plt.tight_layout()  # Ensures that the subplots don't overlap
    plt.subplots_adjust(bottom=0.03)  # Adjust the space for the legend
    plt.savefig('Offset.png')
    plt.show()
    
