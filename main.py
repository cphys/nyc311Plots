import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from plotFuns import hBarPlots
from plotFuns import cleanData
from plotFuns import printListOfHeaders
import matplotlib.colors as mcolors

# location of file to import
dataLoc = 'data/NYC_311.csv'
ny311Df = pd.read_csv(dataLoc, skipinitialspace = True)

# printListOfHeaders(ny311Df)

# fields to import

# fields = ['incident_zip','complaint_type']
fields = ['complaint_type', 'borough']
# fields = ['borough','complaint_type']
# fields = ['complaint_type','incident_zip']

ny311Df = pd.read_csv(dataLoc, skipinitialspace = True, usecols = fields)

colDr = None   # column to drop from dataframe

tot = 'Total' # Name of column to be added. Will be the total of all rows

numRows = 7     # Number of rows for group divisions
totTopNum = 20  # Number of rows for y-axis of large plot
numCols = 6     # Number of columns for group divisions

# Convert all zipcodes to integer values
for field in fields:
    if field == 'incident_zip':
        ny311Df[field] = ny311Df[field].apply(pd.to_numeric, errors ='coerce')
        ny311Df[field] = ny311Df[field].astype('Int32')


# Index values to be combined and/or renamed

legStyle = 5

if legStyle ==1:
    legLoc2 = 'below'
    legLoc3 = None

else:  
    legLoc2 = 'uR'
    legLoc3 = 'uR'


if fields[1] == 'complaint_type':
    combRow = None

    combCol = {'Heat/\nHot Water' : ['Heat/Hot Water','Heating'],
               'Paint/\nPlaster' : ['Paint/Plaster','Paint - Plaster'],
               'General\nConstruction' : ['General Construction','Construction'],
               'Non-Construction' : ['Nonconst'],
               'Unsanitary\nCondition' : ['Unsanitary Condition'],
               'Door/\nWindow' : ['Door/Window']}
    yAxisLab1 = fields[0]
    yAxisLab2 = fields[0]
    yAxisLab3 = fields[0]

elif fields[0] == 'complaint_type':
    combCol = None

    combRow = {'Heat/Hot Water' : ['Heat/Hot Water','Heating'],
                 'Paint/Plaster' : ['Paint/Plaster','Paint - Plaster'],
                 'General Construction' : ['General Construction','Construction'],
                 'Non-Construction' : ['Nonconst']}
    yAxisLab1 = fields[0]
    yAxisLab2 = ''
    yAxisLab3 = ''

else:
    combRow = None
    combCol = None
    yAxisLab1 = fields[0]
    yAxisLab2 = ''
    yAxisLab3 = ''




# Create a dataframe with fields[0] as the rows fields[1] as the columns
groupdDf = cleanData(ny311Df, sortVars = fields, totNam = tot, inCombVals = [combRow, combCol], colsToDrop = colDr, sortBy = [tot])


# Sort the data and find the top 'numCols' 311 complaints city wide
columnNames = cleanData(ny311Df, sortVars = [fields[1],fields[0]], totNam = tot, inCombVals = [combCol, combRow], colsToDrop = colDr, sortBy = [tot]).index.values[:numCols]


# Columns are currently sorted according to highest total complaints
# Uncomment to sort alphabetically
# columnNames = np.sort(columnNames)

groupdDf = groupdDf[np.append(columnNames, [tot])]

rowNames = list(groupdDf.index)

# legNams = columnNames


## Plot Parameters ##
width = 8   # Total Width of Figure
p1Width = 2 # Width of first large plot
p2Width = 2 # Width of second large plot

ttlVal1 = 'Top {} NYC 311 Call {}s'.format(totTopNum, fields[0])
ttlVal2 = 'Top {}s by Top {}'.format(fields[0], fields[1])
ttlVal3 = 'Top {}s by Top {}'.format(fields[1], fields[0])

xlab = 'Number of Complaints'
# list of colors to be used in the plot
cols = list(mcolors.TABLEAU_COLORS.values())
# pop the first color off of 'cols' list and save
blCol = cols.pop(0)


# Create the series of subplots for figure
fig, axs = plt.subplots(numCols, width, figsize = (16, numCols*2))
gs = axs[0,0].get_gridspec()

# remove the underlying axes
for i in range(width):
    for ax in axs[0:, i]:
        ax.remove()

# create spaces for plots
axbig1 = fig.add_subplot(gs[0:, 0:p1Width]) # first large space on right
axbig2 = fig.add_subplot(gs[0:, (p1Width+1):(p1Width+1+p2Width)]) # large space in center
# list of spaces on RHS
axrs = [fig.add_subplot(gs[i, (width - 2):width]) for i in range(numCols)]


# Sort the items in the dataframe first by total and then by groups
# groupdDf.sort_values(by = [tot] + list(columnNames), inplace = True, ascending = False)
groupdDf.sort_values(by = [tot], inplace = True, ascending = False)

# Add large plot on LHS using 
hBarPlots(groupdDf[tot], axbig1,
          leg = [tot],
          num = totTopNum,
          pTitle = ttlVal1,
          xAxisLab = xlab,
          yAxisLab = yAxisLab1,
          cols=[blCol],
          bwScale = 0.35
         )

# Add large plot in center
hBarPlots(groupdDf[columnNames], axbig2,
          leg = columnNames,
          legLoc = legLoc2,
          num = numRows,
          pTitle = ttlVal2,
          xAxisLab = xlab,
          yAxisLab = yAxisLab2,
          bwScale = .4,
          cols=cols,
         )

# Create row of bar plots each with a single value
# Only show the title on the top plot and the x-axis label on the bottom
for i in range(numCols):
    groupdDf.sort_values(by = [columnNames[i]], inplace = True, ascending = False)
    if i == 0:
        ttl = ttlVal3
        xVal = xlab
    elif i == numCols - 1:
        xVal = xlab
    else:
        ttl = ''
        xVal = ''
    hBarPlots(groupdDf[columnNames[i]], axrs[i],
              leg = [columnNames[i]],
              legLoc = legLoc3,
              num = numRows,
              cols = cols[i],
              xAxisLab = xVal,
              yAxisLab = yAxisLab3,
              pTitle = ttl,
             ) 

dirName = os.getcwd()
plt.savefig(os.path.join(dirName, '{}.png'.format(ttlVal2).replace(' ','_')), bbox_inches = 'tight') 


