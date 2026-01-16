import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime
import matplotlib.font_manager as fm
import os

# 1. 한글 폰트 및 그래프 설정
def set_korean_font():
    # 1. 시스템에 설치된 폰트 확인
    # 리눅스(Streamlit Cloud) 환경인 경우
    if os.name == 'posix':
        plt.rc('font', family='NanumGothic')
    # 윈도우 환경인 경우
    elif os.name == 'nt':
        plt.rc('font', family='Malgun Gothic')
    
    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
set_korean_font()

# 2. 페이지 설정 (브라우저 탭 제목과 레이아웃)
st.set_page_config(page_title="섬유산업 대시보드", page_icon="🧵", layout="wide")

# 3. 커스텀 CSS (카드 디자인 적용)
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

# --- 메인 타이틀 ---
st.title("🧵 대한민국 섬유산업 수출입 동향 분석기")
st.markdown("전체 산업 대비 섬유산업의 성장과 변화를 한눈에 확인해 보세요!")
st.write("") # 간격 조절

# -----------------------------------------------------------------------------

# 파일명 (업로드하신 파일명과 일치해야 합니다)
file_path = "산업통상부_섬유산업 수출입 현황_20241231.csv"

try:
    # 4. 데이터 불러오기
    df = pd.read_csv(file_path, encoding='cp949')
    
    # 최신 데이터 추출
    latest_data = df.iloc[-1]
    column_names = df.columns.drop('연도').tolist()

    # --- 5. 사이드바 구성 ---
    with st.sidebar:
        st.header("⚙️ 분석 설정")
        st.write("그래프에 표시할 항목을 선택하세요.")
        selected_col = st.selectbox("데이터 항목 선택", column_names, index=5)
        
        st.divider()
        st.write("💡 아래 체크박스를 누르면 전체 산업과의 비교 그래프가 나타납니다.")
        show_compare = st.checkbox("전체 산업과 비교하기")

    # --- 6. 상단 요약 카드 (환율 사이트 느낌 탈출!) ---
    col1, col2, col3 = st.columns(3)

    with col1:
        delta_val = latest_data['섬유산업수출증감(전년대비_퍼센트)']
        delta_color = "#FF4B4B" if delta_val > 0 else "#1C83E1" # 상승 빨강, 하락 파랑
        st.markdown(f"""
            <div class="main-card">
                <div class="card-title">🧶 섬유 수출액</div>
                <div class="card-value">{latest_data['섬유산업수출금액(백만불)']:,.0f} M$</div>
                <div class="card-delta" style="color: {delta_color};">
                    {"▲" if delta_val > 0 else "▼"} {abs(delta_val)}% (전년비)
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        delta_val_in = latest_data['섬유산업수입증감(전년대비_퍼센트)']
        delta_color_in = "#FF4B4B" if delta_val_in > 0 else "#1C83E1"
        st.markdown(f"""
            <div class="main-card">
                <div class="card-title">📉 섬유 수입액</div>
                <div class="card-value">{latest_data['섬유산업수입금액(백만불)']:,.0f} M$</div>
                <div class="card-delta" style="color: {delta_color_in};">
                    {"▲" if delta_val_in > 0 else "▼"} {abs(delta_val_in)}% (전년비)
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        balance = latest_data['섬유산업무역수지(백만불)']
        balance_color = "#2E8B57" if balance > 0 else "#CD5C5C"
        st.markdown(f"""
            <div class="main-card">
                <div class="card-title">💰 섬유 무역수지</div>
                <div class="card-value" style="color: {balance_color};">{balance:,.0f} M$</div>
                <div class="card-delta" style="color: #666;">수출 비중: {latest_data['섬유산업수출비중(전년대비_퍼센트)']}%</div>
            </div>
        """, unsafe_allow_html=True)

    # --- 7. 메인 그래프 ---
    st.subheader(f"📈 {selected_col} 추이 분석")
    
    sns.set_theme(style="whitegrid", font="Malgun Gothic")
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # 선 그래프 디자인
    sns.lineplot(data=df, x='연도', y=selected_col, ax=ax, marker='o', 
                 color='#8A2BE2', linewidth=2.5, markersize=8)
    
    ax.set_title(f"연도별 {selected_col} 변화 추이", fontsize=16, pad=20, fontweight='bold')
    ax.set_xlabel("연도", fontsize=12)
    ax.set_ylabel("수치", fontsize=12)
    
    st.pyplot(fig)

    # 8. 비교 그래프 (사이드바 체크박스 연동)
    if show_compare:
        st.divider()
        st.subheader("📊 전체 산업 vs 섬유산업 수출 규모 비교")
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        
        sns.lineplot(data=df, x='연도', y='전체산업수출금액(백만불)', label='전체 산업', ax=ax2, color='#A9A9A9', alpha=0.7)
        sns.lineplot(data=df, x='연도', y='섬유산업수출금액(백만불)', label='섬유 산업', ax=ax2, color='#8A2BE2', linewidth=3)
        
        plt.fill_between(df['연도'], df['섬유산업수출금액(백만불)'], color='#8A2BE2', alpha=0.1) # 아래 영역 채우기
        plt.legend()
        st.pyplot(fig2)

    # 9. 데이터 상세 보기
    with st.expander("📄 원본 데이터 확인하기"):
        st.dataframe(df.sort_values('연도', ascending=False), use_container_width=True)

except FileNotFoundError:
    st.error(f"❌ '{file_path}' 파일을 찾을 수 없습니다.")
except Exception as e:
    st.error(f"❌ 예상치 못한 오류가 발생했습니다: {e}")

# 하단 캡션
st.caption(f"최종 업데이트: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 데이터 출처: 산업통상자원부")