#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib import font_manager,rc  #한글 폰트 입력을 위한 라이브러리

#폰트 경로 가져오기
font_path = 'C:\\Windows\\Fonts\\SGL.ttf' #삼성고딕체
 
# 폰트 이름 얻어오기
font_name = font_manager.FontProperties(fname=font_path).get_name()
 
#폰트 설정하기
mpl.rc('font',family=font_name)

#%%
workdir = ""
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
dm_ctrl.loc[(dm_ctrl['BL3164'] < 7.0), '{}_CTRL_YN'.format(GRP)] = '조절군'
dm_ctrl['{}_CTRL_YN'.format(GRP)].fillna('비조절군',inplace=True)
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
value01 = dm_ctrl_per_subt.iloc[1,:-1]


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
value01 = dm_ctrl_per_m.iloc[1,:-1]
value02 = dm_ctrl_per_f.iloc[1,:-1]

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
# %%
