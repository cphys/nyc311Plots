import os
import re
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

# Change the zip code to an integer
ny311Df['incident_zip'] = ny311Df['incident_zip'].apply(pd.to_numeric, errors ='coerce')
ny311Df['incident_zip'] = ny311Df['incident_zip'].astype('Int32')

colHeads = np.array(ny311Df.columns).astype(str)


### Question 1 ###

fields = np.array([['complaint_type'], 'borough'])
wScale = 1.25   # scale the total width of the plot
hScale = 1.0    # scale the total height of the plot
numRows = 7     # Number of rows for group divisions
totTopNum = 20  # Number of rows for y-axis of large plot
numCols = 8     # Number of columns for group divisions
legLoc2 = 'uR'
legLoc3 = 'uR'

##################

### Question 2 ###
'''
fields = np.array([['incident_address'],'complaint_type' ])
wScale = 1.75   # scale the total width of the plot
hScale = 1.5    # scale the total height of the plot
numRows = 7     # Number of rows for group divisions
totTopNum = 20  # Number of rows for y-axis of large plot
numCols = 6     # Number of columns for group divisions
legLoc2 = 'uR'
legLoc3 = 'uR'
'''
##################


ny311Df = pd.read_csv(dataLoc, skipinitialspace = True, usecols = np.hstack(fields))

colDr = None    # column to drop from dataframe
# colDr = ['Unspecified']

tot = 'Total'   # Name of column to be added. Will be the total of all rows

# Convert all zipcodes to integer values
for field in fields:
    if field == 'incident_zip':
        ny311Df[field] = ny311Df[field].apply(pd.to_numeric, errors ='coerce')
        ny311Df[field] = ny311Df[field].astype('Int32')





# wScale = 1.5 # scale the total width of the plot
  
# Index values to be combined and/or renamed
if fields[1] == 'complaint_type':
    combRow = None

    combCol = {'Heat/\nHot Water' : ['Heat/Hot Water','Heating'],
               'Paint/\nPlaster' : ['Paint/Plaster','Paint - Plaster'],
               'General\nConstruction' : ['General Construction','Construction'],
               'Non-Construction' : ['Nonconst'],
               'Unsanitary\nCondition' : ['Unsanitary Condition'],
               'Door/\nWindow' : ['Door/Window']}

elif fields[0][0] == 'complaint_type':
    combCol = None

    combRow = {'Heat/Hot Water' : ['Heat/Hot Water','Heating'],
                 'Paint/Plaster' : ['Paint/Plaster','Paint - Plaster'],
                 'General Construction' : ['General Construction','Construction'],
                 'Non-Construction' : ['Nonconst']}

else:
    combRow = None
    combCol = None


# Sort the data and find the top 'numCols' 311 complaints city wide
columnNames = cleanData(ny311Df, sortVars = [[fields[1]], fields[0][0]], totNam = tot, inCombVals = [combCol, combRow], rowsToDrop = colDr, sortBy = [tot]).index.values

# Create a dataframe with fields[0] as the rows fields[1] as the columns
groupdDf = cleanData(ny311Df, sortVars = fields, totNam = tot, inCombVals = [combRow, combCol], colsToDrop = colDr, toNum = columnNames, sortBy = [tot])

if numCols > len(columnNames):
    numCols = len(columnNames)
columnNames = columnNames[:numCols]


# Columns are currently sorted according to highest total complaints
# Uncomment to sort alphabetically
# columnNames = np.sort(columnNames)

groupdDf = groupdDf[np.append(columnNames, [tot])]

rowNames = list(groupdDf.index)



## Plot Parameters ##
width = 8   # Total Width of Figure
p1Width = 2 # Width of first large plot
p2Width = 2 # Width of second large plot

ttlVal1 = 'Top {} NYC 311 Call {}s'.format(totTopNum, fields[0][0])
ttlVal2 = 'Top {}s by Top {}'.format(fields[0][0], fields[1])
ttlVal3 = 'Top {}s by Top {}'.format(fields[1], fields[0][0])

xlab = 'Number of Complaints'
# list of colors to be used in the plot
cols = list(mcolors.TABLEAU_COLORS.values())
# pop the first color off of 'cols' list and save
blCol = cols.pop(0)


# Create the series of subplots for figure
fig, axs = plt.subplots(numCols, width, figsize = (wScale * 16, hScale * numCols*2))
gs = axs[0,0].get_gridspec()

# remove the underlying axes
for i in range(width):
    for ax in axs[0:, i]:
        ax.remove()

# create spaces for plots
axbig1 = fig.add_subplot(gs[0:, 0:p1Width]) # first large space on right
axbig2 = fig.add_subplot(gs[0:, (p1Width + 1):(p1Width + 1 + p2Width)]) # large space in center
# list of spaces on RHS
axrs = [fig.add_subplot(gs[i, (width - 2):width]) for i in range(numCols)]


# Sort the items in the dataframe first by total and then by groups
# groupdDf.sort_values(by = [tot] + list(columnNames), inplace = True, ascending = False)
groupdDf.sort_values(by = [tot], inplace = True, ascending = False)


# Add large plot on LHS using 
hBarPlots(groupdDf[tot].head(totTopNum), axbig1,
          totLeg = [groupdDf[tot].sum()],
          leg = [tot],
          pTitle = ttlVal1,
          xAxisLab = xlab,
          cols=[blCol],
          bwScale = 0.35
         )

# Add large plot in center
hBarPlots(groupdDf[columnNames].head(numRows), axbig2,
          totLeg = groupdDf[columnNames].sum(),
          leg = columnNames,
          legLoc = legLoc2,
          pTitle = ttlVal2,
          xAxisLab = xlab,
          bwScale = .4,
          cols=cols,
         )

# Create row of bar plots each with a single value
# Only show the title on the top plot and the x-axis label on the bottom
for i in range(numCols):
    groupdDf.sort_values(by = [columnNames[i]], inplace = True, ascending = False)
    if i == 0:
        ttl = ttlVal3
        xVal = ''
    elif i == numCols - 1:
        xVal = xlab
    else:
        ttl = ''
        xVal = ''
    hBarPlots(groupdDf[columnNames[i]].head(numRows), axrs[i],
              totLeg = [groupdDf[columnNames[i]].sum()],
              leg = [columnNames[i]],
              legLoc = legLoc3,
              cols = cols[i],
              xAxisLab = xVal,
              pTitle = ttl,
             ) 

dirName = os.getcwd()
plt.savefig(os.path.join(dirName, '{}.png'.format(ttlVal2).replace(' ','_')), bbox_inches = 'tight') 


'''
for colH in colHeads:
    df = ny311Df.groupby(['incident_address','incident_zip'])[colH].count()
    df.sort_values(axis = 0, inplace = True, ascending = False)
    print(df.head(1))
print(df['34 ARDEN STREET'])
'''
