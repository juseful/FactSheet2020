#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib import font_manager,rc  #한글 폰트 입력을 위한 라이브러리
from matplotlib.patches import ConnectionPatch

#폰트 경로 가져오기
font_path = 'C:\\Windows\\Fonts\\SGL.ttf' #삼성고딕체
 
# 폰트 이름 얻어오기
font_name = font_manager.FontProperties(fname=font_path).get_name()
 
#폰트 설정하기
mpl.rc('font',family=font_name)

#%%
workdir = "C:/Users/smcljy/data/20211115_Factsheet/data"
file_path = '{}/NUM_DATA.dta'.format(workdir)

data = pd.read_stata(file_path)

#%%
# 조건별 그룹 설정
### 정상, 기타 결과 그룹 분리
GRP = 'DM'
data.loc[(data['BL3118'] < 100) & (data['BL3164'] < 5.7) & (data['TRT_MED_DIABETES'] != '1'), GRP] = '정상'
data.loc[(data['BL3118'] >= 126) | (data['BL3164'] >= 6.5) | (data['TRT_MED_DIABETES'] == '1'), GRP] = '당뇨병'
data['DM'].fillna('전당뇨',inplace=True)

data.loc[data['GEND_CD'] == 'M', 'GENDER'] = '남'
data.loc[data['GEND_CD'] == 'F', 'GENDER'] = '여'

data.loc[ data['AGE'] < 30                      ,'AGEGRP'] = '29세 이하'
data.loc[(data['AGE'] > 29) & (data['AGE'] < 40),'AGEGRP'] = '30~39세'
data.loc[(data['AGE'] > 39) & (data['AGE'] < 50),'AGEGRP'] = '40~49세'
data.loc[(data['AGE'] > 49) & (data['AGE'] < 60),'AGEGRP'] = '50~59세'
data.loc[(data['AGE'] > 59) & (data['AGE'] < 70),'AGEGRP'] = '60~69세'
data.loc[ data['AGE'] > 69                      ,'AGEGRP'] = '70세 이상'
# data.head(100)

#%%
### 특정 그룹 별도 저장
dm_ctrl = data.drop(data.loc[data[GRP]!='당뇨병'].index)
dm_ctrl.loc[(dm_ctrl['BL3164'] < 7.0), '{}_CTRL_YN'.format(GRP)] = '조절되는 그룹'
dm_ctrl['{}_CTRL_YN'.format(GRP)].fillna('조절되지 않는 그룹',inplace=True)
# dm_ctrl
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)
data_ctrl_m = dm_ctrl.drop(dm_ctrl.loc[dm_ctrl['GEND_CD']=='F'].index)
data_ctrl_f = dm_ctrl.drop(dm_ctrl.loc[dm_ctrl['GEND_CD']=='M'].index)

#%%
## pivot table create
dm_cnt_m = data_m.pivot_table(
                             index=[GRP,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# dm_cnt_m
# dm_per_m = round(dm_cnt_m.div(dm_cnt_m.iloc[-1,-1], axis=0).astype(float)*100,1) # total value
# each column total value percentile
dm_per_m = round(dm_cnt_m.div(dm_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# dm_per_m

dm_agegrp_m = pd.DataFrame()

for i in range(len(dm_cnt_m.columns)):
    if i == 0:
        dm_agegrp_m = pd.concat(
                                [
                                 dm_cnt_m.iloc[:,i]
                                ,dm_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        dm_agegrp_m = pd.concat(
                                [
                                 dm_agegrp_m
                                ,dm_cnt_m.iloc[:,i]
                                ,dm_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# dm_agegrp_m
dm_cnt_f = data_f.pivot_table(
                             index=[GRP,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# dm_cnt_f
# dm_per_f = round(dm_cnt_f.div(dm_cnt_f.iloc[-1,-1], axis=0).astype(float)*100,1) # total value
# each column total value percentile
dm_per_f = round(dm_cnt_f.div(dm_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# dm_per_f

dm_agegrp_f = pd.DataFrame()

for i in range(len(dm_cnt_f.columns)):
    if i == 0:
        dm_agegrp_f = pd.concat(
                                [
                                 dm_cnt_f.iloc[:,i]
                                ,dm_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        dm_agegrp_f = pd.concat(
                                [
                                 dm_agegrp_f
                                ,dm_cnt_f.iloc[:,i]
                                ,dm_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# dm_agegrp_f
dm_agegrp = pd.concat([dm_agegrp_m.iloc[:-1,:], dm_agegrp_f.iloc[:-1,:]],axis=0)
# dm_agegrp = pd.concat([dm_agegrp_m, dm_agegrp_f],axis=0)

dm_agegrp.columns = pd.MultiIndex.from_tuples(
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
dm_agegrp = dm_agegrp.sort_index()

labels = []
for i in range(len(dm_per_m.columns)-1):
    labels.append(dm_per_m.columns[i][1])
    
dm_agegrp
    
#%%
dm_cnt_t = data.pivot_table(
                             index=[GRP]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
dm_per_t = round(dm_cnt_t.div(dm_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

dm_per_t

dm_agegrp_t = pd.DataFrame()

for i in range(len(dm_cnt_t.columns)):
    if i == 0:
        dm_agegrp_t = pd.concat(
                                [
                                 dm_cnt_t.iloc[:,i]
                                ,dm_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        dm_agegrp_t = pd.concat(
                                [
                                 dm_agegrp_t
                                ,dm_cnt_t.iloc[:,i]
                                ,dm_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

dm_agegrp_t.columns = dm_agegrp.columns = pd.MultiIndex.from_tuples(
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

dm_agegrp_t
#%%
dm_cnt_subt = data.pivot_table(
                             index=[GRP]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# dm_per_t = round(dm_cnt_t.div(dm_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
dm_per_subt = round(dm_cnt_subt.div(dm_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

dm_per_subt

dm_agegrp_subt = pd.DataFrame()

for i in range(len(dm_cnt_subt.columns)):
    if i == 0:
        dm_agegrp_subt = pd.concat(
                                [
                                 dm_cnt_subt.iloc[:,i]
                                ,dm_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        dm_agegrp_subt = pd.concat(
                                [
                                 dm_agegrp_subt
                                ,dm_cnt_subt.iloc[:,i]
                                ,dm_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

dm_agegrp_subt.columns = dm_agegrp.columns = pd.MultiIndex.from_tuples(
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

dm_agegrp_subt
#%%
### control group data
dm_ctrl_cnt_m = data_ctrl_m.pivot_table(
                             index=['{}_CTRL_YN'.format(GRP),'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# dm_ctrl_cnt_m
# dm_per_m = round(dm_cnt_m.div(dm_cnt_m.iloc[-1,-1], axis=0).astype(float)*100,1) # total value
# each column total value percentile
dm_ctrl_per_m = round(dm_ctrl_cnt_m.div(dm_ctrl_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# dm_ctrl_per_m

dm_ctrl_agegrp_m = pd.DataFrame()

for i in range(len(dm_ctrl_cnt_m.columns)):
    if i == 0:
        dm_ctrl_agegrp_m = pd.concat(
                                [
                                 dm_ctrl_cnt_m.iloc[:,i]
                                ,dm_ctrl_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        dm_ctrl_agegrp_m = pd.concat(
                                [
                                 dm_ctrl_agegrp_m
                                ,dm_ctrl_cnt_m.iloc[:,i]
                                ,dm_ctrl_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# dm_ctrl_agegrp_m
dm_ctrl_cnt_f = data_ctrl_f.pivot_table(
                             index=['{}_CTRL_YN'.format(GRP),'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# dm_ctrl_cnt_m
# dm_per_m = round(dm_cnt_m.div(dm_cnt_m.iloc[-1,-1], axis=0).astype(float)*100,1) # total value
# each column total value percentile
dm_ctrl_per_f = round(dm_ctrl_cnt_f.div(dm_ctrl_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# dm_ctrl_per_m

dm_ctrl_agegrp_f = pd.DataFrame()

for i in range(len(dm_ctrl_cnt_f.columns)):
    if i == 0:
        dm_ctrl_agegrp_f = pd.concat(
                                [
                                 dm_ctrl_cnt_f.iloc[:,i]
                                ,dm_ctrl_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        dm_ctrl_agegrp_f = pd.concat(
                                [
                                 dm_ctrl_agegrp_f
                                ,dm_ctrl_cnt_f.iloc[:,i]
                                ,dm_ctrl_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# dm_ctrl_agegrp_f
dm_ctrl_agegrp = pd.concat([dm_ctrl_agegrp_m.iloc[:-1,:], dm_ctrl_agegrp_f.iloc[:-1,:]],axis=0)
# dm_agegrp = pd.concat([dm_agegrp_m, dm_agegrp_f],axis=0)
    
dm_ctrl_agegrp.columns = dm_agegrp.columns = pd.MultiIndex.from_tuples(
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
dm_ctrl_agegrp = dm_ctrl_agegrp.sort_index()

dm_ctrl_agegrp
#%%
dm_ctrl_cnt_t = dm_ctrl.pivot_table(
                             index=['{}_CTRL_YN'.format(GRP)]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# dm_ctrl_cnt_t

# total value percentile
dm_ctrl_per_t = round(dm_ctrl_cnt_t.div(dm_ctrl_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

dm_ctrl_per_t

dm_ctrl_agegrp_t = pd.DataFrame()

for i in range(len(dm_ctrl_cnt_t.columns)):
    if i == 0:
        dm_ctrl_agegrp_t = pd.concat(
                                [
                                 dm_ctrl_cnt_t.iloc[:,i]
                                ,dm_ctrl_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        dm_ctrl_agegrp_t = pd.concat(
                                [
                                 dm_ctrl_agegrp_t
                                ,dm_ctrl_cnt_t.iloc[:,i]
                                ,dm_ctrl_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

dm_ctrl_agegrp_t.columns = dm_agegrp.columns = pd.MultiIndex.from_tuples(
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

dm_ctrl_agegrp_t
#%%
dm_ctrl_cnt_subt = dm_ctrl.pivot_table(
                             index=['{}_CTRL_YN'.format(GRP)]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# dm_ctrl_cnt_t
# total value percentile
dm_ctrl_per_subt = round(dm_ctrl_cnt_subt.div(dm_ctrl_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

dm_ctrl_agegrp_subt = pd.DataFrame()

for i in range(len(dm_ctrl_cnt_subt.columns)):
    if i == 0:
        dm_ctrl_agegrp_subt = pd.concat(
                                [
                                 dm_ctrl_cnt_subt.iloc[:,i]
                                ,dm_ctrl_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        dm_ctrl_agegrp_subt = pd.concat(
                                [
                                 dm_ctrl_agegrp_subt
                                ,dm_ctrl_cnt_subt.iloc[:,i]
                                ,dm_ctrl_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

dm_ctrl_agegrp_subt.columns = dm_agegrp.columns = pd.MultiIndex.from_tuples(
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

dm_ctrl_agegrp_subt
#%%
# Bar chart create
value01 = dm_per_subt.iloc[0,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
# rects1 = ax.bar(x,  value01, width, label='전체',color='cornflowerblue')
rects1 = ax.bar(x,  value01, width,color='cornflowerblue')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 당뇨병 유병율(2020년)\n\n',fontsize=30)
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

plt.text(-0.3, -4, '          ', fontsize=17)
plt.text(-0.4, -5,  '당뇨병: 다음 세 가지 기준 중 하나라도 만족', fontsize=22)
plt.text(-0.3, -6, '① 건진 당일 측정한 공복혈당 ≥ 126mg/dL', fontsize=17)
plt.text(-0.3, -7, '② 건진 당일 측정한 당화혈색소(HbA1c) ≥ 6.5%', fontsize=17)
plt.text(-0.3, -8, '③ 문진에서 현재 당뇨약 복용 중이거나 인슐린 치료 중이라고 응답한 경우', fontsize=17)
plt.text(-0.3, -9, '          ', fontsize=17)
plt.text(-0.3, -10, '          ', fontsize=17)
fig.tight_layout()

plt.savefig("{}/02_02당뇨병_01유병율.png".format(workdir[:-5])
           , dpi=175)

# plt.show()
#%%
value01 = dm_per_m.iloc[0,:-1]
value02 = dm_per_f.iloc[0,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label='남자',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(dm_per_m.iloc[0,:-1]).shape[0]))[4])
rects2 = ax.bar(x + 0.2, value02, width, label='여자',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(dm_per_m.iloc[0,:-1]).shape[0]))[1])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('성별 연령별 당뇨병 유병율(2020년)\n\n',fontsize=30)
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
ax.legend(fontsize=17,loc='best')

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

plt.text(-0.3, -4, '          ', fontsize=17)
plt.text(-0.4, -5,  '당뇨병: 다음 세 가지 기준 중 하나라도 만족', fontsize=22)
plt.text(-0.3, -6, '① 건진 당일 측정한 공복혈당 ≥ 126mg/dL', fontsize=17)
plt.text(-0.3, -7, '② 건진 당일 측정한 당화혈색소(HbA1c) ≥ 6.5%', fontsize=17)
plt.text(-0.3, -8, '③ 문진에서 현재 당뇨약 복용 중이거나 인슐린 치료 중이라고 응답한 경우', fontsize=17)
plt.text(-0.3, -9, '          ', fontsize=17)
plt.text(-0.3, -10, '          ', fontsize=17)
fig.tight_layout()

plt.savefig("{}/02_02당뇨병_02성별유병율.png".format(workdir[:-5])
           , dpi=175)

plt.show()
#%%
value01 = dm_ctrl_per_subt.iloc[0,:-1] # 조절군 명칭변경으로 순서조정


x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x,  value01, width,color='cornflowerblue')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 당뇨병 조절율(2020년)\n\n',fontsize=30)
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
plt.text(-0.3, -10, '          ', fontsize=17)
plt.text(-0.4, -12.5,'당뇨병 조절율은 아래와 같이 정의하였다.', fontsize=22)
plt.text(-0.3, -15, '당뇨병 유병자 중 당화혈색소(HbA1c) < 7.0% 에 해당하는 분율(%)', fontsize=17)
plt.text(-0.3, -18, '', fontsize=17)
plt.text(-0.3, -21, '', fontsize=17)
plt.text(-0.3, -24, '          ', fontsize=17)
plt.text(-0.3, -27, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/02_02당뇨병_03조절율.png".format(workdir[:-5])
           , dpi=175)

plt.show()
#%%
value01 = dm_ctrl_per_m.iloc[0,:-1] # 조절군 명칭변경으로 순서조정
value02 = dm_ctrl_per_f.iloc[0,:-1] # 조절군 명칭변경으로 순서조정

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label='남자',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(dm_ctrl_per_m.iloc[0,:-1]).shape[0]))[4])
rects2 = ax.bar(x + 0.2, value02, width, label='여자',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(dm_ctrl_per_m.iloc[0,:-1]).shape[0]))[1])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('성별 연령별 당뇨병 조절율(2020년)\n\n',fontsize=30)
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
ax.legend(fontsize=17,loc='upper left')

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

plt.text(-0.3, -10, '          ', fontsize=17)
plt.text(-0.4, -12.5,'당뇨병 조절율은 아래와 같이 정의하였다.', fontsize=22)
plt.text(-0.3, -15, '당뇨병 유병자 중 당화혈색소(HbA1c) < 7.0% 에 해당하는 분율(%)', fontsize=17)
plt.text(-0.3, -18, '', fontsize=17)
plt.text(-0.3, -21, '', fontsize=17)
plt.text(-0.3, -24, '          ', fontsize=17)
plt.text(-0.3, -27, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/02_02당뇨병_04성별조절율.png".format(workdir[:-5])
           , dpi=175)

plt.show()

#%%
# data merge, export
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    dm_agegrp_t.to_excel(writer,sheet_name="02_02당뇨병유병율")
    dm_agegrp.to_excel(writer,sheet_name="02_02당뇨병성별유병율")
    dm_ctrl_agegrp_t.to_excel(writer,sheet_name="02_02당뇨병조절율")
    dm_ctrl_agegrp.to_excel(writer,sheet_name="02_02당뇨병성별조절율")

#%%
dm_grp = data.pivot_table(
                          columns=['DM']
                         ,values=['ID']
                         ,aggfunc='count'
)

# dm_grp

label_pie = dm_grp.columns.to_list()
label_pie

data_pie = dm_grp.iloc[0,:].to_list()
# data_pie

# %%
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] < 6.5)                          ,'DM_HbA1c'] = '01_~6.4'
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] > 6.4) & (data['BL3164'] <  7.0),'DM_HbA1c'] = '02_6.5~6.9'
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] > 6.9) & (data['BL3164'] <  8.0),'DM_HbA1c'] = '03_7.0~7.9'
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] > 7.9) & (data['BL3164'] <  9.0),'DM_HbA1c'] = '04_8.0~8.9'
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] > 8.9) & (data['BL3164'] < 10.0),'DM_HbA1c'] = '05_9.0~9.9'
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] > 9.9)                          ,'DM_HbA1c'] = '06_10.0~'

# data

DM_HbA1c_cat = data.pivot_table(
                              columns=['DM_HbA1c']
                             ,values=['ID'] 
                             ,aggfunc='count'
                             )
DM_HbA1c_cat
# %%
data_bar = DM_HbA1c_cat.iloc[0,:].to_list()
data_bar

data_bar_per = []

for i in range(len(data_bar)):
    data_bar_per.append(round(data_bar[i]/data_pie[0],3))

data_bar_per

label_bar = ['6.4 이하'
            ,'6.5~6.9'
            ,'7.0~7.9'
            ,'8.0~8.9'
            ,'9.0~9.9'
            ,'10.0 이상'
            ]

label_bar
# %%
# make figure and assign axis objects
fig = plt.figure(figsize=(12, 12))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
fig.subplots_adjust(wspace=0.1)

# pie chart parameters
ratios = data_pie
pie_labels = label_pie
explode = [0.05, 0, 0]
colors = plt.get_cmap('Set2')(
np.linspace(0.15, 0.85, np.array(data_pie).shape[0])
)

def func(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals)))
#     return "{:.1f}%\n({:,d})".format(pct, absolute) # %값(수치)로 표현하고 싶을 때, 1000 단위 마다 (,)표시하기
    return "{:,d}\n({:.1f}%)".format(absolute, pct) # 수치(%값)로 표현하고 싶을 때1000 단위미다 ','표시

# rotate so that first wedge is split by the x-axis
ax1.pie(ratios, autopct=lambda pct: func(pct, ratios)
        , startangle=-15, labels=pie_labels, explode=explode, colors=colors
,textprops=dict(color="black",fontsize=22)
)

# bar chart parameters
xpos = 0.05
bottom = 0
ratios = data_bar_per #bar chart using category percentile
width = .2
colors = plt.get_cmap('coolwarm')(
np.linspace(0.15, 0.85, np.array(data_bar_per).shape[0])
)

for j in range(len(ratios)):
    height = ratios[j]
    ax2.bar(xpos, height, width, bottom=bottom, color=colors[j],alpha=0.7)
    ypos = bottom + ax2.patches[j].get_height() / 2
    bottom += height
    ax2.text(xpos, ypos, "%1.1f%%" % (ax2.patches[j].get_height() * 100),
             ha='center',color="black",fontsize=15)
# ax2.text(xpos, ypos, "%d%%" % (ax2.patches[j].get_height() * 100),
# ha='center')

ax2.set_title('분포(%)', fontsize=17)

# plt.text(-1.35, -0.005, '   ', fontsize=22)
plt.text(-1.35, -0.005,  '당화혈색소 분류 기준:', fontsize=22)
lg = ax2.legend(label_bar
               ,bbox_to_anchor=(-0.85,-0.105)
               ,ncol=3
               ,loc='lower left' ,fontsize=15
               )
plt.text(-1.6, -0.15,  '  ', fontsize=22)
# ax2.legend(label_bar,
# title="결과 분류",
# title_fontsize=20,
# loc="center left",
# bbox_to_anchor=(0.65,0, 0.5, 1),
# fontsize=20
# )
ax2.axis('off')
ax2.set_xlim(- 2.5 * width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
# get the wedge data
theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
center, r = ax1.patches[0].center, ax1.patches[0].r
bar_height = sum([item.get_height() for item in ax2.patches])

# draw top connecting line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(- width / 3, bar_height), xyB=(x, y),
coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
con.set_linewidth(2)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0] 
y = np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(- width / 3, 0), xyB=(x, y), coordsA="data",
coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(2)
 
# ax1.set_title("복부초음파에서 지방간 현황(2020년)\n\n",fontsize=30)
# ax2.set_title("  \n\n",fontsize=30)
# all subplot's title setting
plt.suptitle('당뇨병 유병자의 당화혈색소 분포(2020년)\n\n',fontsize=30)

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# fig.tight_layout()

plt.savefig("{}/02_02당뇨병_05당뇨유병자당화혈색소.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )
 
plt.show()
# %%
