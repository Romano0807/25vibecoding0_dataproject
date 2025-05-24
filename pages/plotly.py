import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("202504_202504_연령별인구현황_월간_합계.csv", encoding="cp949")
    return df

df = load_data()

# 데이터 전처리
df_cleaned = df.copy()
df_cleaned.columns = df_cleaned.columns.str.strip()
df_cleaned = df_cleaned.rename(columns={"행정구역": "지역"})
age_cols = [col for col in df_cleaned.columns if "세" in col]
for col in age_cols:
    df_cleaned[col] = df_cleaned[col].str.replace(",", "").astype(int)

# 지역 선택
지역목록 = df_cleaned["지역"].unique().tolist()
선택지역 = st.selectbox("지역을 선택하세요", 지역목록)

# 해당 지역 데이터 추출
지역데이터 = df_cleaned[df_cleaned["지역"] == 선택지역]
연령별인구 = 지역데이터[age_cols].T.reset_index()
연령별인구.columns = ["연령", "인구수"]
연령별인구["연령"] = 연령별인구["연령"].str.extract(r"(\d+세|100세 이상)")

# Plotly 그래프
fig = px.bar(
    연령별인구,
    x="연령",
    y="인구수",
    title=f"{선택지역} 연령별 인구 분포",
    labels={"연령": "연령", "인구수": "인구 수"},
)
st.plotly_chart(fig)

