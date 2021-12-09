# %%
import pandas as pd
import json

# import mapboxgl
import os
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.io as pio

import plotly.offline as pyo
#plotly offline 모드 변경
pyo.init_notebook_mode()
# %%
workdir = ''
filepath1 = '{}/HPC_CNT.dta'.format(workdir)

df = pd.read_stata(filepath1)

df = df.rename(columns={'PROVIENCE_cd':'CTPRVN_CD'})
# %%
filepath3 = '{}/rok0_008.zip.geojson'.format(workdir)
state_geo2 = json.load(open(filepath3,encoding='utf-8'))

# state_geo2
# %%
# # carto-positron에 mapping해 보았으나 색이 칠해지지 않는 지역이 있음. finetunnig이 필요한듯....
# fig = px.choropleth_mapbox( df
#                            ,geojson=state_geo2
#                            ,locations='PROVIENCE'
#                            ,color='CNT'
#                            ,color_continuous_scale='bluyl'
# #                            ,range_color=(0,1)
#                            ,mapbox_style="carto-positron"#"carto-positron"#"open-street-map"#
#                            ,featureidkey='properties.CTP_KOR_NM'
#                            ,zoom=7.1
#                            ,center={"lat":36.2, "lon":127.8}
#                            ,opacity=1
#                            ,labels={'CNT':'수진인원'}
#                           )
# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(title=dict(text="지역별 수진현황(2020년)"
#                             ,font_size=60
#                             ,x=0.5
#                             ,y=0.975
#                             )
#                  )#, **layout_setting)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# pio.write_image( fig
#                 ,"{}/01_02지역별수진현황_01전국_sample4.png".format(workdir[:-5])
#                 ,width=1728, height=1584
#                 # ,scale=1.5
#                )

# fig.show()
#%%
df
# %%
fig = px.choropleth( df
                    ,geojson=state_geo2
                    ,locations='PROVIENCE'
                    ,color='CNT'
                    ,color_continuous_scale='bluyl'
                    ,featureidkey='properties.CTP_KOR_NM'
                    ,labels={'CNT':'수진인원'}
                    )
# 이거 설정해 주지 않으면 세계 지도 나와버림.
fig.update_geos( fitbounds="geojson"
                ,visible=False
                ,projection=dict(type="mercator" # 지도를 보여주는 방식. mercator, miller, orthographic type recommend
                                ,scale=1.5
                                )
                ,bgcolor="whitesmoke"
                #  ,center=dict(lat=37, lon=120)
               )

fig.update_layout(margin={"r":30,"t":30,"l":30,"b":30})
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(#title=dict(text="지역별 수진현황(2020년, 전국)"
                #             ,font_size=30
                #             ,x=0.5
                #             ,y=0.975
                #             )
                #  ,
                paper_bgcolor="whitesmoke"
                 )#, **layout_setting)
# fig.add_annotation(dict(font_size=15,
#                         x=0.1,
#                         y=-0.05,
#                         showarrow=False,
#                         text="<b>2020년 건진 수진자의 약 46%가 서울시에, 약 31%가 경기도에 거주하였다.</b>",
#                         textangle=0,
#                         xanchor='left',
#                         xref="paper",
#                         yref="paper"))
# pio.write_image( fig
#                 ,"{}/01_02지역별수진현황_01전국_t.png".format(workdir[:-5])
#                 ,width=864, height=792
#                 ,scale=2
#                )

fig.show()

# %%
filepath4 = '{}/HPC_SUDO.dta'.format(workdir)

df_sudo = pd.read_stata(filepath4)

# df_sudo
filepath5 = '{}/seoul.zip.geojson'.format(workdir)
state_seoul = json.load(open(filepath5,encoding='utf-8'))

# state_seoul

#%%
fig = px.choropleth( df_sudo
                    ,geojson=state_seoul
                    ,locations='SIG_ENG_NM'
                    ,color='CNT'
                    ,color_continuous_scale='bluyl'
                    ,featureidkey='properties.SIG_ENG_NM'
                    ,labels={'CNT':'수진인원'}
                    )
# 이거 설정해 주지 않으면 세계 지도 나와버림.
fig.update_geos( fitbounds="geojson"
                ,visible=False
                ,projection=dict(type="mercator" # 지도를 보여주는 방식. mercator, miller, orthographic 추천
                                ,scale=1.5
                                )
                ,bgcolor="whitesmoke"
#                 ,center=dict(lat=37, lon=126.986)
               )

fig.update_layout(margin={"r":30,"t":30,"l":30,"b":30})
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(#title=dict(text="지역별 수진현황(2020년, 서울)"
                #             ,font_size=30
                #             ,x=0.5
                #             ,y=0.975
                #             )
                #  ,
                 paper_bgcolor="whitesmoke"
                 )#, **layout_setting)

# pio.write_image( fig
#                 ,"{}/01_02지역별수진현황_02서울.png".format(workdir[:-5])
#                 ,width=864, height=792
#                 ,scale=2
#                )

fig.show()
# %%
filepath6 = '{}/gyeonggi.zip.geojson'.format(workdir)
state_gyeonggi = json.load(open(filepath6,encoding='utf-8'))

# state_gyeonggi
#%%
fig = px.choropleth( df_sudo
                    ,geojson=state_gyeonggi
                    ,locations='SIG_ENG_NM'
                    ,color='CNT'
                    ,color_continuous_scale='bluyl'
                    ,featureidkey='properties.SIG_ENG_NM'
                    ,labels={'CNT':'수진인원'}
                    )
# 이거 설정해 주지 않으면 세계 지도 나와버림.
fig.update_geos( fitbounds="geojson"
                ,visible=False
                ,projection=dict(type="mercator" # 지도를 보여주는 방식. mercator, miller, orthographic type recommend
                                ,scale=1.5
                                )
                ,bgcolor="whitesmoke"
#                 ,center=dict(lat=37, lon=126.986)
               )

fig.update_layout(margin={"r":30,"t":30,"l":30,"b":30})
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(#title=dict(text="지역별 수진현황(2020년, 경기)"
                #             ,font_size=30
                #             ,x=0.5
                #             ,y=0.975
                #             )
                #  ,
                 paper_bgcolor="whitesmoke"
                 )#, **layout_setting)

# pio.write_image( fig
#                 ,"{}/01_02지역별수진현황_03경기.png".format(workdir[:-5])
#                 ,width=864, height=792
#                 ,scale=2
#                )

fig.show()

# %%
# data merge, export
with pd.ExcelWriter('{}/FACTSHEET_2020_TABLE.xlsx'.format(workdir[:-5]), mode='a',engine='openpyxl') as writer:
    df.to_excel(writer,sheet_name="01_02지역별", index=False)
    df_sudo.to_excel(writer,sheet_name="01_02지역별_수도권", index=False)
# %%
