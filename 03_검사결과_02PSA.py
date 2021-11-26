#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib import font_manager,rc  #한글 폰트 입력을 위한 라이브러리
from pathlib import Path

#폰트 경로 가져오기
font_path = 'C:\Windows\Fonts\SGL.ttf' #삼성고딕체
 
# 폰트 이름 얻어오기
font_name = font_manager.FontProperties(fname=font_path).get_name()
 
#폰트 설정하기
mpl.rc('font',family=font_name)
# %%
workdir = ""

file_path = '{}/BL3713.dta'.format(workdir)

BL3713 = pd.read_stata(file_path)

# 30세 미만은 버림
BL3713 = BL3713.drop(BL3713.loc[BL3713['AGE']<30].index)
# BL3713

#%% 
# 데이터 편집
# BL3713.loc[ BL3713['AGE'] < 30                        ,'AGEGRP'] = '0~29yrs'
BL3713.loc[(BL3713['AGE'] > 29) & (BL3713['AGE'] < 40),'AGEGRP'] = '30~39세'
BL3713.loc[(BL3713['AGE'] > 39) & (BL3713['AGE'] < 50),'AGEGRP'] = '40~49세'
BL3713.loc[(BL3713['AGE'] > 49) & (BL3713['AGE'] < 60),'AGEGRP'] = '50~59세'
BL3713.loc[(BL3713['AGE'] > 59) & (BL3713['AGE'] < 70),'AGEGRP'] = '60~69세'
BL3713.loc[ BL3713['AGE'] > 69                        ,'AGEGRP'] = '70세 이상'
BL3713
BL3713 = BL3713.astype({'EXRS_NCVL_VL': 'float'})
GRP = 'PSA'
BL3713.loc[ BL3713['EXRS_NCVL_VL'] < 2.5                                      ,GRP] = 'Group1'#'0~2.4'
BL3713.loc[(BL3713['EXRS_NCVL_VL'] >= 2.500) & (BL3713['EXRS_NCVL_VL'] < 4.0) ,GRP] = 'Group2'#''2.5~3.9'
BL3713.loc[(BL3713['EXRS_NCVL_VL'] >= 4.000) & (BL3713['EXRS_NCVL_VL'] < 10.0),GRP] = 'Group3'#''4.0~9.9'
BL3713.loc[(BL3713['EXRS_NCVL_VL'] >= 10.000)                                 ,GRP] = 'Group4'#''10.0~'
BL3713
# nan 값 확인
BL3713.loc[BL3713['EXRS_NCVL_VL'] == 'nan']
# %%
# pivot table
psa_cnt = BL3713.pivot_table(
                             index=[GRP]
                            ,columns=['AGEGRP']
    ,values=['ID']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )

# psa_cnt
psa_per = round(psa_cnt.div(len(BL3713), axis=0).astype(float)*100,1).add_suffix("(%)")

# psa_per
psa_table = pd.DataFrame()

for i in range(len(psa_cnt.columns)):
    if i == 0:
        psa_table = pd.concat(
                                [
                                 psa_cnt.iloc[:,i]
                                ,psa_per.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        psa_table = pd.concat(
                                [
                                 psa_table
                                ,psa_cnt.iloc[:,i]
                                ,psa_per.iloc[:,i]
                                ]
                            ,axis=1
        )
        
# psa_table

# 각 열합계를 기준으로 한 비율 구하기
psa_agegrp_per = round(psa_cnt.div(psa_cnt.iloc[-1],axis=1).astype(float)*100,1)

# psa_agegrp_per

labels = []

for i in psa_cnt.columns[:-1]:
    labels.append(i[1])
    
labels

labels_per = []

for i in psa_per.columns:
    labels_per.append(i)
    
# labels_per

# %%
value = psa_cnt.iloc[-1,:-1]

fig, ax = plt.subplots(figsize=(12, 11), subplot_kw=dict(aspect="equal"),linewidth=2)
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

ax.set_title("PSA 연령별 검사 현황(2020년)",fontsize=35)

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

plt.setp(autotexts, size=20, weight="bold") # 내부 text 속성 수정

fig.tight_layout()

plt.savefig("{}/03_02PSA_01검사현황.png".format(workdir[:-5]))

plt.show()
# %%
value01 = psa_per.iloc[0,:-1]
value02 = psa_per.iloc[1,:-1]
value03 = psa_per.iloc[2,:-1]
value04 = psa_per.iloc[3,:-1]

label1 = '0~2.4 ng/ml'
label2 = '2.5~3.9 ng/ml'
label3 = '4.0~9.9 ng/ml'
label4 = '10.0~ ng/ml'

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.22  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 11))#,linewidth=2) # 캔버스 배경 사이즈 설정
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# rects1 = ax.bar(x - width-0.17 , value01, width, label=label1,color='lightslategray') RdYlBu
rects1 = ax.bar(x - width-0.15, value01, width, label=label1, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[3])
rects2 = ax.bar(x - width+0.1 , value02, width, label=label2, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[4])
rects3 = ax.bar(x + width-0.1 , value03, width, label=label3, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])
rects4 = ax.bar(x + width+0.15, value04, width, label=label4, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[0])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('PSA 결과 분포(2020년)\n',fontsize=30)
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
        ax.annotate(height, # 천단위마다 콤마 표시
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 8),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom'
                   ,fontsize=18
                   )

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)
# autolabel(rects3)

plt.text(-0.7, -4,  'PSA 분류기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.18)
          ,ncol=4  ,loc='lower left' ,fontsize=15
          )

fig.tight_layout()

plt.savefig("{}/03_02PSA_02결과분포.png".format(workdir[:-5]))

plt.show()

#%%
# psa_agegrp_per.iloc[0,:-1].to_list()
labels
# %%
value01 = psa_agegrp_per.iloc[0,:-1].to_list()
value02 = psa_agegrp_per.iloc[1,:-1].to_list()
value03 = psa_agegrp_per.iloc[2,:-1].to_list()
value04 = psa_agegrp_per.iloc[3,:-1].to_list()

label1 = '0~2.4 ng/ml'
label2 = '2.5~3.9 ng/ml'
label3 = '4.0~9.9 ng/ml'
label4 = '10.0~ ng/ml'

wCDWth = 0.5       # the wCDWth of the bars: can also be len(x) sequence

fig, ax = plt.subplots(figsize=(12, 11))#,linewCDWth=2) # 캔버스 배경 사이즈 설정
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정


rects1 = ax.bar(labels, value01, wCDWth, label=label1
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[3])
rects2 = ax.bar(labels, value02, wCDWth, label=label2
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[4])
rects3 = ax.bar(labels, value03, wCDWth, label=label3
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[1])
rects4 = ax.bar(labels, value04, wCDWth, label=label4
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(labels).shape[0]))[0])

ax.set_title('PSA 연령별 결과 분포(2020년)\n',fontsize=30)
ax.set_ylabel(
                '(단위: %)\n' # 표시값
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

plt.text(-0.45, -10,  'PSA 분류기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(-0.01,-0.18)
          ,ncol=4  ,loc='lower left' ,fontsize=15
          )

fig.tight_layout()

plt.savefig("{}/03_02PSA_03연령별결과분포.png".format(workdir[:-5]))

plt.show()
# %%
