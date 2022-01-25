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
# 다른 검사 제외
data = data[
            ((data['EXMN_CD'].str.contains('RC')) & 
            (data['EXMN_CD']!='RC1241')) |
            (data['EXMN_CD'].str.contains('RM'))
           ]
# data = data.drop(data[(data['EXMN_CD']!='BP1A151') | (data['EXMN_CD']!=exmn_cd2)].index)
# data

# 검사 코드는 변동 가능성이 있으므로 해당 검사코드 기준으로 pivot_table 생성
tt=data.pivot_table(index=['EXMN_CD'],values=['ID'],aggfunc='count',fill_value=0)
# tt.index[0]
#%%
# 생성된 pivot_table 기준으로 index에 해당 되는 검사코드 사용
# 각 검사별로 dataframe 생성 후 생성된 dataframe에서 결과값 표시
for exmn_cd in tt.index:
    globals()['data_{}'.format(exmn_cd)] = data[(data['EXMN_CD']==exmn_cd)]
    if exmn_cd == 'RC2020':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == 'YYYYYY'
                     ).any(axis=1).astype(int)
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_MASS')
                 ] = (
                     globals()['data_{}'.format(exmn_cd)].loc[:,'RSLT_CD01':'RSLT_CD13'] == '1015'
                     ).any(axis=1).astype(int)
    elif exmn_cd == 'RC2030':
        globals()['data_{}'.format(exmn_cd)]['{}_YN'.format('PAN_CYST')
                 ] = (
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
                 ] = (
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

data = pd.DataFrame()

for exmn_cd in tt.index:
    data = pd.concat([
                    data
                    ,globals()['data_{}'.format(exmn_cd)]
                    ]
        ,axis = 0
    )
    
data

# #%%
# data.to_excel('{}/ABD_PCM.xlsx'.format(workdir[:-5]),index=False)
# %%
GRP1 = "01_Pancreatic_Cyst"
data.loc[data['{}_YN'.format('PAN_CYST')] == 1,GRP1] = GRP1
data[GRP1].fillna('02_Absent',inplace=True)
GRP2 = "01_Pancreatic_Mass"
data.loc[data['{}_YN'.format('PAN_MASS')] == 1,GRP2] = GRP2
data[GRP2].fillna('02_Absent',inplace=True)
data

#%%
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

#%%
ABD_P_CYST_cnt_m = data_m.pivot_table(
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
ABD_P_CYST_cnt_f = data_f.pivot_table(
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
ABD_P_CYST_agegrp = pd.concat([ABD_P_CYST_agegrp_m.iloc[:-1,:], ABD_P_CYST_agegrp_f.iloc[:-1,:]],axis=0)
ABD_P_CYST_agegrp = ABD_P_CYST_agegrp.sort_index()
ABD_P_CYST_agegrp

labels = ABD_P_CYST_per_m.columns[:-1].to_list()
# ABD_P_CYST_agegrp
# labels

# %%
ABD_P_CYST_cnt_t = data.pivot_table(
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

# ABD_P_CYST_agegrp_t
# %%
ABD_P_CYST_cnt_subt = data.pivot_table(
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

# ABD_P_CYST_agegrp_subt
    
# %%
# PANCREAS MASS
ABD_P_MASS_cnt_m = data_m.pivot_table(
                                    index=[GRP2,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

ABD_P_MASS_cnt_m.columns = ABD_P_MASS_cnt_m.columns.droplevel()

# ABD_P_MASS_cnt_m
# each column total value percentile
ABD_P_MASS_per_m = round(ABD_P_MASS_cnt_m.div(ABD_P_MASS_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# ABD_P_MASS_per_m

ABD_P_MASS_agegrp_m = pd.DataFrame()

for i in range(len(ABD_P_MASS_cnt_m.columns)):
    if i == 0:
        ABD_P_MASS_agegrp_m = pd.concat(
                                [
                                 ABD_P_MASS_cnt_m.iloc[:,i]
                                ,ABD_P_MASS_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_P_MASS_agegrp_m = pd.concat(
                                [
                                 ABD_P_MASS_agegrp_m
                                ,ABD_P_MASS_cnt_m.iloc[:,i]
                                ,ABD_P_MASS_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# ABD_P_MASS_agegrp_m
# %%
ABD_P_MASS_cnt_f = data_f.pivot_table(
                                    index=[GRP2,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

ABD_P_MASS_cnt_f.columns = ABD_P_MASS_cnt_f.columns.droplevel()

# ABD_P_MASS_cnt_f
# each column total value percentile
ABD_P_MASS_per_f = round(ABD_P_MASS_cnt_f.div(ABD_P_MASS_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# ABD_P_MASS_per_f

ABD_P_MASS_agegrp_f = pd.DataFrame()

for i in range(len(ABD_P_MASS_cnt_f.columns)):
    if i == 0:
        ABD_P_MASS_agegrp_f = pd.concat(
                                [
                                 ABD_P_MASS_cnt_f.iloc[:,i]
                                ,ABD_P_MASS_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_P_MASS_agegrp_f = pd.concat(
                                [
                                 ABD_P_MASS_agegrp_f
                                ,ABD_P_MASS_cnt_f.iloc[:,i]
                                ,ABD_P_MASS_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# ABD_P_MASS_agegrp_f

# %%
ABD_P_MASS_agegrp = pd.concat([ABD_P_MASS_agegrp_m.iloc[:-1,:], ABD_P_MASS_agegrp_f.iloc[:-1,:]],axis=0)
ABD_P_MASS_agegrp = ABD_P_MASS_agegrp.sort_index()
# ABD_P_MASS_agegrp

# labels = ABD_P_MASS_per_m.columns[:-1].to_list()
    
# %%
ABD_P_MASS_cnt_t = data.pivot_table(
                                    index=[GRP2]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

ABD_P_MASS_cnt_t.columns = ABD_P_MASS_cnt_t.columns.droplevel()

# total value percentile
ABD_P_MASS_per_t = round(ABD_P_MASS_cnt_t.div(ABD_P_MASS_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# ABD_P_MASS_per_t

ABD_P_MASS_agegrp_t = pd.DataFrame()

for i in range(len(ABD_P_MASS_cnt_t.columns)):
    if i == 0:
        ABD_P_MASS_agegrp_t = pd.concat(
                                [
                                 ABD_P_MASS_cnt_t.iloc[:,i]
                                ,ABD_P_MASS_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_P_MASS_agegrp_t = pd.concat(
                                [
                                 ABD_P_MASS_agegrp_t
                                ,ABD_P_MASS_cnt_t.iloc[:,i]
                                ,ABD_P_MASS_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

# ABD_P_MASS_agegrp_t
# %%
ABD_P_MASS_cnt_subt = data.pivot_table(
                                     index=[GRP2]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

ABD_P_MASS_cnt_subt.columns = ABD_P_MASS_cnt_subt.columns.droplevel()

# total value percentile
# ABD_P_MASS_per_t = round(ABD_P_MASS_cnt_t.div(ABD_P_MASS_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
ABD_P_MASS_per_subt = round(ABD_P_MASS_cnt_subt.div(ABD_P_MASS_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# ABD_P_MASS_per_subt

ABD_P_MASS_agegrp_subt = pd.DataFrame()

for i in range(len(ABD_P_MASS_cnt_subt.columns)):
    if i == 0:
        ABD_P_MASS_agegrp_subt = pd.concat(
                                [
                                 ABD_P_MASS_cnt_subt.iloc[:,i]
                                ,ABD_P_MASS_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        ABD_P_MASS_agegrp_subt = pd.concat(
                                [
                                 ABD_P_MASS_agegrp_subt
                                ,ABD_P_MASS_cnt_subt.iloc[:,i]
                                ,ABD_P_MASS_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

# ABD_P_MASS_agegrp_subt
#%%
value01 = ABD_P_CYST_per_subt.iloc[0,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
# rects1 = ax.bar(x,  value01, width, label='전체',color='cornflowerblue')
rects1 = ax.bar(x,  value01, width,color='cornflowerblue')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 복부 CT/MRI 췌장 낭종 유병률(2020년)\n\n',fontsize=30)
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
        ax.annotate(height, 
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 8),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom'
                   ,fontsize=18
                   )

autolabel(rects1)

plt.text(-0.3, -8, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_06_복부CTMR_01췌장낭종_01연령별유병률.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )

# plt.show()
# %%
value01 = ABD_P_CYST_per_m.iloc[0,:-1]
value02 = ABD_P_CYST_per_f.iloc[0,:-1]

label01 = '남자'
label02 = '여자'

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label=label01,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(ABD_P_CYST_per_m.iloc[0,:-1]).shape[0]))[5])
rects2 = ax.bar(x + 0.2, value02, width, label=label02,color='coral')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('성별 연령별 복부 CT/MRI 췌장 낭종 유병률(2020년)\n\n',fontsize=30)
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

plt.text(-0.3, -9, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_06_복부CTMR_01췌장낭종_02성별유병률.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )

# plt.show()

# %%
value01 = ABD_P_MASS_per_subt.iloc[0,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
# rects1 = ax.bar(x,  value01, width, label='전체',color='cornflowerblue')
rects1 = ax.bar(x,  value01, width,color='cornflowerblue')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 복부 CT/MRI 췌장 종괴 유병률(2020년)\n\n',fontsize=30)
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
        ax.annotate(height, 
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 8),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom'
                   ,fontsize=18
                   )

autolabel(rects1)

plt.text(-0.3, -0.22, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_06_복부CTMR_02췌장종괴_01유병률.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )

# plt.show()
# %%
value01 = ABD_P_MASS_per_m.iloc[0,:-1]
value02 = ABD_P_MASS_per_f.iloc[0,:-1]

label01 = '남자'
label02 = '여자'

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label=label01,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(ABD_P_MASS_per_m.iloc[0,:-1]).shape[0]))[5])
rects2 = ax.bar(x + 0.2, value02, width, label=label02,color='coral')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('성별 연령별 복부 CT/MRI 췌장 종괴 유병률(2020년)\n\n',fontsize=30)
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

plt.text(-0.3, -0.22, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_06_복부CTMR_02췌장종괴_02연령별유병률.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )

# plt.show()
# %%
value01 = ABD_P_CYST_per_subt.iloc[0,:-1]
value02 = ABD_P_MASS_per_subt.iloc[0,:-1]

label01 = '췌장 낭종'
label02 = '췌장 종괴'

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label=label01,color=plt.get_cmap('PuBuGn')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects2 = ax.bar(x + 0.2, value02, width, label=label02,color=plt.get_cmap('PuBuGn')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[3])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 복부 CT/MRI 질환별 유병률(2020년)\n\n',fontsize=30)
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

plt.savefig("{}/03_06_복부CTMR_03췌장낭종종괴_01유병률.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )
# # %%
# value01 = ABD_P_CYST_per_m.iloc[0,:-1]
# value02 = ABD_P_MASS_per_m.iloc[0,:-1]
# value03 = ABD_P_CYST_per_f.iloc[0,:-1]
# value04 = ABD_P_MASS_per_f.iloc[0,:-1]

# label01 = '췌장 낭종(남)'
# label02 = '췌장 종괴(남)'
# label03 = '췌장 낭종(여)'
# label04 = '췌장 종괴(여)'

# x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
# width = 0.2  # the width of the bars

# # fig, ax = plt.subplots()
# fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

# fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
# rects1 = ax.bar(x - 0.3, value01, width, label=label01,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(ABD_P_MASS_per_m.iloc[0,:-1]).shape[0]))[5])
# rects2 = ax.bar(x - 0.1, value02, width, label=label02,color=plt.get_cmap('PuBu')(np.linspace(0.15, 0.85,np.array(ABD_P_MASS_per_m.iloc[0,:-1]).shape[0]))[5])
# rects3 = ax.bar(x + 0.1, value03, width, label=label03,color='coral')
# rects4 = ax.bar(x + 0.3, value04, width, label=label04,color='brown')

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_title('복부 CT/MRI에서 질환별 연령별 유병률(2020년)\n\n',fontsize=30)
# ax.set_ylabel(
#                 '(단위: %)' # 표시값
#                  ,labelpad=-70 # 여백값 설정
#                 ,fontsize=20 # 글씨크기 설정
#                 ,rotation=0 # 회전값 조정
# #                 ,ha='center' # 위치조정
#                 ,loc='top' # 위치조정, ha와 동시에 사용은 불가함.
#             )
# ax.yaxis.set_tick_params(labelsize=15) # y축 표시값 글씨크기 조정
# ax.set_xticks(x)
# ax.set_xticklabels(
#                    labels[0:len(labels)] # all 값이 list에는 포함되지 않았기 때문임.
#                   , fontsize=17
#                   )
# ax.legend(fontsize=17)

# # bar위에 값 label 표시
# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate(height, 
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 8),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom'
#                    ,fontsize=18
#                    )

# autolabel(rects1)
# autolabel(rects2)
# autolabel(rects3)
# autolabel(rects4)

# fig.tight_layout()

# # plt.savefig("{}/03_06_복부CTMR_03췌장낭종종괴_02연령별유병률.png".format(workdir[:-5])
# #             , dpi=175 #72의 배수 ,edgecolor='black'
# #            )
# %%
value01 = ABD_P_CYST_per_m.iloc[0,:-1]
value02 = ABD_P_MASS_per_m.iloc[0,:-1]

label01 = '췌장 낭종'
label02 = '췌장 종괴'

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label=label01,color=plt.get_cmap('PuBuGn')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects2 = ax.bar(x + 0.2, value02, width, label=label02,color=plt.get_cmap('PuBuGn')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[3])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('성별 연령별 복부 CT/MRI 질환별 유병률(2020년, 남자)\n\n',fontsize=30)
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

plt.text(-0.3, -8.5, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_06_복부CTMR_03췌장낭종종괴_02유병률_남자.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )
# %%
value01 = ABD_P_CYST_per_f.iloc[0,:-1]
value02 = ABD_P_MASS_per_f.iloc[0,:-1]

label01 = '췌장 낭종'
label02 = '췌장 종괴'

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label=label01,color=plt.get_cmap('PuBuGn')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects2 = ax.bar(x + 0.2, value02, width, label=label02,color=plt.get_cmap('PuBuGn')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[3])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('성별 연령별 복부 CT/MRI 질환별 유병률(2020년, 여자)\n\n',fontsize=30)
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

plt.text(-0.3, -6.8, '          ', fontsize=17)

fig.tight_layout()
plt.savefig("{}/03_06_복부CTMR_03췌장낭종종괴_03유병률_여자.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )
# %%
ABD_P_subt = pd.concat(
                               [
                                ABD_P_CYST_agegrp_subt.iloc[0,:]
                               ,ABD_P_MASS_agegrp_subt.iloc[0,:]
                               ,ABD_P_CYST_agegrp_subt.iloc[-1,:] 
                               ]
                              ,axis=1
                              ).T

ABD_P_subt.columns = pd.MultiIndex.from_tuples(
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

ABD_P_subt
# %%
agegrp_t = pd.concat([ABD_P_MASS_agegrp_m, ABD_P_MASS_agegrp_f],axis=0)
agegrp_t = agegrp_t.sort_index()

ABD_P_agegrp = pd.concat(
                        [ABD_P_CYST_agegrp.iloc[0:2,:]
                        ,ABD_P_MASS_agegrp.iloc[0:2,:]
                        ,agegrp_t.iloc[-2:,:]
                        ]
                        ,axis=0
                        )

ABD_P_agegrp.columns = pd.MultiIndex.from_tuples(
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

ABD_P_agegrp
# %%
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # cact_agegrp_t.to_excel(writer,sheet_name="03_01이상지질혈증유병율")
    ABD_P_subt.to_excel(writer,sheet_name="03_06_1ABD_P")
    ABD_P_agegrp.to_excel(writer,sheet_name="03_06_2ABD_P_GENDER")
# %%
