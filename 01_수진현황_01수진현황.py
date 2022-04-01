# %%
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
workdir = 'C:/Users/smcljy/data/20211115_Factsheet/data'
data = pd.read_stata('{}/SMHIS_2020.dta'.format(workdir))

data.loc[data['GEND_CD'] == 'M', 'GENDER'] = '남자'
data.loc[data['GEND_CD'] == 'F', 'GENDER'] = '여자'

data.loc[data['AGEGRP2'] =='~29'  , 'AGEGRP2'] = '29세 이하'
data.loc[data['AGEGRP2'] =='30~39', 'AGEGRP2'] = '30~39세'
data.loc[data['AGEGRP2'] =='40~49', 'AGEGRP2'] = '40~49세'
data.loc[data['AGEGRP2'] =='50~59', 'AGEGRP2'] = '50~59세'
data.loc[data['AGEGRP2'] =='60~69', 'AGEGRP2'] = '60~69세'
data.loc[data['AGEGRP2'] =='70~'  , 'AGEGRP2'] = '70세 이상'

# data
# %%
# pivot table create
# margins=True면 total값이 같이 나오지만, 피봇테이블 컬럼 변경을 위해 미적용
pivot_gend_cnt = data.pivot_table(index=['YYYY', 'GENDER'], columns=['AGEGRP2'], values=['ID'], aggfunc='count', margins=True)

pivot_gend_cnt
# 각 행의 총합을 기준으로 백분율이 설정되어야 함.
# pivot_gend_cnt2[('ID', 'All')] 이게 기준 값이 되는 것임.
pivot_gend_per = round(pivot_gend_cnt.div(pivot_gend_cnt[('ID', 'All')], axis=0).astype(float)*100,2).add_suffix("(%)")
# pivot_gend_per = round(pivot_gend_cnt.div(pivot_gend_cnt.iloc[-1], axis=1).astype(float)*100,1)
pivot_gend_per

pivot_gend = pd.DataFrame() # 빈 DataFrame 만들기

for i in range(len(pivot_gend_cnt.columns)):
    if i == 0:
        pivot_gend = pd.concat(
                                [
                                    pivot_gend_cnt.iloc[:,i]
                                   ,pivot_gend_per.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        pivot_gend = pd.concat(
                                [
                                 pivot_gend
                                ,pivot_gend_cnt.iloc[:,i]
                                ,pivot_gend_per.iloc[:,i]
                                ]
                            ,axis=1
        )

pivot_gend_label = []

for i in range(len(pivot_gend.columns)):
    pivot_gend_label.append(pivot_gend.columns[i][1])

pivot_gend.columns = pd.MultiIndex.from_tuples(
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

pivot_gend
# %%
labels = []

for i in pivot_gend_cnt.columns[:-1]:
    labels.append(i[1])
    
labels
# %%
value01 = pivot_gend_cnt.iloc[2,:-1]
label01 = '전체'

x = np.arange(len(labels))
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(12, 15))#,linewidth=2) # 캔버스 배경 사이즈 설정
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

rects1 = ax.bar(x, value01, width, label=label01, color='darkmagenta')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 수진현황(2020년)\n\n',fontsize=30)
ax.set_ylabel(
                '(단위: 명)' # 표시값
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
        ax.annotate('{:,d}'.format(height), # 천단위마다 콤마 표시
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 8),  # X points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom'
                   ,fontsize=18
                   )

autolabel(rects1)

plt.text(-0.3, -2000, ' ', fontsize=17)
plt.text(-0.3, -3000, ' ', fontsize=22)
plt.text(-0.3, -4000, ' ', fontsize=17)
plt.text(-0.3, -5000, ' ', fontsize=17)
plt.text(-0.3, -6000, ' ', fontsize=17)
plt.text(-0.3, -7000, ' ', fontsize=17)
plt.text(-0.3, -8000, ' ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/01_01수진현황_01전체.png".format(workdir[:-5])
            # ,edgecolor='black'
            , dpi=175)

# plt.show()
# %%
value01 = pivot_gend_cnt.iloc[0,:-1]
value02 = pivot_gend_cnt.iloc[1,:-1]

label01 = '남자'
label02 = '여자'

x = np.arange(len(labels))
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(12, 15))#,linewidth=2) # 캔버스 배경 사이즈 설정
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

rects1 = ax.bar(x - 0.2, value01, width, label=label01,color='cornflowerblue')
rects2 = ax.bar(x + 0.2, value02, width, label=label02,color='salmon')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('성별 수진현황(2020년)\n\n',fontsize=30)
ax.set_ylabel(
                '(단위: 명)' # 표시값
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
        ax.annotate('{:,d}'.format(height), # 천단위마다 콤마 표시
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 8),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom'
                   ,fontsize=18
                   )

autolabel(rects1)
autolabel(rects2)

plt.text(-0.3, -1000, ' ', fontsize=17)
plt.text(-0.3, -1500, ' ', fontsize=22)
plt.text(-0.3, -2000, ' ', fontsize=17)
plt.text(-0.3, -2500, ' ', fontsize=17)
plt.text(-0.3, -3000, ' ', fontsize=17)
plt.text(-0.3, -3500, ' ', fontsize=17)
plt.text(-0.3, -4000, ' ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/01_01수진현황_02성별.png".format(workdir[:-5])
            # ,edgecolor='black'
            , dpi=175)

plt.show()
# %%
pivot_gend.to_excel('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]),sheet_name="01_수진현황")
# %%
