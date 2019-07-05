# import sys
# import types
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
# from botocore.client import Config
import matplotlib.pyplot as plt
from plotFuns import hBarPlots
from plotFuns import cleanData
import matplotlib.colors as mcolors

# location of file to import
dataLoc = 'data/NYC_311.csv'
# fields to import
fields = ['complaint_type', 'borough']
ny311Df = pd.read_csv(dataLoc, skipinitialspace = True, usecols = fields)

# Variables to be used as col and row headers.
colVar = 'borough'              # variable to be listed as column headers
rowVar = 'complaint_type'       # variable to be listed as row headers
colsToDrop = ['Unspecified']    # column to drop from dataframe
totNam = 'Total'

# Clean the data using cleanData function
groupdDf = cleanData(ny311Df, colVar,rowVar,colsToDrop,totNam)


colNams = groupdDf.columns.values
grpNams = np.setdiff1d(colNams,[totNam])
nGrps = len(grpNams)

## Plot Parameters ##
width = 8   # Total Width of Figure
p1Width = 2 # Width of first large plot
p2Width = 2 # Width of second large plot
ttlLarge = 'Total New York City 311 Complaints by Categroy'
ttlVal = 'Top {} 311 complaints by Borough'.format(nGrps)
xlab = 'Number of Complaints'
# list of colors to be used in the plot
cols = list(mcolors.TABLEAU_COLORS.values())
# pop the first color off of 'cols' list and save
blCol = cols.pop(0)


# Create the series of subplots for figure
fig, axs = plt.subplots(nGrps, width, figsize = (16, 9))
gs = axs[0,0].get_gridspec()

# remove the underlying axes
for i in range(width):
    for ax in axs[0:, i]:
        ax.remove()

# create spaces for plots
axbig1 = fig.add_subplot(gs[0:, 0:p1Width]) # first large space on right
axbig2 = fig.add_subplot(gs[0:, (p1Width+1):(p1Width+1+p2Width)]) # large space in center
# list of spaces on RHS
axrs = [fig.add_subplot(gs[i, (width - 2):width]) for i in range(nGrps)]


# Sort the items in the dataframe first by total and then by groups
groupdDf.sort_values(by = [totNam] + list(grpNams), inplace = True, ascending = False)

# Add large plot on LHS using 
hBarPlots(groupdDf[totNam], axbig1,
          leg = [totNam],
          pTitle = ttlLarge,
          xAxisLab = xlab,
          yAxisLab = rowVar,
          bWidth = .5,
          cols=[blCol],
         )

# Add large plot in center
hBarPlots(groupdDf[grpNams], axbig2,
          leg = grpNams,
          num = nGrps,
          pTitle = ttlVal,
          xAxisLab = xlab,
          cols=cols,
         )

# Create row of bar plots each with a single value
# Only show the title on the top plot and the x-axis label on the bottom
for i in range(nGrps):
    groupdDf.sort_values(by = [grpNams[i]],inplace = True, ascending = False)
    if i == 0:
        ttl = ttlVal
    else:
        ttl = ''
    if i == nGrps:
        xlab = xlab
    else:
        xlab = ''

    hBarPlots(groupdDf[grpNams[i]], axrs[i],
              leg = [grpNams[i]],
              num = nGrps,
              cols = cols[i],
              xAxisLab = xlab,
              pTitle = ttl,
             ) 

dirName = os.getcwd()
plt.savefig(os.path.join(dirName, '{}.png'.format(ttlLarge)), bbox_inches = 'tight') 

