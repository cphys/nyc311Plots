import sys
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
mpl.style.use('ggplot') # optional: for ggplot-like style

def cleanData(df, sortVars = None, totNam = None, rowsToDrop = None, toNum = None, colsToDrop = None, inCombVals = [None,None], delNA = None, sortBy = None):

    if sortVars is not None:
        # Count number of 'rowVar' and group by 'colVar'.
        df = df.groupby(by = sortVars[0])[sortVars[1]].value_counts()
        df = df.unstack()

    else:
        df = df
    # Variables with list of columns and rows.
    colNams = df.columns.values
    rowNams = list(df.index)

    # Rename all of the variables with first letters capitalized.
    # and cast labels to strings
    colDict = {col: str(col).title() for col in colNams}
    rowDict = {row: str(row).title() for row in rowNams}
    df.rename(index = rowDict, columns = colDict, inplace=True)

    # Convert data to numerical values
    sizeBefore = df.size

    # Remove columns saved in 'colsToDrop' variable
    if colsToDrop is not None:
        colsToDrop = [str(col).title() for col in colsToDrop]
        df.drop(colsToDrop, axis = 1, inplace = True)

    # Remove rows saved in 'rowsToDrop' variable
    if rowsToDrop is not None:
        rowsToDrop = [str(row).title() for row in rowsToDrop]
        df.drop(rowsToDrop, inplace = True)

    # Update column and row names to reflect formatting and dropped vals
    colNams = df.columns
    rowNams = list(df.index)

    if toNum is not None:    
        df[toNum] = df[toNum].apply(pd.to_numeric, errors ='coerce')

    # Drop any rows containing na values
    if delNA is not None:
        df = df.dropna()

    # Print the number of rows deleted during data cleaning
    sizeAfter = df.size
    if sizeAfter == 0:
        sys.exit('All rows contained na values. Cleaning deleted all data')        
    print("\nCleaning deleted: {} rows\n".format(sizeBefore-sizeAfter)) 
 
    # Combine any row values passed to the 'inCombVals' dict value
    if inCombVals[0] is not None:
        rws = list(inCombVals[0].keys())
        for rw in rws:
            df.loc[rw] = df.loc[inCombVals[0][rw]].sum()
            dropRows = np.setdiff1d(inCombVals[0][rw], rws)
            df.drop(dropRows, inplace = True)

    # Combine any column values passed to the 'inCombVals' dict value
    if inCombVals[1] is not None:
        cls = list(inCombVals[1].keys())
        for cl in cls:
            df[cl] = df[inCombVals[1][cl]].sum(axis = 1)
            dropRows = np.setdiff1d(inCombVals[1][cl], cls)
            for row in dropRows:
                df.drop(row, axis=1, inplace = True)
        
    # Add a column with is the total of all of the values in the df
    if totNam is not None:
        # Add a column named Total to the end of the table
        df[totNam] = df.sum(axis=1)

    if sortBy is not None:
        # Sort columns by 'Total' and then in order of the colNams
        df.sort_values(by = sortBy, inplace = True, ascending = False)

    return df



def hBarPlots(df, axVal, leg = "", totLeg = "", recCol='steelblue', fcol1 = 'white', fcol2 = 'black', fsiz = 12, fws = .01, xAxisLab = '', yAxisLab = True, pTitle = '', bwScale = 0.2, bWidth = .75, cols = list(mcolors.TABLEAU_COLORS.values()), stkd = False, legLoc = 'uR'):   

    ax = df.plot(ax = axVal, kind = 'barh', stacked = stkd, rot = 0, width = bWidth, color = cols)

    # create annotations at the end of the plots
    if not stkd:
        # find maximum value rectangle width
        maxVal = np.max([i.get_width() for i in ax.patches])
        for i in ax.patches:
            # get_width pulls left or right; get_y pushes up or down
            width = i.get_width()
            height = i.get_height()

            label = format(int(width), ',')

            if width < bwScale * maxVal:
                ax.text(width + fws * width,
                        i.get_y() + (.5 * height),
                        label,
                        fontsize = fsiz,
                        color = fcol2,
                        horizontalalignment='left',
                        verticalalignment = 'center')

            else:
                ax.text(width - fws * width,
                        i.get_y() + (.5 * height),
                        label,
                        fontsize = fsiz,
                        color = fcol1,
                        horizontalalignment='right',
                        verticalalignment = 'center')

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

    if yAxisLab:
        ax.set_ylabel(str(df.index.name).replace("_"," ").title())
    elif not yAxisLab:
        pass
    else:
        ax.set_ylabel(yAxisLab.replace("_"," ").title())

    ax.set_title(pTitle.replace("_"," ").title())

    # Create the legend based on input variables and location
    if leg is not None:
        if legLoc is not None:
            legLen = len(leg)
            if totLeg is not None:
                formLeg = [str(leg[i]).replace("_"," ").title() + "\n({})".format(format(int(totLeg[i]), ',')) for i in range(len(leg))]
            else:
                formLeg = [str(leg[i]).replace("_"," ").title() for i in range(len(leg))]

            if legLoc =='below':
                ax.legend(formLeg, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=legLen)
            else:
                ax.legend(formLeg, loc='upper right', fancybox=True, shadow=True)

         
        
    # list x-axis in scientific notation
    ax.ticklabel_format(axis='x',scilimits=(0,0))
    return ax


# function for printing the column headers
def printListOfHeaders(df):
    return print('\nAvalable headers are:\n' + '%s' % '\n'.join(map(str, df.columns.values)) + '\n')
