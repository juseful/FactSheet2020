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
data = pd.read_stata('{}/EGD.dta'.format(workdir))
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
rslt_01 = 'Adenoma, stomach'
rslt_01_cd = ['G051','G052','G080','G301','G303','G304']
for i in range(len(rslt_01_cd)):
    data['rslt_01_{}'.format(i)] = (
                     (data.loc[:,'BP1A151_RSLT_CD01':'BP1A151_RSLT_CD07'] == rslt_01_cd[i])
                    ).any(axis=1).astype(int)
    data.loc[data['rslt_01_{}'.format(i)] == 1,rslt_01] = '01_'+rslt_01
data[rslt_01].fillna('00_Absent',inplace=True)

rslt_02 = 'Stomach cancer'
rslt_02_cd = ['G100','G101','G104']
for i in range(len(rslt_02_cd)):
    data['rslt_02_{}'.format(i)] = (
                     (data.loc[:,'BP1A151_RSLT_CD01':'BP1A151_RSLT_CD07'] == rslt_02_cd[i])
                    ).any(axis=1).astype(int)
    data.loc[data['rslt_02_{}'.format(i)] == 1,rslt_02] = '01_'+rslt_02
data[rslt_02].fillna('00_Absent',inplace=True)

rslt_03 = 'B cell lymphoma, stomach'
rslt_03_cd = ['G102','G103']
for i in range(len(rslt_03_cd)):
    data['rslt_03_{}'.format(i)] = (
                     (data.loc[:,'BP1A151_RSLT_CD01':'BP1A151_RSLT_CD07'] == rslt_03_cd[i])
                    ).any(axis=1).astype(int)
    data.loc[data['rslt_03_{}'.format(i)] == 1,rslt_03] = '01_'+rslt_03
data[rslt_03].fillna('00_Absent',inplace=True)

rslt_04 = 'Esophageal cancer'
rslt_04_cd = ['G100','G101','G104']
for i in range(len(rslt_04_cd)):
    data['rslt_04_{}'.format(i)] = (
                     (data.loc[:,'BP1A155_RSLT_CD01':'BP1A155_RSLT_CD07'] == rslt_04_cd[i])
                    ).any(axis=1).astype(int)
    data.loc[data['rslt_04_{}'.format(i)] == 1,rslt_04] = '01_'+rslt_04
data[rslt_04].fillna('00_Absent',inplace=True)

rslt_05 = 'Duodenal adenoma'
rslt_05_cd = ['D406','G051','G080']
for i in range(len(rslt_05_cd)):
    data['rslt_05_{}'.format(i)] = (
                     (data.loc[:,'BP1A154_RSLT_CD01':'BP1A154_RSLT_CD07'] == rslt_05_cd[i])
                    ).any(axis=1).astype(int)
    data.loc[data['rslt_05_{}'.format(i)] == 1,rslt_05] = '01_'+rslt_05
data[rslt_05].fillna('00_Absent',inplace=True)

data

#%%
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

# %%
EGD_rslt_01_cnt_m = data_m.pivot_table(
                             index=[rslt_01,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# EGD_rslt_01_cnt_m
# each column total value percentile
EGD_rslt_01_per_m = round(EGD_rslt_01_cnt_m.div(EGD_rslt_01_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_01_per_m

EGD_rslt_01_agegrp_m = pd.DataFrame()

for i in range(len(EGD_rslt_01_cnt_m.columns)):
    if i == 0:
        EGD_rslt_01_agegrp_m = pd.concat(
                                [
                                 EGD_rslt_01_cnt_m.iloc[:,i]
                                ,EGD_rslt_01_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_01_agegrp_m = pd.concat(
                                [
                                 EGD_rslt_01_agegrp_m
                                ,EGD_rslt_01_cnt_m.iloc[:,i]
                                ,EGD_rslt_01_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# EGD_rslt_01_agegrp_m
# %%
EGD_rslt_01_cnt_f = data_f.pivot_table(
                             index=[rslt_01,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# EGD_rslt_01_cnt_f
# each column total value percentile
EGD_rslt_01_per_f = round(EGD_rslt_01_cnt_f.div(EGD_rslt_01_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_01_per_f

EGD_rslt_01_agegrp_f = pd.DataFrame()

for i in range(len(EGD_rslt_01_cnt_f.columns)):
    if i == 0:
        EGD_rslt_01_agegrp_f = pd.concat(
                                [
                                 EGD_rslt_01_cnt_f.iloc[:,i]
                                ,EGD_rslt_01_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_01_agegrp_f = pd.concat(
                                [
                                 EGD_rslt_01_agegrp_f
                                ,EGD_rslt_01_cnt_f.iloc[:,i]
                                ,EGD_rslt_01_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# EGD_rslt_01_agegrp_f

# %%
EGD_rslt_01_agegrp = pd.concat([EGD_rslt_01_agegrp_m, EGD_rslt_01_agegrp_f],axis=0)
EGD_rslt_01_agegrp = EGD_rslt_01_agegrp.sort_index()
EGD_rslt_01_agegrp.columns = pd.MultiIndex.from_tuples(
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

# labels = EGD_rslt_01_cnt_m.columns[:-1].to_list()
labels = EGD_rslt_01_cnt_m.columns.droplevel()[:-1].to_list()

# EGD_rslt_01_agegrp
# %%
EGD_rslt_01_cnt_t = data.pivot_table(
                             index=[rslt_01]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
EGD_rslt_01_per_t = round(EGD_rslt_01_cnt_t.div(EGD_rslt_01_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# EGD_rslt_01_per_t

EGD_rslt_01_agegrp_t = pd.DataFrame()

for i in range(len(EGD_rslt_01_cnt_t.columns)):
    if i == 0:
        EGD_rslt_01_agegrp_t = pd.concat(
                                [
                                 EGD_rslt_01_cnt_t.iloc[:,i]
                                ,EGD_rslt_01_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_01_agegrp_t = pd.concat(
                                [
                                 EGD_rslt_01_agegrp_t
                                ,EGD_rslt_01_cnt_t.iloc[:,i]
                                ,EGD_rslt_01_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

EGD_rslt_01_agegrp_t.columns = pd.MultiIndex.from_tuples(
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

# EGD_rslt_01_agegrp_t
# %%
EGD_rslt_01_cnt_subt = data.pivot_table(
                             index=[rslt_01]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# EGD_rslt_01_per_t = round(EGD_rslt_01_cnt_t.div(EGD_rslt_01_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
EGD_rslt_01_per_subt = round(EGD_rslt_01_cnt_subt.div(EGD_rslt_01_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_01_per_subt

EGD_rslt_01_agegrp_subt = pd.DataFrame()

for i in range(len(EGD_rslt_01_cnt_subt.columns)):
    if i == 0:
        EGD_rslt_01_agegrp_subt = pd.concat(
                                [
                                 EGD_rslt_01_cnt_subt.iloc[:,i]
                                ,EGD_rslt_01_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_01_agegrp_subt = pd.concat(
                                [
                                 EGD_rslt_01_agegrp_subt
                                ,EGD_rslt_01_cnt_subt.iloc[:,i]
                                ,EGD_rslt_01_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

EGD_rslt_01_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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

# EGD_rslt_01_agegrp_subt
# %%
EGD_rslt_02_cnt_m = data_m.pivot_table(
                             index=[rslt_02,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# EGD_rslt_02_cnt_m
# each column total value percentile
EGD_rslt_02_per_m = round(EGD_rslt_02_cnt_m.div(EGD_rslt_02_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_02_per_m

EGD_rslt_02_agegrp_m = pd.DataFrame()

for i in range(len(EGD_rslt_02_cnt_m.columns)):
    if i == 0:
        EGD_rslt_02_agegrp_m = pd.concat(
                                [
                                 EGD_rslt_02_cnt_m.iloc[:,i]
                                ,EGD_rslt_02_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_02_agegrp_m = pd.concat(
                                [
                                 EGD_rslt_02_agegrp_m
                                ,EGD_rslt_02_cnt_m.iloc[:,i]
                                ,EGD_rslt_02_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# EGD_rslt_02_agegrp_m
# %%
EGD_rslt_02_cnt_f = data_f.pivot_table(
                             index=[rslt_02,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# EGD_rslt_02_cnt_f
# each column total value percentile
EGD_rslt_02_per_f = round(EGD_rslt_02_cnt_f.div(EGD_rslt_02_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_02_per_f

EGD_rslt_02_agegrp_f = pd.DataFrame()

for i in range(len(EGD_rslt_02_cnt_f.columns)):
    if i == 0:
        EGD_rslt_02_agegrp_f = pd.concat(
                                [
                                 EGD_rslt_02_cnt_f.iloc[:,i]
                                ,EGD_rslt_02_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_02_agegrp_f = pd.concat(
                                [
                                 EGD_rslt_02_agegrp_f
                                ,EGD_rslt_02_cnt_f.iloc[:,i]
                                ,EGD_rslt_02_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# EGD_rslt_02_agegrp_f

# %%
EGD_rslt_02_agegrp = pd.concat([EGD_rslt_02_agegrp_m, EGD_rslt_02_agegrp_f],axis=0)
EGD_rslt_02_agegrp = EGD_rslt_02_agegrp.sort_index()
EGD_rslt_02_agegrp.columns = pd.MultiIndex.from_tuples(
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

# labels = EGD_rslt_02_cnt_m.columns[:-1].to_list()

# EGD_rslt_02_agegrp
# %%
EGD_rslt_02_cnt_t = data.pivot_table(
                             index=[rslt_02]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
EGD_rslt_02_per_t = round(EGD_rslt_02_cnt_t.div(EGD_rslt_02_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# EGD_rslt_02_per_t

EGD_rslt_02_agegrp_t = pd.DataFrame()

for i in range(len(EGD_rslt_02_cnt_t.columns)):
    if i == 0:
        EGD_rslt_02_agegrp_t = pd.concat(
                                [
                                 EGD_rslt_02_cnt_t.iloc[:,i]
                                ,EGD_rslt_02_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_02_agegrp_t = pd.concat(
                                [
                                 EGD_rslt_02_agegrp_t
                                ,EGD_rslt_02_cnt_t.iloc[:,i]
                                ,EGD_rslt_02_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

EGD_rslt_02_agegrp_t.columns = pd.MultiIndex.from_tuples(
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

# EGD_rslt_02_agegrp_t
# %%
EGD_rslt_02_cnt_subt = data.pivot_table(
                             index=[rslt_02]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# EGD_rslt_02_per_t = round(EGD_rslt_02_cnt_t.div(EGD_rslt_02_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
EGD_rslt_02_per_subt = round(EGD_rslt_02_cnt_subt.div(EGD_rslt_02_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_02_per_subt

EGD_rslt_02_agegrp_subt = pd.DataFrame()

for i in range(len(EGD_rslt_02_cnt_subt.columns)):
    if i == 0:
        EGD_rslt_02_agegrp_subt = pd.concat(
                                [
                                 EGD_rslt_02_cnt_subt.iloc[:,i]
                                ,EGD_rslt_02_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_02_agegrp_subt = pd.concat(
                                [
                                 EGD_rslt_02_agegrp_subt
                                ,EGD_rslt_02_cnt_subt.iloc[:,i]
                                ,EGD_rslt_02_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

EGD_rslt_02_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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

# EGD_rslt_02_agegrp_subt
# %%
EGD_rslt_03_cnt_m = data_m.pivot_table(
                             index=[rslt_03,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# EGD_rslt_03_cnt_m
# each column total value percentile
EGD_rslt_03_per_m = round(EGD_rslt_03_cnt_m.div(EGD_rslt_03_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_03_per_m

EGD_rslt_03_agegrp_m = pd.DataFrame()

for i in range(len(EGD_rslt_03_cnt_m.columns)):
    if i == 0:
        EGD_rslt_03_agegrp_m = pd.concat(
                                [
                                 EGD_rslt_03_cnt_m.iloc[:,i]
                                ,EGD_rslt_03_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_03_agegrp_m = pd.concat(
                                [
                                 EGD_rslt_03_agegrp_m
                                ,EGD_rslt_03_cnt_m.iloc[:,i]
                                ,EGD_rslt_03_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# EGD_rslt_03_agegrp_m
# %%
EGD_rslt_03_cnt_f = data_f.pivot_table(
                             index=[rslt_03,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# EGD_rslt_03_cnt_f
# each column total value percentile
EGD_rslt_03_per_f = round(EGD_rslt_03_cnt_f.div(EGD_rslt_03_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_03_per_f

EGD_rslt_03_agegrp_f = pd.DataFrame()

for i in range(len(EGD_rslt_03_cnt_f.columns)):
    if i == 0:
        EGD_rslt_03_agegrp_f = pd.concat(
                                [
                                 EGD_rslt_03_cnt_f.iloc[:,i]
                                ,EGD_rslt_03_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_03_agegrp_f = pd.concat(
                                [
                                 EGD_rslt_03_agegrp_f
                                ,EGD_rslt_03_cnt_f.iloc[:,i]
                                ,EGD_rslt_03_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# EGD_rslt_03_agegrp_f

# %%
EGD_rslt_03_agegrp = pd.concat([EGD_rslt_03_agegrp_m, EGD_rslt_03_agegrp_f],axis=0)
EGD_rslt_03_agegrp = EGD_rslt_03_agegrp.sort_index()
EGD_rslt_03_agegrp.columns = pd.MultiIndex.from_tuples(
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

# labels = EGD_rslt_03_per_m.columns[:-1].to_list()

# EGD_rslt_03_agegrp
# %%
EGD_rslt_03_cnt_t = data.pivot_table(
                             index=[rslt_03]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
EGD_rslt_03_per_t = round(EGD_rslt_03_cnt_t.div(EGD_rslt_03_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# EGD_rslt_03_per_t

EGD_rslt_03_agegrp_t = pd.DataFrame()

for i in range(len(EGD_rslt_03_cnt_t.columns)):
    if i == 0:
        EGD_rslt_03_agegrp_t = pd.concat(
                                [
                                 EGD_rslt_03_cnt_t.iloc[:,i]
                                ,EGD_rslt_03_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_03_agegrp_t = pd.concat(
                                [
                                 EGD_rslt_03_agegrp_t
                                ,EGD_rslt_03_cnt_t.iloc[:,i]
                                ,EGD_rslt_03_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

EGD_rslt_03_agegrp_t.columns = pd.MultiIndex.from_tuples(
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

# EGD_rslt_03_agegrp_t
# %%
EGD_rslt_03_cnt_subt = data.pivot_table(
                             index=[rslt_03]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# EGD_rslt_03_per_t = round(EGD_rslt_03_cnt_t.div(EGD_rslt_03_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
EGD_rslt_03_per_subt = round(EGD_rslt_03_cnt_subt.div(EGD_rslt_03_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_03_per_subt

EGD_rslt_03_agegrp_subt = pd.DataFrame()

for i in range(len(EGD_rslt_03_cnt_subt.columns)):
    if i == 0:
        EGD_rslt_03_agegrp_subt = pd.concat(
                                [
                                 EGD_rslt_03_cnt_subt.iloc[:,i]
                                ,EGD_rslt_03_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_03_agegrp_subt = pd.concat(
                                [
                                 EGD_rslt_03_agegrp_subt
                                ,EGD_rslt_03_cnt_subt.iloc[:,i]
                                ,EGD_rslt_03_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

EGD_rslt_03_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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

# EGD_rslt_03_agegrp_subt
# %%
EGD_rslt_04_cnt_m = data_m.pivot_table(
                             index=[rslt_04,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# EGD_rslt_04_cnt_m
# each column total value percentile
EGD_rslt_04_per_m = round(EGD_rslt_04_cnt_m.div(EGD_rslt_04_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_04_per_m

EGD_rslt_04_agegrp_m = pd.DataFrame()

for i in range(len(EGD_rslt_04_cnt_m.columns)):
    if i == 0:
        EGD_rslt_04_agegrp_m = pd.concat(
                                [
                                 EGD_rslt_04_cnt_m.iloc[:,i]
                                ,EGD_rslt_04_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_04_agegrp_m = pd.concat(
                                [
                                 EGD_rslt_04_agegrp_m
                                ,EGD_rslt_04_cnt_m.iloc[:,i]
                                ,EGD_rslt_04_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# EGD_rslt_04_agegrp_m
# %%
EGD_rslt_04_cnt_f = data_f.pivot_table(
                             index=[rslt_04,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# EGD_rslt_04_cnt_f
# each column total value percentile
EGD_rslt_04_per_f = round(EGD_rslt_04_cnt_f.div(EGD_rslt_04_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_04_per_f

EGD_rslt_04_agegrp_f = pd.DataFrame()

for i in range(len(EGD_rslt_04_cnt_f.columns)):
    if i == 0:
        EGD_rslt_04_agegrp_f = pd.concat(
                                [
                                 EGD_rslt_04_cnt_f.iloc[:,i]
                                ,EGD_rslt_04_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_04_agegrp_f = pd.concat(
                                [
                                 EGD_rslt_04_agegrp_f
                                ,EGD_rslt_04_cnt_f.iloc[:,i]
                                ,EGD_rslt_04_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# EGD_rslt_04_agegrp_f

# %%
EGD_rslt_04_agegrp = pd.concat([EGD_rslt_04_agegrp_m, EGD_rslt_04_agegrp_f],axis=0)
EGD_rslt_04_agegrp = EGD_rslt_04_agegrp.sort_index()
EGD_rslt_04_agegrp.columns = pd.MultiIndex.from_tuples(
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

# labels = EGD_rslt_04_per_m.columns[:-1].to_list()

# EGD_rslt_04_agegrp
# %%
EGD_rslt_04_cnt_t = data.pivot_table(
                             index=[rslt_04]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
EGD_rslt_04_per_t = round(EGD_rslt_04_cnt_t.div(EGD_rslt_04_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# EGD_rslt_04_per_t

EGD_rslt_04_agegrp_t = pd.DataFrame()

for i in range(len(EGD_rslt_04_cnt_t.columns)):
    if i == 0:
        EGD_rslt_04_agegrp_t = pd.concat(
                                [
                                 EGD_rslt_04_cnt_t.iloc[:,i]
                                ,EGD_rslt_04_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_04_agegrp_t = pd.concat(
                                [
                                 EGD_rslt_04_agegrp_t
                                ,EGD_rslt_04_cnt_t.iloc[:,i]
                                ,EGD_rslt_04_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

EGD_rslt_04_agegrp_t.columns = pd.MultiIndex.from_tuples(
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

# EGD_rslt_04_agegrp_t
# %%
EGD_rslt_04_cnt_subt = data.pivot_table(
                             index=[rslt_04]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# EGD_rslt_04_per_t = round(EGD_rslt_04_cnt_t.div(EGD_rslt_04_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
EGD_rslt_04_per_subt = round(EGD_rslt_04_cnt_subt.div(EGD_rslt_04_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_04_per_subt

EGD_rslt_04_agegrp_subt = pd.DataFrame()

for i in range(len(EGD_rslt_04_cnt_subt.columns)):
    if i == 0:
        EGD_rslt_04_agegrp_subt = pd.concat(
                                [
                                 EGD_rslt_04_cnt_subt.iloc[:,i]
                                ,EGD_rslt_04_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_04_agegrp_subt = pd.concat(
                                [
                                 EGD_rslt_04_agegrp_subt
                                ,EGD_rslt_04_cnt_subt.iloc[:,i]
                                ,EGD_rslt_04_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

EGD_rslt_04_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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

# EGD_rslt_04_agegrp_subt
# %%
EGD_rslt_05_cnt_m = data_m.pivot_table(
                             index=[rslt_05,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# EGD_rslt_05_cnt_m
# each column total value percentile
EGD_rslt_05_per_m = round(EGD_rslt_05_cnt_m.div(EGD_rslt_05_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_05_per_m

EGD_rslt_05_agegrp_m = pd.DataFrame()

for i in range(len(EGD_rslt_05_cnt_m.columns)):
    if i == 0:
        EGD_rslt_05_agegrp_m = pd.concat(
                                [
                                 EGD_rslt_05_cnt_m.iloc[:,i]
                                ,EGD_rslt_05_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_05_agegrp_m = pd.concat(
                                [
                                 EGD_rslt_05_agegrp_m
                                ,EGD_rslt_05_cnt_m.iloc[:,i]
                                ,EGD_rslt_05_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# EGD_rslt_05_agegrp_m
# %%
EGD_rslt_05_cnt_f = data_f.pivot_table(
                             index=[rslt_05,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# EGD_rslt_05_cnt_f
# each column total value percentile
EGD_rslt_05_per_f = round(EGD_rslt_05_cnt_f.div(EGD_rslt_05_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_05_per_f

EGD_rslt_05_agegrp_f = pd.DataFrame()

for i in range(len(EGD_rslt_05_cnt_f.columns)):
    if i == 0:
        EGD_rslt_05_agegrp_f = pd.concat(
                                [
                                 EGD_rslt_05_cnt_f.iloc[:,i]
                                ,EGD_rslt_05_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_05_agegrp_f = pd.concat(
                                [
                                 EGD_rslt_05_agegrp_f
                                ,EGD_rslt_05_cnt_f.iloc[:,i]
                                ,EGD_rslt_05_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# EGD_rslt_05_agegrp_f

# %%
EGD_rslt_05_agegrp = pd.concat([EGD_rslt_05_agegrp_m, EGD_rslt_05_agegrp_f],axis=0)
EGD_rslt_05_agegrp = EGD_rslt_05_agegrp.sort_index()
EGD_rslt_05_agegrp.columns = pd.MultiIndex.from_tuples(
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

# labels = EGD_rslt_05_per_m.columns[:-1].to_list()

# EGD_rslt_05_agegrp
# %%
EGD_rslt_05_cnt_t = data.pivot_table(
                             index=[rslt_05]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
EGD_rslt_05_per_t = round(EGD_rslt_05_cnt_t.div(EGD_rslt_05_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# EGD_rslt_05_per_t

EGD_rslt_05_agegrp_t = pd.DataFrame()

for i in range(len(EGD_rslt_05_cnt_t.columns)):
    if i == 0:
        EGD_rslt_05_agegrp_t = pd.concat(
                                [
                                 EGD_rslt_05_cnt_t.iloc[:,i]
                                ,EGD_rslt_05_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_05_agegrp_t = pd.concat(
                                [
                                 EGD_rslt_05_agegrp_t
                                ,EGD_rslt_05_cnt_t.iloc[:,i]
                                ,EGD_rslt_05_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

EGD_rslt_05_agegrp_t.columns = pd.MultiIndex.from_tuples(
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

# EGD_rslt_05_agegrp_t
# %%
EGD_rslt_05_cnt_subt = data.pivot_table(
                             index=[rslt_05]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# EGD_rslt_05_per_t = round(EGD_rslt_05_cnt_t.div(EGD_rslt_05_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
EGD_rslt_05_per_subt = round(EGD_rslt_05_cnt_subt.div(EGD_rslt_05_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# EGD_rslt_05_per_subt

EGD_rslt_05_agegrp_subt = pd.DataFrame()

for i in range(len(EGD_rslt_05_cnt_subt.columns)):
    if i == 0:
        EGD_rslt_05_agegrp_subt = pd.concat(
                                [
                                 EGD_rslt_05_cnt_subt.iloc[:,i]
                                ,EGD_rslt_05_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        EGD_rslt_05_agegrp_subt = pd.concat(
                                [
                                 EGD_rslt_05_agegrp_subt
                                ,EGD_rslt_05_cnt_subt.iloc[:,i]
                                ,EGD_rslt_05_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

EGD_rslt_05_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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

# EGD_rslt_05_agegrp_subt
#%%
# axis=0으로 concat시 원하는 format이 안 됨. 그래서 matrix를 Transposed 함.
EGD_rslt_per_subt = pd.concat(
                               [
                                EGD_rslt_01_per_subt.iloc[1,:]
                               ,EGD_rslt_02_per_subt.iloc[1,:]
                               ,EGD_rslt_03_per_subt.iloc[1,:]
                               ,EGD_rslt_04_per_subt.iloc[1,:]
                               ,EGD_rslt_05_per_subt.iloc[1,:]
                               ,EGD_rslt_05_per_subt.iloc[-1,:]
                               ]
                              ,axis=1
                              ).T

# EGD_rslt_per_subt

EGD_rslt_agegrp_subt = pd.concat(
                               [
                                EGD_rslt_01_agegrp_subt.iloc[1,:]
                               ,EGD_rslt_02_agegrp_subt.iloc[1,:]
                               ,EGD_rslt_03_agegrp_subt.iloc[1,:]
                               ,EGD_rslt_04_agegrp_subt.iloc[1,:]
                               ,EGD_rslt_05_agegrp_subt.iloc[1,:]
                               ,EGD_rslt_05_agegrp_subt.iloc[-1,:]
                               ]
                              ,axis=1
                              ).T

# EGD_rslt_agegrp_subt

#%%
value02 = EGD_rslt_per_subt.iloc[0,:-1].to_list()
value03 = EGD_rslt_per_subt.iloc[1,:-1].to_list()
value04 = EGD_rslt_per_subt.iloc[2,:-1].to_list()
value05 = EGD_rslt_per_subt.iloc[3,:-1].to_list()
value06 = EGD_rslt_per_subt.iloc[4,:-1].to_list()

label02 = rslt_01
label03 = rslt_02
label04 = rslt_03
label05 = rslt_04
label06 = rslt_05
rslttext = [rslt_01, rslt_02, rslt_03, rslt_04, rslt_05]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.15  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# rects1 = ax.bar(x - width-0.17 , value01, width, label=label1,color='lightslategray') RdYlBu
rects2 = ax.bar(x - width-0.2 , value02, width, label=label02, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[4])
rects3 = ax.bar(x - width-0.03, value03, width, label=label03, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[3])
rects4 = ax.bar(x             , value04, width, label=label04, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[2])
rects5 = ax.bar(x + width+0.03, value05, width, label=label05, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[1])
rects6 = ax.bar(x + width+0.2 , value06, width, label=label06, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[0])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 상부위장관 내시경 결과 분포(2020년)\n\n',fontsize=30)
ax.set_ylabel(
                '(단위: %)' # 표시값
                 ,labelpad=-70 # 여백값 설정
                ,fontsize=20 # 글씨크기 설정
                ,rotation=0 # 회전값 조정
#                 ,ha='center' # 위치조정
                ,loc='top' # 위치조정, ha와 동시에 사용은 불가함.
            )
ax.yaxis.set_tick_params(labelsize=15) # y축 표시값 글씨크기 조정
ax.set_xticks(x)
ax.set_xticklabels(
                   labels[0:len(labels)] # all 값이 list에는 포함되지 않았기 때문임.
                  , fontsize=17
                  )

# bar위에 값 label 표시
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(height, # 천단위마다 콤마 표시
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 8),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom'
                   ,fontsize=18
                   )


autolabel(rects2)
autolabel(rects3)
autolabel(rects4)
autolabel(rects5)
autolabel(rects6)
# autolabel(rects3)

plt.text(-0.5, -0.1,  '상부위장관 내시경 결과 분류 기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(0.03,-0.21)
          ,ncol=3
          ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -0.25, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_11_01상부위장관내시경.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
            )

# plt.show()

#%%
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # cact_agegrp_t.to_excel(writer,sheet_name="03_01이상지질혈증유병율")
    # liquiprep_agegrp_subt.to_excel(writer,sheet_name="03_09_1액상자궁세포")
    EGD_rslt_agegrp_subt.to_excel(writer,sheet_name="03_11_1EGDBP")
# %%
labels
# %%
