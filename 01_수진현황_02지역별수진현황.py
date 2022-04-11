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
pio.renderers.default = "notebook_connected"
# import add module
import plotly.graph_objects as go
import geopandas as gpd
# pyo.renderers.default = "vscode"
# %%
workdir = 'C:/Users/smcljy/data/20211115_Factsheet/data'
filepath1 = '{}/HPC_CNT.dta'.format(workdir)

df = pd.read_stata(filepath1)

df = df.rename(columns={'PROVIENCE_cd':'CTPRVN_CD'})
# %%
filepath3 = '{}/rok0_008.zip.geojson'.format(workdir)
state_geo2 = json.load(open(filepath3,encoding='utf-8'))

# state_geo2
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
#                         # text="<b>2020년 건진 수진자의 약 46%가 서울시에, 약 31%가 경기도에 거주하였다.</b>",
#                         textangle=0,
#                         xanchor='left',
#                         xref="paper",
#                         yref="paper"))
# pio.write_image( fig
#                 ,"{}/01_02지역별수진현황_01전국.png".format(workdir[:-5])
#                 ,width=864, height=792
#                 ,scale=2
#                )

fig.show()

#%%
# 수도권(서울+경기도) 수진자 분포
filepath4 = '{}/HPC_SUDO.dta'.format(workdir)
df_sudo = pd.read_stata(filepath4)

filepath6 = '{}/gyeonggi.zip.geojson'.format(workdir)
state_sudo = json.load(open(filepath6,encoding='utf-8'))

fig = px.choropleth( df_sudo
                    ,geojson=state_sudo
                    ,locations='SIG_ENG_NM'
                    ,color='CNT'
                    ,color_continuous_scale='bluyl'#'bluyl'
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
# fig.add_scattergeo(
#   geojson=state_sudo,
#   locations = df_sudo['SIG_ENG_NM'],
#   text = df_sudo['CNT'],
#   featureidkey="properties.SIG_ENG_NM",
#   textfont={"size":13,"color":"orangered"},# orangered
#   textposition="middle center",
# #   textfont={"size":15,"lat":gdf.geometry.centroid.y,"lon":gdf.geometry.centroid.x},
# #   lat=gdf.geometry.centroid.y,
# #   lon=gdf.geometry.centroid.x,
#   mode = 'text')


fig.update_layout(margin={"r":30,"t":30,"l":30,"b":30})
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(#title=dict(text="지역별 수진현황(2020년, 수도권)"
                #             ,font_size=30
                #             ,x=0.5
                #             ,y=0.975
                #             )
                #  ,
                 paper_bgcolor="whitesmoke"
                 )#, **layout_setting)
# pio.write_image( fig
#                 ,"{}/01_02지역별수진현황_02수도권.png".format(workdir[:-5])
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
filepath4 = '{}/HPC_SUDO.dta'.format(workdir)
df_sudo = pd.read_stata(filepath4)

# df_sudo
filepath5 = '{}/seoul.zip.geojson'.format(workdir)
state_seoul = json.load(open(filepath5,encoding='utf-8'))

# state_seoul
# #%%
# df_sudo
# #%%
# gdf_sudo = (
#     gpd.GeoDataFrame.from_features(state_seoul)
#     .merge(df_sudo, on="SIG_CD")
#     .assign(lat=lambda d: d.geometry.centroid.y, lon=lambda d: d.geometry.centroid.x)
#     .set_index("SIG_CD", drop=False)
# )

# gdf_sudo
# # %%
fig = px.choropleth( df_sudo
                    ,geojson=state_seoul
                    ,locations='SIG_ENG_NM'
                    ,color='CNT'
                    ,color_continuous_scale='bluyl' # magenta, oranges, sunsetdark, teal
# ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
# 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
# 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
# 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
# 'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
# 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
# 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
# 'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
# 'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
# 'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
# 'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
# 'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
# 'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
# 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
# 'ylorrd']
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

fig.add_scattergeo(
  geojson=state_seoul,
  locations = df_sudo['SIG_ENG_NM'],
  text = df_sudo['CNT'],
  featureidkey="properties.SIG_ENG_NM",
  textfont={"size":27,"color":"chocolate"},# orangered
# - A named CSS color:
# aliceblue, antiquewhite, aqua, aquamarine, azure,
# beige, bisque, black, blanchedalmond, blue,
# blueviolet, brown, burlywood, cadetblue,
# chartreuse, chocolate, coral, cornflowerblue,
# cornsilk, crimson, cyan, darkblue, darkcyan,
# darkgoldenrod, darkgray, darkgrey, darkgreen,
# darkkhaki, darkmagenta, darkolivegreen, darkorange,
# darkorchid, darkred, darksalmon, darkseagreen,
# darkslateblue, darkslategray, darkslategrey,
# darkturquoise, darkviolet, deeppink, deepskyblue,
# dimgray, dimgrey, dodgerblue, firebrick,
# floralwhite, forestgreen, fuchsia, gainsboro,
# ghostwhite, gold, goldenrod, gray, grey, green,
# greenyellow, honeydew, hotpink, indianred, indigo,
# ivory, khaki, lavender, lavenderblush, lawngreen,
# lemonchiffon, lightblue, lightcoral, lightcyan,
# lightgoldenrodyellow, lightgray, lightgrey,
# lightgreen, lightpink, lightsalmon, lightseagreen,
# lightskyblue, lightslategray, lightslategrey,
# lightsteelblue, lightyellow, lime, limegreen,
# linen, magenta, maroon, mediumaquamarine,
# mediumblue, mediumorchid, mediumpurple,
# mediumseagreen, mediumslateblue, mediumspringgreen,
# mediumturquoise, mediumvioletred, midnightblue,
# mintcream, mistyrose, moccasin, navajowhite, navy,
# oldlace, olive, olivedrab, orange, orangered,
# orchid, palegoldenrod, palegreen, paleturquoise,
# palevioletred, papayawhip, peachpuff, peru, pink,
# plum, powderblue, purple, red, rosybrown,
# royalblue, rebeccapurple, saddlebrown, salmon,
# sandybrown, seagreen, seashell, sienna, silver,
# skyblue, slateblue, slategray, slategrey, snow,
# springgreen, steelblue, tan, teal, thistle, tomato,
# turquoise, violet, wheat, white, whitesmoke,
# yellow, yellowgreen
  textposition="middle center",
#   textfont={"size":15,"lat":gdf.geometry.centroid.y,"lon":gdf.geometry.centroid.x},
#   lat=gdf.geometry.centroid.y,
#   lon=gdf.geometry.centroid.x,
  mode = 'text')

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
#                 ,"{}/01_02지역별수진현황_03서울.png".format(workdir[:-5])
#                 ,width=864, height=792
#                 ,scale=2
#                )

# %%
