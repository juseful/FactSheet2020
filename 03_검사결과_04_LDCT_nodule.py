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
exmn_cd = 'RC1241'
data = data.drop(data.loc[data['EXMN_CD']!=exmn_cd].index)
# data
# %%
GRP = "nodule(lung)"
rsltcd01 = '1033'
rsltcd02 = '1049'
data['{}_YN'.format(exmn_cd)] = ((data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd01) | (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd01)).any(axis=1).astype(int)
data.loc[data['{}_YN'.format(exmn_cd)] == 1,GRP] = GRP
data[GRP].fillna('정상',inplace=True)
# data
#%%
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

# %%
RC1241_cnt_m = data_m.pivot_table(
                             index=[GRP,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_cnt_m.columns = RC1241_cnt_m.columns.droplevel()
# RC1241_cnt_m
# each column total value percentile
RC1241_per_m = round(RC1241_cnt_m.div(RC1241_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_per_m

RC1241_agegrp_m = pd.DataFrame()

for i in range(len(RC1241_cnt_m.columns)):
    if i == 0:
        RC1241_agegrp_m = pd.concat(
                                [
                                 RC1241_cnt_m.iloc[:,i]
                                ,RC1241_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_agegrp_m = pd.concat(
                                [
                                 RC1241_agegrp_m
                                ,RC1241_cnt_m.iloc[:,i]
                                ,RC1241_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# RC1241_agegrp_m
# %%
RC1241_cnt_f = data_f.pivot_table(
                             index=[GRP,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_cnt_f.columns = RC1241_cnt_f.columns.droplevel()
# RC1241_cnt_f
# each column total value percentile
RC1241_per_f = round(RC1241_cnt_f.div(RC1241_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_per_f

RC1241_agegrp_f = pd.DataFrame()

for i in range(len(RC1241_cnt_f.columns)):
    if i == 0:
        RC1241_agegrp_f = pd.concat(
                                [
                                 RC1241_cnt_f.iloc[:,i]
                                ,RC1241_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_agegrp_f = pd.concat(
                                [
                                 RC1241_agegrp_f
                                ,RC1241_cnt_f.iloc[:,i]
                                ,RC1241_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# RC1241_agegrp_f

# %%
RC1241_agegrp = pd.concat([RC1241_agegrp_m.iloc[:-1,:], RC1241_agegrp_f.iloc[:-1,:]],axis=0)
RC1241_agegrp = RC1241_agegrp.sort_index()
RC1241_agegrp

labels = RC1241_cnt_m.columns[:-1].to_list()  
# labels
# %%
RC1241_cnt_t = data.pivot_table(
                             index=[GRP]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RC1241_cnt_t.columns = RC1241_cnt_t.columns.droplevel()
# total value percentile
RC1241_per_t = round(RC1241_cnt_t.div(RC1241_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# RC1241_per_t

RC1241_agegrp_t = pd.DataFrame()

for i in range(len(RC1241_cnt_t.columns)):
    if i == 0:
        RC1241_agegrp_t = pd.concat(
                                [
                                 RC1241_cnt_t.iloc[:,i]
                                ,RC1241_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_agegrp_t = pd.concat(
                                [
                                 RC1241_agegrp_t
                                ,RC1241_cnt_t.iloc[:,i]
                                ,RC1241_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

# RC1241_agegrp_t
# %%
RC1241_cnt_subt = data.pivot_table(
                             index=[GRP]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
# RC1241_per_t = round(RC1241_cnt_t.div(RC1241_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)
# 211123 기준 변경
RC1241_per_subt = round(RC1241_cnt_subt.div(RC1241_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# RC1241_per_subt

RC1241_agegrp_subt = pd.DataFrame()

for i in range(len(RC1241_cnt_subt.columns)):
    if i == 0:
        RC1241_agegrp_subt = pd.concat(
                                [
                                 RC1241_cnt_subt.iloc[:,i]
                                ,RC1241_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RC1241_agegrp_subt = pd.concat(
                                [
                                 RC1241_agegrp_subt
                                ,RC1241_cnt_subt.iloc[:,i]
                                ,RC1241_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )

# RC1241_agegrp_subt
# %%
value01 = RC1241_per_subt.iloc[0,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 11),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
# rects1 = ax.bar(x,  value01, width, label='전체',color='cornflowerblue')
rects1 = ax.bar(x,  value01, width,color='cornflowerblue')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('저선량 폐CT에서 결절 유병률(2020년)\n',fontsize=30)
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

fig.tight_layout()

plt.savefig("{}/03_04_LDCT_01유병률.png".format(workdir[:-5])
            ,edgecolor='black', dpi=144) #72의 배수

# plt.show()
# %%
value01 = RC1241_per_m.iloc[0,:-1]
value02 = RC1241_per_f.iloc[0,:-1]

label01 = '남자'
label02 = '여자'

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 11),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label=label01,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(RC1241_per_m.iloc[0,:-1]).shape[0]))[5])
rects2 = ax.bar(x + 0.2, value02, width, label=label02,color='coral')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('저선량 폐CT에서 결절 연령별 유병률(2020년)\n',fontsize=30)
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

fig.tight_layout()

plt.savefig("{}/03_04_LDCT_02연령별유병률.png".format(workdir[:-5])
            ,edgecolor='black', dpi=144) #72의 배수

# plt.show()
# %%
# data merge, export
RC1241_agegrp_t.to_excel('{}/03_04_LDCT.xlsx'.format(workdir[:-5]),sheet_name="유병률")
with pd.ExcelWriter('{}/03_04_LDCT.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    RC1241_agegrp.to_excel(writer,sheet_name="연령별유병률")
# %%
