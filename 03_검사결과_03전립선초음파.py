#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib import font_manager,rc  #한글 폰트 입력을 위한 라이브러리
from pathlib import Path

#폰트 경로 가져오기
font_path = 'C:\\Windows\\Fonts\\SGL.ttf' #삼성고딕체
 
# 폰트 이름 얻어오기
font_name = font_manager.FontProperties(fname=font_path).get_name()
 
#폰트 설정하기
mpl.rc('font',family=font_name)
# %%
workdir = "C:/Users/smcljy/data/20211115_Factsheet/data"

file_path = '{}/RS1140N.dta'.format(workdir)

RS1140 = pd.read_stata(file_path)

# 40세 미만은 버림
RS1140 = RS1140.drop(RS1140.loc[RS1140['AGE']<40].index)
# RS1140

#%% 
# 데이터 편집
RS1140.loc[ RS1140['AGE'] < 30                        ,'AGEGRP'] = '0~29세'
RS1140.loc[(RS1140['AGE'] > 29) & (RS1140['AGE'] < 40),'AGEGRP'] = '30~39세'
RS1140.loc[(RS1140['AGE'] > 39) & (RS1140['AGE'] < 50),'AGEGRP'] = '40~49세'
RS1140.loc[(RS1140['AGE'] > 49) & (RS1140['AGE'] < 60),'AGEGRP'] = '50~59세'
RS1140.loc[(RS1140['AGE'] > 59) & (RS1140['AGE'] < 70),'AGEGRP'] = '60~69세'
RS1140.loc[ RS1140['AGE'] > 69                        ,'AGEGRP'] = '70세 이상'

GRP = 'BPH'

RS1140.loc[(RS1140['BPH_YN'] != 'Y') & (RS1140['MILD_BPH_YN'] != 'Y') ,GRP] = '0~25.0'
RS1140.loc[(RS1140['BPH_YN'] != 'Y') & (RS1140['MILD_BPH_YN'] == 'Y') ,GRP] = '25.1~30.0'
RS1140.loc[(RS1140['BPH_YN'] == 'Y') & (RS1140['MILD_BPH_YN'] != 'Y') ,GRP] = '30.1~'

# nan 값 확인
RS1140.loc[RS1140[GRP] == 'nan']

# %%
# pivot table
bph_cnt = RS1140.pivot_table(
                             index=[GRP]
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# bph_cnt
bph_per = round(bph_cnt.div(len(RS1140), axis=0).astype(float)*100,1).add_suffix("(%)")

# bph_per
bph_table = pd.DataFrame()

for i in range(len(bph_cnt.columns)):
    if i == 0:
        bph_table = pd.concat(
                                [
                                 bph_cnt.iloc[:,i]
                                ,bph_per.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bph_table = pd.concat(
                                [
                                 bph_table
                                ,bph_cnt.iloc[:,i]
                                ,bph_per.iloc[:,i]
                                ]
                            ,axis=1
        )

bph_table.columns = pd.MultiIndex.from_tuples(
        (
         ('40~49세', 'N')
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
        
# bph_table

# 각 열합계를 기준으로 한 비율 구하기
bph_agegrp_per = round(bph_cnt.div(bph_cnt.iloc[-1],axis=1).astype(float)*100,1)

bph_table_agegrp = pd.DataFrame()

for i in range(len(bph_cnt.columns)):
    if i == 0:
        bph_table_agegrp = pd.concat(
                                [
                                 bph_cnt.iloc[:,i]
                                ,bph_agegrp_per.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bph_table_agegrp = pd.concat(
                                [
                                 bph_table_agegrp
                                ,bph_cnt.iloc[:,i]
                                ,bph_agegrp_per.iloc[:,i]
                                ]
                            ,axis=1
        )

bph_table_agegrp.columns = pd.MultiIndex.from_tuples(
        (
         ('40~49세', 'N')
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

# bph_agegrp_per

labels = []

for i in bph_cnt.columns[:-1]:
    labels.append(i[1])
    
labels

labels_per = []

for i in bph_per.columns:
    labels_per.append(i)
    
# labels_per

# bph_table
# bph_table_agegrp
# %%
value = bph_cnt.iloc[-1,:-1]

fig, ax = plt.subplots(figsize=(12, 15), subplot_kw=dict(aspect="equal"),linewidth=2)
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

ax.set_title("연령별 전립선초음파 검사 현황(2020년)\n\n",fontsize=35)

def func(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals)))
#     return "{:.1f}%\n({:,d})".format(pct, absolute) # %값(수치)로 표현하고 싶을 때, 1000 단위 마다 (,)표시하기
    return "{:,d}\n({:.1f}%)".format(absolute, pct) # 수치(%값)로 표현하고 싶을 때1000 단위미다 ','표시

wedgeprop={'width': 0.4, 'edgecolor': 'lightgray', 'linewidth': 1}
wedges, texts, autotexts = ax.pie(value, autopct=lambda pct: func(pct, value)
                                 ,pctdistance=0.8 # 숫자를 표시하는 거리, 중앙점 기준
                                 ,startangle=90 # 시작점 각도. 90이 일반적으로 상단가운데점. 기준은 가운데 평행선 우측기준
                                 ,counterclock=False
                                 #,shadow=True
                                 # 색상선택 명령어 참조 https://matplotlib.org/stable/tutorials/colors/colormaps.html
                                 ,colors= plt.get_cmap('Spectral')(
                                                                    np.linspace(0.15, 0.85, np.array(value).shape[0])
                                                                  )
                                 ,wedgeprops=wedgeprop
                                 #,wedgeprops=dict(width=0.45) 
                                 ,textprops=dict(color="black",size=18,weight='heavy')
                                 ,rotatelabels=True
                                 )

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=10, va="center"
         ,size=20)

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(labels[i], xy=(x, y), xytext=(1.1*np.sign(x), 1.1*y),
                horizontalalignment=horizontalalignment, **kw)

plt.setp(autotexts, size=20, weight="bold") # 내부 text 속성 수정plt.text(-0.3, -1.2  , '          ', fontsize=17)
plt.text(-0.3, -1.2  , '          ', fontsize=17)
plt.text(-0.3, -1.5, '          ', fontsize=17)
plt.text(-0.3, -1.8, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_10전립선초음파_01검사현황.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
            )

plt.show()
# %%
# value01 = bph_per.iloc[0,:-1]
# value02 = bph_per.iloc[1,:-1]
# value03 = bph_per.iloc[2,:-1]

# label1 = bph_cnt.index[0]+' ml'
# label2 = bph_cnt.index[1]+' ml'
# label3 = bph_cnt.index[2]+' ml'

# x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
# width = 0.25  # the width of the bars

# # fig, ax = plt.subplots()
# fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정
# fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# # rects1 = ax.bar(x - width-0.17 , value01, width, label=label1,color='lightslategray') RdYlBu
# rects1 = ax.bar(x - width-0.03, value01, width, label=label1, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[3])
# rects2 = ax.bar(x             , value02, width, label=label2, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])
# rects3 = ax.bar(x + width+0.03, value03, width, label=label3, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[0])

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_title('전립선초음파 결과 분포(2020년)\n\n',fontsize=30)
# ax.set_ylabel(
#                 '(단위: %)' # 표시값
#                  ,labelpad=-70 # 여백값 설정
#                 ,fontsize=20 # 글씨크기 설정
#                 ,rotation=0 # 회전값 조정
# #                 ,ha='center' # 위치조정
#                 ,loc='top' # 위치조정, ha와 동시에 사용은 불가함.
#             )
# ax.yaxis.set_tick_params(labelsize=15) # y축 표시값 글씨크기 조정
# ax.set_xticks(x)
# ax.set_xticklabels(
#                    labels[0:len(labels)] # all 값이 list에는 포함되지 않았기 때문임.
#                   , fontsize=17
#                   )

# # bar위에 값 label 표시
# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate(height, # 천단위마다 콤마 표시
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 8),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom'
#                    ,fontsize=18
#                    )

# autolabel(rects1)
# autolabel(rects2)
# autolabel(rects3)

# plt.text(-0.6, -3,  '전립선초음파 결과 분류기준:', fontsize=22)
# lg = ax.legend(bbox_to_anchor=(-0.01,-0.23)
#           ,title='Prostate volume', title_fontsize=17
#           ,ncol=4  ,loc='lower left' ,fontsize=15
#           )
# plt.text(-0.3, -6.75, '          ', fontsize=17)

# fig.tight_layout()

# plt.savefig("{}/03_03전립선초음파_02결과분포.png".format(workdir[:-5])
#             , dpi=175 #72의 배수 ,edgecolor='black'
#             )

# plt.show()

#%%
# bph_agegrp_per.iloc[0,:-1].to_list()
labels
# %%
value01 = bph_agegrp_per.iloc[0,:-1].to_list()
value02 = bph_agegrp_per.iloc[1,:-1].to_list()
value03 = bph_agegrp_per.iloc[2,:-1].to_list()
value04 = bph_agegrp_per.iloc[3,:-1].to_list()

label1 = bph_cnt.index[0]+' ml'
label2 = bph_cnt.index[1]+' ml'
label3 = bph_cnt.index[2]+' ml'

wCDWth = 0.5       # the wCDWth of the bars: can also be len(x) sequence

fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정


rects1 = ax.bar(labels, value01, wCDWth, label=label1
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[3])
rects2 = ax.bar(labels, value02, wCDWth, label=label2
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])
rects3 = ax.bar(labels, value03, wCDWth, label=label3
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[0])

ax.set_title('연령별 전립선초음파 결과 분포(2020년)\n\n',fontsize=30)
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

plt.text(-0.4, -12,  '전립선초음파 결과 분류기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.205)
          ,title='Prostate volume', title_fontsize=17
          ,ncol=4  ,loc='lower left' ,fontsize=15
          )
# plt.text(-0.4, -25, '          ', fontsize=17)
plt.text(-0.4, -31, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_10전립선초음파_03연령별결과분포.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
            )

plt.show()
# %%
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # cact_agegrp_t.to_excel(writer,sheet_name="03_01이상지질혈증유병율")
    bph_table.to_excel(writer,sheet_name="03_10BPH")
    bph_table_agegrp.to_excel(writer,sheet_name="03_10BPH_agegrp")
# %%
