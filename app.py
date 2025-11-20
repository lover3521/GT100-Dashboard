"""GT100 진입전략 대시보드 메인 애플리케이션."""

from pathlib import Path
import math

import altair as alt
import pandas as pd
import streamlit as st


# 대시보드 전역 설정(타이틀, 레이아웃 등)을 한 번만 정의한다.
st.set_page_config(
    page_title="GT100 진입전략 대시보드",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 사이드바 톤앤매너를 통일하기 위한 간단한 CSS 커스터마이징.
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #dadada;
            padding-top: 0.5rem;
        }
        [data-testid="stSidebar"] .sidebar-nav-title {
            font-size: 0.95rem;
            font-weight: 600;
            margin: 0.25rem 0 0.35rem;
        }
        [data-testid="stSidebar"] div[data-baseweb="select"] {
            margin-bottom: 0.8rem;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label {
            padding: 0.15rem 0;
            border-bottom: 1px solid #f0f0f0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# 헤더와 요약 설명을 통해 대시보드 목적을 한 눈에 전달한다.
st.title("GT100 진입전략 대시보드")
st.caption("전북대학교의 GT100 진입전략 수립을 지원하는 내부용 모니터링 페이지입니다.")


summary_cols = st.columns(4)
summary_metrics = [
    {"label": "THE 2026 순위", "value": "801-1000위", "delta": "+0단계"},
    {"label": "QS 2026 순위", "value": "701-710위", "delta": "-10단계"},
    {"label": "논문 수 (최근 5년)", "value": "12,095편", "delta": "+15.5%"},
    {
        "label": "피인용 수 (최근 5년)",
        "value": "158,624회",
        "note": "2020-2024 누적 값",
    },
]
for col, metric in zip(summary_cols, summary_metrics):
    if "delta" in metric:
        col.metric(metric["label"], metric["value"], metric["delta"])
    else:
        col.metric(metric["label"], metric["value"])
    if note := metric.get("note"):
        col.caption(note)

st.divider()


FACT_SHEET_FILE = Path(__file__).with_name("통합 문서1.xlsx")
SCOPUS_EXPORT_FILE = Path(__file__).with_name('Publications_at_Jeonbuk_National_University_2020_-_2024.csv')
