#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.patches import ConnectionPatch
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

#%%
#복부 CT/MRI에서의 CYST, MASS
# 다른 검사 제외
data_01 = data[
            ((data['EXMN_CD'].str.contains('RC')) & 
            (data['EXMN_CD']!='RC1241')) |
            (data['EXMN_CD'].str.contains('RM'))
           ]
# data = data.drop(data[(data['EXMN_CD']!='BP1A151') | (data['EXMN_CD']!=exmn_cd2)].index)
# data_abdcm

# 검사 코드는 변동 가능성이 있으므로 해당 검사코드 기준으로 pivot_table 생성
tt=data_01.pivot_table(index=['EXMN_CD'],values=['ID'],aggfunc='count',fill_value=0)
# tt.index[0]
#%%
# 생성된 pivot_table 기준으로 index에 해당 되는 검사코드 사용
# 각 검사별로 dataframe 생성 후 생성된 dataframe에서 결과값 표시
for exmn_cd in tt.index:
    globals()['data_{}'.format(exmn_cd)] = data_01[(data_01['EXMN_CD']==exmn_cd)]
    if exmn_cd == 'RC2020':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (# 해당 검사에 CYST 결과에 대한 결과코드가 없음.
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == 'YYYYYY'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RC2030':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (# 해당 검사에 CYST 결과에 대한 결과코드가 없음.
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == 'YYYYYY'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RC20301':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1058'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RC2050':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1080'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RC2060':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (# 해당 검사에 CYST 결과에 대한 결과코드가 없음.
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == 'YYYYYY'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RC31202':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1054'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RM2020':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '0006'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '5001'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '5005'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RM2040':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1055'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RM2040N':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1055'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RM2041C':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1055'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RM2075':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1054'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    else:
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')] = 0
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')] = 0
                  
#%%
data_abdcm = pd.DataFrame()

for exmn_cd in tt.index:
    data_abdcm = pd.concat([
                     data_abdcm
                    ,globals()['data_{}'.format(exmn_cd)]
                    ]
        ,axis = 0
    )
    
data_abdcm

# #%%
# data.to_excel('{}/ABD_PCM.xlsx'.format(workdir[:-5]),index=False)
# %%
GRP1 = "01_Pancreatic_Cyst"
data_abdcm.loc[data_abdcm['{}_YN'.format('PAN_CYST')] == 1,GRP1] = GRP1
data_abdcm[GRP1].fillna('02_Absent',inplace=True)
GRP2 = "01_Pancreatic_Mass"
data_abdcm.loc[data_abdcm['{}_YN'.format('PAN_MASS')] == 1,GRP2] = GRP2
data_abdcm[GRP2].fillna('02_Absent',inplace=True)
data_abdcm

#%%
data_abdcm_m = data_abdcm.drop(data_abdcm.loc[data_abdcm['GEND_CD']=='F'].index)
data_abdcm_f = data_abdcm.drop(data_abdcm.loc[data_abdcm['GEND_CD']=='M'].index)

#%%
ABD_P_CYST_cnt_m = data_abdcm_m.pivot_table(
                                    index=[GRP1,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# ABD_P_CYST_cnt_m
# multi level column to single level
ABD_P_CYST_cnt_m.columns = ABD_P_CYST_cnt_m.columns.droplevel()
# each column total value percentile
ABD_P_CYST_per_m = round(ABD_P_CYST_cnt_m.div(ABD_P_CYST_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

ABD_P_CYST_agegrp_m = pd.DataFrame()

for i in range(len(ABD_P_CYST_cnt_m.columns)):
    if i == 0:
        ABD_P_CYST_agegrp_m = pd.concat(
                                [
                                 ABD_P_CYST_cnt_m.iloc[:,i]
                                ,ABD_P_CYST_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_P_CYST_agegrp_m = pd.concat(
                                [
                                 ABD_P_CYST_agegrp_m
                                ,ABD_P_CYST_cnt_m.iloc[:,i]
                                ,ABD_P_CYST_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# ABD_P_CYST_agegrp_m

# %%
ABD_P_CYST_cnt_f = data_abdcm_f.pivot_table(
                                    index=[GRP1,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# ABD_P_CYST_cnt_f
ABD_P_CYST_cnt_f.columns = ABD_P_CYST_cnt_f.columns.droplevel()
# each column total value percentile
ABD_P_CYST_per_f = round(ABD_P_CYST_cnt_f.div(ABD_P_CYST_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# ABD_P_CYST_per_f

ABD_P_CYST_agegrp_f = pd.DataFrame()

for i in range(len(ABD_P_CYST_cnt_f.columns)):
    if i == 0:
        ABD_P_CYST_agegrp_f = pd.concat(
                                [
                                 ABD_P_CYST_cnt_f.iloc[:,i]
                                ,ABD_P_CYST_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_P_CYST_agegrp_f = pd.concat(
                                [
                                 ABD_P_CYST_agegrp_f
                                ,ABD_P_CYST_cnt_f.iloc[:,i]
                                ,ABD_P_CYST_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# ABD_P_CYST_agegrp_f

# %%
# ABD_P_CYST_agegrp = pd.concat([ABD_P_CYST_agegrp_m.iloc[:-1,:], ABD_P_CYST_agegrp_f.iloc[:-1,:]],axis=0)
ABD_P_CYST_agegrp = pd.concat([ABD_P_CYST_agegrp_m, ABD_P_CYST_agegrp_f],axis=0)
ABD_P_CYST_agegrp = ABD_P_CYST_agegrp.sort_index()
ABD_P_CYST_agegrp.columns = pd.MultiIndex.from_tuples(
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

labels = ABD_P_CYST_per_m.columns[:-1].to_list()

# ABD_P_CYST_agegrp
# labels

# %%
ABD_P_CYST_cnt_t = data_abdcm.pivot_table(
                                    index=[GRP1]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

ABD_P_CYST_cnt_t.columns = ABD_P_CYST_cnt_t.columns.droplevel()

# total value percentile
ABD_P_CYST_per_t = round(ABD_P_CYST_cnt_t.div(ABD_P_CYST_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# ABD_P_CYST_per_t

ABD_P_CYST_agegrp_t = pd.DataFrame()

for i in range(len(ABD_P_CYST_cnt_t.columns)):
    if i == 0:
        ABD_P_CYST_agegrp_t = pd.concat(
                                [
                                 ABD_P_CYST_cnt_t.iloc[:,i]
                                ,ABD_P_CYST_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_P_CYST_agegrp_t = pd.concat(
                                [
                                 ABD_P_CYST_agegrp_t
                                ,ABD_P_CYST_cnt_t.iloc[:,i]
                                ,ABD_P_CYST_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
ABD_P_CYST_agegrp_t.columns = pd.MultiIndex.from_tuples(
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

# ABD_P_CYST_agegrp_t

# %%
ABD_P_CYST_cnt_subt = data_abdcm.pivot_table(
                                    index=[GRP1]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

ABD_P_CYST_cnt_subt.columns = ABD_P_CYST_cnt_subt.columns.droplevel()
# total value percentile
# ABD_P_CYST_per_t = round(ABD_P_CYST_cnt_t.div(ABD_P_CYST_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
ABD_P_CYST_per_subt = round(ABD_P_CYST_cnt_subt.div(ABD_P_CYST_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# ABD_P_CYST_per_subt

ABD_P_CYST_agegrp_subt = pd.DataFrame()

for i in range(len(ABD_P_CYST_cnt_subt.columns)):
    if i == 0:
        ABD_P_CYST_agegrp_subt = pd.concat(
                                [
                                 ABD_P_CYST_cnt_subt.iloc[:,i]
                                ,ABD_P_CYST_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_P_CYST_agegrp_subt = pd.concat(
                                [
                                 ABD_P_CYST_agegrp_subt
                                ,ABD_P_CYST_cnt_subt.iloc[:,i]
                                ,ABD_P_CYST_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

ABD_P_CYST_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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

ABD_P_CYST_agegrp_subt


# %%
# 다른 검사 제외
exmn_cd = 'RS10'
data_abdus = data[data['EXMN_CD'].str.contains(exmn_cd)]
data_abdus

#%%
GRP_USNM1 = "01_cyst"
GRP_USNM2 = "01_mass"
GRP_US1 = 'ABDUS_CYST'
GRP_US2 = 'ABDUS_MASS'

rsltcd_GRP1 = ['5004']
rsltcd_GRP2 = ['5001','5005']
# GRP1 = "01_Pancreatic_Cyst"
# data_abdcm.loc[data_abdcm['{}_YN'.format('PAN_CYST')] == 1,GRP1] = GRP1
# data_abdcm[GRP1].fillna('02_Absent',inplace=True)

for i in range(len(rsltcd_GRP1)):
    data_abdus['GRP_US1_{}'.format(i)] = (
        (data_abdus.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd_GRP1[i])
        ).any(axis=1).astype(int)
    data_abdus.loc[data_abdus['GRP_US1_{}'.format(i)] == 1,GRP_US1] = GRP_USNM1
for i in range(len(rsltcd_GRP2)):
    data_abdus['GRP_US2_{}'.format(i)] = (
        (data_abdus.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd_GRP2[i])
        ).any(axis=1).astype(int)
    data_abdus.loc[data_abdus['GRP_US2_{}'.format(i)] == 1,GRP_US2] = GRP_USNM2

data_abdus[GRP_US1].fillna('02_Absent',inplace=True)
data_abdus[GRP_US2].fillna('02_Absent',inplace=True)
# data[GRP2].fillna('00_Absent',inplace=True)
# data.loc[data[GRP1] == "",GRP1] = '08_Absent'
    
data_abdus

#%%
data_abdus_m = data_abdus.drop(data_abdus.loc[data_abdus['GEND_CD']=='F'].index)
data_abdus_f = data_abdus.drop(data_abdus.loc[data_abdus['GEND_CD']=='M'].index)

#%%
ABD_US_CYST_cnt_m = data_abdus_m.pivot_table(
                                    index=[GRP_US1,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# ABD_US_CYST_cnt_m
# multi level column to single level
ABD_US_CYST_cnt_m.columns = ABD_US_CYST_cnt_m.columns.droplevel()
# each column total value percentile
ABD_US_CYST_per_m = round(ABD_US_CYST_cnt_m.div(ABD_US_CYST_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

ABD_US_CYST_agegrp_m = pd.DataFrame()

for i in range(len(ABD_US_CYST_cnt_m.columns)):
    if i == 0:
        ABD_US_CYST_agegrp_m = pd.concat(
                                [
                                 ABD_US_CYST_cnt_m.iloc[:,i]
                                ,ABD_US_CYST_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_US_CYST_agegrp_m = pd.concat(
                                [
                                 ABD_US_CYST_agegrp_m
                                ,ABD_US_CYST_cnt_m.iloc[:,i]
                                ,ABD_US_CYST_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# ABD_US_CYST_agegrp_m

# %%
ABD_US_CYST_cnt_f = data_abdus_f.pivot_table(
                                    index=[GRP_US1,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# ABD_US_CYST_cnt_f
ABD_US_CYST_cnt_f.columns = ABD_US_CYST_cnt_f.columns.droplevel()
# each column total value percentile
ABD_US_CYST_per_f = round(ABD_US_CYST_cnt_f.div(ABD_US_CYST_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# ABD_US_CYST_per_f

ABD_US_CYST_agegrp_f = pd.DataFrame()

for i in range(len(ABD_US_CYST_cnt_f.columns)):
    if i == 0:
        ABD_US_CYST_agegrp_f = pd.concat(
                                [
                                 ABD_US_CYST_cnt_f.iloc[:,i]
                                ,ABD_US_CYST_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_US_CYST_agegrp_f = pd.concat(
                                [
                                 ABD_US_CYST_agegrp_f
                                ,ABD_US_CYST_cnt_f.iloc[:,i]
                                ,ABD_US_CYST_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# ABD_US_CYST_agegrp_f

# %%
# ABD_US_CYST_agegrp = pd.concat([ABD_US_CYST_agegrp_m.iloc[:-1,:], ABD_US_CYST_agegrp_f.iloc[:-1,:]],axis=0)
ABD_US_CYST_agegrp = pd.concat([ABD_US_CYST_agegrp_m, ABD_US_CYST_agegrp_f],axis=0)
ABD_US_CYST_agegrp = ABD_US_CYST_agegrp.sort_index()
ABD_US_CYST_agegrp.columns = pd.MultiIndex.from_tuples(
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

labels = ABD_US_CYST_per_m.columns[:-1].to_list()

# ABD_US_CYST_agegrp
# labels

# %%
ABD_US_CYST_cnt_t = data_abdus.pivot_table(
                                    index=[GRP_US1]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

ABD_US_CYST_cnt_t.columns = ABD_US_CYST_cnt_t.columns.droplevel()

# total value percentile
ABD_US_CYST_per_t = round(ABD_US_CYST_cnt_t.div(ABD_US_CYST_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# ABD_US_CYST_per_t

ABD_US_CYST_agegrp_t = pd.DataFrame()

for i in range(len(ABD_US_CYST_cnt_t.columns)):
    if i == 0:
        ABD_US_CYST_agegrp_t = pd.concat(
                                [
                                 ABD_US_CYST_cnt_t.iloc[:,i]
                                ,ABD_US_CYST_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_US_CYST_agegrp_t = pd.concat(
                                [
                                 ABD_US_CYST_agegrp_t
                                ,ABD_US_CYST_cnt_t.iloc[:,i]
                                ,ABD_US_CYST_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
ABD_US_CYST_agegrp_t.columns = pd.MultiIndex.from_tuples(
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

# ABD_US_CYST_agegrp_t

# %%
ABD_US_CYST_cnt_subt = data_abdus.pivot_table(
                                    index=[GRP_US1]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

ABD_US_CYST_cnt_subt.columns = ABD_US_CYST_cnt_subt.columns.droplevel()
# total value percentile
# ABD_US_CYST_per_t = round(ABD_US_CYST_cnt_t.div(ABD_US_CYST_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
ABD_US_CYST_per_subt = round(ABD_US_CYST_cnt_subt.div(ABD_US_CYST_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# ABD_US_CYST_per_subt

ABD_US_CYST_agegrp_subt = pd.DataFrame()

for i in range(len(ABD_US_CYST_cnt_subt.columns)):
    if i == 0:
        ABD_US_CYST_agegrp_subt = pd.concat(
                                [
                                 ABD_US_CYST_cnt_subt.iloc[:,i]
                                ,ABD_US_CYST_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_US_CYST_agegrp_subt = pd.concat(
                                [
                                 ABD_US_CYST_agegrp_subt
                                ,ABD_US_CYST_cnt_subt.iloc[:,i]
                                ,ABD_US_CYST_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

ABD_US_CYST_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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

# ABD_US_CYST_agegrp_subt



#%%
# ABD_P_CYST_agegrp
# ABD_P_CYST_agegrp_subt
# ABD_P_MASS_agegrp
# ABD_P_MASS_agegrp_subt

ABD_US_CYST_agegrp
# ABD_US_CYST_agegrp_subt
# ABD_US_MASS_agegrp
# ABD_US_MASS_agegrp_subt

#%%
value01 = ABD_P_CYST_per_subt.iloc[0,:-1]
value02 = ABD_US_CYST_per_subt.iloc[0,:-1]

label01 = '복부CT/MRI'
label02 = '복부초음파'

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label=label01,color=plt.get_cmap('PuBuGn')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects2 = ax.bar(x + 0.2, value02, width, label=label02,color=plt.get_cmap('YlGn')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[3])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('검사방법에 따른 췌장낭종 유병률 차이(2020년)\n\n',fontsize=30)
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
ax.legend(fontsize=17)

# bar위에 값 label 표시
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(height, 
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 8),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom'
                   ,fontsize=18
                   )

autolabel(rects1)
autolabel(rects2)

plt.text(-0.3, -8, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_07_01췌장낭종유병률.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )

# %%
ABD_P_CYST_agegrp_subt
# %%
ABD_US_CYST_agegrp_subt
# %%
data
# %%
# 각 검사방법의 CYST 연령별 건수 CONCAT
rslt_CYST_grp_sub = pd.concat(
                     [
                      ABD_P_CYST_agegrp_subt.iloc[0,:-2]
                     ,ABD_US_CYST_agegrp_subt.iloc[0,:-2]
                     ]
                    ,axis=1
                    )

rslt_CYST_grp_sub

#%%
# 각 검사 전체건수 CONCAT
rslt_CYST_grp_t = pd.concat(
                     [
                      ABD_P_CYST_agegrp_subt.iloc[-1,-2:]
                     ,ABD_US_CYST_agegrp_subt.iloc[-1,-2:]
                     ]
                    ,axis=1
                    )

rslt_CYST_grp_t.columns= ['01_Pancreatic_Cyst','01_cyst']

rslt_CYST_grp_t
#%%
# 각 검사방법의 CYST 연령별 건수 + 각 검사 전체건수
rslt_CYST_grp = pd.concat(
    [
     rslt_CYST_grp_sub
    ,rslt_CYST_grp_t
    ]
    ,axis=0
)

rslt_CYST_grp.columns= ['복부CT/MRI','복부초음파']

rslt_CYST_grp = rslt_CYST_grp.T

rslt_CYST_grp


# rslt_MASS_grp
# %%
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # cact_agegrp_t.to_excel(writer,sheet_name="03_01이상지질혈증유병율")
    # liquiprep_agegrp_subt.to_excel(writer,sheet_name="03_09_1액상자궁세포")
    rslt_CYST_grp.to_excel(writer,sheet_name="03_07_1복부검사_CYST")
    # rslt_MASS_grp.to_excel(writer,sheet_name="03_07_1복부검사_MASS")
# %%
