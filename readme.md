Readme Please?
------


Code collection used for Master's thesis.

Code are written and adapted for NIH3T3 cell line with optoFGFR and microscopy setup.
There are four main experiments, two micropatterning codes, two viewers and additions including tools.


  Experiments
  - Doseresponse
      Single stim on nucleus area to test sensitivity of optoFGFR. Includes shuffle of stim regimes.
  - Global/Local
      Two stimulations, one global (Nr.1) and one local (Nr.2). Stimulation areas along major axis of cell.
  - Directed Migration
      Novel stimulation mask tool, using 4 additional variables:
        - axis: 'y-axis' or 'x-axis'
        - type: 'outline' or 'surface'
        - direction: 'up-right' or 'down-left'
        - width: value in px (in case of 'outline' stim)
  - Bottom / Top
      Stimulation along major axis either on bottom or top with adjustable location on axis. New variable in stim regime called 'location' ('top' or 'bottom').


  Micropatterns
  - Micropatterning
      Micropatterning requiring 1024x1024 mask. 
  - Micropatterning DMD
      Novel approach using DMD px, thus image 600x800 mask.

  Viewers
  - Dask Viewer
      Simple viewer of tiff image stacks of experiment including masks.
  - Superviewer (found in sperate repository /super-viewer)
      Sophisticated viewer to load image stacks of experiment, descriptions of FOV/experiment and graph ERK graphs


  Additions
  - Required for pipeline
    - acquisition
    - stim
    - utils
    - semantic segmentation
  - Value
      Tinker window for easy stim regime input
  - Tools
        Include functions for mask creation and function to get next experiment number
  - Offset
        Calculate offset for stimulation
  - Mail
        Send mails during experiment for remote overview over exp status
  - Checklist
        Create checklist before exp start
  - Anch mask
        For bottom / top stimulation mask creation
        

    
