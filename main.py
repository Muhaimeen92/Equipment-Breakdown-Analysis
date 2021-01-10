import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from nltk.corpus import stopwords
import math
import datetime

def main():
    breakdowns = pd.read_csv('./data.analysis.csv')
    parameters_to_analyse = ['Date', 'Type of Loss', 'BD Description', 'Equipment Description']
    database = breakdowns[parameters_to_analyse]

    bd_text = database['BD Description']
    bd_text.dropna()

    counter = []
    for description in bd_text:
        for word in str(description).split():
            if word not in stopwords.words('english') and word != '#N/A':
                counter.append(word)

    equipment_description = database['Equipment Description']
    avoid = ['#N/A', '#REF!', 'nan']
    most_eq = [eq for eq in equipment_description if str(eq) not in avoid]
    highest_eq = Counter(most_eq)
    highest_eq = sorted(highest_eq.items(), key=lambda max: max[1], reverse=True)
    barPlot(highest_eq)

    eq_dict = {}
    for eq in highest_eq:
        eq_rows = database['Equipment Description'] == eq[0]
        df = database[eq_rows]
        keywords = findKeywords(df['BD Description'])
        eq_dict[eq] = Counter(keywords)

    weeklyBreakdownAnalysis(database)

def weeklyBreakdownAnalysis(database, *equipment):
    '''First Prepare the database needed for the required equipment
    and parse the dates to a timestamp object'''
    if len(equipment) == 1:
        rows_needed = database['Equipment Description'] == equipment[0]
        database = database[rows_needed]
        equipment_name = equipment[0]
    else:
        equipment_name = "All Plant Equipment"
    database = database.dropna()
    if len(database) == 0:
        print('Sth went wrong')

    index = 0
    for date in database['Date']:
        if len(date) < 7:
            database['Date'].iloc[index] += '-20'
        index += 1
    database['parsed_time'] = pd.to_datetime(database['Date'])
    bds = []
    for week in database['parsed_time'].dt.isocalendar().week:
        bds.append(week)
    bds2 = Counter(bds)

    week_no = []
    bd_number = []
    for week, number in bds2.items():
        week_no.append(week)
        bd_number.append(number)

    plt.plot(week_no, bd_number)
    plt.xlabel('Week Number')
    plt.ylabel('Number of Breakdowns')
    plt.title(equipment_name)
    plt.show()

def barPlot(dataframe):
    '''Dataframe is a list of tuples with the first item the name of the
    equipment and the second item the number of breakdowns.
    This Function will draw a barplot of the top x breakdowns determined by the
    'number' variable'''

    number = 5  # number of top equipment you want to view
    indx = np.arange(number)
    equipment = []
    breakdowns = []
    for item in dataframe:
        equipment.append(item[0])
        breakdowns.append(item[1])
    plt.bar(indx, breakdowns[:number], width=0.4)
    plt.xticks(indx, equipment[:number])
    plt.xticks(rotation=45)
    plt.ylabel('Total number of breakdowns recorded')
    plt.show()

def findKeywords(dataframe):
    counter = []
    for description in dataframe:
        for word in str(description).split():
            if word not in stopwords.words('english') and word != '#N/A':
                counter.append(word)
    return counter

if __name__ == '__main__':
    main()