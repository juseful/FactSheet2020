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
exmn_cd = 'BP2E0'
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
GRP = "PAP결과"
# data[GRP1] = ""
rsltcd_GRP = ['0003','00032','00033'
             ,'0005'
             ,'0006'
             ,'0007'
             ,'0008'
             ]
rslttext = [
            '01_비정형성 상피세포(Atypical Squamous Cells)','01_비정형성 상피세포(Atypical Squamous Cells)','01_비정형성 상피세포(Atypical Squamous Cells)'
           ,'02_경도경관 상피 이형성증(Mild dysplasia/CIN I)'
           ,'03_중등도경관 상피 이형성증(Moderate dysplasia/CIN II)'
           ,'04_고도경관 상피 이형성증(Severe dysplasia/CIN III)'
           ,'05_자궁경부 상피내 암종(Carcinoma in Situ))'
           ]

for i in range(len(rsltcd_GRP)):
    data['CAT_{}'.format(i)] = (
        (data.loc[:,'RSLT_CD01':'RSLT_CD13'] == rsltcd_GRP[i])
        ).any(axis=1).astype(int)
    data.loc[data['CAT_{}'.format(i)] == 1,GRP] = rslttext[i]

data[GRP].fillna('00_Absent',inplace=True)
# data.loc[data[GRP1] == "",GRP1] = '08_Absent'
    
data
#%%
# data_m = data.drop(data.loc[data['GEND_CD']=='F'].index)
data_f = data.drop(data.loc[data['GEND_CD']=='M'].index)

# %%
liquiprep_cnt_f = data_f.pivot_table(
                                    index=[GRP,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# liquiprep_cnt_f

# each column total value percentile
liquiprep_per_f = round(liquiprep_cnt_f.div(liquiprep_cnt_f.iloc[-1], axis=1).astype(float)*100,1)

liquiprep_agegrp_f = pd.DataFrame()

for i in range(len(liquiprep_cnt_f.columns)):
    if i == 0:
        liquiprep_agegrp_f = pd.concat(
                                [
                                 liquiprep_cnt_f.iloc[:,i]
                                ,liquiprep_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        liquiprep_agegrp_f = pd.concat(
                                [
                                 liquiprep_agegrp_f
                                ,liquiprep_cnt_f.iloc[:,i]
                                ,liquiprep_per_f.iloc[:,i]
                                ]
                            ,axis=1
        )

liquiprep_agegrp_f = liquiprep_agegrp_f.sort_index()

liquiprep_agegrp_f.columns = pd.MultiIndex.from_tuples(
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

liquiprep_agegrp_f

# multi level column to single level
labels = liquiprep_per_f.columns[:-1].droplevel().to_list()
# labels

# %%
liquiprep_cnt_t = data_f.pivot_table(
                                    index=[GRP]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )

# total value percentile
liquiprep_per_t = round(liquiprep_cnt_t.div(liquiprep_cnt_t.iloc[-1,-1], axis=0).astype(float)*100,1)

# ABD_P_CYST_per_t

liquiprep_agegrp_t = pd.DataFrame()

for i in range(len(liquiprep_cnt_t.columns)):
    if i == 0:
        liquiprep_agegrp_t = pd.concat(
                                [
                                 liquiprep_cnt_t.iloc[:,i]
                                ,liquiprep_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        liquiprep_agegrp_t = pd.concat(
                                [
                                 liquiprep_agegrp_t
                                ,liquiprep_cnt_t.iloc[:,i]
                                ,liquiprep_per_t.iloc[:,i]
                                ]
                            ,axis=1
        )

liquiprep_agegrp_t.columns = pd.MultiIndex.from_tuples(
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

liquiprep_agegrp_t
# %%
liquiprep_cnt_subt = data_f.pivot_table(
                                    index=[GRP]#,'GENDER']
                                    ,columns=['AGEGRP']
                                    ,values=['ID']
                                    ,aggfunc='count'
                                    ,margins=True
                                    ,fill_value=0
                                    )


# total value percentile
liquiprep_per_subt = round(liquiprep_cnt_subt.div(liquiprep_cnt_subt.iloc[-1], axis=1).astype(float)*100,1)

# ABD_P_CYST_per_subt

liquiprep_agegrp_subt = pd.DataFrame()

for i in range(len(liquiprep_cnt_subt.columns)):
    if i == 0:
        liquiprep_agegrp_subt = pd.concat(
                                [
                                 liquiprep_cnt_subt.iloc[:,i]
                                ,liquiprep_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        liquiprep_agegrp_subt = pd.concat(
                                [
                                 liquiprep_agegrp_subt
                                ,liquiprep_cnt_subt.iloc[:,i]
                                ,liquiprep_per_subt.iloc[:,i]
                                ]
                            ,axis=1
        )
        
liquiprep_agegrp_subt.columns = pd.MultiIndex.from_tuples(
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

liquiprep_agegrp_subt

#%%
value02 = liquiprep_per_f.iloc[1,:-1].to_list()
value03 = liquiprep_per_f.iloc[2,:-1].to_list()
value04 = [0, 0, 0, 0, 0, 0] # liquiprep_per_f.iloc[3,:-1].to_list()
value05 = liquiprep_per_f.iloc[3,:-1].to_list()
value06 = [0, 0, 0, 0, 0, 0] # liquiprep_per_f.iloc[5,:-1].to_list()

label02 = rslttext[0][3:]
label03 = rslttext[3][3:]
label04 = rslttext[4][3:]
label05 = rslttext[5][3:]
label06 = rslttext[6][3:]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.15  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(12, 15),linewidth=2) # 캔버스 배경 사이즈 설정
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# rects1 = ax.bar(x - width-0.17 , value01, width, label=label1,color='lightslategray') RdYlBu
rects2 = ax.bar(x - width-0.2 , value02, width, label=label02, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[5])
rects3 = ax.bar(x - width-0.03, value03, width, label=label03, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[6])
rects4 = ax.bar(x             , value04, width, label=label04, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[3])
rects5 = ax.bar(x + width+0.03, value05, width, label=label05, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[2])
rects6 = ax.bar(x + width+0.2 , value06, width, label=label06, color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(rslttext).shape[0]))[1])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 액상자궁세포검사 결과 분포(2020년, 여자)\n\n',fontsize=30)
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


autolabel(rects2)
autolabel(rects3)
autolabel(rects4)
autolabel(rects5)
autolabel(rects6)
# autolabel(rects3)

plt.text(-0.5, -0.4,  '액상자궁세포검사 결과 분류 기준:', fontsize=22)
lg = ax.legend(bbox_to_anchor=(0.03,-0.30)
        #   ,ncol=2  
          ,loc='lower left' ,fontsize=15
          )
# plt.text(-0.3, -26, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_08_액상자궁세포검사결과.png".format(workdir[:-5])
            , dpi=175 #72의 배수 ,edgecolor='black'
            )

# plt.show()

# %%
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    # cact_agegrp_t.to_excel(writer,sheet_name="03_01이상지질혈증유병율")
    # liquiprep_agegrp_subt.to_excel(writer,sheet_name="03_09_1액상자궁세포")
    liquiprep_agegrp_f.to_excel(writer,sheet_name="03_08_1액상자궁세포검사")
# %%
