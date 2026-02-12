import streamlit as st

# 페이지 설정
st.set_page_config(page_title="HwaruhK Analysis", layout="centered")

# 디자인 입히기
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%; height: 65px;
        font-weight: bold; font-size: 18px;
        border-radius: 12px; margin-bottom: 5px;
    }
    .report-box {
        background-color: #1e272e;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #3498db;
        margin-bottom: 25px;
    }
    .stat-text { font-size: 18px; color: #ece8e1; margin-bottom: 5px; }
    .highlight { color: #3498db; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기화
if 'data' not in st.session_state:
    st.session_state.data = {
        'fk_w': 0, 'fk_l': 0, 'fd_w': 0, 'fd_l': 0,
        'tr_s': 0, 'deaths': 0,
        'st_s': 0, 'st_p': 0, 'st_f': 0
    }

d = st.session_state.data

# --- [상단 리포트 창] PC 버전처럼 실시간 계산 ---
fk_total = d['fk_w'] + d['fk_l']
fk_r = (d['fk_w'] / fk_total * 100) if fk_total > 0 else 0

fd_total = d['fd_w'] + d['fd_l']
fd_r = (d['fd_w'] / fd_total * 100) if fd_total > 0 else 0

tr_r = (d['tr_s'] / d['deaths'] * 100) if d['deaths'] > 0 else 0

st_total = d['st_s'] + d['st_p'] + d['st_f']
st_r = ((d['st_s'] + (d['st_p'] * 0.5)) / st_total * 100) if st_total > 0 else 0

st.markdown(f"""
<div class="report-box">
    <h2 style='color:#3498db; margin-top:0;'>📊 SCRIM REPORT</h2>
    <div class="stat-text">▶ 작전 성공률: <span class="highlight">{st_r:.1f}%</span> ({d['st_s']}/{st_total})</div>
    <div class="stat-text">▶ FK 승률: <span class="highlight">{fk_r:.1f}%</span> (승:{d['fk_w']}/패:{d['fk_l']})</div>
    <div class="stat-text">▶ FD 승률: <span class="highlight">{fd_r:.1f}%</span> (승:{d['fd_w']}/패:{d['fd_l']})</div>
    <div class="stat-text">▶ 트레이드 성공: <span class="highlight">{tr_r:.1f}%</span> ({d['tr_s']}/{d['deaths']})</div>
</div>
""", unsafe_allow_html=True)

# --- [버튼 섹션] ---
st.subheader("🎯 STRATEGY (작전)")
c1, c2, c3 = st.columns(3)
if c1.button("성공", type="primary"): d['st_s'] += 1; st.rerun()
if c2.button("부분"): d['st_p'] += 1; st.rerun()
if c3.button("실패"): d['st_f'] += 1; st.rerun()

st.subheader("⚔️ OPENING (초반 주도권)")
f1, f2 = st.columns(2)
if f1.button("FK 승리"): d['fk_w'] += 1; st.rerun()
if f1.button("FD 승리"): d['fd_w'] += 1; d['deaths'] += 1; st.rerun()
if f2.button("FK 패배"): d['fk_l'] += 1; st.rerun()
if f2.button("FD 패배"): d['fd_l'] += 1; d['deaths'] += 1; st.rerun()

st.subheader("🔄 COMBAT (교전 지원)")
t1, t2 = st.columns(2)
if t1.button("아군 데스"): d['deaths'] += 1; st.rerun()
if t2.button("트레이드 성공"): d['tr_s'] += 1; st.rerun()

st.divider()

# 초기화 버튼
if st.button("♻️ RESET (다음 경기 시작)", use_container_width=True):
    for k in d.keys(): d[k] = 0
    st.rerun()
