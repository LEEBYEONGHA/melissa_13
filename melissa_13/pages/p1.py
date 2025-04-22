import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# --- 스타일 커스텀 ---
st.markdown("""
<style>
        /* 전체 레이아웃 단일화 */
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

            color: black !important;
        }

        /* 사이드바 완전히 숨기기 */
        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="stHeader"] {
            background: none;
        }

        body {
            background-color: #f1f3f6;
        }

        h1 {
            font-size: 28px !important;
            text-align: center;
            color: black !important;
            
        }

        h3 {
            font-size: 18px !important;
            text-align: center;
            color: black !important;
        }

        button {
            font-size: 16px !important;
        }
    </style>
""", unsafe_allow_html=True)



# --- 앱 이름 ---


# st.markdown("<h1>개인정보 입력 페이지</h1>", unsafe_allow_html=True)

# # --- 로그인 / 회원가입 선택 ---
# # mode = st.radio("모드를 선택하세요", ["로그인", "회원가입"], horizontal=True)

# st.write("")

# # if mode == "로그인":
# st.subheader("개인정보 입력")

# # username = st.text_input("이름??", placeholder="아이디를 입력하세요")
# # password = st.text_input("전화번호??", type="password", placeholder="비밀번호를 입력하세요")

# --- 가운데 정렬된 제목부 ---
st.markdown("""
    <h1 style="text-align:center; margin-bottom:0.5rem;">
        개인정보 입력 페이지
    </h1>
    <h3 style="text-align:center; margin-top:0;">
        개인정보 입력
    </h3>
""", unsafe_allow_html=True)



st.text_input("이름", placeholder="이름을 입력하세요")
st.text_input("생년월일", placeholder="주민번호 앞 6자리를 입력하세요")
st.text_input("전화번호", placeholder="-없이 입력하세요")






# if st.button("로그인"):
#     # 여기에 로그인 로직 추가
#     st.success(f"환영합니다, {username}님!")
#     st.markdown("""
#     <a href='/s2'>
#         <button style='font-size:18px;padding:10px 20px;border:none;border-radius:10px;background:#4CAF50;color:white;'>
#             설문조사 시작하기
#         </button>
#     </a>
#     """, unsafe_allow_html=True)


# 1. 좌측에 빈 공간, 우측에 '이전'·'다음' 버튼 두 개를 놓을 칼럼을 생성
col1, col2, col3 = st.columns([1, 4, 1])

# 2. col2에 '이전' 버튼 배치
with col1:
    if st.button("이전"):
        st.markdown(
            "<meta http-equiv='refresh' content='0;url=/m2'>",
            unsafe_allow_html=True
        )

# 3. col3에 '다음' 버튼 배치
with col3:
    if st.button("다음"):
        st.markdown(
            "<meta http-equiv='refresh' content='0;url=/s7'>",
            unsafe_allow_html=True
        )




# if st.button("이전"):
#     st.markdown("<meta http-equiv='refresh' content='0;url=/m1'>", unsafe_allow_html=True)



# if st.button("다음"):
#     # if username and password:
#         # st.success(f"환영합니다, {username}님!")
#     st.markdown("<meta http-equiv='refresh' content='0;url=/s7'>", unsafe_allow_html=True)
#     # else:
#     #     st.warning("아이디와 비밀번호를 모두 입력해주세요.")


# else:
#     st.subheader("📝 회원가입")

#     new_username = st.text_input("아이디", placeholder="사용할 아이디 입력")
#     new_password = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력")
#     confirm_password = st.text_input("비밀번호 확인", type="password", placeholder="비밀번호 다시 입력")

#     if st.button("회원가입"):
#         if new_password != confirm_password:
#             st.error("비밀번호가 일치하지 않습니다.")
#         elif not new_username or not new_password:
#             st.warning("모든 필드를 입력해주세요.")
#         else:
#             # 회원가입 처리 로직 추가
#             st.success(f"{new_username}님, 회원가입이 완료되었습니다!")
