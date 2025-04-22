import streamlit as st

# --- 스타일 커스텀 ---
st.markdown("""
    <style>
        .block-container {
            max-width: 450px;
            min-height: 1168px;
            padding-top: 2rem;
            padding-bottom: 2rem;
            margin: auto;
            background-color: white;
            border: 5px solid #ddd;
            border-radius: 20px;
            padding: 30px 20px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 1.05);
        }
        [data-testid="stSidebar"] { display: none;}
        [data-testid="stHeader"] { background: none; }
        body { background-color: #f1f3f6; }
            
        /* 버튼 기본 스타일 */
        div.stButton > button {
            background-color: white;
            color: black;
            height: 120px;
            width: 100%;
            border-radius: 15px;

            /* 테두기 두께와 색상 지정 */
            border: 3px solid grey !important;
            

        }
            
        
            
        /* 버튼 내부 모든 텍스트 컨테이너에 폰트 크기·굵기 적용 */
        div.stButton > button * {
            font-size: 24px !important;
            line-height: 1.2 !important;
            font-weight: 700 !important;
        }

        .button-space { margin-bottom: 20px; }
    </style>

""", unsafe_allow_html=True)

# --- 로고 & 타이틀 ---
st.image("logo.png", use_container_width=False)
st.markdown("""
    <div style='margin-top: -30px; text-align: center; font-size: 25px; font-weight: bold;'>
        
    </div>
""", unsafe_allow_html=True)

# --- 세로 버튼 4개 ---
buttons = [
    ("내 점수 확인하기", lambda: st.success("내 점수 확인 페이지로 이동")),
    ("설문조사 하러가기", lambda: st.markdown("<meta http-equiv='refresh' content='0;url=/p1'>", unsafe_allow_html=True)),
    ("1대1 매칭",       lambda: st.success("1대1 매칭 페이지로 이동")),
    ("학습하기",        lambda: st.success("학습 페이지로 이동")),
]

for label, action in buttons:
    st.markdown("<div class='button-space'>", unsafe_allow_html=True)
    if st.button(label):
        action()
    st.markdown("</div>", unsafe_allow_html=True)
