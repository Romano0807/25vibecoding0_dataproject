import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("2025년 4월 전국 연령별 인구 시각화 (남녀구분)")

# 파일 업로드 (혹은 파일 경로 지정)
mf_file = st.file_uploader("남녀구분 인구 CSV 파일 업로드", type=['csv'], key="mf")
total_file = st.file_uploader("합계 인구 CSV 파일 업로드", type=['csv'], key="total")

if mf_file and total_file:
    # 한글 인코딩 읽기
    df_mf = pd.read_csv(mf_file, encoding='euc-kr')
    df_total = pd.read_csv(total_file, encoding='euc-kr')

    # 전국 데이터만 추출
    df_nat_mf = df_mf[df_mf['행정구역'].str.contains('전국')].iloc[0]
    df_nat_total = df_total[df_total['행정구역'].str.contains('전국')].iloc[0]

    ages = [f"{i}세" for i in range(0, 100)] + ["100세 이상"]

    male_pop = [int(str(df_nat_mf[f'2025년04월_남_{age}']).replace(',', '')) for age in ages]
    female_pop = [int(str(df_nat_mf[f'2025년04월_여_{age}']).replace(',', '')) for age in ages]
    total_pop = [int(str(df_nat_total[f'2025년04월_계_{age}']).replace(',', '')) for age in ages]

    # 인구 피라미드
    fig_pyramid = go.Figure()
    fig_pyramid.add_trace(go.Bar(
        y=ages,
        x=[-n for n in male_pop],
        name='남성',
        orientation='h',
        marker_color='blue'
    ))
    fig_pyramid.add_trace(go.Bar(
        y=ages,
        x=female_pop,
        name='여성',
        orientation='h',
        marker_color='pink'
    ))
    fig_pyramid.update_layout(
        title='2025년 4월 전국 연령별 인구 피라미드(남녀구분)',
        barmode='relative',
        xaxis=dict(title='인구수', tickformat=','),
        yaxis=dict(title='연령'),
        legend=dict(x=0.75, y=0.05),
        template='plotly_white',
        height=800
    )

    st.subheader("연령별 인구 피라미드 (남녀구분)")
    st.plotly_chart(fig_pyramid, use_container_width=True)

    # 전체 인구 막대그래프
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=ages,
        y=total_pop,
        name='전체 인구'
    ))
    fig_bar.update_layout(
        title='2025년 4월 전국 연령별 전체 인구',
        xaxis=dict(title='연령'),
        yaxis=dict(title='인구수', tickformat=','),
        template='plotly_white',
        height=500
    )
    st.subheader("연령별 전체 인구")
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("위의 두 CSV 파일을 모두 업로드해주세요.")
