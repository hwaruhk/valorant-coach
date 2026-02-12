import streamlit as st

# 페이지 설정
st.set_page_config(page_title="HwaruhK Pro", layout="centered")

# 발로란트 스타일의 UI 디자인 (압축형)
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    .stApp { background-color: #0F1923; }
    
    /* 버튼 스타일 압축 */
    div.stButton > button {
        width: 100%; height: 50px;
        font-weight: bold; font-size: 15px;
        border-radius: 4px; border: 1px solid #35393D;
        background-color: #1F2326; color: #ECE8E1;
        margin-bottom: -10px;
    }
    /* 강조 버튼 (성공/승리) */
    div.stButton > button[kind="primary"] {
        background-color: #00F5FF; color: #0F1923; border: none;
    }
    /* 위험 버튼 (실패/패배) */
    .st-emotion-cache-12w0qpk { 
        background-color: #FF4655 !important; color: white !important; 
    }
    
    /* 결과창 디자인 (상단 고정 느낌) */
    .report-card {
        background-color: #1F2326;
        padding: 15px; border-radius: 8px;
        border-top: 4px solid #FF4655;
        margin-bottom: 15px;
    }
    .stat-row { display: flex; justify-content: space-between; margin-bottom: 5px; }
    .stat-label { color: #8B9795; font-size: 14px; }
    .stat-value { color: #FF4655; font-weight: bold; font-size: 16px; }
    
    /* 섹션 타이틀 압축 */
    .section-title { 
        font-size: 14px; color: #8B9795; font-weight: bold; 
        margin: 10px 0 5px 0; border-bottom: 1px solid #35393D; 
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

# --- [상단 리포트 카드] 데이터 계산 ---
st_total = d['st_s'] + d['st_p'] + d['st_f']
st_r = ((d['st_s'] + (d['st_p'] * 0.5)) / st_total * 100) if st_total > 0 else 0
fk_total = d['fk_w'] + d['fk_l']; fk_r = (d['fk_w'] / fk_total * 100) if fk_total > 0 else 0
tr_r = (d['tr_s'] / d['deaths'] * 100) if d['deaths'] > 0 else 0

st.markdown(f"""
<div class="report-card">
    <div class="stat-row">
        <span class="stat-label">STRATEGY</span><span class="stat-value">{st_r:.1f}%</span>
    </div>
    <div class="stat-row">
        <span class="stat-label">FK WIN</span><span class="stat-value">{fk_r:.1f}%</span>
    </div>
    <div class="stat-row">
        <span class="stat-label">TRADE</span><span class="stat-value">{tr_r:.1f}%</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- [버튼 영역] 2열/3열 배치로 스크롤 최소화 ---
st.markdown('<div class="section-title">STRATEGY EXECUTION</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
if c1.button("성공", type="primary"): d['st_s'] += 1; st.rerun()
if c2.button("부분"): d['st_p'] += 1; st.rerun()
if c3.button("실패"): d['st_f'] += 1; st.rerun()

st.markdown('<div class="section-title">OPENING DUAL</div>', unsafe_allow_html=True)
f1, f2 = st.columns(2)
if f1.button("FK WIN", type="primary"): d['fk_w'] += 1; st.rerun()
if f2.button("FK LOSS"): d['fk_l'] += 1; st.rerun()
if f1.button("FD WIN"): d['fd_w'] += 1; d['deaths'] += 1; st.rerun()
if f2.button("FD LOSS"): d['fd_l'] += 1; d['deaths'] += 1; st.rerun()

st.markdown('<div class="section-title">TEAM COMBAT</div>', unsafe_allow_html=True)
t1, t2 = st.columns(2)
if t1.button("TEAM DEATH"): d['deaths'] += 1; st.rerun()
if t2.button("TRADE KILL", type="primary"): d['tr_s'] += 1; st.rerun()

# 하단 리셋 (작게)
st.write("")
if st.button("♻️ RESET MATCH", use_container_width=True):
    for k in d.keys(): d[k] = 0
    st.rerun()

