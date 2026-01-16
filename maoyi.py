import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime
import os

# 1. 한글 폰트 설정 (더 강력한 로직)
def set_korean_font():
    # Streamlit Cloud(Linux) 환경
    if os.name == 'posix':
        # 서버에 나눔고딕이 설치되어 있다면 사용
        plt.rc('font', family='NanumGothic')
    # Windows 환경
    elif os.name == 'nt':
        plt.rc('font', family='Malgun Gothic')
    
    # 공통 설정
    plt.rcParams['axes.unicode_minus'] = False
    # 그래프를 캔버스에 그릴 때 폰트가 누락되지 않도록 설정
    plt.rcParams['font.size'] = 10

set_korean_font()

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
st.markdown("전체 산업 대비 섬유산업의 성장과 변화를 한눈에 확인해 보세요!")

# -----------------------------------------------------------------------------

file_path = "산업통상부_섬유산업 수출입 현황_20241231.csv"

try:
    df = pd.read_csv(file_path, encoding='cp949')
    latest_data = df.iloc[-1]
    column_names = df.columns.drop('연도').tolist()

    # --- 5. 사이드바 ---
    with st.sidebar:
        st.header("⚙️ 분석 설정")
        selected_col = st.selectbox("데이터 항목 선택", column_names, index=5)
        st.divider()
        show_compare = st.checkbox("전체 산업과 비교하기")

    # --- 6. 상단 요약 카드 ---
    col1, col2, col3 = st.columns(3)
    
    # (카드는 HTML 기반이라 폰트 깨짐과 무관합니다)
    for col, title, val_key, delta_key, unit in zip(
        [col1, col2, col3], 
        ["🧶 섬유 수출액", "📉 섬유 수입액", "💰 섬유 무역수지"],
        ['섬유산업수출금액(백만불)', '섬유산업수입금액(백만불)', '섬유산업무역수지(백만불)'],
        ['섬유산업수출증감(전년대비_퍼센트)', '섬유산업수입증감(전년대비_퍼센트)', None],
        ["M$", "M$", "M$"]
    ):
        with col:
            val = latest_data[val_key]
            delta = latest_data[delta_key] if delta_key else None
            color = "#FF4B4B" if delta and delta > 0 else "#1C83E1"
            
            st.markdown(f"""
                <div class="main-card">
                    <div class="card-title">{title}</div>
                    <div class="card-value">{val:,.0f} {unit}</div>
                    <div class="card-delta" style="color: {color if delta else '#666'};">
                        {("▲ " + str(abs(delta)) + "%") if delta else ("비중: " + str(latest_data['섬유산업수출비중(전년대비_퍼센트)']) + "%")}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # --- 7. 메인 그래프 (여기서 폰트를 다시 한 번 잡아줍니다) ---
    st.subheader(f"📈 {selected_col} 추이 분석")
    
    # Seaborn 테마 설정 시 폰트 깨짐이 잦으므로 명시적으로 지정
    target_font = 'NanumGothic' if os.name == 'posix' else 'Malgun Gothic'
    sns.set_theme(style="whitegrid", font=target_font)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df, x='연도', y=selected_col, ax=ax, marker='o', color='#8A2BE2', linewidth=2.5)
    
    # 개별 텍스트 요소에 폰트 다시 적용 (강제 해결책)
    ax.set_title(f"연도별 {selected_col} 변화 추이", fontsize=16, pad=20, fontfamily=target_font)
    ax.set_xlabel("연도", fontfamily=target_font)
    ax.set_ylabel("수치", fontfamily=target_font)
    
    st.pyplot(fig)

    # 8. 비교 그래프
    if show_compare:
        st.divider()
        st.subheader("📊 전체 산업 vs 섬유산업 수출 규모 비교")
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=df, x='연도', y='전체산업수출금액(백만불)', label='전체 산업', ax=ax2, color='#A9A9A9')
        sns.lineplot(data=df, x='연도', y='섬유산업수출금액(백만불)', label='섬유 산업', ax=ax2, color='#8A2BE2', linewidth=3)
        plt.fill_between(df['연도'], df['섬유산업수출금액(백만불)'], color='#8A2BE2', alpha=0.1)
        st.pyplot(fig2)

    with st.expander("📄 원본 데이터 확인하기"):
        st.dataframe(df.sort_values('연도', ascending=False), use_container_width=True)

except Exception as e:
    st.error(f"❌ 오류 발생: {e}")

st.caption(f"최종 업데이트: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")