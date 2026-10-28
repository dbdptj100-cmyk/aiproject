import streamlit as st
st.title('나의 첫 웹 서비스 만들기')
a=st.text_input('이름을 입력하세요!')
b=st.selelctbox('좋아하는 음식을 선택하세요',['마라탕','떡볶이','와플'])
if st.button('인사말 생성'):
  st.write('반갑습니다')
  st.onfo(a+'님, 안녕하세요')
  st.qarning(b+'를 좋아하시는군요!)
  st.error('잘부탁드려요')
