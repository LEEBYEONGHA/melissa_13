import streamlit as st
import os
import base64

# 스타일 주입 (사이드바 제거 및 전체 페이지 중앙화)
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
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stHeader"] { background: none; }
        body { background-color: #f1f3f6; }
        h1 { font-size: 28px !important; text-align: center; }
        h3 { font-size: 18px !important; text-align: center; }
        button { font-size: 16px !important; }
    </style>
""", unsafe_allow_html=True)

# 버튼 중앙 정렬
st.markdown("""
    <style>
      div.stButton > button {
        display: block;
        margin: 0 auto;
      }
    </style>
""", unsafe_allow_html=True)

# 이미지 폴더 경로
IMAGE_DIR = os.path.join(os.path.dirname(__file__), '카페 무인 키오스크 이미지')

# 페이지 세션 초기화
if 'page' not in st.session_state:
    st.session_state.page = 1

# 이미지 로드 함수
def get_image_path(page):
    return os.path.join(IMAGE_DIR, f"{page}.png")
def get_image_data(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 히트박스 및 스타일 매핑
hotspot_mapping = {1:("시작하기",2),2:("매장",3),3:("카페라떼",4),4:("차갑게",5),5:("다음",6),6:("중간컵",7),7:("다음",8),8:("+",9),9:("주문하기",10),10:("결제하기",11),11:("아니오",12),12:("신용카드",13),13:("결제완료",14),14:("출력완료",15),15:("예",16),16:("임시버튼",1)}
hitbox_styles = {i:style for i,style in {
    1:{"top":"77%","left":"23%","width":"220px","height":"80px"},
    2:{"top":"41%","left":"13%","width":"146px","height":"147px"},
    3:{"top":"18%","left":"37%","width":"105px","height":"120px"},
    4:{"top":"41%","left":"50%","width":"130px","height":"100px"},
    5:{"top":"82%","left":"50%","width":"130px","height":"55px"},
    6:{"top":"41%","left":"50%","width":"130px","height":"100px"},
    7:{"top":"82%","left":"50%","width":"130px","height":"55px"},
    8:{"top":"75%","left":"39%","width":"30px","height":"55px"},
    9:{"top":"80%","left":"72%","width":"120px","height":"115px"},
    10:{"top":"76%","left":"73%","width":"115px","height":"130px"},
    11:{"top":"70%","left":"14%","width":"150px","height":"110px"},
    12:{"top":"46%","left":"7%","width":"125px","height":"125px"},
    13:{"top":"10%","left":"85%","width":"77px","height":"77px"},
    14:{"top":"3%","left":"86%","width":"70px","height":"70px"},
    15:{"top":"75%","left":"49%","width":"156px","height":"112px"},
    16:{"top":"1%","left":"1%","width":"150px","height":"70px"}
}.items()}

# 쿼리 파라미터로 페이지 이동
if "target_page" in st.query_params:
    raw=st.query_params["target_page"]
    if isinstance(raw,list): raw=raw[0]
    try: st.session_state.page=int(raw)
    except: st.error("잘못된 페이지 번호입니다.")

# 이미지 및 히트박스 링크 설정
path=get_image_path(st.session_state.page)
img_data=get_image_data(path)
if st.session_state.page in hotspot_mapping:
    _, tgt=hotspot_mapping[st.session_state.page]
    href=f"?target_page={tgt}"
else: href="#"
style=hitbox_styles.get(st.session_state.page,{})
inline=f"top:{style.get('top')};left:{style.get('left')};width:{style.get('width')};height:{style.get('height')};line-height:{style.get('height')};"
# 히트박스 CSS
st.markdown("""
<style>
.image-container{position:relative;display:inline-block;}
.hitbox-button{position:absolute;background-color:rgba(255,0,0,0);border:none;cursor:pointer;z-index:9999;}
</style>""",unsafe_allow_html=True)

# 페이지 설명
page_desc={i:("매장에서 차가운 카페라떼를 중간 사이즈로 두 잔 주문하세요<br>포인트 적립은 하지 말고 신용카드로 결제하면서<br>영수증은 챙기세요") for i in range(1,16)}
# page_desc[16]=" 당신의 역량 수준에 맞는 학습하기가 완료되었습니다. 아래의 '점수 확인하기'를 누르세요"
page_desc[16]=" 당신의 역량 수준에 맞는 학습이 완료되었습니다.<br> 아래의 버튼을 눌러 점수를 확인하고 <br>다음 단계로 이동하세요"

# 진행바
total=16
cur=st.session_state.page
prog=int((cur-1)/(total-1)*100)
st.markdown("<div style='margin-top:-30px;text-align:center;font-size:18px;font-weight:bold;'>진행 상황</div>",unsafe_allow_html=True)
st.progress(prog)
st.markdown(f"<p style='font-size:18px;margin-top:-10px;'>현재 <strong>{cur}/{total}</strong> 단계입니다.</p>",unsafe_allow_html=True)

# 이미지 렌더링
st.markdown(f"""
<div style='display:flex;justify-content:center;'><div class='image-container'>
<img src='data:image/png;base64,{img_data}' style='max-width:100%;height:auto;'/>
<a href='{href}' target='_self' class='hitbox-button' style='{inline}'></a>
</div></div>
""",unsafe_allow_html=True)

# 1~15페이지: 문제 보기
if cur!=16:
    if 'show_desc' not in st.session_state: st.session_state.show_desc=False
    lbl="문제 보기" if not st.session_state.show_desc else "문제 숨기기"
    st.markdown("<div style='text-align:center;margin-top:1.5rem;'>",unsafe_allow_html=True)
    if st.button(lbl): st.session_state.show_desc=not st.session_state.show_desc; st.rerun()
    st.markdown("</div>",unsafe_allow_html=True)
    if st.session_state.show_desc:
        st.markdown(f"<div style='text-align:center;font-size:20px;padding:1rem;'>{page_desc[cur]}</div>",unsafe_allow_html=True)

# 16페이지: 점수 확인 로직
if cur==16:
    if 'show_score' not in st.session_state: st.session_state.show_score=False
    if not st.session_state.show_score:
        st.markdown(f"<div style='text-align:center;font-size:18px;padding:1rem;'>{page_desc[16]}</div>",unsafe_allow_html=True)
        if st.button("다음 단계"): st.session_state.show_score=True; st.rerun()
        # if st.button("다음 단계"): st.session_state.show_score=True; st.rerun()
    else:
        # st.markdown("---")
        # st.markdown("<h1 style='text-align:center;color:#4CAF50;'>초기 점수(설문조사 점수)점에서 <br>(문제 풀이 점수)점을 더하여 <br>현재 점수는 (합산)점 입니다",unsafe_allow_html=True)
        # st.markdown("### 👇 다음 단계로 진행하려면 아래 버튼을 누르세요.")
        if st.button("다음 단계"): st.session_state.page=1; st.rerun()
