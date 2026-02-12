import streamlit as st

# 페이지 설정
st.set_page_config(page_title="HwaruhK Pro", layout="centered")

# 수직형 나열 및 카테고리 강조 CSS
st.markdown("""
    <style>
    .stApp { background-color: #0F1923; }
    
    /* 상단 결과창: 가독성 중심 */
    .report-card {
        background-color: #1F2326; padding: 20px; border-radius: 12px;
        border: 1px solid #35393D; border-top: 5px solid #FF4655;
        margin-bottom: 20px; text-align: center;
    }
    .stat-container { display: flex; justify-content: space-between; }
    .stat-label { color: #8B9795; font-size: 12px; display: block; }
    .stat-value { color: #ECE8E1; font-weight: bold; font-size: 24px; }
    
    /* 카테고리 구분 칸 */
    .category-container {
        border: 1px solid #35393D;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 25px;
        background-color: #161A1E;
    }
    .category-header {
        color: #00F5FF; font-size: 13px; font-weight: bold;
        margin-bottom: 15px; border-left: 3px solid #00F5FF; padding-left: 10px;
    }

    /* 버튼: 수직형으로 크게 */
    button {
        width: 100% !important; height: 60px !important;
        font-weight: bold !important; font-size: 18px !important;
        border-radius: 8px !important; margin-bottom: 10px !important;
        background-color: #1F2326 !important; color: #ECE8E1 !important;
        border: 1px solid #35393D !important;
    }
    
    /* 강조 버튼 색상 */
    .cyan-btn button { background-color: #00F5FF !important; color: #0F1923 !important; border: none !important; }
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

# 데이터 계산
st_total = d['st_s'] + d['st_p'] + d['st_f']
st_r = ((d['st_s'] + (d['st_p'] * 0.5)) / st_total * 100) if st_total > 0 else 0
fk_total = d['fk_w'] + d['fk_l']; fk_r = (d['fk_w'] / fk_total * 100) if fk_total > 0 else 0
tr_r = (d['tr_s'] / d['deaths'] * 100) if d['deaths'] > 0 else 0

# --- 상단 리포트 ---
st.markdown(f"""
<div class="report-card">
    <div class="stat-container">
        <div><span class="stat-label">STRAT</span><span class="stat-value">{st_r:.0f}%</span></div>
        <div><span class="stat-label">FK WIN</span><span class="stat-value">{fk_r:.0f}%</span></div>
        <div><span class="stat-label">TRADE</span><span class="stat-value">{tr_r:.0f}%</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 섹션 1: STRATEGY (수직) ---
st.markdown('<div class="category-container"><div class="category-header">01 STRATEGY</div>', unsafe_allow_html=True)
st.markdown('<div class="cyan-btn">', unsafe_allow_html=True)
if st.button("작전 성공", key="s1"): d['st_s'] += 1; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
if st.button("부분 성공", key="s2"): d['st_p'] += 1; st.rerun()
st.markdown('<div class="red-btn">', unsafe_allow_html=True)
if st.button("작전 실패", key="s3"): d['st_f'] += 1; st.rerun()
st.markdown('</div></div>', unsafe_allow_html=True)

# --- 섹션 2: OPENING (수직) ---
st.markdown('<div class="category-container"><div class="category-header">02 OPENING DUELS</div>', unsafe_allow_html=True)
st.markdown('<div class="cyan-btn">', unsafe_allow_html=True)
if st.button("FK 승리", key="f1"): d['fk_w'] += 1; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="red-btn">', unsafe_allow_html=True)
if st.button("FK 패배", key="f2"): d['fk_l'] += 1; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
if st.button("FD 승리 (아군생존)", key="f3"): d['fd_w'] += 1; d['deaths'] += 1; st.rerun()
st.markdown('<div class="red-btn">', unsafe_allow_html=True)
if st.button("FD 패배 (아군사망)", key="f4"): d['fd_l'] += 1; d['deaths'] += 1; st.rerun()
st.markdown('</div></div>', unsafe_allow_html=True)

# --- 섹션 3: COMBAT (수직) ---
st.markdown('<div class="category-container"><div class="category-header">03 TEAM COMBAT</div>', unsafe_allow_html=True)
if st.button("아군 데스 발생", key="t1"): d['deaths'] += 1; st.rerun()
st.markdown('<div class="cyan-btn">', unsafe_allow_html=True)
if st.button("트레이드 성공", key="t2"): d['tr_s'] += 1; st.rerun()
st.markdown('</div></div>', unsafe_allow_html=True)

# 리셋 버튼
if st.button("♻️ RESET MATCH", use_container_width=True):
    for k in d.keys(): d[k] = 0
    st.rerun()


