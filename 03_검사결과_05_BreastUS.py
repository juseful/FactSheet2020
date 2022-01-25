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
data = pd.read_stata('{}/RSLT_CD_EXMN.dta'.format(workdir))
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
exmn_cd = 'RS1190'
data = data.drop(data.loc[data['EXMN_CD']!=exmn_cd].index)
# data
# %%
GRP = "결절의심"
rsltcd01 = '1004'
rsltcd02 = '1005'
rsltcd03 = '1008'
rsltcd04 = '1032'
rsltcd05 = '1036'
rsltcd06 = '1049'
data['{}_YN'.format("nodule")] = (
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd01) | 
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd02) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd03) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd04) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd05) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd06)
    ).any(axis=1).astype(int)
data.loc[data['{}_YN'.format("nodule")] == 1,'{}_YN'.format("nodule")] = GRP
data.loc[data['{}_YN'.format("nodule")] == 0,'{}_YN'.format("nodule")] = "기타결과"
# data
#%%
# data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

# %%
RS1190_cnt_f = data_f.pivot_table(
                             index=['{}_YN'.format("nodule")]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RS1190_cnt_f.columns = RS1190_cnt_f.columns.droplevel()

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

RS1190_agegrp_f.columns = pd.MultiIndex.from_tuples(
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

labels = RS1190_cnt_f.columns[:-1].to_list()

# %%
value01 = RS1190_per_f.iloc[0,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
# rects1 = ax.bar(x,  value01, width, label='전체',color='cornflowerblue')
rects1 = ax.bar(x,  value01, width,label='결절 의심',color='coral')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 유방초음파 결과 분포(2020년)\n\n',fontsize=30)
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
plt.text(-0.3, -20, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_05_BreastUS_01유병률.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )
#%%
GRP2 = "Category"
# rsltcd_GRP2 = ['C0','C1','C2','C3','C4A','C4B','C4C','C5','C6']

# def rslt_match(x):
#     for i in rsltcd_GRP2:
#         if i in x:
#             return i
#         else:
#             return np.nan
        
# data[GRP2] = data.loc[:,'RSLT_CD01':'RSLT_CD13'].apply(rslt_match)
rsltcd01_2 = 'C0'
rsltcd02_2 = 'C1'
rsltcd03_2 = 'C2'
# rsltcd04_2 = 'C3'
# rsltcd05_2 = 'C4A'
# rsltcd06_2 = 'C4B'
# rsltcd07_2 = 'C4C'
# rsltcd08_2 = 'C5'
# rsltcd09_2 = 'C6'
# data[GRP2] = (
#     (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd01_2)
#     ).any(axis=1).astype(int)
# data.loc[data[GRP2] == 1, GRP2] = 'Category C0'
# data[GRP2] = (
#     (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd02_2)
#     ).any(axis=1).astype(int)
# data.loc[data[GRP2] == 1, GRP2] = 'Category 1'
# data[GRP2] = (
#     (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd03_2)
#     ).any(axis=1).astype(int)
# data.loc[data[GRP2] == 1, GRP2] = 'Category 2'
if ((data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd01_2).any(axis=1).astype(int))==1:
    data.loc[GRP2] = 'Category C0'
# elif (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd02_2).any(axis=1).astype(int) == 1:
#     data[GRP2] = 'Category C1'
# elif (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd03_2).any(axis=1).astype(int) == 1:
#     data[GRP2] = 'Category C2'

data
#%%
data_f
#%%
GRP2 = "Category"
data_f[GRP2] = ""
rsltcd_GRP2 = ['C0','C1','C2','C3','C4A','C4B','C4C','C5','C6']
rslttext = [
            'Category 0'
           ,'Category 1'
           ,'Category 2'
           ,'Category 3'
           ,'Category 4a'
           ,'Category 4b'
           ,'Category 4c'
           ,'Category 5'
           ,'Category 6'           
]

for i in range(len(rsltcd_GRP2)):
    data_f['CAT_{}'.format(i)] = (
        (data_f.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd_GRP2[i])
        ).any(axis=1).astype(int)
    data_f.loc[data_f['CAT_{}'.format(i)] == 1,'Category'] = rslttext[i]
    
data_f
#%%
data_f2 = data_f.drop(data_f.loc[data_f[GRP2]==""].index)
data_f2
#%%
RS1190_cnt_grp2 = data_f2.pivot_table(
                             index=[GRP2]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
RS1190_cnt_grp2.columns = RS1190_cnt_grp2.columns.droplevel()

# RS1190_cnt_f
# each column total value percentile
RS1190_per_grp2 = round(RS1190_cnt_grp2.div(RS1190_cnt_grp2.iloc[-1], axis=1).astype(float)*100,1)

# RS1190_per_f

RS1190_agegrp_grp2 = pd.DataFrame()

for i in range(len(RS1190_cnt_grp2.columns)):
    if i == 0:
        RS1190_agegrp_grp2 = pd.concat(
                                [
                                 RS1190_cnt_grp2.iloc[:,i]
                                ,RS1190_per_grp2.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        RS1190_agegrp_grp2 = pd.concat(
                                [
                                 RS1190_agegrp_grp2
                                ,RS1190_cnt_grp2.iloc[:,i]
                                ,RS1190_per_grp2.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# RS1190_agegrp_f

RS1190_agegrp_grp2.columns = pd.MultiIndex.from_tuples(
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

labels_grp2 = RS1190_cnt_grp2.columns[:-1].to_list()

# labels_grp2

# RS1190_agegrp_grp2
#%%
value01 = RS1190_per_grp2.iloc[0,:-1].to_list()
value02 = RS1190_per_grp2.iloc[1,:-1].to_list()
value03 = RS1190_per_grp2.iloc[2,:-1].to_list()
value04 = RS1190_per_grp2.iloc[3,:-1].to_list()
value05 = RS1190_per_grp2.iloc[4,:-1].to_list()
value06 = RS1190_per_grp2.iloc[5,:-1].to_list()
value07 = RS1190_per_grp2.iloc[6,:-1].to_list()
value08 = RS1190_per_grp2.iloc[7,:-1].to_list()
value09 = RS1190_per_grp2.iloc[8,:-1].to_list()

label01 = rslttext[0]
label02 = rslttext[1]
label03 = rslttext[2]
label04 = rslttext[3]
label05 = rslttext[4]
label06 = rslttext[5]
label07 = rslttext[6]
label08 = rslttext[7]
label09 = rslttext[8]


width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels, value01, width, label=label01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[5])
rects2 = ax.bar(labels, value02, width, label=label02
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[4])
rects3 = ax.bar(labels, value03, width, label=label03
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[6])
rects4 = ax.bar(labels, value04, width, label=label04
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[7])
rects5 = ax.bar(labels, value05, width, label=label05
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[8])
rects6 = ax.bar(labels, value06, width, label=label06
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i]+value05[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[3])
rects7 = ax.bar(labels, value07, width, label=label07
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i]+value05[i]+value06[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[2])
rects8 = ax.bar(labels, value08, width, label=label08
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i]+value05[i]+value06[i]+value07[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[1])
rects9 = ax.bar(labels, value09, width, label=label09
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i]+value05[i]+value06[i]+value07[i]+value08[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[0])

ax.set_title('연령별 유방초음파 Category 분포(2020년, 여자)\n\n',fontsize=30)
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
                   labels_grp2
                  , fontsize=17
                  )

# Label with label_type 'center' instead of the default 'edge'
ax.bar_label(rects1, label_type='center',fontsize=16)
ax.bar_label(rects2, label_type='center',fontsize=16)
ax.bar_label(rects3, label_type='center',fontsize=16)
ax.bar_label(rects4, label_type='center',fontsize=16)
ax.bar_label(rects5, label_type='center',fontsize=16)
ax.bar_label(rects6, label_type='center',fontsize=16)
ax.bar_label(rects7, label_type='center',fontsize=16)
ax.bar_label(rects8, label_type='center',fontsize=16)
ax.bar_label(rects9, label_type='center',fontsize=16)

plt.text(-0.5, -12,  '유방초음파 Category 분류 기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.24)
          ,ncol=4  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -27, '          ', fontsize=17)

fig.tight_layout()
plt.savefig("{}/03_05_BreastUS_02BreastUScat.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )
# %%
# data merge, export
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    RS1190_agegrp_f.to_excel(writer,sheet_name="03_05_1nodule")
    RS1190_agegrp_grp2.to_excel(writer,sheet_name="03_05_2category")

# %%
data_f.to_excel('{}/RS1190_CAT.xlsx'.format(workdir[:-5]),index=False)
                
#%%
RS1190_agegrp_f
# %%
