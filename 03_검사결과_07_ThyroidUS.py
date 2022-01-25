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
# 다른 검사 제외
exmn_cd = 'RS1172'
data = data.drop(data.loc[data['EXMN_CD']!=exmn_cd].index)
data

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
GRP = "Category"
data[GRP] = ""
rsltcd_GRP = ['5001','5002','5003','5004','5005']
rslttext = [
            '01_K-TIRADS: 1 (No nodule)'
           ,'02_K-TIRADS: 2 (Benign)'
           ,'03_K-TIRADS: 3 (Low suspicion)'
           ,'04_K-TIRADS: 4 (Intermediate suspicion)'
           ,'05_K-TIRADS: 5 (High suspicion)'
           ]

for i in range(len(rsltcd_GRP)):
    data['CAT_{}'.format(i)] = (
        (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd_GRP[i])
        ).any(axis=1).astype(int)
    data.loc[data['CAT_{}'.format(i)] == 1,'Category'] = rslttext[i]
    
data

#%%
# category가 없는 경우 삭제
data = data.drop(data.loc[data[GRP]==""].index)
data

#%%
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

#%%
Thyroid_cnt_m = data_m.pivot_table(
                                    index=[GRP,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# ABD_P_CYST_cnt_m

# Thyroid_cnt_m.columns = Thyroid_cnt_m.columns.droplevel()
# each column total value percentile
Thyroid_per_m = round(Thyroid_cnt_m.div(Thyroid_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

Thyroid_agegrp_m = pd.DataFrame()

for i in range(len(Thyroid_cnt_m.columns)):
    if i == 0:
        Thyroid_agegrp_m = pd.concat(
                                [
                                 Thyroid_cnt_m.iloc[:,i]
                                ,Thyroid_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        Thyroid_agegrp_m = pd.concat(
                                [
                                 Thyroid_agegrp_m
                                ,Thyroid_cnt_m.iloc[:,i]
                                ,Thyroid_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# Thyroid_agegrp_m

# %%
Thyroid_cnt_f = data_f.pivot_table(
                                    index=[GRP,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# ABD_P_CYST_cnt_m
# multi level column to single level
# Thyroid_cnt_f.columns = Thyroid_cnt_f.columns.droplevel()
# each column total value percentile
Thyroid_per_f = round(Thyroid_cnt_f.div(Thyroid_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

Thyroid__agegrp_f = pd.DataFrame()

for i in range(len(Thyroid_cnt_f.columns)):
    if i == 0:
        Thyroid_agegrp_f = pd.concat(
                                [
                                 Thyroid_cnt_f.iloc[:,i]
                                ,Thyroid_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        Thyroid_agegrp_f = pd.concat(
                                [
                                 Thyroid_agegrp_f
                                ,Thyroid_cnt_f.iloc[:,i]
                                ,Thyroid_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# Thyroid_agegrp_f

# %%
Thyroid_agegrp = pd.concat([Thyroid_agegrp_m, Thyroid_agegrp_f],axis=0)
Thyroid_agegrp = Thyroid_agegrp.sort_index()

Thyroid_agegrp.columns = pd.MultiIndex.from_tuples(
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

# multi level column to single level
labels = Thyroid_per_m.columns[:-1].droplevel().to_list()
# labels

Thyroid_agegrp

# %%
Thyroid_cnt_t = data.pivot_table(
                                    index=[GRP]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# total value percentile
Thyroid_per_t = round(Thyroid_cnt_t.div(Thyroid_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# ABD_P_CYST_per_t

Thyroid_agegrp_t = pd.DataFrame()

for i in range(len(Thyroid_cnt_t.columns)):
    if i == 0:
        Thyroid_agegrp_t = pd.concat(
                                [
                                 Thyroid_cnt_t.iloc[:,i]
                                ,Thyroid_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        Thyroid_agegrp_t = pd.concat(
                                [
                                 Thyroid_agegrp_t
                                ,Thyroid_cnt_t.iloc[:,i]
                                ,Thyroid_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

Thyroid_agegrp_t.columns = pd.MultiIndex.from_tuples(
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

Thyroid_agegrp_t
# %%
Thyroid_cnt_subt = data.pivot_table(
                                    index=[GRP]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )


# total value percentile
Thyroid_per_subt = round(Thyroid_cnt_subt.div(Thyroid_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# ABD_P_CYST_per_subt

Thyroid_agegrp_subt = pd.DataFrame()

for i in range(len(Thyroid_cnt_subt.columns)):
    if i == 0:
        Thyroid_agegrp_subt = pd.concat(
                                [
                                 Thyroid_cnt_subt.iloc[:,i]
                                ,Thyroid_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        Thyroid_agegrp_subt = pd.concat(
                                [
                                 Thyroid_agegrp_subt
                                ,Thyroid_cnt_subt.iloc[:,i]
                                ,Thyroid_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
        
Thyroid_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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

Thyroid_agegrp_subt

#%%
value01 = Thyroid_per_subt.iloc[0,:-1].to_list()
value02 = Thyroid_per_subt.iloc[1,:-1].to_list()
value03 = Thyroid_per_subt.iloc[2,:-1].to_list()
value04 = Thyroid_per_subt.iloc[3,:-1].to_list()
value05 = Thyroid_per_subt.iloc[4,:-1].to_list()

label01 = rslttext[0]
label02 = rslttext[1]
label03 = rslttext[2]
label04 = rslttext[3]
label05 = rslttext[4]

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels, value01, width, label=label01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[2])
rects2 = ax.bar(labels, value02, width, label=label02
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[3])
rects3 = ax.bar(labels, value03, width, label=label03
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[4])
rects4 = ax.bar(labels, value04, width, label=label04
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[1])
rects5 = ax.bar(labels, value05, width, label=label05
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[0])

ax.set_title('연령별 갑상선초음파 Category 분포(2020년)\n\n',fontsize=30)
ax.set_ylabel(
                '(단위: %)' # 표시값
                 ,labelpad=-70 # 여백값 설정
                ,fontsize=20 # 글씨크기 설정
                ,rotation=0 # 회전값 조정
#                 ,ha='center' # 위치조정
                ,loc='top' # 위치조정, ha와 동시에 사용은 불가함.
            )
ax.yaxis.set_tick_params(labelsize=15) # y축 표시값 글씨크기 조정

ax.set_xticklabels(
                   labels
                  , fontsize=17
                  )

# Label with label_type 'center' instead of the default 'edge'
ax.bar_label(rects1, label_type='center',fontsize=16)
ax.bar_label(rects2, label_type='center',fontsize=16)
ax.bar_label(rects3, label_type='center',fontsize=16)
ax.bar_label(rects4, label_type='center',fontsize=16)
ax.bar_label(rects5, label_type='center',fontsize=16)

plt.text(-0.5, -12,  '갑상선초음파 Category 분류 기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.24)
          ,ncol=2  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -27, '          ', fontsize=17)

fig.tight_layout()
plt.savefig("{}/03_07_ThyroidUS_01cat_전체.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )

#%%
value01 = Thyroid_per_m.iloc[0,:-1].to_list()
value02 = Thyroid_per_m.iloc[1,:-1].to_list()
value03 = Thyroid_per_m.iloc[2,:-1].to_list()
value04 = Thyroid_per_m.iloc[3,:-1].to_list()
value05 = Thyroid_per_m.iloc[4,:-1].to_list()

label01 = rslttext[0][3:]
label02 = rslttext[1][3:]
label03 = rslttext[2][3:]
label04 = rslttext[3][3:]
label05 = rslttext[4][3:]

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels, value01, width, label=label01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[2])
rects2 = ax.bar(labels, value02, width, label=label02
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[3])
rects3 = ax.bar(labels, value03, width, label=label03
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[4])
rects4 = ax.bar(labels, value04, width, label=label04
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[1])
rects5 = ax.bar(labels, value05, width, label=label05
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[0])

ax.set_title('연령별 갑상선초음파 Category 분포(2020년, 남자)\n\n',fontsize=30)
ax.set_ylabel(
                '(단위: %)' # 표시값
                 ,labelpad=-70 # 여백값 설정
                ,fontsize=20 # 글씨크기 설정
                ,rotation=0 # 회전값 조정
#                 ,ha='center' # 위치조정
                ,loc='top' # 위치조정, ha와 동시에 사용은 불가함.
            )
ax.yaxis.set_tick_params(labelsize=15) # y축 표시값 글씨크기 조정

ax.set_xticklabels(
                   labels
                  , fontsize=17
                  )

# Label with label_type 'center' instead of the default 'edge'
ax.bar_label(rects1, label_type='center',fontsize=16)
ax.bar_label(rects2, label_type='center',fontsize=16)
ax.bar_label(rects3, label_type='center',fontsize=16)
ax.bar_label(rects4, label_type='center',fontsize=16)
ax.bar_label(rects5, label_type='center',fontsize=16)

plt.text(-0.5, -12,  '갑상선초음파 Category 분류 기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.24)
          ,ncol=2  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -27, '          ', fontsize=17)

fig.tight_layout()
plt.savefig("{}/03_07_ThyroidUS_02cat_남자.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )

#%%
value01 = Thyroid_per_f.iloc[0,:-1].to_list()
value02 = Thyroid_per_f.iloc[1,:-1].to_list()
value03 = Thyroid_per_f.iloc[2,:-1].to_list()
value04 = Thyroid_per_f.iloc[3,:-1].to_list()
value05 = Thyroid_per_f.iloc[4,:-1].to_list()

label01 = rslttext[0][3:]
label02 = rslttext[1][3:]
label03 = rslttext[2][3:]
label04 = rslttext[3][3:]
label05 = rslttext[4][3:]

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels, value01, width, label=label01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[2])
rects2 = ax.bar(labels, value02, width, label=label02
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[3])
rects3 = ax.bar(labels, value03, width, label=label03
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[4])
rects4 = ax.bar(labels, value04, width, label=label04
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[1])
rects5 = ax.bar(labels, value05, width, label=label05
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[0])

ax.set_title('연령별 갑상선초음파 Category 분포(2020년, 여자)\n\n',fontsize=30)
ax.set_ylabel(
                '(단위: %)' # 표시값
                 ,labelpad=-70 # 여백값 설정
                ,fontsize=20 # 글씨크기 설정
                ,rotation=0 # 회전값 조정
#                 ,ha='center' # 위치조정
                ,loc='top' # 위치조정, ha와 동시에 사용은 불가함.
            )
ax.yaxis.set_tick_params(labelsize=15) # y축 표시값 글씨크기 조정

ax.set_xticklabels(
                   labels
                  , fontsize=17
                  )

# Label with label_type 'center' instead of the default 'edge'
ax.bar_label(rects1, label_type='center',fontsize=16)
ax.bar_label(rects2, label_type='center',fontsize=16)
ax.bar_label(rects3, label_type='center',fontsize=16)
ax.bar_label(rects4, label_type='center',fontsize=16)
ax.bar_label(rects5, label_type='center',fontsize=16)

plt.text(-0.5, -12,  '갑상선초음파 Category 분류 기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.24)
          ,ncol=2  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -27, '          ', fontsize=17)

fig.tight_layout()
plt.savefig("{}/03_07_ThyroidUS_03cat_여자.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )
# %%
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # cact_agegrp_t.to_excel(writer,sheet_name="03_01이상지질혈증유병율")
    Thyroid_agegrp_subt.to_excel(writer,sheet_name="03_07_1Thy_C")
    Thyroid_agegrp.to_excel(writer,sheet_name="03_07_2Thy_C_GENDER")
# %%
