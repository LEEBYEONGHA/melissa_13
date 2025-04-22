import streamlit as st
import streamlit.components.v1 as components
import pandas as pd  # ← 추가

# -----------------------------
# 공통 CSS 스타일 (내부 스크롤 허용)
# -----------------------------
st.markdown("""
    <style>
        .block-container {
            max-width: 450px;
            min-height: 1168px;
            margin: auto;
            background-color: white;
            border: 5px solid #ddd;
            border-radius: 20px;
            padding: 30px 20px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 1.05);
            overflow-y: auto !important;
        }
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stHeader"] { background: none; }
        body { background-color: #f1f3f6; }
        h1 {
            font-size: 28px !important;
            text-align: center;
            margin-bottom: 0.2rem;
        }
        h3 { font-size: 18px !important; text-align: center; }
        button { font-size: 16px !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .block-container h3 {
            margin: 0 !important;
            padding: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)


# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "survey"
if "current_page" not in st.session_state:
    st.session_state.current_page = 0
if "final_score" not in st.session_state:
    st.session_state.final_score = None


# -----------------------------
# 설문 문항 정의 (25문항, 5페이지 × 5문항)
# -----------------------------
questions = [
    {"id":"Q1","text":"문1. 나는 이용 가능한 노트북이 있다.","labels":["예","아니오"],"values":[1.0,0.0],"weight":6.666666667},
    {"id":"Q2","text":"문2. 나는 이용 가능한 스마트패드가 있다.","labels":["예","아니오"],"values":[1.0,0.0],"weight":6.666666667},
    {"id":"Q3","text":"문3. 내가 최근 인터넷을 이용한 시기","labels":["최근 30일 이내 이용했다.","최근 30일 이내 이용한 적이 없다.","전혀없다."],"values":[1.0,0.5,0.0],"weight":6.666666667},
    {"id":"Q4","text":"문4. 나는 필요한 프로그램(소프트웨어)을 컴퓨터에 설치/삭제/업데이트 할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":2.666666667},
    {"id":"Q5","text":"문5. 나는 웹 브라우저에서 원하는 환경을 설정할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":2.666666667},
    {"id":"Q6","text":"문6. 나는 PC에 다양한 외장기기를 연결하여 이용할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":2.666666667},
    {"id":"Q7","text":"문7. 나는 PC에 있는 파일을 인터넷을 통해 다른 사람에게 전송할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":2.666666667},
    {"id":"Q8","text":"문8. 나는 PC의 악성코드를 검사/치료할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":2.666666667},
    {"id":"Q9","text":"문9. 나는 PC에서 문서를 작성할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":2.666666667},
    {"id":"Q10","text":"문10. 나는 비대면 원격회의 앱을 이용해 회의를 개최할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":8.0},
    {"id":"Q11","text":"문11. 온라인 협업프로그램을 이용해 다른 사람과 함께 과제를 할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":2.0},
    {"id":"Q12","text":"문12. 관심사와 비슷한 커뮤니티를 찾아 참여할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":2.0},
    {"id":"Q13","text":"문13. 소셜미디어에 글을 쓸 때 공개범위를 설정할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":2.0},
    {"id":"Q14","text":"문14. IoT 기기를 활용할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":2.0},
    {"id":"Q15","text":"문15. 허위조작정보를 구별하기 위해 참고자료를 활용할 수 있다.","labels":["매우 그렇다","그런 편이다","보통이다","그렇지 않은 편이다","전혀 그렇지 않다"],"values":[1.0,0.75,0.5,0.25,0.0],"weight":8.0},
    {"id":"Q16","text":"문16. 이메일 서비스를 얼마나 이용하셨습니까?","labels":["자주 이용한다","다소 이용하는 편이다","별로 이용 안하는 편이다","전혀 이용 안한다","이용해 본적이 없다."],"values":[1.0,0.75,0.5,0.25,0.0],"weight":3.2},
    {"id":"Q17","text":"문17. 미디어콘텐츠 서비스를 얼마나 이용하셨습니까?","labels":["자주 이용한다","다소 이용하는 편이다","별로 이용 안하는 편이다","전혀 이용 안한다","이용해 본적이 없다."],"values":[1.0,0.75,0.5,0.25,0.0],"weight":3.2},
    {"id":"Q18","text":"문18. 개인블로그를 얼마나 이용하셨습니까?","labels":["자주 이용한다","다소 이용하는 편이다","별로 이용 안하는 편이다","전혀 이용 안한다","이용해 본적이 없다."],"values":[1.0,0.75,0.5,0.25,0.0],"weight":5.333333333},
    {"id":"Q19","text":"문19. SNS 서비스를 얼마나 이용하셨습니까?","labels":["자주 이용한다","다소 이용하는 편이다","별로 이용 안하는 편이다","전혀 이용 안한다","이용해 본적이 없다."],"values":[1.0,0.75,0.5,0.25,0.0],"weight":5.333333333},
    {"id":"Q20","text":"문20. 생활정보 서비스를 얼마나 이용하셨습니까?","labels":["자주 이용한다","다소 이용하는 편이다","별로 이용 안하는 편이다","전혀 이용 안한다","이용해 본적이 없다."],"values":[1.0,0.75,0.5,0.25,0.0],"weight":3.2},
    {"id":"Q21","text":"문21. 전자상거래 서비스를 얼마나 이용하셨습니까?","labels":["자주 이용한다","다소 이용하는 편이다","별로 이용 안하는 편이다","전혀 이용 안한다","이용해 본적이 없다."],"values":[1.0,0.75,0.5,0.25,0.0],"weight":3.2},
    {"id":"Q22","text":"문22. 금융거래 서비스를 얼마나 이용하셨습니까?","labels":["자주 이용한다","다소 이용하는 편이다","별로 이용 안하는 편이다","전혀 이용 안한다","이용해 본적이 없다."],"values":[1.0,0.75,0.5,0.25,0.0],"weight":3.2},
    {"id":"Q23","text":"문23. 만든 콘텐츠를 SNS에 올린 적이 있습니까?","labels":["자주 이용한다","다소 이용하는 편이다","별로 이용 안하는 편이다","전혀 이용 안한다","이용해 본적이 없다."],"values":[1.0,0.75,0.5,0.25,0.0],"weight":5.333333333},
    {"id":"Q24","text":"문24. 사회적 관심사에 대해 의견 표명을 한 적이 있습니까?","labels":["자주 이용한다","다소 이용하는 편이다","별로 이용 안하는 편이다","전혀 이용 안한다","이용해 본적이 없다."],"values":[1.0,0.75,0.5,0.25,0.0],"weight":4.0},
    {"id":"Q25","text":"문25. 공공기관에 정책 제안을 한 적이 있습니까?","labels":["자주 이용한다","다소 이용하는 편이다","별로 이용 안하는 편이다","전혀 이용 안한다","이용해 본적이 없다."],"values":[1.0,0.75,0.5,0.25,0.0],"weight":4.0},
]


# -----------------------------
# 점수 계산 및 결과 페이지로 이동
# -----------------------------
def calculate_and_go():
    total_score = 0.0
    for q in questions:
        choice = st.session_state.get(q["id"], q["labels"][0])
        idx = q["labels"].index(choice)
        total_score += q["values"][idx] * q["weight"]
    st.session_state.final_score = total_score
    st.session_state.page = "result"

# def calculate_and_go():
#     # 1) 영역별 문항 ID 정의
#     access_qs = ["Q1", "Q2", "Q3"]
#     competency_qs = ["Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15"]
#     utilization_qs = [q["id"] for q in questions if q["id"] not in access_qs + competency_qs]

#     # 2) 그룹별 백분율 점수 계산 함수
#     def calc_group_score(q_ids):
#         total = 0.0
#         total_weight = 0.0
#         for q in questions:
#             if q["id"] in q_ids:
#                 choice = st.session_state.get(q["id"], q["labels"][0])
#                 idx = q["labels"].index(choice)
#                 total += q["values"][idx] * q["weight"]
#                 total_weight += q["weight"]
#         # (가중합 ÷ 총가중치) * 100 → 백분율
#         return (total / total_weight) * 100 if total_weight > 0 else 0

#     # 3) 각 영역별 점수
#     access_score      = calc_group_score(access_qs)
#     competency_score  = calc_group_score(competency_qs)
#     utilization_score = calc_group_score(utilization_qs)

#     # 4) 최종 가중평균
#     total_score = 0.2 * access_score + 0.4 * competency_score + 0.4 * utilization_score

#     # 5) 결과 저장 후 결과 페이지로 이동
#     st.session_state.final_score = total_score
#     st.session_state.page        = "result"




# -----------------------------
# 설문조사 페이지 (5페이지 × 5문항)
# -----------------------------
def survey_page():
    st.markdown(
        "<h1>디지털 정보화 수준 자가 진단</h1>",
        unsafe_allow_html=True
    )
    page = st.session_state.current_page
    total_pages = 5
    progress = int(page / (total_pages - 1) * 100)
    st.markdown(f"<div style='text-align:center; font-weight:bold;'>진행 상황 {page+1}/{total_pages}</div>", unsafe_allow_html=True)
    st.progress(progress)

    start = page * 5
    for q in questions[start:start+5]:
        st.radio(q["text"], q["labels"], key=q["id"])

    cols = st.columns([1,2,1])
    if page > 0:
        cols[0].button("이전", on_click=lambda: st.session_state.update({"current_page": page-1}))
    if page < total_pages - 1:
        cols[2].button("다음", on_click=lambda: st.session_state.update({"current_page": page+1}))
    else:
        cols[2].button("점수 받기", on_click=calculate_and_go)


# -----------------------------
# 결과 출력 페이지
# -----------------------------
def result_page():
    st.markdown('<a name="top"></a>', unsafe_allow_html=True)
    components.html('<script>window.location.href="#top";</script>', height=0)

    st.title("디지털 정보화 수준 예측 결과")
    score = st.session_state.get("final_score", None)
    if score is None:
        st.error("설문조사 데이터를 찾을 수 없습니다.")
        if st.button("설문조사 페이지로"):
            st.session_state.page = "survey"
            st.session_state.current_page = 0
        return

    # 기존 결과 부분 건드리지 않음
    st.markdown(f"## {score:.2f}점")
    if score >= 80:
        st.success(
            "L4: 상급 (80점 이상)\n"
            "- 고숙련자 구간, 일반국민 최고 수준\n"
            "- ACSF Level 3 (자율적 활용 가능)\n"
            "- 독립적 정보 검색, 트러블슈팅, 인증 기반 활용"
        )
    elif 60 <= score < 80:
        st.info(
            "L3: 중급 (60~79점)\n"
            "- 일반국민 평균 수준\n"
            "- ACSF Level 2 (일상적 작업 수행)\n"
            "- 인터넷 활용, 앱 설치, 계정관리 등 반복 가능한 실습"
        )
    elif 40 <= score < 60:
        st.warning(
            "L2: 초급 (40~59점)\n"
            "- 정보취약계층 평균 수준 이하\n"
            "- ACSF Level 1 (기초적 조작 가능)\n"
            "- 기본 터치, 키오스크 메뉴 탐색, 간단한 입력 등"
        )
    else:
        st.error(
            "L1: 위험군 (39점 이하)\n"
            "- 디지털 소외 우려 그룹\n"
            "- ACSF Pre‑level (지원 필요)\n"
            "- 버튼 인식, 홈/뒤로 이동도 어려움 → 시뮬레이션 필수"
        )

    # → 여기부터 추가된 도메인별 정밀 분류 차트
    domain_map = {
        "접근":            ["Q1","Q2","Q3"],
        "기본기술 역량":    ["Q4","Q5","Q6","Q7","Q8","Q9","Q10"],
        "생활활용 역량":    ["Q11","Q16","Q17","Q20","Q21","Q22"],
        "생산과 공유 역량": ["Q18","Q23"],
        "사회참여 역량":    ["Q12","Q19","Q24","Q25"],
        "권리보호 역량":    ["Q13"],
        "비판적 이해 역량":["Q14"],
        "보안":            ["Q15"],
    }
    resp = {}
    for q in questions:
        ans = st.session_state.get(q["id"])
        idx = q["labels"].index(ans) if ans in q["labels"] else len(q["values"])-1
        resp[q["id"]] = q["values"][idx]
    domain_scores = {
        dom: sum(resp[qid] for qid in qids)/len(qids)*100
        for dom, qids in domain_map.items()
    }
    chart_df = (
        pd.DataFrame({
            "도메인": list(domain_scores.keys()),
            "점수":   list(domain_scores.values())
        })
        .sort_values("점수", ascending=False)
        .set_index("도메인")
    )
    st.subheader("도메인별 정밀 분류 점수")
    st.bar_chart(chart_df)
    # ← 추가 끝

    st.markdown(
        """
        <div style="
            display: flex;
            justify-content: space-between;
            margin-top: 1.5rem;
        ">
            <a href="/k19" target="_self" style="width:48%; text-decoration:none;">
                <button style="
                    width:100%;
                    padding:0.6rem 1.2rem;
                    font-size:1rem;
                    border:none;
                    border-radius:8px;
                    cursor:pointer;
                    background-color: #e0e0e0;
                ">
                    학습하기
                </button>
            </a>
            <a href="/" target="_self" style="width:48%; text-decoration:none;">
                <button style="
                    width:100%;
                    padding:0.6rem 1.2rem;
                    font-size:1rem;
                    border:none;
                    border-radius:8px;
                    cursor:pointer;
                    background-color: #e0e0e0;
                ">
                    메인 화면
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # if st.button("작업용 임시버튼"):
    #     st.session_state.page = "survey"
    #     st.session_state.current_page = 0


# -----------------------------
# 페이지 제어
# -----------------------------
if st.session_state.page == "survey":
    survey_page()
else:
    result_page()