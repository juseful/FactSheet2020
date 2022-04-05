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
file_path = '{}/BMD_DATA.dta'.format(workdir)

data = pd.read_stata(file_path)

#%%
data.loc[data['GEND_CD'] == 'M', 'GENDER'] = '남'
data.loc[data['GEND_CD'] == 'F', 'GENDER'] = '여'

data.loc[ data['AGE'] < 30                      ,'AGEGRP'] = '29세 이하'
data.loc[(data['AGE'] > 29) & (data['AGE'] < 40),'AGEGRP'] = '30~39세'
data.loc[(data['AGE'] > 39) & (data['AGE'] < 50),'AGEGRP'] = '40~49세'
data.loc[(data['AGE'] > 49) & (data['AGE'] < 60),'AGEGRP'] = '50~59세'
data.loc[(data['AGE'] > 59) & (data['AGE'] < 70),'AGEGRP'] = '60~69세'
data.loc[ data['AGE'] > 69                      ,'AGEGRP'] = '70세 이상'

# %% 결과별 정리
GRP01 = "골감소증"
bmd_rslt_cd01 = ['113','123','13','131','132','133','213','223','23','231','232','233'
                ,'31','311','312','313','32','321','322','323','33','331','332','333'
                ]

data[GRP01] = (
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[0]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[1]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[2]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[3]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[4]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[5]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[6]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[7]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[8]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[9]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[10]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[11]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[12]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[13]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[14]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[15]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[16]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[17]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[18]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[19]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[20]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[21]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[22]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd01[23])
    ).any(axis=1).astype(int)
data.loc[data[GRP01] == 1,GRP01] = GRP01
data.loc[data[GRP01] == 0,GRP01] = "기타결과"

GRP02 = "골다공증"
bmd_rslt_cd02 = ['112','12','121','122','123','132','21','211','212','213','22','221'
                ,'222','223','23','231','232','233','312','32','321','322','323','332'
                ]
data[GRP02] = (
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[0]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[1]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[2]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[3]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[4]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[5]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[6]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[7]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[8]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[9]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[10]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[11]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[12]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[13]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[14]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[15]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[16]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[17]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[18]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[19]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[20]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[21]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[22]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd02[23])
    ).any(axis=1).astype(int)
data.loc[data[GRP02] == 1,GRP02] = GRP02
data.loc[data[GRP02] == 0,GRP02] = "기타결과"

GRP03 = "골밀도정상"
bmd_rslt_cd03 = ['11','111']
data[GRP03] = (
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd03[0]) |
    (data.loc[:,'RSLT_CD01':'RSLT_CD03'] == bmd_rslt_cd03[1])
    ).any(axis=1).astype(int)
data.loc[data[GRP03] == 1,GRP03] = GRP03
data.loc[data[GRP03] == 0,GRP03] = "기타결과"
# data.loc[(data['{}_YN'.format(GRP01)] == "기타결과") & (data['{}_YN'.format(GRP02)] == "기타결과"),GRP03] = GRP03
# data.loc[data[GRP03] !="정상",GRP03] = "기타결과"

# data

#%%
# ### 특정 그룹 별도 저장
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

#%%
## pivot table create
## GRP01-골감소증
BMD_GRP01_cnt_m = data_m.pivot_table(
                             index=[GRP01,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# each column total value percentile
BMD_GRP01_per_m = round(BMD_GRP01_cnt_m.div(BMD_GRP01_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

BMD_GRP01_agegrp_m = pd.DataFrame()

for i in range(len(BMD_GRP01_cnt_m.columns)):
    if i == 0:
        BMD_GRP01_agegrp_m = pd.concat(
                                [
                                 BMD_GRP01_cnt_m.iloc[:,i]
                                ,BMD_GRP01_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        BMD_GRP01_agegrp_m = pd.concat(
                                [
                                 BMD_GRP01_agegrp_m
                                ,BMD_GRP01_cnt_m.iloc[:,i]
                                ,BMD_GRP01_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# BMD_GRP01_agegrp_m

BMD_GRP01_cnt_f = data_f.pivot_table(
                             index=[GRP01,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# each column total value percentile
BMD_GRP01_per_f = round(BMD_GRP01_cnt_f.div(BMD_GRP01_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

BMD_GRP01_agegrp_f = pd.DataFrame()

for i in range(len(BMD_GRP01_cnt_f.columns)):
    if i == 0:
        BMD_GRP01_agegrp_f = pd.concat(
                                [
                                 BMD_GRP01_cnt_f.iloc[:,i]
                                ,BMD_GRP01_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        BMD_GRP01_agegrp_f = pd.concat(
                                [
                                 BMD_GRP01_agegrp_f
                                ,BMD_GRP01_cnt_f.iloc[:,i]
                                ,BMD_GRP01_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# BMD_GRP01_agegrp_f

#%%
## pivot table create
## GRP02-골다공증
BMD_GRP02_cnt_m = data_m.pivot_table(
                             index=[GRP02,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# each column total value percentile
BMD_GRP02_per_m = round(BMD_GRP02_cnt_m.div(BMD_GRP02_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

BMD_GRP02_agegrp_m = pd.DataFrame()

for i in range(len(BMD_GRP02_cnt_m.columns)):
    if i == 0:
        BMD_GRP02_agegrp_m = pd.concat(
                                [
                                 BMD_GRP02_cnt_m.iloc[:,i]
                                ,BMD_GRP02_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        BMD_GRP02_agegrp_m = pd.concat(
                                [
                                 BMD_GRP02_agegrp_m
                                ,BMD_GRP02_cnt_m.iloc[:,i]
                                ,BMD_GRP02_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# BMD_GRP02_agegrp_m

BMD_GRP02_cnt_f = data_f.pivot_table(
                             index=[GRP02,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# each column total value percentile
BMD_GRP02_per_f = round(BMD_GRP02_cnt_f.div(BMD_GRP02_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

BMD_GRP02_agegrp_f = pd.DataFrame()

for i in range(len(BMD_GRP02_cnt_f.columns)):
    if i == 0:
        BMD_GRP02_agegrp_f = pd.concat(
                                [
                                 BMD_GRP02_cnt_f.iloc[:,i]
                                ,BMD_GRP02_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        BMD_GRP02_agegrp_f = pd.concat(
                                [
                                 BMD_GRP02_agegrp_f
                                ,BMD_GRP02_cnt_f.iloc[:,i]
                                ,BMD_GRP02_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# BMD_GRP02_agegrp_f

#%%
## pivot table create
## GRP03-정상
BMD_GRP03_cnt_m = data_m.pivot_table(
                             index=[GRP03,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# each column total value percentile
BMD_GRP03_per_m = round(BMD_GRP03_cnt_m.div(BMD_GRP03_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

BMD_GRP03_agegrp_m = pd.DataFrame()

for i in range(len(BMD_GRP03_cnt_m.columns)):
    if i == 0:
        BMD_GRP03_agegrp_m = pd.concat(
                                [
                                 BMD_GRP03_cnt_m.iloc[:,i]
                                ,BMD_GRP03_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        BMD_GRP03_agegrp_m = pd.concat(
                                [
                                 BMD_GRP03_agegrp_m
                                ,BMD_GRP03_cnt_m.iloc[:,i]
                                ,BMD_GRP03_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# BMD_GRP03_agegrp_m

BMD_GRP03_cnt_f = data_f.pivot_table(
                             index=[GRP03,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# each column total value percentile
BMD_GRP03_per_f = round(BMD_GRP03_cnt_f.div(BMD_GRP03_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

BMD_GRP03_agegrp_f = pd.DataFrame()

for i in range(len(BMD_GRP03_cnt_f.columns)):
    if i == 0:
        BMD_GRP03_agegrp_f = pd.concat(
                                [
                                 BMD_GRP03_cnt_f.iloc[:,i]
                                ,BMD_GRP03_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        BMD_GRP03_agegrp_f = pd.concat(
                                [
                                 BMD_GRP03_agegrp_f
                                ,BMD_GRP03_cnt_f.iloc[:,i]
                                ,BMD_GRP03_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# BMD_GRP03_agegrp_f

#%%
# table data concat
BMD_rslt_m = pd.concat(
                        [BMD_GRP01_agegrp_m.iloc[0,:]
                        ,BMD_GRP02_agegrp_m.iloc[0,:]
                        ,BMD_GRP03_agegrp_m.iloc[0,:]
                        ,BMD_GRP03_agegrp_m.iloc[-1,:]
                        ]
                        ,axis=1
                      ).T
BMD_rslt_m.columns = BMD_rslt_m.columns = pd.MultiIndex.from_tuples(
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

# BMD_rslt_m

BMD_rslt_f = pd.concat(
                        [BMD_GRP01_agegrp_f.iloc[0,:]
                        ,BMD_GRP02_agegrp_f.iloc[0,:]
                        ,BMD_GRP03_agegrp_f.iloc[0,:]
                        ,BMD_GRP03_agegrp_f.iloc[-1,:]
                        ]
                        ,axis=1
                      ).T

BMD_rslt_f.columns = BMD_rslt_f.columns = pd.MultiIndex.from_tuples(
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

# BMD_rslt_f

#%%
# Bar chart create
labels = []
for i in range(len(BMD_GRP01_per_m.columns)-1):
    labels.append(BMD_GRP01_per_m.columns[i][1])
    
value01 = BMD_GRP01_per_m.iloc[0,:-1].to_list()
value02 = BMD_GRP02_per_m.iloc[0,:-1].to_list()
value03 = BMD_GRP03_per_m.iloc[0,:-1].to_list()

label01 = '골감소증'
label02 = '골다공증'
label03 = '정상'

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
# rects1 = ax.bar(x,  value01, width, label='전체',color='cornflowerblue')
rects1 = ax.bar(labels, value01, width, label=label01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects2 = ax.bar(labels, value02, width, label=label02
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])
rects3 = ax.bar(labels, value03, width, label=label03
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[4])

ax.set_title('연령별 골밀도 검사결과 분포(2020년, 남자)\n\n',fontsize=30)
ax.set_ylabel(
                '(단위: %)' # 표시값
                 ,labelpad=-70 # 여백값 설정
                ,fontsize=20 # 글씨크기 설정
                ,rotation=0 # 회전값 조정
#                 ,ha='center' # 위치조정
                ,loc='top' # 위치조정, ha와 동시에 사용은 불가함.
            )
ax.yaxis.set_tick_params(labelsize=0) # y축 표시값 글씨크기 조정

ax.set_xticklabels(
                   labels
                  , fontsize=17
                  )

lg = ax.legend(bbox_to_anchor=(-0.01,-0.175)
          ,ncol=3  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.5, -12,  '골밀도 결과분류 기준', fontsize=22)
plt.text(-0.3, -24, '          ', fontsize=17)
plt.text(-0.3, -27, '          ', fontsize=17)
plt.text(-0.3, -30, '          ', fontsize=17)

# Label with label_type 'center' instead of the default 'edge'
ax.bar_label(rects1, label_type='center',fontsize=16)
ax.bar_label(rects2, label_type='center',fontsize=16)
ax.bar_label(rects3, label_type='center',fontsize=16)

fig.tight_layout()

plt.savefig("{}/03_11골밀도_01남자분포.png".format(workdir[:-5])
            , dpi=175
            ,bbox_extra_artists=(lg,)
            # ,bbox_inches='tight'
            )

plt.show()
#%%
value01 = BMD_GRP01_per_f.iloc[0,:-1].to_list()
value02 = BMD_GRP02_per_f.iloc[0,:-1].to_list()
value03 = BMD_GRP03_per_f.iloc[0,:-1].to_list()

label01 = '골감소증'
label02 = '골다공증'
label03 = '정상'

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
# rects1 = ax.bar(x,  value01, width, label='전체',color='cornflowerblue')
rects1 = ax.bar(labels, value01, width, label=label01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects2 = ax.bar(labels, value02, width, label=label02
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])
rects3 = ax.bar(labels, value03, width, label=label03
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[4])

ax.set_title('연령별 골밀도 검사결과 분포(2020년, 여자)\n\n',fontsize=30)
ax.set_ylabel(
                '(단위: %)' # 표시값
                 ,labelpad=-70 # 여백값 설정
                ,fontsize=20 # 글씨크기 설정
                ,rotation=0 # 회전값 조정
#                 ,ha='center' # 위치조정
                ,loc='top' # 위치조정, ha와 동시에 사용은 불가함.
            )
ax.yaxis.set_tick_params(labelsize=0) # y축 표시값 글씨크기 조정

ax.set_xticklabels(
                   labels
                  , fontsize=17
                  )

lg = ax.legend(bbox_to_anchor=(-0.01,-0.155)
          ,ncol=3  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.5, -12,  '골밀도 결과분류 기준', fontsize=22)
plt.text(-0.3, -24, '          ', fontsize=17)
plt.text(-0.3, -27, '          ', fontsize=17)
plt.text(-0.3, -30, '          ', fontsize=17)

# Label with label_type 'center' instead of the default 'edge'
ax.bar_label(rects1, label_type='center',fontsize=16)
ax.bar_label(rects2, label_type='center',fontsize=16)
ax.bar_label(rects3, label_type='center',fontsize=16)

fig.tight_layout()

plt.savefig("{}/03_11골밀도_02여자분포.png".format(workdir[:-5])
            , dpi=175
            ,bbox_extra_artists=(lg,)
            # ,bbox_inches='tight'
            )

plt.show()

#%%
# data merge, export
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # obd_agegrp_t.to_excel(writer,sheet_name="02_04이상지질혈증유병율")
    BMD_rslt_m.to_excel(writer,sheet_name="03_11골밀도분포남자")
    BMD_rslt_f.to_excel(writer,sheet_name="03_11골밀도분포여자")
# %%
