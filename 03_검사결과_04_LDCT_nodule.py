# %%
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
data = pd.read_stata('{}/RSLT_CD_EXMN_최종.dta'.format(workdir))
data.drop(data.loc[:,'RSLT_CD14':], axis=1, inplace=True)

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
# %%
# LDCT 검사만 대상
exmn_cd = 'RC1241'
data = data.drop(data.loc[data['EXMN_CD']!=exmn_cd].index)
# data
# %%
GRP1 = "01_폐 결절(pulmonary nodule)"
GRP2 = "02_폐 종괴(pulmonary mass)"
GRP3 = "03_불투명 혼탁 음영(ground-glass opacity)"
GRP4 = "04_폐암(lung cancer)의심"
rsltcd01 = '1033'
rsltcd02 = '1049'
rsltcd03 = "1043"
rsltcd04 = "1016"
rsltcd05 = "1050"
data['{}_01'.format(exmn_cd)] = ((data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd01) | (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd02)).any(axis=1).astype(int)
data['{}_02'.format(exmn_cd)] = ((data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd03)                                                    ).any(axis=1).astype(int)
data['{}_03'.format(exmn_cd)] = ((data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd04)                                                    ).any(axis=1).astype(int)
data['{}_04'.format(exmn_cd)] = ((data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd05)                                                    ).any(axis=1).astype(int)
data.loc[data['{}_01'.format(exmn_cd)] == 1,"GRP1"] = GRP1
data.loc[data['{}_02'.format(exmn_cd)] == 1,"GRP2"] = GRP2
data.loc[data['{}_03'.format(exmn_cd)] == 1,"GRP3"] = GRP3
data.loc[data['{}_04'.format(exmn_cd)] == 1,"GRP4"] = GRP4
data["GRP1"].fillna('정상',inplace=True)
data["GRP2"].fillna('정상',inplace=True)
data["GRP3"].fillna('정상',inplace=True)
data["GRP4"].fillna('정상',inplace=True)
# data
#%%
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

# %%
RC1241_GRP1_cnt_m = data_m.pivot_table(
                             index=['GRP1','GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP1_cnt_m.columns = RC1241_GRP1_cnt_m.columns.droplevel()
# RC1241_GRP1_cnt_m
# each column total value percentile
RC1241_GRP1_per_m = round(RC1241_GRP1_cnt_m.div(RC1241_GRP1_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_GRP1_per_m
RC1241_GRP1_agegrp_m = pd.DataFrame()

for i in range(len(RC1241_GRP1_cnt_m.columns)):
    if i == 0:
        RC1241_GRP1_agegrp_m = pd.concat(
                                [
                                 RC1241_GRP1_cnt_m.iloc[:,i]
                                ,RC1241_GRP1_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP1_agegrp_m = pd.concat(
                                [
                                 RC1241_GRP1_agegrp_m
                                ,RC1241_GRP1_cnt_m.iloc[:,i]
                                ,RC1241_GRP1_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
RC1241_GRP1_agegrp_m
# # %%
RC1241_GRP1_cnt_f = data_f.pivot_table(
                             index=['GRP1','GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP1_cnt_f.columns = RC1241_GRP1_cnt_f.columns.droplevel()
# RC1241_GRP1_cnt_m
# each column total value percentile
RC1241_GRP1_per_f = round(RC1241_GRP1_cnt_f.div(RC1241_GRP1_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_GRP1_per_m
RC1241_GRP1_agegrp_f = pd.DataFrame()

for i in range(len(RC1241_GRP1_cnt_f.columns)):
    if i == 0:
        RC1241_GRP1_agegrp_f = pd.concat(
                                [
                                 RC1241_GRP1_cnt_f.iloc[:,i]
                                ,RC1241_GRP1_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP1_agegrp_f = pd.concat(
                                [
                                 RC1241_GRP1_agegrp_f
                                ,RC1241_GRP1_cnt_f.iloc[:,i]
                                ,RC1241_GRP1_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
RC1241_GRP1_agegrp_f

# # %%
RC1241_GRP1_agegrp = pd.concat([RC1241_GRP1_agegrp_m.iloc[:-1,:], RC1241_GRP1_agegrp_f.iloc[:-1,:]],axis=0)
RC1241_GRP1_agegrp = RC1241_GRP1_agegrp.sort_index()
RC1241_GRP1_agegrp.columns = pd.MultiIndex.from_tuples(
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

labels = RC1241_GRP1_cnt_m.columns[:-1].to_list()

RC1241_GRP1_agegrp

# labels
# # %%
RC1241_GRP1_cnt_t = data.pivot_table(
                             index=['GRP1']#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP1_cnt_t.columns = RC1241_GRP1_cnt_t.columns.droplevel()
# total value percentile
RC1241_GRP1_per_t = round(RC1241_GRP1_cnt_t.div(RC1241_GRP1_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# RC1241_per_t

RC1241_GRP1_agegrp_t = pd.DataFrame()

for i in range(len(RC1241_GRP1_cnt_t.columns)):
    if i == 0:
        RC1241_GRP1_agegrp_t = pd.concat(
                                [
                                 RC1241_GRP1_cnt_t.iloc[:,i]
                                ,RC1241_GRP1_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP1_agegrp_t = pd.concat(
                                [
                                 RC1241_GRP1_agegrp_t
                                ,RC1241_GRP1_cnt_t.iloc[:,i]
                                ,RC1241_GRP1_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
RC1241_GRP1_agegrp_t.columns = pd.MultiIndex.from_tuples(
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
RC1241_GRP1_agegrp_t
# # %%
RC1241_GRP1_cnt_subt = data.pivot_table(
                             index=['GRP1']#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# RC1241_per_t = round(RC1241_cnt_t.div(RC1241_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
RC1241_GRP1_per_subt = round(RC1241_GRP1_cnt_subt.div(RC1241_GRP1_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_per_subt

RC1241_GRP1_agegrp_subt = pd.DataFrame()

for i in range(len(RC1241_GRP1_cnt_subt.columns)):
    if i == 0:
        RC1241_GRP1_agegrp_subt = pd.concat(
                                [
                                 RC1241_GRP1_cnt_subt.iloc[:,i]
                                ,RC1241_GRP1_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP1_agegrp_subt = pd.concat(
                                [
                                 RC1241_GRP1_agegrp_subt
                                ,RC1241_GRP1_cnt_subt.iloc[:,i]
                                ,RC1241_GRP1_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
RC1241_GRP1_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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
# RC1241_GRP1_agegrp_subt

#%%
RC1241_GRP2_cnt_m = data_m.pivot_table(
                             index=['GRP2','GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP2_cnt_m.columns = RC1241_GRP2_cnt_m.columns.droplevel()
# RC1241_GRP2_cnt_m
# each column total value percentile
RC1241_GRP2_per_m = round(RC1241_GRP2_cnt_m.div(RC1241_GRP2_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_GRP2_per_m
RC1241_GRP2_agegrp_m = pd.DataFrame()

for i in range(len(RC1241_GRP2_cnt_m.columns)):
    if i == 0:
        RC1241_GRP2_agegrp_m = pd.concat(
                                [
                                 RC1241_GRP2_cnt_m.iloc[:,i]
                                ,RC1241_GRP2_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP2_agegrp_m = pd.concat(
                                [
                                 RC1241_GRP2_agegrp_m
                                ,RC1241_GRP2_cnt_m.iloc[:,i]
                                ,RC1241_GRP2_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
RC1241_GRP2_agegrp_m

RC1241_GRP2_cnt_f = data_f.pivot_table(
                             index=['GRP2','GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP2_cnt_f.columns = RC1241_GRP2_cnt_f.columns.droplevel()
# RC1241_GRP2_cnt_m
# each column total value percentile
RC1241_GRP2_per_f = round(RC1241_GRP2_cnt_f.div(RC1241_GRP2_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_GRP2_per_m
RC1241_GRP2_agegrp_f = pd.DataFrame()

for i in range(len(RC1241_GRP2_cnt_f.columns)):
    if i == 0:
        RC1241_GRP2_agegrp_f = pd.concat(
                                [
                                 RC1241_GRP2_cnt_f.iloc[:,i]
                                ,RC1241_GRP2_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP2_agegrp_f = pd.concat(
                                [
                                 RC1241_GRP2_agegrp_f
                                ,RC1241_GRP2_cnt_f.iloc[:,i]
                                ,RC1241_GRP2_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
RC1241_GRP2_agegrp_f


RC1241_GRP2_agegrp = pd.concat([RC1241_GRP2_agegrp_m.iloc[:-1,:], RC1241_GRP2_agegrp_f.iloc[:-1,:]],axis=0)
RC1241_GRP2_agegrp = RC1241_GRP2_agegrp.sort_index()
RC1241_GRP2_agegrp.columns = pd.MultiIndex.from_tuples(
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

labels = RC1241_GRP2_cnt_m.columns[:-1].to_list()

RC1241_GRP2_agegrp

# labels

RC1241_GRP2_cnt_t = data.pivot_table(
                             index=['GRP2']#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP2_cnt_t.columns = RC1241_GRP2_cnt_t.columns.droplevel()
# total value percentile
RC1241_GRP2_per_t = round(RC1241_GRP2_cnt_t.div(RC1241_GRP2_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# RC1241_per_t

RC1241_GRP2_agegrp_t = pd.DataFrame()

for i in range(len(RC1241_GRP2_cnt_t.columns)):
    if i == 0:
        RC1241_GRP2_agegrp_t = pd.concat(
                                [
                                 RC1241_GRP2_cnt_t.iloc[:,i]
                                ,RC1241_GRP2_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP2_agegrp_t = pd.concat(
                                [
                                 RC1241_GRP2_agegrp_t
                                ,RC1241_GRP2_cnt_t.iloc[:,i]
                                ,RC1241_GRP2_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
RC1241_GRP2_agegrp_t.columns = pd.MultiIndex.from_tuples(
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
RC1241_GRP2_agegrp_t

RC1241_GRP2_cnt_subt = data.pivot_table(
                             index=['GRP2']#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# RC1241_per_t = round(RC1241_cnt_t.div(RC1241_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
RC1241_GRP2_per_subt = round(RC1241_GRP2_cnt_subt.div(RC1241_GRP2_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_per_subt

RC1241_GRP2_agegrp_subt = pd.DataFrame()

for i in range(len(RC1241_GRP2_cnt_subt.columns)):
    if i == 0:
        RC1241_GRP2_agegrp_subt = pd.concat(
                                [
                                 RC1241_GRP2_cnt_subt.iloc[:,i]
                                ,RC1241_GRP2_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP2_agegrp_subt = pd.concat(
                                [
                                 RC1241_GRP2_agegrp_subt
                                ,RC1241_GRP2_cnt_subt.iloc[:,i]
                                ,RC1241_GRP2_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
RC1241_GRP2_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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
# RC1241_GRP2_agegrp_subt

#%%
RC1241_GRP3_cnt_m = data_m.pivot_table(
                             index=['GRP3','GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP3_cnt_m.columns = RC1241_GRP3_cnt_m.columns.droplevel()
# RC1241_GRP3_cnt_m
# each column total value percentile
RC1241_GRP3_per_m = round(RC1241_GRP3_cnt_m.div(RC1241_GRP3_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_GRP3_per_m
RC1241_GRP3_agegrp_m = pd.DataFrame()

for i in range(len(RC1241_GRP3_cnt_m.columns)):
    if i == 0:
        RC1241_GRP3_agegrp_m = pd.concat(
                                [
                                 RC1241_GRP3_cnt_m.iloc[:,i]
                                ,RC1241_GRP3_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP3_agegrp_m = pd.concat(
                                [
                                 RC1241_GRP3_agegrp_m
                                ,RC1241_GRP3_cnt_m.iloc[:,i]
                                ,RC1241_GRP3_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
RC1241_GRP3_agegrp_m

RC1241_GRP3_cnt_f = data_f.pivot_table(
                             index=['GRP3','GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP3_cnt_f.columns = RC1241_GRP3_cnt_f.columns.droplevel()
# RC1241_GRP3_cnt_m
# each column total value percentile
RC1241_GRP3_per_f = round(RC1241_GRP3_cnt_f.div(RC1241_GRP3_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_GRP3_per_m
RC1241_GRP3_agegrp_f = pd.DataFrame()

for i in range(len(RC1241_GRP3_cnt_f.columns)):
    if i == 0:
        RC1241_GRP3_agegrp_f = pd.concat(
                                [
                                 RC1241_GRP3_cnt_f.iloc[:,i]
                                ,RC1241_GRP3_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP3_agegrp_f = pd.concat(
                                [
                                 RC1241_GRP3_agegrp_f
                                ,RC1241_GRP3_cnt_f.iloc[:,i]
                                ,RC1241_GRP3_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
RC1241_GRP3_agegrp_f


RC1241_GRP3_agegrp = pd.concat([RC1241_GRP3_agegrp_m.iloc[:-1,:], RC1241_GRP3_agegrp_f.iloc[:-1,:]],axis=0)
RC1241_GRP3_agegrp = RC1241_GRP3_agegrp.sort_index()
RC1241_GRP3_agegrp.columns = pd.MultiIndex.from_tuples(
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

labels = RC1241_GRP3_cnt_m.columns[:-1].to_list()

RC1241_GRP3_agegrp

# labels

RC1241_GRP3_cnt_t = data.pivot_table(
                             index=['GRP3']#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP3_cnt_t.columns = RC1241_GRP3_cnt_t.columns.droplevel()
# total value percentile
RC1241_GRP3_per_t = round(RC1241_GRP3_cnt_t.div(RC1241_GRP3_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# RC1241_per_t

RC1241_GRP3_agegrp_t = pd.DataFrame()

for i in range(len(RC1241_GRP3_cnt_t.columns)):
    if i == 0:
        RC1241_GRP3_agegrp_t = pd.concat(
                                [
                                 RC1241_GRP3_cnt_t.iloc[:,i]
                                ,RC1241_GRP3_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP3_agegrp_t = pd.concat(
                                [
                                 RC1241_GRP3_agegrp_t
                                ,RC1241_GRP3_cnt_t.iloc[:,i]
                                ,RC1241_GRP3_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
RC1241_GRP3_agegrp_t.columns = pd.MultiIndex.from_tuples(
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
RC1241_GRP3_agegrp_t

RC1241_GRP3_cnt_subt = data.pivot_table(
                             index=['GRP3']#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# RC1241_per_t = round(RC1241_cnt_t.div(RC1241_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
RC1241_GRP3_per_subt = round(RC1241_GRP3_cnt_subt.div(RC1241_GRP3_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_per_subt

RC1241_GRP3_agegrp_subt = pd.DataFrame()

for i in range(len(RC1241_GRP3_cnt_subt.columns)):
    if i == 0:
        RC1241_GRP3_agegrp_subt = pd.concat(
                                [
                                 RC1241_GRP3_cnt_subt.iloc[:,i]
                                ,RC1241_GRP3_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP3_agegrp_subt = pd.concat(
                                [
                                 RC1241_GRP3_agegrp_subt
                                ,RC1241_GRP3_cnt_subt.iloc[:,i]
                                ,RC1241_GRP3_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
RC1241_GRP3_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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
# RC1241_GRP3_agegrp_subt

# %%
RC1241_GRP4_cnt_m = data_m.pivot_table(
                             index=['GRP4','GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP4_cnt_m.columns = RC1241_GRP4_cnt_m.columns.droplevel()
# RC1241_GRP4_cnt_m
# each column total value percentile
RC1241_GRP4_per_m = round(RC1241_GRP4_cnt_m.div(RC1241_GRP4_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_GRP4_per_m
RC1241_GRP4_agegrp_m = pd.DataFrame()

for i in range(len(RC1241_GRP4_cnt_m.columns)):
    if i == 0:
        RC1241_GRP4_agegrp_m = pd.concat(
                                [
                                 RC1241_GRP4_cnt_m.iloc[:,i]
                                ,RC1241_GRP4_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP4_agegrp_m = pd.concat(
                                [
                                 RC1241_GRP4_agegrp_m
                                ,RC1241_GRP4_cnt_m.iloc[:,i]
                                ,RC1241_GRP4_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
RC1241_GRP4_agegrp_m

RC1241_GRP4_cnt_f = data_f.pivot_table(
                             index=['GRP4','GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP4_cnt_f.columns = RC1241_GRP4_cnt_f.columns.droplevel()
# RC1241_GRP4_cnt_m
# each column total value percentile
RC1241_GRP4_per_f = round(RC1241_GRP4_cnt_f.div(RC1241_GRP4_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_GRP4_per_m
RC1241_GRP4_agegrp_f = pd.DataFrame()

for i in range(len(RC1241_GRP4_cnt_f.columns)):
    if i == 0:
        RC1241_GRP4_agegrp_f = pd.concat(
                                [
                                 RC1241_GRP4_cnt_f.iloc[:,i]
                                ,RC1241_GRP4_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP4_agegrp_f = pd.concat(
                                [
                                 RC1241_GRP4_agegrp_f
                                ,RC1241_GRP4_cnt_f.iloc[:,i]
                                ,RC1241_GRP4_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
RC1241_GRP4_agegrp_f


RC1241_GRP4_agegrp = pd.concat([RC1241_GRP4_agegrp_m.iloc[:-1,:], RC1241_GRP4_agegrp_f.iloc[:-1,:]],axis=0)
RC1241_GRP4_agegrp = RC1241_GRP4_agegrp.sort_index()
RC1241_GRP4_agegrp.columns = pd.MultiIndex.from_tuples(
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

labels = RC1241_GRP4_cnt_m.columns[:-1].to_list()

RC1241_GRP4_agegrp

# labels

RC1241_GRP4_cnt_t = data.pivot_table(
                             index=['GRP4']#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_GRP4_cnt_t.columns = RC1241_GRP4_cnt_t.columns.droplevel()
# total value percentile
RC1241_GRP4_per_t = round(RC1241_GRP4_cnt_t.div(RC1241_GRP4_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# RC1241_per_t

RC1241_GRP4_agegrp_t = pd.DataFrame()

for i in range(len(RC1241_GRP4_cnt_t.columns)):
    if i == 0:
        RC1241_GRP4_agegrp_t = pd.concat(
                                [
                                 RC1241_GRP4_cnt_t.iloc[:,i]
                                ,RC1241_GRP4_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP4_agegrp_t = pd.concat(
                                [
                                 RC1241_GRP4_agegrp_t
                                ,RC1241_GRP4_cnt_t.iloc[:,i]
                                ,RC1241_GRP4_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
RC1241_GRP4_agegrp_t.columns = pd.MultiIndex.from_tuples(
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
RC1241_GRP4_agegrp_t

RC1241_GRP4_cnt_subt = data.pivot_table(
                             index=['GRP4']#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# RC1241_per_t = round(RC1241_cnt_t.div(RC1241_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
RC1241_GRP4_per_subt = round(RC1241_GRP4_cnt_subt.div(RC1241_GRP4_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_per_subt

RC1241_GRP4_agegrp_subt = pd.DataFrame()

for i in range(len(RC1241_GRP4_cnt_subt.columns)):
    if i == 0:
        RC1241_GRP4_agegrp_subt = pd.concat(
                                [
                                 RC1241_GRP4_cnt_subt.iloc[:,i]
                                ,RC1241_GRP4_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_GRP4_agegrp_subt = pd.concat(
                                [
                                 RC1241_GRP4_agegrp_subt
                                ,RC1241_GRP4_cnt_subt.iloc[:,i]
                                ,RC1241_GRP4_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
RC1241_GRP4_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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
# RC1241_GRP4_agegrp_subt

# %%
# axis=0으로 concat시 원하는 format이 안 됨. 그래서 matrix를 Transposed 함.
RC1241_per_subt = pd.concat(
                            [
                             RC1241_GRP1_per_subt.iloc[0,:]
                            ,RC1241_GRP2_per_subt.iloc[0,:]
                            ,RC1241_GRP3_per_subt.iloc[0,:]
                            ,RC1241_GRP4_per_subt.iloc[0,:]
                            ,RC1241_GRP4_per_subt.iloc[-1,:]
                            ]
                           ,axis=1
                           ).T

# axis=0으로 concat시 원하는 format이 안 됨. 그래서 matrix를 Transposed 함.
RC1241_agegrp_subt = pd.concat(
                               [
                                RC1241_GRP1_agegrp_subt.iloc[0,:]
                               ,RC1241_GRP2_agegrp_subt.iloc[0,:]
                               ,RC1241_GRP3_agegrp_subt.iloc[0,:]
                               ,RC1241_GRP4_agegrp_subt.iloc[0,:]
                               ,RC1241_GRP4_agegrp_subt.iloc[-1,:]
                               ]
                              ,axis=1
                              ).T

RC1241_per_m = pd.concat(
                         [
                          RC1241_GRP1_per_m.iloc[0,:]
                         ,RC1241_GRP2_per_m.iloc[0,:]
                         ,RC1241_GRP3_per_m.iloc[0,:]
                         ,RC1241_GRP4_per_m.iloc[0,:]
                         ]
                        ,axis=1 
                        ).T

RC1241_per_f = pd.concat(
                         [
                          RC1241_GRP1_per_f.iloc[0,:]
                         ,RC1241_GRP2_per_f.iloc[0,:]
                         ,RC1241_GRP3_per_f.iloc[0,:]
                         ,RC1241_GRP4_per_f.iloc[0,:]
                         ]
                        ,axis=1 
                        ).T

RC1241_agegrp_m = pd.concat(
                         [
                          RC1241_GRP1_agegrp_m.iloc[0,:]
                         ,RC1241_GRP2_agegrp_m.iloc[0,:]
                         ,RC1241_GRP3_agegrp_m.iloc[0,:]
                         ,RC1241_GRP4_agegrp_m.iloc[0,:]
                         ,RC1241_GRP4_agegrp_m.iloc[-1,:]
                         ]
                        ,axis=1 
                        ).T

RC1241_agegrp_m.columns = pd.MultiIndex.from_tuples(
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

RC1241_agegrp_f = pd.concat(
                         [
                          RC1241_GRP1_agegrp_f.iloc[0,:]
                         ,RC1241_GRP2_agegrp_f.iloc[0,:]
                         ,RC1241_GRP3_agegrp_f.iloc[0,:]
                         ,RC1241_GRP4_agegrp_f.iloc[0,:]
                         ,RC1241_GRP4_agegrp_f.iloc[-1,:]
                         ]
                        ,axis=1 
                        ).T

RC1241_agegrp_f.columns = pd.MultiIndex.from_tuples(
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

RC1241_agegrp = pd.concat(
                         [
                          RC1241_GRP1_agegrp.iloc[0:2,:]
                         ,RC1241_GRP2_agegrp.iloc[0:2,:]
                         ,RC1241_GRP3_agegrp.iloc[0:2,:]
                         ,RC1241_GRP4_agegrp.iloc[0:2,:]
                        #  ,RC1241_GRP1_agegrp_m.iloc[-1,:]
                        #  ,RC1241_GRP1_agegrp_f.iloc[-1,:]
                        #  ,RC1241_GRP_agegrp.iloc[-1,:]
                         ]
                        ,axis=0
                        )

#%%
# RC1241_per_subt # chart 용
# RC1241_agegrp_subt # excel table 용
# RC1241_per_m # chart 용
# RC1241_per_f # chart 용
# RC1241_agegrp_m # excel table 용
# RC1241_agegrp_f # excel table 용
# RC1241_agegrp # excel table 용

# %%
value01 = RC1241_per_subt.iloc[0,:-1]
value02 = RC1241_per_subt.iloc[1,:-1]
value03 = RC1241_per_subt.iloc[2,:-1]
value04 = RC1241_per_subt.iloc[3,:-1]

label1 = RC1241_per_subt.index[0][3:]
label2 = RC1241_per_subt.index[1][3:]
label3 = RC1241_per_subt.index[2][3:]
label4 = RC1241_per_subt.index[3][3:]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.22  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# rects1 = ax.bar(x - width-0.17 , value01, width, label=label1,color='lightslategray') RdYlBu
rects1 = ax.bar(x - width-0.15, value01, width, label=label1, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[4])
rects2 = ax.bar(x - width+0.1 , value02, width, label=label2, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[5])
rects3 = ax.bar(x + width-0.1 , value03, width, label=label3, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects4 = ax.bar(x + width+0.15, value04, width, label=label4, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 저선량 폐CT 결과 분포(2020년)\n\n',fontsize=30)
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

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)
# autolabel(rects3)

plt.text(-0.7, -10,  '저선량 폐CT 결과분류:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.205)
          ,ncol=2  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -26, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_04_LDCT_01유병률.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
            )

plt.show()

# %%
# %%
value01 = RC1241_per_m.iloc[0,:-1]
value02 = RC1241_per_m.iloc[1,:-1]
value03 = RC1241_per_m.iloc[2,:-1]
value04 = RC1241_per_m.iloc[3,:-1]

label1 = RC1241_per_subt.index[0][3:]
label2 = RC1241_per_subt.index[1][3:]
label3 = RC1241_per_subt.index[2][3:]
label4 = RC1241_per_subt.index[3][3:]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.22  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# rects1 = ax.bar(x - width-0.17 , value01, width, label=label1,color='lightslategray') RdYlBu
rects1 = ax.bar(x - width-0.15, value01, width, label=label1, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[4])
rects2 = ax.bar(x - width+0.1 , value02, width, label=label2, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[5])
rects3 = ax.bar(x + width-0.1 , value03, width, label=label3, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects4 = ax.bar(x + width+0.15, value04, width, label=label4, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 저선량 폐CT 결과 분포(2020년, 남자)\n\n',fontsize=30)
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

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)
# autolabel(rects3)

plt.text(-0.7, -10,  '저선량 폐CT 결과분류:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.205)
          ,ncol=2  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -26, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_04_LDCT_02남자유병률.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
            )

plt.show()

# %%
value01 = RC1241_per_f.iloc[0,:-1]
value02 = RC1241_per_f.iloc[1,:-1]
value03 = RC1241_per_f.iloc[2,:-1]
value04 = RC1241_per_f.iloc[3,:-1]

label1 = RC1241_per_subt.index[0][3:]
label2 = RC1241_per_subt.index[1][3:]
label3 = RC1241_per_subt.index[2][3:]
label4 = RC1241_per_subt.index[3][3:]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.22  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# rects1 = ax.bar(x - width-0.17 , value01, width, label=label1,color='lightslategray') RdYlBu
rects1 = ax.bar(x - width-0.15, value01, width, label=label1, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[4])
rects2 = ax.bar(x - width+0.1 , value02, width, label=label2, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[5])
rects3 = ax.bar(x + width-0.1 , value03, width, label=label3, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects4 = ax.bar(x + width+0.15, value04, width, label=label4, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 저선량 폐CT 결과 분포(2020년, 여자)\n\n',fontsize=30)
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

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)
# autolabel(rects3)

plt.text(-0.7, -10,  '저선량 폐CT 결과분류:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.205)
          ,ncol=2  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -26, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_04_LDCT_03여자유병률.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
            )

plt.show()

# %%
# data merge, export
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # cact_agegrp_t.to_excel(writer,sheet_name="03_01이상지질혈증유병율")
    RC1241_agegrp_subt.to_excel(writer,sheet_name="03_04LDCT")
    RC1241_agegrp.to_excel(writer,sheet_name="03_04LDCT_GENDER")
    # RC1241_agegrp_m.to_excel(writer,sheet_name="03_04LDCT_M")
    # RC1241_agegrp_f.to_excel(writer,sheet_name="03_04LDCT_F")

# %%
