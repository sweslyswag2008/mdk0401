import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")
USER = os.getenv("DASH_USER", "admin")
PASSWORD = os.getenv("DASH_PASSWORD", "admin")

st.set_page_config(page_title="Библиотека — аналитика", page_icon="📚", layout="wide")
st.title("Библиотека — панель заведующего")


@st.cache_data(ttl=3000)
def get_token():
    r = requests.post(f"{API_URL}/api/auth/login/", json={"username": USER, "password": PASSWORD})
    r.raise_for_status()
    return r.json()["access"]


def api_get(path, **params):
    headers = {"Authorization": f"Bearer {get_token()}"}
    return requests.get(f"{API_URL}/api/reports/{path}/", params=params, headers=headers).json()


with st.sidebar:
    st.header("Фильтры")
    days = st.selectbox("Период", [7, 30, 90, 365], index=1,
                        format_func=lambda x: f"{x} дней")
    if st.button("Обновить"):
        st.cache_data.clear()
        st.rerun()


kpi = api_get("kpi", days=days)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Выдач за период", kpi["loans_count"])
c2.metric("На руках", kpi["on_hands"])
c3.metric("Просрочено", kpi["overdue"])
c4.metric("Штрафы, руб.", f"{kpi['fines_total']:,.0f}")
c5.metric("Книг в фонде", kpi["books_available"])


st.header("Динамика выдач")
loans_df = pd.DataFrame(api_get("loans", days=days))
if not loans_df.empty:
    st.plotly_chart(px.line(loans_df, x="date", y="total", markers=True), use_container_width=True)


col1, col2 = st.columns(2)
with col1:
    st.header("Самые читаемые книги")
    top = pd.DataFrame(api_get("top-books"))
    if not top.empty:
        st.plotly_chart(px.bar(top, x="count", y="title", color="author", orientation="h"),
                        use_container_width=True)
with col2:
    st.header("Загрузка библиотекарей")
    load = pd.DataFrame(api_get("librarian-load", days=days))
    if not load.empty:
        st.plotly_chart(px.pie(load, values="loans", names="librarian"), use_container_width=True)


st.header("Состояние книжного фонда")
stock = pd.DataFrame(api_get("stock"))
if not stock.empty:
    st.plotly_chart(
        px.pie(stock, values="count", names="status",
               color_discrete_map={"available": "green", "reserved": "orange",
                                   "issued": "royalblue", "written_off": "gray"}),
        use_container_width=True)


st.header("Должники")
overdue = pd.DataFrame(api_get("overdue"))
if overdue.empty:
    st.success("Просроченных книг нет")
else:
    st.dataframe(overdue, use_container_width=True)
