import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime
import os
import matplotlib.font_manager as fm

# 1. [완벽 해결] 폰트 파일 직접 로드 로직
@st.cache_resource # 폰트를 매번 로드하면 느려지므로 캐싱합니다.
def load_custom_font():
    # 현재 파일(maoyi.py)이 있는 폴더 경로
    current_path = os.path.dirname(__file__)
    # 업로드한 폰트 파일 경로 (파일명 확인 필수!)
    font_path = os.path.join(current_path, 'malgun.ttf')
    
    if os.path.exists(font_path):
        # 폰트 속성 설정
        prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=prop.get_name())
        plt.rcParams['axes.unicode_minus'] = False
        return prop.get_name()
    else:
        # 폰트 파일이 없을 경우 기본 설정 유지
        return None

font_name = load_custom_font()

# 2. 페이지 설정
st.set_page_config(page_title="섬유산업 대시보드", page_icon="🧵", layout="wide")

# 3. 커스텀 CSS (카드 디자인)
st.markdown("""
    <style>
    .main-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #eee;
        margin-bottom: 20px;
    }
    .card-title { font-size: 16px; color: #555; margin-bottom: 10px; font-weight: bold; }
    .card-value { font-size: 28px; font-weight: 800; color: #8A2BE2; }
    .card-delta { font-size: 15px; margin-top: 8px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

st.title("🧵 대한민국 섬유산업 수출입 동향 분석기")

# -----------------------------------------------------------------------------

file_path = "산업통상부_섬유산업 수출입 현황_20241231.csv"

try:
    df = pd.read_csv(file_path, encoding='cp949')
    latest_data = df.iloc[-1]
    column_names = df.columns.drop('연도').tolist()

    with st.sidebar:
        st.header("⚙️ 분석 설정")
        selected_col = st.selectbox("데이터 항목 선택", column_names, index=5)
        show_compare = st.checkbox("전체 산업과 비교하기")

    # 상단 요약 카드 (중략 - 이전과 동일)
    col1, col2, col3 = st.columns(3)
    # ... (생략된 요약 카드 로직은 동일하게 유지)

    # 7. 메인 그래프 (폰트 강제 적용)
    st.subheader(f"📈 {selected_col} 추이 분석")
    
    # Seaborn 테마 설정 후 폰트 재설정
    sns.set_theme(style="whitegrid")
    if font_name:
        plt.rc('font', family=font_name)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df, x='연도', y=selected_col, ax=ax, marker='o', color='#8A2BE2', linewidth=2.5)
    
    ax.set_title(f"연도별 {selected_col} 변화 추이", fontsize=16, pad=20, fontweight='bold')
    ax.set_xlabel("연도")
    ax.set_ylabel("수치")
    
    st.pyplot(fig)

    if show_compare:
        st.divider()
        st.subheader("📊 전체 산업 vs 섬유산업 수출 규모 비교")
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=df, x='연도', y='전체산업수출금액(백만불)', label='전체 산업', ax=ax2, color='#A9A9A9')
        sns.lineplot(data=df, x='연도', y='섬유산업수출금액(백만불)', label='섬유 산업', ax=ax2, color='#8A2BE2', linewidth=3)
        st.pyplot(fig2)

except Exception as e:
    st.error(f"❌ 오류 발생: {e}")