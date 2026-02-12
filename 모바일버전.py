import streamlit as st
from datetime import datetime

# 페이지 설정 (모바일 최적화)
st.set_page_config(page_title="HwaruhK Pro Analysis", layout="centered")

# CSS로 모바일 버튼 디자인 강화
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
        border-radius: 10px;
    }
    .main-title { font-size: 24px; font-weight: bold; color: #3498db; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">HwaruhK ULTIMATE ANALYSIS v1.0 (Mobile)</p>', unsafe_allow_html=True)

# 데이터 초기화 (세션 상태 이용)
if 'data' not in st.session_state:
    st.session_state.data = {
        'fk_win': 0, 'fk_loss': 0, 'fd_win': 0, 'fd_loss': 0,
        'trades': 0, 'deaths': 0, 'strat_success': 0, 'strat_partial': 0, 'strat_fail': 0
    }

# --- 1. 작전 성공률 섹션 ---
st.subheader("🎯 STRATEGY (작전)")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("성공", type="primary", key="s_ok"): st.session_state.data['strat_success'] += 1
with col2:
    if st.button("부분", key="s_pa"): st.session_state.data['strat_partial'] += 1
with col3:
    if st.button("실패", key="s_no"): st.session_state.data['strat_fail'] += 1

# --- 2. 초반 교전 섹션 ---
st.subheader("⚔️ OPENING (초반 주도권)")
col_f1, col_f2 = st.columns(2)
with col_f1:
    if st.button("FK 승리", key="fk_w"): st.session_state.data['fk_win'] += 1
    if st.button("FD 승리", key="fd_w"): st.session_state.data['fd_win'] += 1; st.session_state.data['deaths'] += 1
with col_f2:
    if st.button("FK 패배", key="fk_l"): st.session_state.data['fk_loss'] += 1
    if st.button("FD 패배", key="fd_l"): st.session_state.data['fd_loss'] += 1; st.session_state.data['deaths'] += 1

# --- 3. 트레이드 섹션 ---
st.subheader("🔄 COMBAT (교전 지원)")
col_t1, col_t2 = st.columns(2)
with col_t1:
    if st.button("아군 데스", key="d_add"): st.session_state.data['deaths'] += 1
with col_t2:
    if st.button("트레이드", key="t_add"): st.session_state.data['trades'] += 1

# --- 데이터 계산 ---
d = st.session_state.data
fk_total = d['fk_win'] + d['fk_loss']
fk_r = (d['fk_win'] / fk_total * 100) if fk_total > 0 else 0
tr_r = (d['trades'] / d['deaths'] * 100) if d['deaths'] > 0 else 0
strat_total = d['strat_success'] + d['strat_partial'] + d['strat_fail']
strat_r = ((d['strat_success'] + (d['strat_partial'] * 0.5)) / strat_total * 100) if strat_total > 0 else 0

# --- 결과 출력 ---
st.divider()
st.markdown(f"""
### 📊 Scrim Report
- **작전 성공률:** `{strat_r:.1f}%`
- **FK 승률:** `{fk_r:.1f}%`
- **트레이드 성공률:** `{tr_r:.1f}%`
""")

# 초기화 버튼
if st.button("♻️ 다음 경기 초기화", use_container_width=True):
    st.session_state.data = {k: 0 for k in st.session_state.data}
    st.rerun()