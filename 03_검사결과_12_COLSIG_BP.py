#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib import font_manager,rc  #한글 폰트 입력을 위한 라이브러리
from pathlib import Path

#폰트 경로 가져오기
font_path = 'C:/Windows/Fonts/SGL.ttf' #삼성고딕체
 
# 폰트 이름 얻어오기
font_name = font_manager.FontProperties(fname=font_path).get_name()
 
#폰트 설정하기
mpl.rc('font',family=font_name)
# %%
workdir = 'C:/Users/smcljy/data/20211115_Factsheet/data'
data = pd.read_stata('{}/COLSIG.dta'.format(workdir))
# data.drop(data.loc[:,'RSLT_CD14':], axis=1, inplace=True)

# data.describe()

# %%
data.loc[data['GEND_CD'] == 'M', 'GENDER'] = '남'
data.loc[data['GEND_CD'] == 'F', 'GENDER'] = '여'

data[['AGE']] = data[['AGE']].apply(pd.to_numeric)
data.loc[ data['AGE'] < 30                      ,'AGEGRP'] = '29세 이하'
data.loc[(data['AGE'] > 29) & (data['AGE'] < 40),'AGEGRP'] = '30~39세'
data.loc[(data['AGE'] > 39) & (data['AGE'] < 50),'AGEGRP'] = '40~49세'
data.loc[(data['AGE'] > 49) & (data['AGE'] < 60),'AGEGRP'] = '50~59세'
data.loc[(data['AGE'] > 59) & (data['AGE'] < 70),'AGEGRP'] = '60~69세'
data.loc[ data['AGE'] > 69                      ,'AGEGRP'] = '70세 이상'
# data.head(100)
# data
# %% 결과별 정리
rslt_01 = 'Cancer'
rslt_01_cd = ['060']
for i in range(len(rslt_01_cd)):
    data['rslt_01_{}'.format(i)] = (
                     (data.loc[:,'BP1A152':'BP1A153_RSLT_CD07'] == rslt_01_cd[i])
                    ).any(axis=1).astype(int)
    data.loc[data['rslt_01_{}'.format(i)] == 1,rslt_01] = '01_'+rslt_01
data[rslt_01].fillna('00_Absent',inplace=True)

rslt_02 = 'High grade dysplasia'
rslt_02_cd = ['091']
for i in range(len(rslt_02_cd)):
    data['rslt_02_{}'.format(i)] = (
                     (data.loc[:,'BP1A152':'BP1A153_RSLT_CD07'] == rslt_02_cd[i])
                    ).any(axis=1).astype(int)
    data.loc[data['rslt_02_{}'.format(i)] == 1,rslt_02] = '01_'+rslt_02
data[rslt_02].fillna('00_Absent',inplace=True)

rslt_03 = 'Adenomatous polyp'
rslt_03_cd = ['010','012','090','092']
for i in range(len(rslt_03_cd)):
    data['rslt_03_{}'.format(i)] = (
                     (data.loc[:,'BP1A152':'BP1A153_RSLT_CD07'] == rslt_03_cd[i])
                    ).any(axis=1).astype(int)
    data.loc[data['rslt_03_{}'.format(i)] == 1,rslt_03] = '01_'+rslt_03
data[rslt_03].fillna('00_Absent',inplace=True)

rslt_04 = 'Hyperplastic polyp'
rslt_04_cd = ['011']
for i in range(len(rslt_04_cd)):
    data['rslt_04_{}'.format(i)] = (
                     (data.loc[:,'BP1A152':'BP1A153_RSLT_CD07'] == rslt_04_cd[i])
                    ).any(axis=1).astype(int)
    data.loc[data['rslt_04_{}'.format(i)] == 1,rslt_04] = '01_'+rslt_04
data[rslt_04].fillna('00_Absent',inplace=True)

rslt_05 = 'Carcinoid tumor'
rslt_05_cd = ['110','130']
for i in range(len(rslt_05_cd)):
    data['rslt_05_{}'.format(i)] = (
                     (data.loc[:,'BP1A152':'BP1A153_RSLT_CD07'] == rslt_05_cd[i])
                    ).any(axis=1).astype(int)
    data.loc[data['rslt_05_{}'.format(i)] == 1,rslt_05] = '01_'+rslt_05
data[rslt_05].fillna('00_Absent',inplace=True)

data
#%%
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

#%%
# 남성
data_org = data_m
gend_cd = "m"

# product pivot_table by result group 
for i in range(1,6):
    globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)] = data_org.pivot_table(
                             index=[globals()['rslt_0{}'.format(i,gend_cd)],'GENDER']
                            ,columns=['AGEGRP']
                            ,values=['ID']
                            ,aggfunc='count'
                            ,margins=True
                            ,fill_value=0
                            )

    # COL_rslt_01_cnt_m
    # each column total value percentile
    globals()['COL_rslt_0{}_per_{}'.format(i,gend_cd)] = round(globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)].div(globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)].iloc[-1], axis=1).astype(float)*100,1)

    # globals()['COL_rslt_0{}_per_m'.format(i)]

    globals()['COL_rslt_0{}_agegrp_{}'.format(i,gend_cd)] = pd.DataFrame()

    for j in range(len(globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)].columns)):
        if j == 0:
            globals()['COL_rslt_0{}_agegrp_{}'.format(i,gend_cd)] = pd.concat(
                                    [
                                    globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)].iloc[:,j]
                                    ,globals()['COL_rslt_0{}_per_{}'.format(i,gend_cd)].iloc[:,j]
                                    ]
                                ,axis=1
            )
        else:
            globals()['COL_rslt_0{}_agegrp_{}'.format(i,gend_cd)] = pd.concat(
                                    [
                                    globals()['COL_rslt_0{}_agegrp_{}'.format(i,gend_cd)]
                                    ,globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)].iloc[:,j]
                                    ,globals()['COL_rslt_0{}_per_{}'.format(i,gend_cd)].iloc[:,j]
                                    ]
                                ,axis=1
            )

# for i in range(1,8):
#     print(globals()['COL_rslt_0{}_agegrp_{}'.format(i,gend_cd)])

# data merge
globals()['COL_rslt_{}'.format(gend_cd)] = pd.concat(
[
    globals()['COL_rslt_01_agegrp_{}'.format(gend_cd)].iloc[1,:]
   ,globals()['COL_rslt_02_agegrp_{}'.format(gend_cd)].iloc[1,:]
   ,globals()['COL_rslt_03_agegrp_{}'.format(gend_cd)].iloc[1,:]
   ,globals()['COL_rslt_04_agegrp_{}'.format(gend_cd)].iloc[1,:]
   ,globals()['COL_rslt_05_agegrp_{}'.format(gend_cd)].iloc[1,:]
   ,globals()['COL_rslt_05_agegrp_{}'.format(gend_cd)].iloc[-1,:] # 전체인원
]
,axis=1
         ).T

globals()['COL_rslt_{}'.format(gend_cd)].columns = pd.MultiIndex.from_tuples(
        (
         ('29세 이하', 'N')
        ,('29세 이하', '%')
        ,('30~39세', 'N')
        ,('30~39세', '%')
        ,('40~49세', 'N')
        ,('40~49세', '%')
        ,('50~59세', 'N')
        ,('50~59세', '%')
        ,('60~69세', 'N')
        ,('60~69세', '%')
        ,('70세 이상', 'N')
        ,('70세 이상', '%')
        ,('전체', 'N')
        ,('전체', '%')
        )
    )

globals()['COL_rslt_{}'.format(gend_cd)]

#%%
# 여성
data_org = data_f
gend_cd = "f"

# product pivot_table by result group 
for i in range(1,6):
    globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)] = data_org.pivot_table(
                             index=[globals()['rslt_0{}'.format(i,gend_cd)],'GENDER']
                            ,columns=['AGEGRP']
                            ,values=['ID']
                            ,aggfunc='count'
                            ,margins=True
                            ,fill_value=0
                            )

    # COL_rslt_01_cnt_m
    # each column total value percentile
    globals()['COL_rslt_0{}_per_{}'.format(i,gend_cd)] = round(globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)].div(globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)].iloc[-1], axis=1).astype(float)*100,1)

    # globals()['COL_rslt_0{}_per_m'.format(i)]

    globals()['COL_rslt_0{}_agegrp_{}'.format(i,gend_cd)] = pd.DataFrame()

    for j in range(len(globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)].columns)):
        if j == 0:
            globals()['COL_rslt_0{}_agegrp_{}'.format(i,gend_cd)] = pd.concat(
                                    [
                                    globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)].iloc[:,j]
                                    ,globals()['COL_rslt_0{}_per_{}'.format(i,gend_cd)].iloc[:,j]
                                    ]
                                ,axis=1
            )
        else:
            globals()['COL_rslt_0{}_agegrp_{}'.format(i,gend_cd)] = pd.concat(
                                    [
                                    globals()['COL_rslt_0{}_agegrp_{}'.format(i,gend_cd)]
                                    ,globals()['COL_rslt_0{}_cnt_{}'.format(i,gend_cd)].iloc[:,j]
                                    ,globals()['COL_rslt_0{}_per_{}'.format(i,gend_cd)].iloc[:,j]
                                    ]
                                ,axis=1
            )

# for i in range(1,8):
#     print(globals()['COL_rslt_0{}_agegrp_{}'.format(i,gend_cd)])

# data merge
globals()['COL_rslt_{}'.format(gend_cd)] = pd.concat(
[
    globals()['COL_rslt_01_agegrp_{}'.format(gend_cd)].iloc[1,:]
   ,globals()['COL_rslt_02_agegrp_{}'.format(gend_cd)].iloc[1,:]
   ,globals()['COL_rslt_03_agegrp_{}'.format(gend_cd)].iloc[1,:]
   ,globals()['COL_rslt_04_agegrp_{}'.format(gend_cd)].iloc[1,:]
   ,globals()['COL_rslt_05_agegrp_{}'.format(gend_cd)].iloc[1,:]
   ,globals()['COL_rslt_05_agegrp_{}'.format(gend_cd)].iloc[-1,:] # 전체인원
]
,axis=1
         ).T

globals()['COL_rslt_{}'.format(gend_cd)].columns = pd.MultiIndex.from_tuples(
        (
         ('29세 이하', 'N')
        ,('29세 이하', '%')
        ,('30~39세', 'N')
        ,('30~39세', '%')
        ,('40~49세', 'N')
        ,('40~49세', '%')
        ,('50~59세', 'N')
        ,('50~59세', '%')
        ,('60~69세', 'N')
        ,('60~69세', '%')
        ,('70세 이상', 'N')
        ,('70세 이상', '%')
        ,('전체', 'N')
        ,('전체', '%')
        )
    )

globals()['COL_rslt_{}'.format(gend_cd)]

#%%
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # cact_agegrp_t.to_excel(writer,sheet_name="03_01이상지질혈증유병율")
    # liquiprep_agegrp_subt.to_excel(writer,sheet_name="03_09_1액상자궁세포")
    COL_rslt_m.to_excel(writer,sheet_name="03_13_COLBP_m")
    COL_rslt_f.to_excel(writer,sheet_name="03_13_COLBP_f")
# %%
