import pandas as pd
from tabula.io import read_pdf  #Option: import tabula and use tabula.read_pdf
import re
import streamlit as st


def create_table(file,subjects,labs):
    Subject_no=int(subjects)
    Labs_no=int(labs)
    filename=file
    try:
        df = read_pdf(filename, pages="all", lattice=True)
    except:
        st.write("Invalid File path")

    #input
    #Subject_no = input("enter the number of subjects" or 5)

    Subjects = []
    Labs = []
    start_sub = 3
    end_sub = Subject_no + 3
    start_labs = end_sub
    end_labs = start_labs + Labs_no  # Where Labs_no is number of labs
    for i in range(start_sub, end_sub):
        Subjects.append(df[1].T.iloc[i][0])
    for j in range(start_labs, end_labs):
        Labs.append(df[1].T.iloc[j][0])

    no_of_subjects = len(Subjects)
    no_of_labs = len(Labs)

    scodes = []
    for i in range(3, int(Subject_no) + 3):
        scodes.append(df[1].T.index[i])
    """
    subject1 = Subjects[0]  # df.T.loc['CSC401'][0]
    subject2 = Subjects[1]  # df.T.loc['CSC402'][0]
    subject3 = Subjects[2]  # df.T.loc['CSC403'][0]
    subject4 = Subjects[3]  # df.T.loc['CSC404'][0]
    subject5 = Subjects[4]  # df.T.loc['CSC405'][0]
    """


    count = 0
    n = len(df)  # 16 pages in the pdf
    index = 1
    list1 = []
    while (index < n):
        list1.append(index)
        index = index + 3

    for i in list1:
        if (count < 1):
            cleandf = pd.DataFrame()
            counter=3
            # cleandf['Name']=[1,2,3,4,5]
            cleandf['Name'] = list(df[i].T.loc['Name of the Student\rSeat No.'][2:23:5])
            for sub in range(no_of_subjects):
                cleandf[Subjects[sub]] = list(df[i].T.iloc[counter][2:23:5])
                counter = counter + 3

            """
            cleandf[subject1] = list(df[i].T.iloc[3][2:23:5])
            cleandf[subject2] = list(df[i].T.iloc[6][2:23:5])
            cleandf[subject3] = list(df[i].T.iloc[9][2:23:5])
            cleandf[subject4] = list(df[i].T.iloc[12][2:23:5])
            cleandf[subject5] = list(df[i].T.iloc[15][2:23:5])
            """
            try:
                cgpa = list(df[i].T.iloc[-1][2:23:5])
                for j in range(len(cgpa)):
                    cgpa[j] = cgpa[j][-1:-5:-1][-1::-1]
                cleandf['CGPA'] = cgpa
            except:
                cgpa = list(df[i].T.iloc[-2][2:23:5])
                for j in range(len(cgpa)):
                    cgpa[j] = cgpa[j][-1:-5:-1][-1::-1]
                cleandf['CGPA'] = cgpa
            count = 1
        else:
            temp = pd.DataFrame()
            counter=3
            # temp['Name']=[1,2,3,4,5]
            temp['Name'] = list(df[i].T.loc['Name of the Student\rSeat No.'][2:23:5])
            for sub in range(no_of_subjects):
                temp[Subjects[sub]] = list(df[i].T.iloc[counter][2:23:5])
                counter = counter + 3
            """
            temp[subject1] = list(df[i].T.iloc[3][2:23:5])
            temp[subject2] = list(df[i].T.iloc[6][2:23:5])
            temp[subject3] = list(df[i].T.iloc[9][2:23:5])
            temp[subject4] = list(df[i].T.iloc[12][2:23:5])
            temp[subject5] = list(df[i].T.iloc[15][2:23:5])
            """
            try:
                cgpa = list(df[i].T.iloc[-1][2:23:5])
                for j in range(len(cgpa)):
                    if cgpa[j][-1] == '#':
                        cgpa[j] = cgpa[j][-3:-6:-1][-1::-1]
                    else:
                        cgpa[j] = cgpa[j][-1:-5:-1][-1::-1]

                temp['CGPA'] = cgpa
            except:
                cgpa = list(df[i].T.iloc[-2][2:23:5])
                for j in range(len(cgpa)):
                    if cgpa[j][-1] == '#':
                        cgpa[j] = cgpa[j][-3:-6:-1][-1::-1]
                    else:
                        cgpa[j] = cgpa[j][-1:-5:-1][-1::-1]

                temp['CGPA'] = cgpa

            cleandf = pd.concat([temp, cleandf], axis=0)


    #Stage 2 cleaning
    cleandf.reset_index(inplace=True)
    cleandf.drop('index', axis=1, inplace=True)
    columns = cleandf.columns
    for i in columns[1:]:
        for j in range(cleandf[i].shape[0]):
            try:
                cleandf[i][j] = float(cleandf[i][j])
            except:
                cleandf[i][j] = 0
    clean_columns = []
    for columns in cleandf.columns:
        clean_columns.append(columns.replace('\r', ' '))
    cleandf.columns = clean_columns

    #block 3
    cleandf['Pass/fail'] = [None] * cleandf.shape[0]
    for i in range(cleandf.shape[0]):
        if (cleandf['CGPA'][i] == 0):
            cleandf['Pass/fail'][i] = 0
        else:
            cleandf['Pass/fail'][i] = 1

    #CGPA cleaning
    for i in range(cleandf.shape[0]):
        if cleandf['CGPA'][i] > 10:
            if float(str(cleandf['CGPA'][i])[-1:-4:-1][-1::-1]) == 0:
                cleandf['CGPA'][i] = 10.0
            else:
                cleandf['CGPA'][i] = float(str(cleandf['CGPA'][i])[-1:-4:-1][-1::-1])

    #practicals
    count = 0
    for i in list1:
        if (count < 1):
            pracsdf = pd.DataFrame()
            # cleandf['Name']=[1,2,3,4,5]
            pracsdf['Name'] = list(df[i].T.loc['Name of the Student\rSeat No.'][2:23:5])
            l_counter = counter
            for lab in range(no_of_labs):
                pracsdf[f'{Labs[lab]}: Term work'] = list(df[i].T.iloc[l_counter][2:23:5])
                pracsdf[f'{Labs[lab]}:Orals'] = list(df[i].T.iloc[l_counter + 1][2:23:5])
                l_counter = l_counter + 2
            """
            pracsdf[f'{Labs[0]}:Term work'] = list(df[i].T.iloc[18][2:23:5])
            pracsdf[f'{Labs[0]}:Orals'] = list(df[i].T.iloc[19][2:23:5])
            pracsdf[f'{Labs[1]}:Term work'] = list(df[i].T.iloc[21][2:23:5])
            pracsdf[f'{Labs[1]}:Orals'] = list(df[i].T.iloc[22][2:23:5])
            pracsdf[f'{Labs[2]}:Term work'] = list(df[i].T.iloc[24][2:23:5])
            pracsdf[f'{Labs[2]}:Orals'] = list(df[i].T.iloc[25][2:23:5])
            pracsdf[f'{Labs[3]}:Term work'] = list(df[i].T.iloc[27][2:23:5])
            pracsdf[f'{Labs[3]}:Orals'] = list(df[i].T.iloc[28][2:23:5])
            pracsdf[f'{Labs[4]}:Term work'] = list(df[i].T.iloc[30][2:23:5])
            pracsdf[f'{Labs[4]}:Orals'] = list(df[i].T.iloc[31][2:23:5])
            """
            count = 1
        else:
            labsdf = pd.DataFrame()
            # cleandf['Name']=[1,2,3,4,5]
            labsdf['Name'] = list(df[i].T.loc['Name of the Student\rSeat No.'][2:23:5])
            l_counter = counter
            for lab in range(no_of_labs):
                labsdf[f'{Labs[lab]}: Term work'] = list(df[i].T.iloc[l_counter][2:23:5])
                labsdf[f'{Labs[lab]}:Orals'] = list(df[i].T.iloc[l_counter + 1][2:23:5])
                l_counter = l_counter + 2
            """
            labsdf[f'{Labs[0]}:Term work'] = list(df[i].T.iloc[18][2:23:5])
            labsdf[f'{Labs[0]}:Orals'] = list(df[i].T.iloc[19][2:23:5])
            labsdf[f'{Labs[1]}:Term work'] = list(df[i].T.iloc[21][2:23:5])
            labsdf[f'{Labs[1]}:Orals'] = list(df[i].T.iloc[22][2:23:5])
            labsdf[f'{Labs[2]}:Term work'] = list(df[i].T.iloc[24][2:23:5])
            labsdf[f'{Labs[2]}:Orals'] = list(df[i].T.iloc[25][2:23:5])
            labsdf[f'{Labs[3]}:Term work'] = list(df[i].T.iloc[27][2:23:5])
            labsdf[f'{Labs[3]}:Orals'] = list(df[i].T.iloc[28][2:23:5])
            """
            if Labs_no == 4:
                pass
            else:
                labsdf[f'{Labs[4]}:Term work'] = list(df[i].T.iloc[30][2:23:5])
                labsdf[f'{Labs[4]}:Orals'] = list(df[i].T.iloc[31][2:23:5])
            pracsdf = pd.concat([labsdf, pracsdf], axis=0)

    pracsdf.reset_index(inplace=True)
    pracsdf.drop('index', axis=1, inplace=True)

    clean_pracs = []
    columns = pracsdf.columns
    for i in columns[1:]:
        for j in range(pracsdf[i].shape[0]):
            try:
                pracsdf[i][j] = float(str(pracsdf[i][j])[:2])
            except:
                pracsdf[i][j] = 0
    for columns in pracsdf.columns:
        clean_pracs.append(columns.replace('\r', ' '))
    pracsdf.columns = clean_pracs

    return cleandf,pracsdf


