# FLOYDS-flats-tools
Scripts to analyze FLOYDS lampflats


This code is designed to work with the `LCOGT/banzai-floyds` pipeline, specifically on the `feature/fringing` branch.
This repository is working smoothly as of **03/31/2023**
<br>
The code in this repository was all run in spyder, which is why the `#%%` symbols exist throughout. These are code cells that can be run separately in spyder.

## Running the pipeline
`floyds_data.py` is a script designed to grab lampflats for the year 2022, and find files with relatively different alt az pointings. Then these files can be downloaded.
<br>
`find_orders.py` is a script that allows the user to run the banzai-floyds pipeline on lampflats, given that the user has downloaded a skyflat.
This is necessary because at this time, lampflats do not have a full blue order, so order solving breaks.
<br>

## Order tweaking results
`order_tweaking_results.py` contains code to collect and plot information about lampflat order location and relative shift after tweaking.
<br>

`floyds_manual_shift.py` is a script that manually shifts lampflats relative to a template in the x and y directions. This is in order to compare the order
tweaking results with a first order guess about where the orders should be located to:

<ol>
<li>Reduce the amount of fringing</li>
<li> Reduce the misalignment along the edge of the order</li>
</ol>

<br>
`floyds_fringe_quantify.py` contains code to find the power spectrum of the fringing region of the red order in a given image. It also contains other code to produce plots
of fringe behaviour.
<br>
`floyds_stability.py` contains code to analyze the stability of the blue and red orders of a lampflat spectrum, as well as the stability of associated parameters.
<br>