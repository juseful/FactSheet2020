#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.patches import ConnectionPatch
from matplotlib import font_manager,rc  #한글 폰트 입력을 위한 라이브러리

#폰트 경로 가져오기
font_path = 'C:\\Windows\\Fonts\\SGL.ttf' #삼성고딕체
 
# 폰트 이름 얻어오기
font_name = font_manager.FontProperties(fname=font_path).get_name()
 
#폰트 설정하기
mpl.rc('font',family=font_name)

#%%
workdir = "C:/Users/smcljy/data/20211115_Factsheet/data"
file_path = '{}/CaCT_SCORE.dta'.format(workdir)

data = pd.read_stata(file_path)

#%%
GRP = 'CACT'

data.loc[data['GEND_CD'] == 'M', 'GENDER'] = '남'
data.loc[data['GEND_CD'] == 'F', 'GENDER'] = '여'

data.loc[ data['AGE'] < 30                      ,'AGEGRP'] = '29세 이하'
data.loc[(data['AGE'] > 29) & (data['AGE'] < 40),'AGEGRP'] = '30~39세'
data.loc[(data['AGE'] > 39) & (data['AGE'] < 50),'AGEGRP'] = '40~49세'
data.loc[(data['AGE'] > 49) & (data['AGE'] < 60),'AGEGRP'] = '50~59세'
data.loc[(data['AGE'] > 59) & (data['AGE'] < 70),'AGEGRP'] = '60~69세'
data.loc[ data['AGE'] > 69                      ,'AGEGRP'] = '70세 이상'
# data.head(100)
data.loc[ data['AJ_130'] == 0                            ,'CACT'] = '01_No calcification(AJ-130 score = 0)'
data.loc[(data['AJ_130'] > 0)    & (data['AJ_130'] < 10) ,'CACT'] = '02_Minimal calcification(AJ-130 score 1 ~ 9)'
data.loc[(data['AJ_130'] >= 10)  & (data['AJ_130'] < 100),'CACT'] = '03_Mild calcification(AJ-130 score 10~99)'
data.loc[(data['AJ_130'] >= 100) & (data['AJ_130'] < 400),'CACT'] = '04_Moderate calcification(AJ-130 score 100 ~ 399)'
data.loc[ data['AJ_130'] >= 400                          ,'CACT'] = '05_Severe calcification(AJ-130 score 400 ~)'

# data

# data

#%%
data.loc[data['AJ_130'] != 0, 'CAL'] = '01_Cal'
data['CAL'].fillna('02_No',inplace=True)# data.loc[data['AJ_130'] == 0, 'CAL'] = '02_No'
data

#%%
coronary_cal_yn = data.pivot_table(
                              columns=['CAL']
                             ,values=['CDW'] 
                             ,aggfunc='count'
                             )
# coronary_cal_yn

label_pie = coronary_cal_yn.columns.to_list()
# label_pie

data_pie = coronary_cal_yn.iloc[0,:].to_list()

#%%
coronary_cal_cat = data.pivot_table(
                              columns=['CACT']
                             ,values=['CDW'] 
                             ,aggfunc='count'
                             )
coronary_cal_cat

data_bar = coronary_cal_cat.iloc[0,1:].to_list()
# data_bar

data_bar_per = []

for i in range(len(data_bar)):
    data_bar_per.append(round(data_bar[i]/data_pie[0],3))

# data_bar_per

label_bar = ['Minimal: AJ-130 1 ~ 9', 'Mild: AJ-130 10 ~ 99'
            ,'Moderate: AJ-130 100 ~ 399','Severe: AJ-130 400 ~'
            ]

# label_bar

#%%
# ### 특정 그룹 별도 저장
# cact_ctrl = data.drop(data.loc[data[GRP]!='비만'].index)
# cact_ctrl.loc[(cact_ctrl['TRT_MED_HYPERLIPIDEMIA'] == '1'), '{}_CTRL_YN'.format(GRP)] = '치료군'
# cact_ctrl['{}_CTRL_YN'.format(GRP)].fillna('비치료군',inplace=True)
# cact_ctrl
# cact_ctrl
data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)
# data_ctrl_m = cact_ctrl.drop(cact_ctrl.loc[cact_ctrl['GEND_CD']=='F'].index)
# data_ctrl_f = cact_ctrl.drop(cact_ctrl.loc[cact_ctrl['GEND_CD']=='M'].index)

#%%
## pivot table create
cact_cnt_m = data_m.pivot_table(
                             index=[GRP,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# cact_cnt_m
# cact_per_m = round(cact_cnt_m.div(cact_cnt_m.iloc[-1,-1], axis=0).astype(float)*100,1) # total value
# each column total value percentile
cact_per_m = round(cact_cnt_m.div(cact_cnt_m.iloc[-1], axis=1).astype(float)*100,1)

# cact_per_m

cact_agegrp_m = pd.DataFrame()

for i in range(len(cact_cnt_m.columns)):
    if i == 0:
        cact_agegrp_m = pd.concat(
                                [
                                 cact_cnt_m.iloc[:,i]
                                ,cact_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        cact_agegrp_m = pd.concat(
                                [
                                 cact_agegrp_m
                                ,cact_cnt_m.iloc[:,i]
                                ,cact_per_m.iloc[:,i]
                                ]
                            ,axis=1
        )
        
cact_agegrp_m

cact_cnt_f = data_f.pivot_table(
                             index=[GRP,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# empty group value insert with multi index
cact_cnt_f['CDW','29세 이하'] = [0, 0, 0, 0, 0, 0]
cact_cnt_f = cact_cnt_f.sort_index(axis=1)
# cact_cnt_f
# cact_per_f = round(cact_cnt_f.div(cact_cnt_f.iloc[-1,-1], axis=0).astype(float)*100,1) # total value
# each column total value percentile
cact_per_f = round(cact_cnt_f.div(cact_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

# empty group value insert with multi index
cact_per_f['CDW','29세 이하'] = [0, 0, 0, 0, 0, 0]
cact_per_f = cact_per_f.sort_index(axis=1)

# cact_per_f

cact_agegrp_f = pd.DataFrame()

for i in range(len(cact_cnt_f.columns)):
    if i == 0:
        cact_agegrp_f = pd.concat(
                                [
                                 cact_cnt_f.iloc[:,i]
                                ,cact_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        cact_agegrp_f = pd.concat(
                                [
                                 cact_agegrp_f
                                ,cact_cnt_f.iloc[:,i]
                                ,cact_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
        
cact_agegrp_f

cact_agegrp = pd.concat([cact_agegrp_m.iloc[:-1,:], cact_agegrp_f.iloc[:-1,:]],axis=0)
cact_agegrp

cact_agegrp.columns = pd.MultiIndex.from_tuples(
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
cact_agegrp = cact_agegrp.sort_index()

labels = []
for i in range(len(cact_per_m.columns)-1):
    labels.append(cact_per_m.columns[i][1])
    
cact_agegrp
    
#%%
cact_cnt_t = data.pivot_table(
                             index=[GRP]#,'GENDER']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# total value percentile
cact_per_t = round(cact_cnt_t.div(cact_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

cact_per_t

cact_agegrp_t = pd.DataFrame()

for i in range(len(cact_cnt_t.columns)):
    if i == 0:
        cact_agegrp_t = pd.concat(
                                [
                                 cact_cnt_t.iloc[:,i]
                                ,cact_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        cact_agegrp_t = pd.concat(
                                [
                                 cact_agegrp_t
                                ,cact_cnt_t.iloc[:,i]
                                ,cact_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

cact_agegrp_t.columns = cact_agegrp.columns = pd.MultiIndex.from_tuples(
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

cact_agegrp_t

#%%
# make figure and assign axis objects
fig = plt.figure(figsize=(12, 12))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
fig.subplots_adjust(wspace=0.1)

# pie chart parameters
ratios = data_pie
labels = ['Calcification','No']
explode = [0.05, 0]
colors = plt.get_cmap('Set2')(
np.linspace(0.15, 0.85, np.array(data_pie).shape[0])
)

# rotate so that first wedge is split by the x-axis
ax1.pie(ratios, autopct='%1.1f%%', startangle=-105,
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

# plt.text(-1.35, -0.005, '   ', fontsize=22)
plt.text(-1.35, -0.005,  '관상동맥 칼슘화 분류 기준:', fontsize=22)
lg = ax2.legend(label_bar
               ,bbox_to_anchor=(-0.85,-0.105)
               ,ncol=2  
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
plt.suptitle('관상동맥 칼슘화 분포(2020년)\n\n',fontsize=30)

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# fig.tight_layout()

plt.savefig("{}/03_01관상동맥칼슘화_00분포.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
           )
 
# plt.show()

#%%
# Bar chart create
value01 = cact_per_m.iloc[0,:-1].to_list()
value02 = cact_per_m.iloc[1,:-1].to_list()
value03 = cact_per_m.iloc[2,:-1].to_list()
value04 = cact_per_m.iloc[3,:-1].to_list()
value05 = cact_per_m.iloc[4,:-1].to_list()

label01 = 'No: AJ-130 = 0'
label02 = 'Minimal: AJ-130 1 ~ 9'
label03 = 'Mild: AJ-130 10 ~ 99'
label04 = 'Moderate: AJ-130 100 ~ 399'
label05 = 'Severe: AJ-130 400 ~'


width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels, value01, width, label=label01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[5])
rects2 = ax.bar(labels, value02, width, label=label02
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[4])
rects3 = ax.bar(labels, value03, width, label=label03
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects4 = ax.bar(labels, value04, width, label=label04
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])
rects5 = ax.bar(labels, value05, width, label=label05
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[0])

ax.set_title('연령별 관상동맥 칼슘화 분포(2020년, 남자)\n\n',fontsize=30)
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

plt.text(-0.5, -12,  '관상동맥 칼슘화 분류 기준', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.21)
          ,ncol=3  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -24, '          ', fontsize=17)
plt.text(-0.3, -27, '          ', fontsize=17)
plt.text(-0.3, -30, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_01관상동맥칼슘화_01남자분포.png".format(workdir[:-5])
            , dpi=175
            ,bbox_extra_artists=(lg,)
            # ,bbox_inches='tight'
            )

plt.show()
#%%
value01 = cact_per_f.iloc[0,:-1].to_list()
value02 = cact_per_f.iloc[1,:-1].to_list()
value03 = cact_per_f.iloc[2,:-1].to_list()
value04 = cact_per_f.iloc[3,:-1].to_list()
value05 = cact_per_f.iloc[4,:-1].to_list()

label01 = 'No: AJ-130 = 0'
label02 = 'Minimal: AJ-130 1 ~ 9'
label03 = 'Mild: AJ-130 10 ~ 99'
label04 = 'Moderate: AJ-130 100 ~ 399'
label05 = 'Severe: AJ-130 400 ~'


width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels, value01, width, label=label01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[5])
rects2 = ax.bar(labels, value02, width, label=label02
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[4])
rects3 = ax.bar(labels, value03, width, label=label03
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[2])
rects4 = ax.bar(labels, value04, width, label=label04
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])
rects5 = ax.bar(labels, value05, width, label=label05
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[0])

ax.set_title('연령별 관상동맥 칼슘화 분포(2020년, 여자)\n\n',fontsize=30)
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

plt.text(-0.5, -12,  '관상동맥 칼슘화 분류 기준', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.21)
          ,ncol=3  ,loc='lower left' ,fontsize=15
          )
plt.text(-0.3, -24, '          ', fontsize=17)
plt.text(-0.3, -27, '          ', fontsize=17)
plt.text(-0.3, -30, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_01관상동맥칼슘화_02여자분포.png".format(workdir[:-5])
            , dpi=175
            ,bbox_extra_artists=(lg,)
            # ,bbox_inches='tight'
            )

plt.show()

#%%
# data merge, export
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # cact_agegrp_t.to_excel(writer,sheet_name="03_01이상지질혈증유병율")
    cact_agegrp.to_excel(writer,sheet_name="03_01관상동맥칼슘화성별분포")
# %%
