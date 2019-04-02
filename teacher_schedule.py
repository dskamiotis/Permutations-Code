import pandas as pd
import numpy as np
import itertools
from itertools import combinations


def get_names_for_cell(cell):
    if cell == 0:
        return
    elif cell.__len__() == 7:
        return cell.split(' ')
    else:
        return cell


def convert_doubles_to_singles(df):
    result = []
    for i in range(0, len(df_names[cols[col]])):
        if df_names[cols[col]].iloc[i] == 0:
            continue
        elif df_names[cols[col]].iloc[i].__len__() == 7:
            result.append(df_names[cols[col]].iloc[i][:3])
            result.append(df_names[cols[col]].iloc[i][4:])
        else:
            result.append(df_names[cols[col]].iloc[i])
    return result


teacher_names_correct = pd.read_csv('teacherinit.csv', header=None)

csv_file = pd.read_csv('Whole_School_TT2.csv')
df = csv_file.dropna(how='all')
df = csv_file.fillna(0)
cols = df.columns
df_class_name = df.copy()
df_names = df.copy()
df_room_number = df.copy()

for col in range(0, len(df.columns)):
    for row in range(0, len(df)):
        if df[cols[col]].iloc[row] is not 0:
            text = df[cols[col]].iloc[row]
            index_dollar = df[cols[col]].iloc[row].find('$')
            r_index_dollar = df[cols[col]].iloc[row].rfind('$')
            if index_dollar is not -1:
                if index_dollar == r_index_dollar:
                    df_names[cols[col]].iloc[row] = df[cols[col]].iloc[row][index_dollar+1:index_dollar+4]
                else:
                    name1 = df[cols[col]].iloc[row][index_dollar + 1:index_dollar + 4]
                    name2 = df[cols[col]].iloc[row][r_index_dollar + 1:r_index_dollar + 4]
                    df_names[cols[col]].iloc[row] = name1 + ' ' + name2
                index_hash = df[cols[col]].iloc[row].find('#')
                df_class_name[cols[col]].iloc[row] = df[cols[col]].iloc[row][:(index_dollar - 1)]
                df_room_number[cols[col]].iloc[row] = df[cols[col]].iloc[row][index_hash + 1:-1]
            else:
                df_names[cols[col]].iloc[row] = 0
                index_hash = df[cols[col]].iloc[row].find('#')
                if index_hash is -1:
                    df_class_name[cols[col]].iloc[row] = df[cols[col]].iloc[row][:3]
                    df_room_number[cols[col]].iloc[row] = 0
                else:
                    df_class_name[cols[col]].iloc[row] = df[cols[col]].iloc[row][:(index_hash - 2 )]
                    df_room_number[cols[col]].iloc[row] = df[cols[col]].iloc[row][index_hash + 1:-1]


teacher_names_correct_list = []
for i in range(0, len(teacher_names_correct)):
    teacher_names_correct_list.append(teacher_names_correct.iloc[i][0])

teacher_names_correct_list_set = set(teacher_names_correct_list)

teacher_names = []
for col in range(0, len(cols)):
    result = convert_doubles_to_singles(df_names[cols[col]])
    result = pd.Series(result)
    period_names = (result.unique())
    teacher_names.extend(period_names)

df_all_names = pd.DataFrame(teacher_names, columns=['Names'])
df_all_names = pd.DataFrame(df_all_names['Names'].unique())
df_all_names = df_all_names[(df_all_names.T != 0).any()]

# i have to break up the cells which contain two names and split it in two cells
teacher_names_stripped = []
for i in range(0, len(df_all_names)):
    if df_all_names.iloc[i][0].__len__() == 7:
        teacher_names_stripped.append(df_all_names.iloc[i][0][:3])
        teacher_names_stripped.append(df_all_names.iloc[i][0][4:])
    else:
        teacher_names_stripped.append(df_all_names.iloc[i][0])

teacher_names_stripped_set = set(teacher_names_stripped)

# here, we have all the teacher names that are cross - referenced with the actual teacher names and are present
# in the .csv file
teacher_names_in_our_csv = teacher_names_correct_list_set.intersection(teacher_names_stripped_set)


# na to kanw gia each cell kai replace me ti mia me to kanoniko onoma
df_ant = pd.DataFrame('0', index=df_names.index, columns=df_names.columns)
for row in range(0, df_names.shape[0]):
    for col in range(0, df_names.shape[1]):
        cell_names = get_names_for_cell(df_names.loc[row][col])
        if cell_names == None:
            continue
        name_to_keep = []
        if type(cell_names) == list:
            for name in cell_names:
                if name in teacher_names_correct_list:
                    df_ant.iloc[row][col] = name
        else:
            df_ant.iloc[row][col] = cell_names



schedule = dict()
all_teacher_array = np.zeros((len(teacher_names_in_our_csv), df_ant.shape[1]), dtype=bool)
for name in range(0, len(teacher_names_in_our_csv)):
    temp = df_ant[df_ant == list(teacher_names_in_our_csv)[name]].any()
    all_teacher_array[name][:] = temp.as_matrix()[:]


def findOccurences(arr, periodIndex, indexesFound, combo, valid, periods, temp):
    # Check which indexes have worked at least one time solo for current period
    period = np.array(arr[:, periodIndex])
    # Check if only one index is true for current period
    if period[period == True].shape[0] == 1:
        solo = np.where(period == True)
        # Checking if current teacher has worked at least one day solo for current
        # period and isn't one of the previous checked teachers which have worked
        # solo in previous periods
        if solo not in indexesFound:
            indexesFound.append(solo[0][0])
            temp.append(periodIndex)
            periodIndex += 1
            if len(indexesFound) == 3:
                valid.append(combo)
                periods.append(temp)
                return
            if periodIndex <= 34:
                findOccurences(arr, periodIndex, indexesFound, combo, valid, periods, temp)
        else:
            periodIndex += 1
            if periodIndex <= 34:
                findOccurences(arr, periodIndex, indexesFound, combo, valid, periods, temp)
    else:
        periodIndex += 1
        if periodIndex <= 34:
            findOccurences(arr, periodIndex, indexesFound, combo, valid, periods, temp)
        else:
            return


teachers = all_teacher_array
combos = [",".join(map(str, comb)) for comb in combinations(range(0, teachers.shape[0]), 3)]
valid = []
periods = []
for combo in combos:
    comboSplit = combo.split(',')
    teacherA = teachers[int(comboSplit[0])][:]
    teacherB = teachers[int(comboSplit[1])][:]
    teacherC = teachers[int(comboSplit[2])][:]

    teachingTable = np.array([teacherA, teacherB, teacherC])
    i = 0
    idxs = []
    temp = []
    findOccurences(teachingTable, i, idxs, combo, valid, periods, temp)


# ground_truth = ['LTA', 'OST', 'SBA']
# ground_truth_combos = list(itertools.permutations(ground_truth))
d1 = dict([(y,x) for x,y in enumerate((teacher_names_in_our_csv))])
d2 = dict([(y,x) for x,y in enumerate((csv_file.columns))])
triads = []
period_names = []
for val in range(0, len(valid)):
    triad = []
    for i in valid[val].split(","):
        triad.append(list(d1.keys())[list(d1.values()).index(int(i))])
    triads.append(triad)
    period = []
    for i in periods[val]:
        period.append(list(d2.keys())[list(d2.values()).index(int(i))])
    period_names.append(period)
    # for c in ground_truth_combos:
    #     if list(c) == triad:
    #         print(triad)


df_with_schedule = pd.DataFrame(all_teacher_array, columns=csv_file.columns, index=d1.keys())
# df_with_schedule contains the schedule of all teachers found in the .csv
# period_names contains the period names where the triad is found to satisfy the condition
# triads contains the triad
# example -> period_names[0] shows the period names where the condition is satisfied for triads[0] and so on...

# so if you want to visually check a triad just open df_with_schedule and inspect the suggested period_names for the
# corresponding triad as in period_names[10] and triads[10] (the are in pairs of triads and their periods)