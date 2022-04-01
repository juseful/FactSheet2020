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
workdir = "C:/Users/smcljy/data/20211115_Factsheet/data"
file_path = '{}/NUM_DATA.dta'.format(workdir)

data = pd.read_stata(file_path)

#%%
# 조건별 그룹 설정
### 정상, 기타 결과 그룹 분리
GRP = 'BP'
data.loc[(data['SBP'] < 120) & (data['DBP'] < 80) & (data['TRT_MED_HYPERTENSION'] != '1'), GRP] = 'OPTIMAL'
data.loc[(data['SBP'] >= 140) | (data['DBP'] >= 90) | (data['TRT_MED_HYPERTENSION'] == '1'), GRP] = '고혈압'
data['BP'].fillna('고혈압전단계',inplace=True)

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
bp_ctrl = data.drop(data.loc[data[GRP]!='고혈압'].index)
bp_ctrl.loc[(bp_ctrl['SBP'] < 140) & (bp_ctrl['DBP'] < 90), '{}_CTRL_YN'.format(GRP)] = '조절되는 그룹' # globals()['{}_CTRL_YN'.format(GRP)]
bp_ctrl['BP_CTRL_YN'].fillna('조절되지 않는 그룹',inplace=True)
# bp_ctrl
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)
data_ctrl_m = bp_ctrl.drop(bp_ctrl.loc[bp_ctrl['GEND_CD']=='F'].index)
data_ctrl_f = bp_ctrl.drop(bp_ctrl.loc[bp_ctrl['GEND_CD']=='M'].index)

#%%
## pivot table create
bp_cnt_m = data_m.pivot_table(
                             index=[GRP,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# bp_cnt_m
# bp_per_m = round(bp_cnt_m.div(bp_cnt_m.iloc[-1,-1], axis=0).astype(float)*100,1) # total value
# each column total value percentile
bp_per_m = round(bp_cnt_m.div(bp_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# bp_per_m

bp_agegrp_m = pd.DataFrame()

for i in range(len(bp_cnt_m.columns)):
    if i == 0:
        bp_agegrp_m = pd.concat(
                                [
                                 bp_cnt_m.iloc[:,i]
                                ,bp_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bp_agegrp_m = pd.concat(
                                [
                                 bp_agegrp_m
                                ,bp_cnt_m.iloc[:,i]
                                ,bp_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# bp_agegrp_m
bp_cnt_f = data_f.pivot_table(
                             index=[GRP,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# bp_cnt_f
# bp_per_f = round(bp_cnt_f.div(bp_cnt_f.iloc[-1,-1], axis=0).astype(float)*100,1) # total value
# each column total value percentile
bp_per_f = round(bp_cnt_f.div(bp_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# bp_per_f

bp_agegrp_f = pd.DataFrame()

for i in range(len(bp_cnt_f.columns)):
    if i == 0:
        bp_agegrp_f = pd.concat(
                                [
                                 bp_cnt_f.iloc[:,i]
                                ,bp_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bp_agegrp_f = pd.concat(
                                [
                                 bp_agegrp_f
                                ,bp_cnt_f.iloc[:,i]
                                ,bp_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# bp_agegrp_f
bp_agegrp = pd.concat([bp_agegrp_m.iloc[:-1,:], bp_agegrp_f.iloc[:-1,:]],axis=0)
# bp_agegrp = pd.concat([bp_agegrp_m, bp_agegrp_f],axis=0)

bp_agegrp.columns = pd.MultiIndex.from_tuples(
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
bp_agegrp = bp_agegrp.sort_index()

labels = []
for i in range(len(bp_per_m.columns)-1):
    labels.append(bp_per_m.columns[i][1])
    
bp_agegrp
    
#%%
bp_cnt_t = data.pivot_table(
                             index=[GRP]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
bp_per_t = round(bp_cnt_t.div(bp_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

bp_per_t

bp_agegrp_t = pd.DataFrame()

for i in range(len(bp_cnt_t.columns)):
    if i == 0:
        bp_agegrp_t = pd.concat(
                                [
                                 bp_cnt_t.iloc[:,i]
                                ,bp_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bp_agegrp_t = pd.concat(
                                [
                                 bp_agegrp_t
                                ,bp_cnt_t.iloc[:,i]
                                ,bp_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

bp_agegrp_t.columns = bp_agegrp.columns = pd.MultiIndex.from_tuples(
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

bp_agegrp_t
#%%
bp_cnt_subt = data.pivot_table(
                             index=[GRP]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# bp_per_t = round(bp_cnt_t.div(bp_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
bp_per_subt = round(bp_cnt_subt.div(bp_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

bp_per_subt

bp_agegrp_subt = pd.DataFrame()

for i in range(len(bp_cnt_subt.columns)):
    if i == 0:
        bp_agegrp_subt = pd.concat(
                                [
                                 bp_cnt_subt.iloc[:,i]
                                ,bp_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bp_agegrp_subt = pd.concat(
                                [
                                 bp_agegrp_subt
                                ,bp_cnt_subt.iloc[:,i]
                                ,bp_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

bp_agegrp_subt.columns = bp_agegrp.columns = pd.MultiIndex.from_tuples(
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

bp_agegrp_subt
#%%
### control group data
bp_ctrl_cnt_m = data_ctrl_m.pivot_table(
                             index=['{}_CTRL_YN'.format(GRP),'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# bp_ctrl_cnt_m
# bp_per_m = round(bp_cnt_m.div(bp_cnt_m.iloc[-1,-1], axis=0).astype(float)*100,1) # total value
# each column total value percentile
bp_ctrl_per_m = round(bp_ctrl_cnt_m.div(bp_ctrl_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# bp_ctrl_per_m

bp_ctrl_agegrp_m = pd.DataFrame()

for i in range(len(bp_ctrl_cnt_m.columns)):
    if i == 0:
        bp_ctrl_agegrp_m = pd.concat(
                                [
                                 bp_ctrl_cnt_m.iloc[:,i]
                                ,bp_ctrl_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bp_ctrl_agegrp_m = pd.concat(
                                [
                                 bp_ctrl_agegrp_m
                                ,bp_ctrl_cnt_m.iloc[:,i]
                                ,bp_ctrl_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# bp_ctrl_agegrp_m
bp_ctrl_cnt_f = data_ctrl_f.pivot_table(
                             index=['{}_CTRL_YN'.format(GRP),'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# bp_ctrl_cnt_m
# bp_per_m = round(bp_cnt_m.div(bp_cnt_m.iloc[-1,-1], axis=0).astype(float)*100,1) # total value
# each column total value percentile
bp_ctrl_per_f = round(bp_ctrl_cnt_f.div(bp_ctrl_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# bp_ctrl_per_m

bp_ctrl_agegrp_f = pd.DataFrame()

for i in range(len(bp_ctrl_cnt_f.columns)):
    if i == 0:
        bp_ctrl_agegrp_f = pd.concat(
                                [
                                 bp_ctrl_cnt_f.iloc[:,i]
                                ,bp_ctrl_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bp_ctrl_agegrp_f = pd.concat(
                                [
                                 bp_ctrl_agegrp_f
                                ,bp_ctrl_cnt_f.iloc[:,i]
                                ,bp_ctrl_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# bp_ctrl_agegrp_f
bp_ctrl_agegrp = pd.concat([bp_ctrl_agegrp_m.iloc[:-1,:], bp_ctrl_agegrp_f.iloc[:-1,:]],axis=0)
# bp_agegrp = pd.concat([bp_agegrp_m, bp_agegrp_f],axis=0)
    
bp_ctrl_agegrp.columns = bp_agegrp.columns = pd.MultiIndex.from_tuples(
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
bp_ctrl_agegrp = bp_ctrl_agegrp.sort_index()

bp_ctrl_agegrp
#%%
bp_ctrl_cnt_t = bp_ctrl.pivot_table(
                             index=['{}_CTRL_YN'.format(GRP)]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# bp_ctrl_cnt_t

# total value percentile
bp_ctrl_per_t = round(bp_ctrl_cnt_t.div(bp_ctrl_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

bp_ctrl_per_t

bp_ctrl_agegrp_t = pd.DataFrame()

for i in range(len(bp_ctrl_cnt_t.columns)):
    if i == 0:
        bp_ctrl_agegrp_t = pd.concat(
                                [
                                 bp_ctrl_cnt_t.iloc[:,i]
                                ,bp_ctrl_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bp_ctrl_agegrp_t = pd.concat(
                                [
                                 bp_ctrl_agegrp_t
                                ,bp_ctrl_cnt_t.iloc[:,i]
                                ,bp_ctrl_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

bp_ctrl_agegrp_t.columns = bp_agegrp.columns = pd.MultiIndex.from_tuples(
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

bp_ctrl_agegrp_t
#%%
bp_ctrl_cnt_subt = bp_ctrl.pivot_table(
                             index=['{}_CTRL_YN'.format(GRP)]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# bp_ctrl_cnt_t
# total value percentile
bp_ctrl_per_subt = round(bp_ctrl_cnt_subt.div(bp_ctrl_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

bp_ctrl_agegrp_subt = pd.DataFrame()

for i in range(len(bp_ctrl_cnt_subt.columns)):
    if i == 0:
        bp_ctrl_agegrp_subt = pd.concat(
                                [
                                 bp_ctrl_cnt_subt.iloc[:,i]
                                ,bp_ctrl_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bp_ctrl_agegrp_subt = pd.concat(
                                [
                                 bp_ctrl_agegrp_subt
                                ,bp_ctrl_cnt_subt.iloc[:,i]
                                ,bp_ctrl_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

bp_ctrl_agegrp_subt.columns = bp_agegrp.columns = pd.MultiIndex.from_tuples(
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

bp_ctrl_agegrp_subt
#%%
# Bar chart create
value01 = bp_per_subt.iloc[1,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
# rects1 = ax.bar(x,  value01, width, label='전체',color='cornflowerblue')
rects1 = ax.bar(x,  value01, width,color='cornflowerblue')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 고혈압 유병율(2020년)\n\n',fontsize=30)
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
plt.text(-0.4, -12.5,  '고혈압: 다음 세 가지 기준 중 하나라도 만족', fontsize=22)
plt.text(-0.3, -15, '① 건진 당일 측정한 수축기 혈압이 140mmHg 이상', fontsize=17)
plt.text(-0.3, -18, '② 건진 당일 측정한 이완기 혈압이 90mmHg 이상', fontsize=17)
plt.text(-0.3, -21, '③ 문진에서 현재 고혈압 약물복용중으로 응답한 경우', fontsize=17)
plt.text(-0.3, -24, '          ', fontsize=17)
plt.text(-0.3, -27, '          ', fontsize=17)
fig.tight_layout()

plt.savefig("{}/02_01고혈압_01유병율.png".format(workdir[:-5])
           , dpi=175)

# plt.show()
#%%
value01 = bp_per_m.iloc[1,:-1]
value02 = bp_per_f.iloc[1,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label='남자',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(bp_per_m.iloc[0,:-1]).shape[0]))[4])
rects2 = ax.bar(x + 0.2, value02, width, label='여자',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(bp_per_m.iloc[0,:-1]).shape[0]))[1])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('성별 연령별 고혈압 유병율(2020년)\n\n',fontsize=30)
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

plt.text(-0.3, -10, '          ', fontsize=17)
plt.text(-0.4, -12.5,  '고혈압: 다음 세 가지 기준 중 하나라도 만족', fontsize=22)
plt.text(-0.3, -15, '① 건진 당일 측정한 수축기 혈압이 140mmHg 이상', fontsize=17)
plt.text(-0.3, -18, '② 건진 당일 측정한 이완기 혈압이 90mmHg 이상', fontsize=17)
plt.text(-0.3, -21, '③ 문진에서 현재 고혈압 약물복용중으로 응답한 경우', fontsize=17)
plt.text(-0.3, -24, '          ', fontsize=17)
plt.text(-0.3, -27, '          ', fontsize=17)
fig.tight_layout()

plt.savefig("{}/02_01고혈압_02성별유병율.png".format(workdir[:-5])
           , dpi=175)

plt.show()
#%%
value01 = bp_ctrl_per_subt.iloc[0,:-1] # 조절군 명칭변경으로 순서조정


x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x,  value01, width,color='cornflowerblue')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 고혈압 조절율(2020년)\n\n',fontsize=30)
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
plt.text(-0.4, -12.5,  '고혈압 조절율은 아래와 같이 정의하였다.', fontsize=22)
plt.text(-0.3, -15, '고혈압 유병자 중 2개 경우 모두 해당하는 분율(%)', fontsize=17)
plt.text(-0.3, -18, '① 건진 당일 측정한 수축기 혈압이 140mmHg 미만', fontsize=17)
plt.text(-0.3, -21, '② 건진 당일 측정한 이완기 혈압이 90mmHg 미만', fontsize=17)
plt.text(-0.3, -24, '          ', fontsize=17)
plt.text(-0.3, -27, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/02_01고혈압_03조절율.png".format(workdir[:-5])
           , dpi=175)

plt.show()
#%%
value01 = bp_ctrl_per_m.iloc[0,:-1] # 조절군 명칭변경으로 순서조정
value02 = bp_ctrl_per_f.iloc[0,:-1] # 조절군 명칭변경으로 순서조정

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label='남자',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(bp_ctrl_per_m.iloc[0,:-1]).shape[0]))[4])
rects2 = ax.bar(x + 0.2, value02, width, label='여자',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(bp_ctrl_per_m.iloc[0,:-1]).shape[0]))[1])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('성별 연령별 고혈압 조절율(2020년)\n\n',fontsize=30)
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
plt.text(-0.4, -12.5,  '고혈압 조절율은 아래와 같이 정의하였다.', fontsize=22)
plt.text(-0.3, -15, '고혈압 유병자 중 2개 경우 모두 해당하는 분율(%)', fontsize=17)
plt.text(-0.3, -18, '① 건진 당일 측정한 수축기 혈압이 140mmHg 미만', fontsize=17)
plt.text(-0.3, -21, '② 건진 당일 측정한 이완기 혈압이 90mmHg 미만', fontsize=17)
plt.text(-0.3, -24, '          ', fontsize=17)
plt.text(-0.3, -27, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/02_01고혈압_04성별조절율.png".format(workdir[:-5])
           , dpi=175)

plt.show()

#%%
# data merge, export
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    bp_agegrp_t.to_excel(writer,sheet_name="02_01고혈압유병율")
    bp_agegrp.to_excel(writer,sheet_name="02_01고혈압성별유병율")
    bp_ctrl_agegrp_t.to_excel(writer,sheet_name="02_01고혈압조절율")
    bp_ctrl_agegrp.to_excel(writer,sheet_name="02_01고혈압성별조절율")

# %%
