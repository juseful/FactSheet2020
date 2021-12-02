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
workdir = ''
data = pd.read_stata('{}/RSLT_CD_EXMN.dta'.format(workdir))
data.drop(data.loc[:,'RSLT_CD14':], axis=1, inplace=True)

# data.describe()

# %%
data.loc[data['GEND_CD'] == 'M', 'GENDER'] = '남'
data.loc[data['GEND_CD'] == 'F', 'GENDER'] = '여'

data[['AGE']] = data[['AGE']].apply(pd.to_numeric)
data.loc[ data['AGE'] < 30                      ,'AGEGRP'] = '0~29세'
data.loc[(data['AGE'] > 29) & (data['AGE'] < 40),'AGEGRP'] = '30~39세'
data.loc[(data['AGE'] > 39) & (data['AGE'] < 50),'AGEGRP'] = '40~49세'
data.loc[(data['AGE'] > 49) & (data['AGE'] < 60),'AGEGRP'] = '50~59세'
data.loc[(data['AGE'] > 59) & (data['AGE'] < 70),'AGEGRP'] = '60~69세'
data.loc[ data['AGE'] > 69                      ,'AGEGRP'] = '70세 이상'
# data.head(100)
# data
# %%
# 다른 검사 제외
exmn_cd = 'RS1190'
data = data.drop(data.loc[data['EXMN_CD']!=exmn_cd].index)
# data
# %%
GRP = "nodule(breast)"
rsltcd01 = '1004'
rsltcd02 = '1005'
rsltcd03 = '1008'
rsltcd04 = '1032'
rsltcd05 = '1036'
rsltcd06 = '1049'
data['{}_YN'.format(exmn_cd)] = (
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd01) | 
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd02) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd03) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd04) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd05) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd06)
    ).any(axis=1).astype(int)
data.loc[data['{}_YN'.format(exmn_cd)] == 1,GRP] = GRP
data[GRP].fillna('정상',inplace=True)
# data
#%%
# data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

# %%
RS1190_cnt_f = data_f.pivot_table(
                             index=[GRP,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# RS1190_cnt_f
# each column total value percentile
RS1190_per_f = round(RS1190_cnt_f.div(RS1190_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# RS1190_per_f

RS1190_agegrp_f = pd.DataFrame()

for i in range(len(RS1190_cnt_f.columns)):
    if i == 0:
        RS1190_agegrp_f = pd.concat(
                                [
                                 RS1190_cnt_f.iloc[:,i]
                                ,RS1190_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RS1190_agegrp_f = pd.concat(
                                [
                                 RS1190_agegrp_f
                                ,RS1190_cnt_f.iloc[:,i]
                                ,RS1190_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# RS1190_agegrp_f
labels = []
for i in range(len(RS1190_per_f.columns)-1):
    labels.append(RS1190_per_f.columns[i][1])
    
# %%
RS1190_cnt_subt = data_f.pivot_table(
                             index=[GRP]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# RS1190_per_t = round(RS1190_cnt_t.div(RS1190_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
RS1190_per_subt = round(RS1190_cnt_subt.div(RS1190_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# RS1190_per_subt

RS1190_agegrp_subt = pd.DataFrame()

for i in range(len(RS1190_cnt_subt.columns)):
    if i == 0:
        RS1190_agegrp_subt = pd.concat(
                                [
                                 RS1190_cnt_subt.iloc[:,i]
                                ,RS1190_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RS1190_agegrp_subt = pd.concat(
                                [
                                 RS1190_agegrp_subt
                                ,RS1190_cnt_subt.iloc[:,i]
                                ,RS1190_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

RS1190_agegrp_subt
# %%
value01 = RS1190_per_subt.iloc[0,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 11),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
# rects1 = ax.bar(x,  value01, width, label='전체',color='cornflowerblue')
rects1 = ax.bar(x,  value01, width,label='여자',color='coral')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('유방초음파에서 결절 유병률(2020년)\n',fontsize=30)
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
ax.legend(fontsize=17)

autolabel(rects1)

fig.tight_layout()

plt.savefig("{}/03_05_BreastUS_01유병률.png".format(workdir[:-5])
            ,edgecolor='black', dpi=144) #72의 배수


# %%
# data merge, export
RS1190_agegrp_subt.to_excel('{}/03_05_BreastUS.xlsx'.format(workdir[:-5]),sheet_name="유병률")

# %%
