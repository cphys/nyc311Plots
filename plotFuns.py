import sys
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
mpl.style.use('ggplot') # optional: for ggplot-like style

def cleanData(df, colVar, rowVar, totNam = None, colsToDrop = None, inCombVals = None, delNA = True):

    # Count number of 'rowVar' and group by 'colVar'.
    groupdDf = df.groupby(by = [rowVar])[colVar].value_counts()
    groupdDf = groupdDf.unstack()

    # Variables with list of columns and rows.
    colNams = groupdDf.columns.values
    rowNams = list(groupdDf.index)

    # Rename all of the variables with first letters capitalized.
    colDict = {col: str(col).title() for col in colNams}
    rowDict = {row: str(row).title() for row in rowNams}
    groupdDf.rename(index = rowDict, columns = colDict, inplace=True)

    # Remove columns saved in 'colsToDrop' variable
    if colsToDrop is not None:
        try:
            groupdDf.drop(colsToDrop, axis = 1, inplace = True)
            print("\nCleaning deleted: columns {}".format(colsToDrop))
        except:
            print("\nCleaning deleted: 0 columns")
    else:
        print("\nCleaning deleted: 0 columns")

    # Create list of colNams
    colNams = groupdDf.columns

    # Convert data to numerical values
    sizeBefore = groupdDf.size
    groupdDf[colNams] = groupdDf[colNams].apply(pd.to_numeric, errors ='coerce')

    if delNA:
        # Drop any rows containing na values
        groupdDf = groupdDf.dropna()
    sizeAfter = groupdDf.size
    if sizeAfter == 0:
        sys.exit('All rows contained na values. Cleaning deleted all data')
        
    print("\nCleaning deleted: {} rows\n".format(sizeBefore-sizeAfter)) 
 
    # Combine any values passed to the 'inCombVals' dict value
    if inCombVals is not None:
        keys = list(inCombVals.keys())
        for key in keys:
            groupdDf.loc[key] = groupdDf.loc[inCombVals[key]].sum()
            dropRows = np.setdiff1d(inCombVals[key], keys)
            groupdDf.drop(dropRows, inplace = True)
        
    # Add a column with is the total of all of the values in the df
    if totNam is not None:
        # Add a column named Total to the end of the table
        groupdDf[totNam] = groupdDf.sum(axis=1)


        # Sort columns by 'Total' and then in order of the colNams
        groupdDf.sort_values(by = [totNam] + list(colNams),
                             inplace = True,
                             ascending = False
                        )
    return groupdDf



def hBarPlots(df, axVal, leg = [], recCol='steelblue', num = False, fcol1 = 'white', fcol2 = 'black', fsiz = 12, fws = .01, fhs = 0.16, xAxisLab = '', yAxisLab = '', pTitle = '', bwScale = 0.2, bWidth = .75, cols = list(mcolors.TABLEAU_COLORS.values()), stkd = False):   

    if not num:
        ax = df.plot(ax = axVal, kind = 'barh', stacked = stkd, rot = 0, width = bWidth, color = cols)
    else:
        ax = df.head(int(num)).plot(ax = axVal, kind = 'barh', stacked = stkd, rot = 0, width = bWidth, color = cols) 


    # create annotations at the end of the plots
    if not stkd:
        # find maximum value rectangle width
        totals = [i.get_width() for i in ax.patches]
        maxVal = np.max(totals)
        for i in ax.patches:
            # get_width pulls left or right; get_y pushes up or down
            width = i.get_width()
            height = i.get_height()

            label = format(int(width), ',')

            if width < bwScale * maxVal:
                ax.text(width + fws * width,
                        i.get_y() + (fhs * height),
                        label,
                        fontsize = fsiz,
                        color = fcol2,
                        horizontalalignment='left')

            else:
                ax.text(width - fws * width,
                        i.get_y() + (fhs * height),
                        label,
                        fontsize = fsiz,
                        color = fcol1,
                        horizontalalignment='right')

    # make the interactive mouse over give the bar title
    def format_ycursor(y):
        indexNames = df.index
        numGroups = len(ax.patches)/len(indexNames)
        barPos = np.arange(len(indexNames)) 
        for bar in barPos:
            if bar - (numGroups * bWidth/2) <= y <= bar + (numGroups * bWidth/2):
                return indexNames[bar].title()
    ax.fmt_ydata = format_ycursor

    # plot labels
    ax.set_xlabel(xAxisLab.replace("_"," ").title())
    ax.set_ylabel(yAxisLab.replace("_"," ").title())
    ax.set_title(pTitle.replace("_"," ").title())
    ax.legend([str(iLeg).replace("_"," ").title() for iLeg in leg])
    # list x-axis in scientific notation
    ax.ticklabel_format(axis='x',scilimits=(0,0))
    return ax


# function for printing the column headers
def printListOfHeaders(df):
    return print('\nAvalable headers are:\n' + '%s' % '\n'.join(map(str, df.columns.values)) + '\n')
