import streamlit as st

# 페이지 설정
st.set_page_config(page_title="HwaruhK Pro", layout="centered")

# 아이폰 한손 조작 최적화 CSS
st.markdown("""
    <style>
    .stApp { background-color: #0F1923; }
    
    /* 버튼 크기 및 간격 압축 */
    div.stButton > button {
        width: 100%; height: 55px;
        font-weight: bold; font-size: 14px;
        border-radius: 2px; border: 1px solid #35393D;
        background-color: #1F2326; color: #ECE8E1;
        margin-bottom: -5px;
    }
    
    /* 포인트 컬러: 성공/승리 (시안) */
    div.stButton > button[kind="primary"] {
        background-color: #00F5FF; color: #0F1923; border: none;
    }
    
    /* 포인트 컬러: 실패/패배 (레드) */
    div.stButton > button[kind="secondary"] {
        background-color: #FF4655; color: white; border: none;
    }

    /* 결과창 박스 */
    .report-card {
        background-color: #1F2326;
        padding: 12px; border-radius: 4px;
        border-left: 4px solid #FF4655;
        margin-bottom: 10px;
    }
    .stat-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
    .stat-item { text-align: center; }
    .stat-label { color: #8B9795; font-size: 11px; display: block; }
    .stat-value { color: #FF4655; font-weight: bold; font-size: 18px; }
    
    .section-title { 
        font-size: 12px; color: #8B9795; font-weight: bold; 
        margin: 15px 0 5px 0; letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기화
if 'data' not in st.session_state:
    st.session_state.data = {
        'fk_w': 0, 'fk_l': 0, 'fd_w': 0, 'fd_l': 0,
        'tr_s': 0, 'deaths': 0, 'st_s': 0, 'st_p': 0, 'st_f': 0
    }
d = st.session_state.data

# --- [상단 리포트] 가로 3열 배치 ---
st_total = d['st_s'] + d['st_p'] + d['st_f']
st_r = ((d['st_s'] + (d['st_p'] * 0.5)) / st_total * 100) if st_total > 0 else 0
fk_total = d['fk_w'] + d['fk_l']; fk_r = (d['fk_w'] / fk_total * 100) if fk_total > 0 else 0
tr_r = (d['tr_s'] / d['deaths'] * 100) if d['deaths'] > 0 else 0

st.markdown(f"""
<div class="report-card">
    <div class="stat-grid">
        <div class="stat-item"><span class="stat-label">STRAT</span><span class="stat-value">{st_r:.0f}%</span></div>
        <div class="stat-item"><span class="stat-label">FK WIN</span><span class="stat-value">{fk_r:.0f}%</span></div>
        <div class="stat-item"><span class="stat-label">TRADE</span><span class="stat-value">{tr_r:.0f}%</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- [버튼 섹션] 좌우 배치 ---

# 1. 작전 (3열 배치)
st.markdown('<div class="section-title">STRATEGY</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
if c1.button("성공", type="primary"): d['st_s'] += 1; st.rerun()
if c2.button("부분"): d['st_p'] += 1; st.rerun()
if c3.button("실패"): d['st_f'] += 1; st.rerun()

# 2. 교전 (2열 배치)
st.markdown('<div class="section-title">OPENING & TRADE</div>', unsafe_allow_html=True)
col_l, col_r = st.columns(2)

with col_l:
    if st.button("FK 승리", type="primary", key="fkw"): d['fk_w'] += 1; st.rerun()
    if st.button("FD 승리", key="fdw"): d['fd_w'] += 1; d['deaths'] += 1; st.rerun()
    if st.button("아군 데스", key="td"): d['deaths'] += 1; st.rerun()

with col_r:
    if st.button("FK 패배", key="fkl"): d['fk_l'] += 1; st.rerun()
    if st.button("FD 패배", key="fdl"): d['fd_l'] += 1; d['deaths'] += 1; st.rerun()
    if st.button("트레이드", type="primary", key="tk"): d['tr_s'] += 1; st.rerun()

# 하단 리셋 (최대한 작게)
st.write("---")
if st.button("♻️ RESET MATCH", use_container_width=True):
    for k in d.keys(): d[k] = 0
    st.rerun()


