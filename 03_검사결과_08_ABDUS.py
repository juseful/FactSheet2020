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
# 다른 검사 제외
exmn_cd = 'RS10'
data = data[data['EXMN_CD'].str.contains(exmn_cd)]
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
GRP1 = "Fatty_YN"
GRP2 = "Category"
# data[GRP1] = ""
rsltcd_GRP = ['0007','0056','0003','0057','0002','0058','0054']
rslttext = [
            '01_Minimal'
           ,'02_Minimal to mild'
           ,'03_Mild'
           ,'04_Mild to Moderate'
           ,'05_Moderate'
           ,'06_Moderate to Severe'
           ,'07_Severe'
           ]

for i in range(len(rsltcd_GRP)):
    data['CAT_{}'.format(i)] = (
        (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd_GRP[i])
        ).any(axis=1).astype(int)
    data.loc[data['CAT_{}'.format(i)] == 1,GRP1] = "01_Fattyliver"
    data.loc[data['CAT_{}'.format(i)] == 1,GRP2] = rslttext[i]

data[GRP1].fillna('02_Absent',inplace=True)
data[GRP2].fillna('00_Absent',inplace=True)
# data.loc[data[GRP1] == "",GRP1] = '08_Absent'
    
data

#%%
fattyliver_yn = data.pivot_table(
                              columns=[GRP1]
                             ,values=['ID'] 
                             ,aggfunc='count'
                             )
fattyliver_yn

label_pie = fattyliver_yn.columns.to_list()
# label_pie

data_pie = fattyliver_yn.iloc[0,:].to_list()
data_pie

#%%
fattyliver_cat = data.pivot_table(
                              columns=[GRP2]
                             ,values=['ID'] 
                             ,aggfunc='count'
                            #  ,margins=True
                             )
fattyliver_cat

data_bar = fattyliver_cat.iloc[0,1:-1].to_list()
# data_bar

data_bar_per = []

for i in range(len(data_bar)):
    data_bar_per.append(round(data_bar[i]/data_pie[0],4))

# data_bar_per

label_bar = []
cat_columns = fattyliver_cat.columns.to_list()[1:-1]
for i in range(len(cat_columns)):
    label_bar.append(cat_columns[i][3:])

# label_bar

#%%
# make figure and assign axis objects
fig = plt.figure(figsize=(12, 12))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
fig.subplots_adjust(wspace=0.1)

# pie chart parameters
ratios = data_pie
labels = ['Fatty liver','Absent']
explode = [0.05, 0]
colors = plt.get_cmap('Set2')(
np.linspace(0.15, 0.85, np.array(data_pie).shape[0])
)

# rotate so that first wedge is split by the x-axis
ax1.pie(ratios, autopct='%1.1f%%', startangle=-75,
labels=labels, explode=explode, colors=colors
,textprops=dict(color="black",fontsize=25)
)

# bar chart parameters
xpos = 0
bottom = 0
ratios = data_bar_per #bar chart using category percentile
width = .2
colors = plt.get_cmap('coolwarm')(
np.linspace(0.15, 0.85, np.array(data_bar_per).shape[0])
)

for j in range(len(ratios)):
    height = ratios[j]
    ax2.bar(xpos, height, width, bottom=bottom, color=colors[j])
    ypos = bottom + ax2.patches[j].get_height() / 2
    bottom += height
    ax2.text(xpos, ypos, "%1.1f%%" % (ax2.patches[j].get_height() * 100),
             ha='center',color="black",fontsize=15)
# ax2.text(xpos, ypos, "%d%%" % (ax2.patches[j].get_height() * 100),
# ha='center')

ax2.set_title('분포(%)', fontsize=17)

plt.text(-1.35, -0.005,  '복부초음파 지방간 분류 기준:', fontsize=22)
lg = ax2.legend(label_bar
               ,bbox_to_anchor=(-0.85,-0.105)
               ,ncol=3  ,loc='lower left' ,fontsize=15
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
con = ConnectionPatch(xyA=(- width / 2, bar_height), xyB=(x, y),
coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
con.set_linewidth(2)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(- width / 2, 0), xyB=(x, y), coordsA="data",
coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(2)
 
# ax1.set_title("복부초음파에서 지방간 현황(2020년)\n\n",fontsize=30)
# ax2.set_title("  \n\n",fontsize=30)
# all subplot's title setting
plt.suptitle('복부초음파 지방간 분포(2020년)\n\n',fontsize=30)

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# fig.tight_layout()

# plt.savefig("{}/03_08_ABDUS_01Fattylivercat.png".format(workdir[:-5])
#             , dpi=175 #72의 배수 ,edgecolor='black'
#            )
 
# plt.show()

#%%
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

#%%
fattyliver_cnt_m = data_m.pivot_table(
                                    index=[GRP2,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# fattyliver_cnt_m

# Thyroid_cnt_m.columns = Thyroid_cnt_m.columns.droplevel()
# each column total value percentile
fattyliver_per_m = round(fattyliver_cnt_m.div(fattyliver_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

fattyliver_agegrp_m = pd.DataFrame()

for i in range(len(fattyliver_cnt_m.columns)):
    if i == 0:
        fattyliver_agegrp_m = pd.concat(
                                [
                                 fattyliver_cnt_m.iloc[:,i]
                                ,fattyliver_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        fattyliver_agegrp_m = pd.concat(
                                [
                                 fattyliver_agegrp_m
                                ,fattyliver_cnt_m.iloc[:,i]
                                ,fattyliver_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# fattyliver_agegrp_m

# %%
fattyliver_cnt_f = data_f.pivot_table(
                                    index=[GRP2,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# fattyliver_cnt_f

# Thyroid_cnt_m.columns = Thyroid_cnt_m.columns.droplevel()
# each column total value percentile
fattyliver_per_f = round(fattyliver_cnt_f.div(fattyliver_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

fattyliver_agegrp_f = pd.DataFrame()

for i in range(len(fattyliver_cnt_f.columns)):
    if i == 0:
        fattyliver_agegrp_f = pd.concat(
                                [
                                 fattyliver_cnt_f.iloc[:,i]
                                ,fattyliver_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        fattyliver_agegrp_f = pd.concat(
                                [
                                 fattyliver_agegrp_f
                                ,fattyliver_cnt_f.iloc[:,i]
                                ,fattyliver_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# fattyliver_agegrp_f

# %%
fattyliver_agegrp = pd.concat([fattyliver_agegrp_m, fattyliver_agegrp_f],axis=0)
fattyliver_agegrp = fattyliver_agegrp.sort_index()

fattyliver_agegrp.columns = pd.MultiIndex.from_tuples(
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
labels = fattyliver_per_m.columns[:-1].droplevel().to_list()
# labels

fattyliver_agegrp

# %%
fattyliver_cnt_t = data.pivot_table(
                                    index=[GRP2]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# total value percentile
fattyliver_per_t = round(fattyliver_cnt_t.div(fattyliver_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# ABD_P_CYST_per_t

fattyliver_agegrp_t = pd.DataFrame()

for i in range(len(fattyliver_cnt_t.columns)):
    if i == 0:
        fattyliver_agegrp_t = pd.concat(
                                [
                                 fattyliver_cnt_t.iloc[:,i]
                                ,fattyliver_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        fattyliver_agegrp_t = pd.concat(
                                [
                                 fattyliver_agegrp_t
                                ,fattyliver_cnt_t.iloc[:,i]
                                ,fattyliver_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

fattyliver_agegrp_t.columns = pd.MultiIndex.from_tuples(
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

fattyliver_agegrp_t
# %%
fattyliver_cnt_subt = data.pivot_table(
                                    index=[GRP2]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )


# total value percentile
fattyliver_per_subt = round(fattyliver_cnt_subt.div(fattyliver_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# ABD_P_CYST_per_subt

fattyliver_agegrp_subt = pd.DataFrame()

for i in range(len(fattyliver_cnt_subt.columns)):
    if i == 0:
        fattyliver_agegrp_subt = pd.concat(
                                [
                                 fattyliver_cnt_subt.iloc[:,i]
                                ,fattyliver_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        fattyliver_agegrp_subt = pd.concat(
                                [
                                 fattyliver_agegrp_subt
                                ,fattyliver_cnt_subt.iloc[:,i]
                                ,fattyliver_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
        
fattyliver_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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

fattyliver_agegrp_subt

#%%
value01 = fattyliver_per_m.iloc[0,:-1].to_list()
value02 = fattyliver_per_m.iloc[1,:-1].to_list()
value03 = fattyliver_per_m.iloc[2,:-1].to_list()
value04 = fattyliver_per_m.iloc[3,:-1].to_list()
value05 = fattyliver_per_m.iloc[4,:-1].to_list()
value06 = fattyliver_per_m.iloc[5,:-1].to_list()
value07 = fattyliver_per_m.iloc[6,:-1].to_list()

label01 = 'Absent'
label02 = 'Minimal'
label03 = 'Mild'
label04 = 'Mild to Moderate'
label05 = 'Moderate'
label06 = 'Moderate to Severe'
label07 = 'Severe'

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels, value01, width, label=label01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[4])
rects2 = ax.bar(labels, value02, width, label=label02
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[5])
rects3 = ax.bar(labels, value03, width, label=label03
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[6])
rects4 = ax.bar(labels, value04, width, label=label04
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[3])
rects5 = ax.bar(labels, value05, width, label=label05
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[2])
rects6 = ax.bar(labels, value06, width, label=label06
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i]+value05[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[1])
rects7 = ax.bar(labels, value07, width, label=label07
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i]+value05[i]+value06[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[0])

ax.set_title('연령별 복부초음파 지방간 분포(2020년, 남자)\n\n',fontsize=30)
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
ax.bar_label(rects6, label_type='center',fontsize=16)
ax.bar_label(rects7, label_type='center',fontsize=16)

plt.text(-0.5, -12,  '복부초음파 지방간 분류 기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.205)
          ,ncol=4  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -27, '          ', fontsize=17)

fig.tight_layout()
plt.savefig("{}/03_08_ABDUS_02성별지방간분포_남자.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )

#%%
value01 = fattyliver_per_f.iloc[0,:-1].to_list()
value02 = fattyliver_per_f.iloc[1,:-1].to_list()
value03 = fattyliver_per_f.iloc[2,:-1].to_list()
value04 = fattyliver_per_f.iloc[3,:-1].to_list()
value05 = fattyliver_per_f.iloc[4,:-1].to_list()
value06 = fattyliver_per_f.iloc[5,:-1].to_list()
value07 = fattyliver_per_f.iloc[6,:-1].to_list()

label01 = 'Absent'
label02 = 'Minimal'
label03 = 'Mild'
label04 = 'Mild to Moderate'
label05 = 'Moderate'
label06 = 'Moderate to Severe'
label07 = 'Severe'

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels, value01, width, label=label01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[4])
rects2 = ax.bar(labels, value02, width, label=label02
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[5])
rects3 = ax.bar(labels, value03, width, label=label03
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[6])
rects4 = ax.bar(labels, value04, width, label=label04
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[3])
rects5 = ax.bar(labels, value05, width, label=label05
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[2])
rects6 = ax.bar(labels, value06, width, label=label06
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i]+value05[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[1])
rects7 = ax.bar(labels, value07, width, label=label07
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i]+value05[i]+value06[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[0])

ax.set_title('연령별 복부초음파 지방간 분포(2020년, 여자)\n\n',fontsize=30)
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
ax.bar_label(rects6, label_type='center',fontsize=16)
ax.bar_label(rects7, label_type='center',fontsize=16)

plt.text(-0.5, -12,  '복부초음파 지방간 분류 기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.205)
          ,ncol=4  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -27, '          ', fontsize=17)

fig.tight_layout()
plt.savefig("{}/03_08_ABDUS_03성별지방간분포_여자.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )
# %%
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # cact_agegrp_t.to_excel(writer,sheet_name="03_01이상지질혈증유병율")
    fattyliver_agegrp_subt.to_excel(writer,sheet_name="03_08_1ABDUS_FL")
    fattyliver_agegrp.to_excel(writer,sheet_name="03_08_2ABDUS_FL_GENDER")
# %%
fattyliver_cat
# %%
