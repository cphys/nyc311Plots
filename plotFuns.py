import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
mpl.style.use('ggplot') # optional: for ggplot-like style

def cleanData(df, colVar, rowVar, totNam = None, colsToDrop = None, inCombVals = None, cleanData = True):
    # Count number of 'rowVar' and group by 'colVar'.
    groupdDf = df.groupby(by = [rowVar])[colVar].value_counts()
    groupdDf = groupdDf.unstack()

    # Variables with list of columns and rows.
    colNams = groupdDf.columns.values
    rowNams = list(groupdDf.index)

    # Rename all of the variables with first letters capitalized.
    colDict = {str(col): str(col.title()) for col in colNams}
    rowDict = {str(row): str(row.title()) for row in rowNams}
    groupdDf.rename(index = rowDict, columns = colDict, inplace=True)


    # Remove columns saved in 'colsToDrop' variable
    if colsToDrop is not None:
        groupdDf.drop(colsToDrop, axis = 1, inplace = True)

    # Create list of colNams
    colNams = groupdDf.columns.values

    if cleanData:
        # clean data removing any rows containing nan and non-numeric values
        sizeBefore = groupdDf.size
        groupdDf[colNams] = groupdDf[colNams].apply(pd.to_numeric, errors ='coerce')
        groupdDf = groupdDf.dropna()
        sizeAfter = groupdDf.size

        print("\nCleaning deleted: {} rows\n".format(sizeBefore-sizeAfter)) 
 
    # Combine any values passed to the 'inCombVals' dict value
    if inCombVals is not None:
        keys = list(inCombVals.keys())
        for key in keys:
            groupdDf.loc[key] = groupdDf.loc[inCombVals[key]].sum()
            print(list(inCombVals[key]))
            groupdDf.drop(list(inCombVals[key]), inplace = True)
        
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
    ax.legend([iLeg.replace("_"," ").title() for iLeg in leg])
    # list x-axis in scientific notation
    ax.ticklabel_format(axis='x',scilimits=(0,0))
    return ax

