import streamlit as st

# 페이지 설정
st.set_page_config(page_title="HwaruhK Pro", layout="centered")

# 카테고리별 칸 나누기 및 UI 강화 CSS
st.markdown("""
    <style>
    .stApp { background-color: #0F1923; }
    
    /* 결과창 박스 */
    .report-card {
        background-color: #1F2326; padding: 12px; border-radius: 8px;
        border: 1px solid #35393D; border-top: 4px solid #FF4655;
        margin-bottom: 15px;
    }
    .stat-grid { display: flex; justify-content: space-around; text-align: center; }
    .stat-label { color: #8B9795; font-size: 10px; display: block; margin-bottom: 2px; }
    .stat-value { color: #ECE8E1; font-weight: bold; font-size: 20px; }
    
    /* ★ 카테고리 섹션 상자 스타일 ★ */
    .category-box {
        background-color: #161A1E;
        border: 1px solid #35393D;
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 15px;
    }
    .category-title {
        font-size: 11px; color: #00F5FF; font-weight: bold;
        margin-bottom: 10px; letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* 버튼 스타일 */
    button {
        width: 100% !important; height: 48px !important;
        font-weight: bold !important; font-size: 14px !important;
        border-radius: 2px !important; border: 1px solid #35393D !important;
        background-color: #1F2326 !important; color: #ECE8E1 !important;
    }
    /* 포인트 컬러 (Cyan) */
    .cyan-btn button { background-color: #00F5FF !important; color: #0F1923 !important; border: none !important; }
    /* 포인트 컬러 (Red) */
    .red-btn button { background-color: #FF4655 !important; color: white !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기화
if 'data' not in st.session_state:
    st.session_state.data = {
        'fk_w': 0, 'fk_l': 0, 'fd_w': 0, 'fd_l': 0,
        'tr_s': 0, 'deaths': 0, 'st_s': 0, 'st_p': 0, 'st_f': 0
    }
d = st.session_state.data

# --- [상단 리포트 카드] ---
st_total = d['st_s'] + d['st_p'] + d['st_f']
st_r = ((d['st_s'] + (d['st_p'] * 0.5)) / st_total * 100) if st_total > 0 else 0
fk_total = d['fk_w'] + d['fk_l']; fk_r = (d['fk_w'] / fk_total * 100) if fk_total > 0 else 0
tr_r = (d['tr_s'] / d['deaths'] * 100) if d['deaths'] > 0 else 0

st.markdown(f"""
<div class="report-card">
    <div class="stat-grid">
        <div><span class="stat-label">STRAT</span><span class="stat-value">{st_r:.0f}%</span></div>
        <div><span class="stat-label">FK WIN</span><span class="stat-value">{fk_r:.0f}%</span></div>
        <div><span class="stat-label">TRADE</span><span class="stat-value">{tr_r:.0f}%</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- [카테고리 1: STRATEGY] ---
with st.container():
    st.markdown('<div class="category-box"><div class="category-title">01 STRATEGY EXECUTION</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.markdown('<div class="cyan-btn">', unsafe_allow_html=True)
        if st.button("성공", key="s1"): d['st_s'] += 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.button("부분", key="s2"): d['st_p'] += 1; st.rerun()
    with c3:
        st.markdown('<div class="red-btn">', unsafe_allow_html=True)
        if st.button("실패", key="s3"): d['st_f'] += 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- [카테고리 2: OPENING] ---
with st.container():
    st.markdown('<div class="category-box"><div class="category-title">02 OPENING DUELS</div>', unsafe_allow_html=True)
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.markdown('<div class="cyan-btn">', unsafe_allow_html=True)
        if st.button("FK 승리", key="f1"): d['fk_w'] += 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("FD 승리", key="f2"): d['fd_w'] += 1; d['deaths'] += 1; st.rerun()
    with f_col2:
        st.markdown('<div class="red-btn">', unsafe_allow_html=True)
        if st.button("FK 패배", key="f3"): d['fk_l'] += 1; st.rerun()
        if st.button("FD 패배", key="f4"): d['fd_l'] += 1; d['deaths'] += 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- [카테고리 3: COMBAT] ---
with st.container():
    st.markdown('<div class="category-box"><div class="category-title">03 TEAM COMBAT</div>', unsafe_allow_html=True)
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        if st.button("아군 데스", key="t1"): d['deaths'] += 1; st.rerun()
    with t_col2:
        st.markdown('<div class="cyan-btn">', unsafe_allow_html=True)
        if st.button("트레이드", key="t2"): d['tr_s'] += 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 하단 리셋 (완전히 아래로 밀기)
st.write("")
if st.button("♻️ RESET MATCH", use_container_width=True):
    for k in d.keys(): d[k] = 0
    st.rerun()
