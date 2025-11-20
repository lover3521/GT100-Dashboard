"""GT100 진입전략 대시보드 메인 애플리케이션."""

import math
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


# 기본 페이지 설정
st.set_page_config(
    page_title="GT100 진입전략 대시보드",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 사이드바 톤앤매너
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
            margin: 0.25rem 0 0.5rem;
        }
        [data-testid="stSidebar"] div[data-baseweb="select"] {
            margin-bottom: 0.8rem;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label {
            padding: 0.2rem 0;
            border-bottom: 1px solid #f0f0f0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 헤더
st.title("GT100 진입전략 대시보드")
st.caption("전북대학교의 GT100 진입전략 수립을 지원하는 내부용 모니터링 페이지입니다.")

# 상단 KPI
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

# 데이터 소스 경로
FACT_SHEET_FILE = Path(__file__).with_name("통합 문서1.xlsx")
SCOPUS_EXPORT_FILE = Path(__file__).with_name(
    "Publications_at_Jeonbuk_National_University_2020_-_2024.csv"
)

# 기본 Fact Sheet (엑셀 미제공 시 사용)
EMBEDDED_FACT_SHEET = {
    "영향력(Impact)": [
        {
            "label": "논문수",
            "unit": "편",
            "values": {2020: 2180, 2021: 2434, 2022: 2433, 2023: 2530, 2024: 2518},
        },
        {
            "label": "총인용수",
            "unit": "회",
            "values": {2020: 48108, 2021: 44630, 2022: 31855, 2023: 23535, 2024: 10496},
        },
        {
            "label": "논문당 평균 인용수",
            "unit": "회",
            "values": {2020: 22.07, 2021: 18.34, 2022: 13.09, 2023: 9.30, 2024: 4.17},
        },
        {
            "label": "FWCI",
            "unit": "",
            "values": {2020: 1.06, 2021: 1.08, 2022: 1.11, 2023: 1.13, 2024: 1.09},
        },
        {
            "label": "피인용 논문 비율",
            "unit": "%",
            "values": {2020: 94.2, 2021: 93.8, 2022: 92.7, 2023: 88.6, 2024: 77.8},
        },
        {
            "label": "매체 노출 및 분야 다양성",
            "unit": "",
            "values": {2020: 390, 2021: 183, 2022: 115, 2023: 159, 2024: None},
        },
    ],
    "우수성(Excellence)": [
        {
            "label": "상위 1% 논문 수",
            "unit": "편",
            "values": {2020: 14, 2021: 29, 2022: 24, 2023: 34, 2024: 32},
        },
        {
            "label": "상위 1% 논문 비율",
            "unit": "%",
            "values": {2020: 0.7, 2021: 1.3, 2022: 1.1, 2023: 1.5, 2024: 1.4},
        },
        {
            "label": "상위 10% 논문 수",
            "unit": "편",
            "values": {2020: 269, 2021: 263, 2022: 309, 2023: 331, 2024: 315},
        },
        {
            "label": "상위 10% 논문 비율",
            "unit": "%",
            "values": {2020: 13.3, 2021: 11.7, 2022: 13.6, 2023: 14.2, 2024: 13.5},
        },
        {
            "label": "Q1 저널 논문 수",
            "unit": "편",
            "values": {2020: 1048, 2021: 1274, 2022: 1374, 2023: 1498, 2024: 1590},
        },
        {
            "label": "Q1 저널 논문 비율",
            "unit": "%",
            "values": {2020: 53.1, 2021: 57.5, 2022: 61.1, 2023: 65.0, 2024: 68.3},
        },
    ],
    "협력(Collaboration)": [
        {
            "label": "국제 공동연구 논문 수",
            "unit": "편",
            "values": {2020: 618, 2021: 700, 2022: 706, 2023: 768, 2024: 768},
        },
        {
            "label": "국제 공동연구 논문 비율",
            "unit": "%",
            "values": {2020: 30.5, 2021: 31.1, 2022: 31.0, 2023: 33.0, 2024: 32.8},
        },
        {
            "label": "국제 공동연구 FWCI",
            "unit": "",
            "values": {2020: 0.67, 2021: 0.70, 2022: 0.71, 2023: 0.75, 2024: 0.75},
        },
        {
            "label": "국내 공동연구 논문 수",
            "unit": "편",
            "values": {2020: 898, 2021: 1005, 2022: 993, 2023: 1017, 2024: 1018},
        },
        {
            "label": "국내 공동연구 논문 비율",
            "unit": "%",
            "values": {2020: 44.3, 2021: 44.7, 2022: 43.6, 2023: 43.7, 2024: 43.5},
        },
        {
            "label": "인용 국가 수",
            "unit": "개",
            "values": {2020: 166, 2021: 165, 2022: 161, 2023: 159, 2024: 141},
        },
    ],
    "공공성 및 개방성": [
        {
            "label": "오픈 액세스 논문 수",
            "unit": "편",
            "values": {2020: 1076, 2021: 1297, 2022: 1310, 2023: 1340, 2024: 1282},
        },
        {
            "label": "오픈 액세스 논문 비율",
            "unit": "%",
            "values": {2020: 49.36, 2021: 53.29, 2022: 53.84, 2023: 52.96, 2024: 50.91},
        },
        {
            "label": "열람 수",
            "unit": "건",
            "values": {2020: 58142, 2021: 70857, 2022: 54029, 2023: 55552, 2024: 36628},
        },
        {
            "label": "미디어 인용 수",
            "unit": "건",
            "values": {2020: 15, 2021: 17, 2022: 9, 2023: 19, 2024: 8},
        },
        {
            "label": "주제 분야 수",
            "unit": "개",
            "values": {2020: 277, 2021: 281, 2022: 284, 2023: 292, 2024: 285},
        },
    ],
}


def _looks_like_year(label: object) -> bool:
    label_str = str(label)
    return label_str.isdigit() and 1900 <= int(label_str) <= 2100


def build_fact_sheet_df_from_embedded() -> pd.DataFrame:
    records: list[dict[str, object]] = []
    for indicator_group, entries in EMBEDDED_FACT_SHEET.items():
        for entry in entries:
            row: dict[str, object] = {
                "indicator_group": indicator_group,
                "지표명": entry["label"],
                "단위": entry.get("unit", "") or "-",
            }
            for year, value in entry["values"].items():
                try:
                    row[int(year)] = value
                except (TypeError, ValueError):
                    continue
            records.append(row)
    return pd.DataFrame(records)


@st.cache_data
def load_fact_sheet_data(xlsx_path: str) -> pd.DataFrame:
    try:
        raw_df = pd.read_excel(xlsx_path)
    except Exception:
        return build_fact_sheet_df_from_embedded()
    if raw_df.empty:
        return build_fact_sheet_df_from_embedded()

    category_col, indicator_col = raw_df.columns[:2]
    fact_df = raw_df.rename(columns={category_col: "indicator_group", indicator_col: "지표명"})
    fact_df["indicator_group"] = fact_df["indicator_group"].ffill()

    year_columns: list[int] = []
    for column in fact_df.columns[2:]:
        if _looks_like_year(column):
            year = int(column)
            fact_df[year] = pd.to_numeric(fact_df[column], errors="coerce")
            year_columns.append(year)
            if column != year:
                fact_df = fact_df.drop(columns=[column])

    if "단위" not in fact_df.columns:
        fact_df["단위"] = "-"

    base_columns = ["indicator_group", "지표명", "단위"] + sorted(set(year_columns))
    fact_df = fact_df[base_columns]
    return fact_df.reset_index(drop=True)


def get_fact_sheet_dataframe() -> pd.DataFrame:
    if not FACT_SHEET_FILE.exists():
        return build_fact_sheet_df_from_embedded()
    return load_fact_sheet_data(str(FACT_SHEET_FILE))


def get_fact_sheet_year_columns(fact_df: pd.DataFrame) -> list[int]:
    return sorted(col for col in fact_df.columns if isinstance(col, int))


def build_indicator_dataframe(fact_df: pd.DataFrame, indicator: str) -> pd.DataFrame:
    if fact_df.empty:
        return pd.DataFrame()
    year_columns = get_fact_sheet_year_columns(fact_df)
    display_columns = ["지표명", "단위"] + year_columns
    subset = fact_df[fact_df["indicator_group"] == indicator][display_columns].copy()
    return subset.reset_index(drop=True)


def rank_range_to_midpoint(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.replace("위", "").strip()
        if "-" in cleaned:
            low, high = cleaned.split("-", 1)
            try:
                return (float(low) + float(high)) / 2
            except ValueError:
                return None
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def describe_rank_delta(current: object, previous: object) -> str | None:
    current_mid = rank_range_to_midpoint(current)
    previous_mid = rank_range_to_midpoint(previous)
    if current_mid is None or previous_mid is None:
        return None
    diff = previous_mid - current_mid
    diff_value = int(round(abs(diff)))
    if diff_value == 0:
        return None
    direction = "개선" if diff > 0 else "하락"
    return f"{diff_value}위 {direction}"


SCIVAL_BENCHMARK_MULTIPLIERS = {
    "전북대": 1.00,
    "University A": 1.12,
    "University B": 0.94,
}


def build_scival_benchmark_dataframe(year: int, fact_df: pd.DataFrame) -> pd.DataFrame:
    columns = []
    data = {uni: [] for uni in SCIVAL_BENCHMARK_MULTIPLIERS}
    for _, row in fact_df.iterrows():
        unit = row.get("단위", "")
        label = row["지표명"]
        label_with_unit = f"{label} ({unit})" if unit and unit != "-" else label
        columns.append((row["indicator_group"], label_with_unit))
        base_value = row.get(year)
        for uni, multiplier in SCIVAL_BENCHMARK_MULTIPLIERS.items():
            if pd.notna(base_value):
                value = round(float(base_value) * multiplier, 2)
            else:
                value = None
            data[uni].append(value)
    multi_columns = pd.MultiIndex.from_tuples(columns, names=["분야", "지표"])
    universities = list(SCIVAL_BENCHMARK_MULTIPLIERS.keys())
    values = [data[uni] for uni in universities]
    df = pd.DataFrame(values, columns=multi_columns, index=universities)
    df.index.name = "기관"
    return df


def render_global_ranking_tab() -> None:
    st.subheader("Global Ranking")
    ranking_df = pd.DataFrame(
        [
            {"연도": 2022, "THE": "1001-1200", "QS": "571-580"},
            {"연도": 2023, "THE": "1001-1200", "QS": "551-560"},
            {"연도": 2024, "THE": "801-1000", "QS": "721-730"},
            {"연도": 2025, "THE": "801-1000", "QS": "681-690"},
            {"연도": 2026, "THE": "801-1000", "QS": "701-710"},
        ]
    )
    ranking_df["THE_value"] = ranking_df["THE"].apply(rank_range_to_midpoint)
    ranking_df["QS_value"] = ranking_df["QS"].apply(rank_range_to_midpoint)

    cols = st.columns(2)
    the_delta = describe_rank_delta(ranking_df.iloc[-1]["THE"], ranking_df.iloc[-2]["THE"])
    qs_delta = describe_rank_delta(ranking_df.iloc[-1]["QS"], ranking_df.iloc[-2]["QS"])
    cols[0].metric("THE 2026", ranking_df.iloc[-1]["THE"], the_delta)
    cols[1].metric("QS 2026", ranking_df.iloc[-1]["QS"], qs_delta)

    chart_records: list[dict[str, object]] = []
    for _, row in ranking_df.iterrows():
        for scheme in ("THE", "QS"):
            numeric_value = row[f"{scheme}_value"]
            if numeric_value is None:
                continue
            chart_records.append(
                {
                    "연도": row["연도"],
                    "평가": scheme,
                    "rank_value": numeric_value,
                    "원본 구간": row[scheme],
                }
            )
    if chart_records:
        chart_df = pd.DataFrame(chart_records)
        chart = (
            alt.Chart(chart_df)
            .mark_line(point=True)
            .encode(
                x=alt.X("연도:O", title="연도"),
                y=alt.Y(
                    "rank_value:Q",
                    title="순위 (낮을수록 우수)",
                    scale=alt.Scale(reverse=True),
                ),
                color=alt.Color(
                    "평가:N",
                    title="평가 체계",
                    scale=alt.Scale(domain=["THE", "QS"], range=["#ec008c", "#f5a623"]),
                ),
                tooltip=["연도:O", "평가:N", "원본 구간:N", alt.Tooltip("rank_value:Q", title="대표값")],
            )
            .properties(height=320)
        )
        st.altair_chart(chart, use_container_width=True)
    st.dataframe(ranking_df[["연도", "THE", "QS"]], use_container_width=True, hide_index=True)


def render_fact_sheet_tab() -> None:
    st.subheader("Fact Sheet")
    metric_cols = st.columns(3)
    summary_metrics = [
        ("재학생 수", "28,450명", "+1.2%"),
        ("전임교원 수", "1,760명", "+0.9%"),
        ("R&D 투자", "4,280억원", "+3.9%"),
    ]
    for col, (label, value, delta) in zip(metric_cols, summary_metrics):
        col.metric(label, value, delta)

    fact_df = get_fact_sheet_dataframe()
    if fact_df.empty:
        st.warning("표시할 Fact Sheet 데이터가 없습니다.")
        return

    indicator_groups = fact_df["indicator_group"].dropna().unique().tolist()
    year_columns = get_fact_sheet_year_columns(fact_df)
    if not indicator_groups or not year_columns:
        st.warning("Fact Sheet 지표 구성이 올바르지 않습니다.")
        return

    st.markdown("#### 지표 상세 보기")
    detail_indicator = st.selectbox(
        "지표 그룹 선택",
        indicator_groups,
        key="fact-detail-indicator",
    )
    detail_df = build_indicator_dataframe(fact_df, detail_indicator)
    if detail_df.empty:
        st.info("해당 지표 그룹 데이터가 없습니다.")
    else:
        detail_display = detail_df.copy()
        palette_cycle = ["#fde9f4", "#eef6ff", "#fef5e5", "#f3f9ef", "#f1e9ff"]
        group_palette = {g: palette_cycle[i % len(palette_cycle)] for i, g in enumerate(indicator_groups)}
        if "단위" in detail_display.columns:
            detail_display["지표명"] = detail_display.apply(
                lambda row: (
                    row["지표명"]
                    if row.get("단위") in ("", "-", None)
                    else f"{row['지표명']} ({row['단위']})"
                ),
                axis=1,
            )
            detail_display = detail_display.drop(columns=["단위"], errors="ignore")
        detail_years = [c for c in detail_display.columns if isinstance(c, int)]
        if detail_years:
            detail_display[detail_years] = detail_display[detail_years].applymap(
                lambda v: "-" if pd.isna(v) else (f"{int(v):,}" if float(v).is_integer() else f"{float(v):,.2f}")
            )
        detail_color = group_palette.get(detail_indicator, "#fafafa")
        def _detail_highlight(_row: pd.Series) -> list[str]:
            return [f"background-color: {detail_color}"] * len(detail_display.columns)
        st.dataframe(
            detail_display.style.apply(_detail_highlight, axis=1),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("#### 지표 추이 차트")
    chart_indicator = st.selectbox(
        "차트 지표 그룹",
        indicator_groups,
        key="fact-chart-indicator",
    )
    chart_df = build_indicator_dataframe(fact_df, chart_indicator)
    numeric_years = [col for col in chart_df.columns if isinstance(col, int)]
    if numeric_years:
        year_min, year_max = min(numeric_years), max(numeric_years)
        year_range = st.slider(
            "연도 범위",
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max),
            step=1,
        )
        c1, c2 = st.columns(2)
        start_input = c1.number_input("시작 연도", min_value=year_min, max_value=year_max, value=year_range[0], step=1)
        end_input = c2.number_input("종료 연도", min_value=year_min, max_value=year_max, value=year_range[1], step=1)
        if start_input > end_input:
            start_input, end_input = end_input, start_input
        year_range = (start_input, end_input)
        metric_multi = st.multiselect(
            "차트 지표 선택",
            chart_df["지표명"],
            default=list(chart_df["지표명"][: min(2, len(chart_df))]),
        )
        if metric_multi:
            plot_df = chart_df[chart_df["지표명"].isin(metric_multi)].set_index("지표명")[numeric_years].T
            filtered_plot = plot_df.loc[(plot_df.index >= year_range[0]) & (plot_df.index <= year_range[1])]
            st.line_chart(filtered_plot)
        else:
            st.info("차트로 보고 싶은 지표를 선택해 주세요.")
    else:
        st.info("연도 데이터가 없어 차트를 그릴 수 없습니다.")

    st.markdown("#### 전체 Fact Sheet")
    combined_df = []
    for indicator_name in indicator_groups:
        df = build_indicator_dataframe(fact_df, indicator_name)
        if df.empty:
            continue
        df = df.copy()
        df.insert(0, "지표 그룹", indicator_name)
        combined_df.append(df)
    if combined_df:
        master_df = pd.concat(combined_df, ignore_index=True)
        display_df = master_df.reset_index(drop=True)
        year_cols = [c for c in display_df.columns if isinstance(c, int)]

        def format_value(val: object) -> object:
            if pd.isna(val):
                return "-"
            try:
                num = float(val)
            except (TypeError, ValueError):
                return val
            if num.is_integer():
                return f"{int(num):,}"
            return f"{num:,.2f}"

        if year_cols:
            display_df[year_cols] = display_df[year_cols].applymap(format_value)

        display_df["지표명"] = display_df.apply(
            lambda row: row["지표명"] if row.get("단위") in ("", "-", None) else f"{row['지표명']} ({row['단위']})",
            axis=1,
        )
        display_df = display_df.drop(columns=["단위"], errors="ignore")

        display_df["__group"] = display_df["지표 그룹"]
        display_df["지표 그룹"] = display_df["지표 그룹"].where(~display_df["지표 그룹"].duplicated(), "")

        palette_cycle = ["#fde9f4", "#eef6ff", "#fef5e5", "#f3f9ef", "#f1e9ff"]
        group_palette = {g: palette_cycle[i % len(palette_cycle)] for i, g in enumerate(indicator_groups)}
        color_series = display_df["__group"].map(group_palette).fillna("#fafafa")

        def highlight_group(row: pd.Series) -> list[str]:
            color = color_series[row.name]
            return [f"background-color: {color}"] * len(row)

        styled_df = (
            display_df.drop(columns=["__group"])
            .style.apply(highlight_group, axis=1)
            .set_properties(subset=["지표 그룹"], **{"font-weight": "600"})
        )
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("표시할 Fact Sheet 데이터가 없습니다.")
    st.caption("지표명 뒤 괄호 안에 단위를 표시했습니다.")


@st.cache_data
def load_publication_csv(csv_path: str) -> pd.DataFrame:
    """Scopus에서 내려받은 CSV를 읽는다(인코딩 자동 판별)."""
    try:
        return pd.read_csv(csv_path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(csv_path, encoding="cp949")


def _build_sample_publications() -> pd.DataFrame:
    """Scopus 데이터를 사용할 수 없을 때 쓰는 예시 데이터."""
    return pd.DataFrame(
        [
            {
                "논문명": "Smart Agriculture using AI",
                "저널/컨퍼런스": "Nature Food",
                "발행년도": 2024,
                "문서 유형": "Article",
                "피인용수": 42,
                "저자": "Kim et al.",
                "DOI": "-",
                "링크": "-",
            },
            {
                "논문명": "Energy Storage Materials",
                "저널/컨퍼런스": "Advanced Energy Materials",
                "발행년도": 2023,
                "문서 유형": "Article",
                "피인용수": 55,
                "저자": "Lee et al.",
                "DOI": "-",
                "링크": "-",
            },
        ]
    )


def get_publications_dataframe() -> pd.DataFrame:
    """전북대 논문 목록을 반환한다."""
    if SCOPUS_EXPORT_FILE.exists():
        try:
            raw_df = load_publication_csv(str(SCOPUS_EXPORT_FILE))
        except Exception:
            raw_df = pd.DataFrame()
    else:
        raw_df = pd.DataFrame()

    if raw_df.empty:
        return _build_sample_publications()

    df = pd.DataFrame(
        {
            "논문명": raw_df.get("Title", ""),
            "저널/컨퍼런스": raw_df.get("Scopus Source title", "").fillna("미상"),
            "발행년도": pd.to_numeric(raw_df.get("Year"), errors="coerce"),
            "문서 유형": raw_df.get("Publication type", "").fillna("기타"),
            "피인용수": pd.to_numeric(raw_df.get("Citations"), errors="coerce"),
            "저자": raw_df.get("Authors", "").fillna("-"),
            "DOI": raw_df.get("DOI", "").fillna("-"),
            "링크": raw_df.get("Publication link to Topic strength", "").fillna("-"),
        }
    )
    df = df.dropna(subset=["발행년도"]).copy()
    df["발행년도"] = df["발행년도"].astype(int)
    df["피인용수"] = df["피인용수"].fillna(0).astype(int)
    df["논문명"] = df["논문명"].replace("", "-")
    df["저널/컨퍼런스"] = df["저널/컨퍼런스"].replace("", "미상")
    df["문서 유형"] = df["문서 유형"].replace("", "기타")
    df["DOI"] = df["DOI"].replace("", "-")
    df["링크"] = df["링크"].replace("", "-")
    return df.reset_index(drop=True)


def render_publications_tab() -> None:
    """전북대 논문 목록 표시."""
    st.subheader("전북대 논문 목록")
    publications_df = get_publications_dataframe()
    if publications_df.empty:
        st.info("표시할 논문 데이터가 없습니다.")
        return

    data_min = int(publications_df["발행년도"].min())
    data_max = int(publications_df["발행년도"].max())
    slider_min = min(2020, data_min)
    slider_max = max(2024, data_max)
    year_range = st.slider(
        "발행년도",
        slider_min,
        slider_max,
        (slider_min, slider_max),
    )

    doc_types = sorted(publications_df["문서 유형"].dropna().unique().tolist())
    selected_types = st.multiselect(
        "문서 유형",
        options=doc_types,
        default=doc_types,
    )
    page_size = st.selectbox(
        "페이지 당 표시 건수",
        options=[10, 50, 100],
        index=0,
    )

    filtered = publications_df[
        publications_df["발행년도"].between(year_range[0], year_range[1])
        & publications_df["문서 유형"].isin(selected_types)
    ]

    if filtered.empty:
        st.info("조건에 맞는 논문이 없습니다.")
        return

    filter_signature = (year_range, tuple(sorted(selected_types)), page_size)
    page_state_key = "publications_page"
    signature_key = "publications_page_signature"
    if st.session_state.get(signature_key) != filter_signature:
        st.session_state[page_state_key] = 1
        st.session_state[signature_key] = filter_signature

    total_pages = max(1, math.ceil(len(filtered) / page_size))
    current_page = st.session_state.get(page_state_key, 1)
    current_page = max(1, min(current_page, total_pages))
    st.session_state[page_state_key] = current_page

    start_idx = (current_page - 1) * page_size
    end_idx = start_idx + page_size
    page_df = filtered.iloc[start_idx:end_idx]

    navbar = st.container()
    if total_pages > 1:
        num_buttons = min(5, total_pages)
        window_start = max(1, current_page - num_buttons // 2)
        window_end = min(total_pages, window_start + num_buttons - 1)
        window_start = max(1, window_end - num_buttons + 1)
        page_numbers = list(range(window_start, window_end + 1))
        cols = navbar.columns(len(page_numbers) + 4)
        if cols[0].button("« 처음", disabled=current_page == 1):
            st.session_state[page_state_key] = 1
            st.experimental_rerun()
        if cols[1].button("‹ 이전", disabled=current_page == 1):
            st.session_state[page_state_key] = current_page - 1
            st.experimental_rerun()
        for idx, page_num in enumerate(page_numbers):
            if cols[idx + 2].button(str(page_num), disabled=page_num == current_page):
                st.session_state[page_state_key] = page_num
                st.experimental_rerun()
        if cols[-2].button("다음 ›", disabled=current_page == total_pages):
            st.session_state[page_state_key] = current_page + 1
            st.experimental_rerun()
        if cols[-1].button("마지막 »", disabled=current_page == total_pages):
            st.session_state[page_state_key] = total_pages
            st.experimental_rerun()

    table_height = min(900, 160 + page_size * 35)
    display_columns = [
        "발행년도",
        "문서 유형",
        "논문명",
        "저널/컨퍼런스",
        "저자",
        "피인용수",
        "DOI",
        "링크",
    ]
    st.dataframe(
        page_df[display_columns],
        use_container_width=True,
        hide_index=True,
        height=table_height,
    )
    st.caption(f"총 {len(filtered):,}건 · 페이지 {current_page}/{total_pages}")
    st.download_button(
        "CSV 다운로드",
        filtered.to_csv(index=False).encode("utf-8-sig"),
        file_name="jbnu_publications.csv",
        mime="text/csv",
    )


def render_benchmark_the_qs_tab() -> None:
    st.subheader("벤치마킹 대학 비교 (THE/QS)")
    comparison_df = pd.DataFrame(
        [
            {"대학": "전북대", "지표": "교육(Teaching)", "THE": 25.1, "QS": 18.4},
            {"대학": "University A", "지표": "교육(Teaching)", "THE": 38.3, "QS": 32.1},
            {"대학": "전북대", "지표": "연구(Research)", "THE": 24.3, "QS": 21.4},
            {"대학": "University A", "지표": "연구(Research)", "THE": 40.2, "QS": 36.8},
        ]
    )
    indicator = st.selectbox("비교 지표", sorted(comparison_df["지표"].unique()))
    scheme = st.selectbox("평가 체계", ["THE", "QS"])
    pivot_df = (
        comparison_df[comparison_df["지표"] == indicator][["대학", scheme]]
        .set_index("대학")
        .rename(columns={scheme: "점수"})
    )
    st.bar_chart(pivot_df)
    st.dataframe(
        comparison_df[comparison_df["지표"] == indicator],
        use_container_width=True,
        hide_index=True,
    )


def render_benchmark_scival_tab() -> None:
    st.subheader("벤치마킹 대학 비교 (SciVal)")
    fact_df = get_fact_sheet_dataframe()
    year_options = get_fact_sheet_year_columns(fact_df)
    if not year_options:
        st.warning("표시할 연도 데이터가 없습니다.")
        return

    selected_year = st.selectbox(
        "비교 연도",
        year_options,
        format_func=lambda y: f"{y}년",
        key="scival-year",
    )
    scival_df = build_scival_benchmark_dataframe(selected_year, fact_df)
    st.dataframe(scival_df, use_container_width=True)
    st.download_button(
        "CSV 다운로드",
        scival_df.to_csv(encoding="utf-8-sig"),
        file_name=f"scival_benchmark_{selected_year}.csv",
        mime="text/csv",
    )
    st.caption("각 대학 값은 Fact Sheet 수치를 단순 가중치로 보정한 모의 값입니다.")


def render_placeholder(section_name: str) -> None:
    st.info(f"{section_name} 섹션은 추후 구현 예정입니다.")


NAV_STRUCTURE = {
    "전북대학교 현황": [
        ("Global Ranking", render_global_ranking_tab),
        ("Fact Sheet", render_fact_sheet_tab),
        ("전북대 논문 목록", render_publications_tab),
        ("벤치마킹 대학 비교 (THE/QS)", render_benchmark_the_qs_tab),
        ("벤치마킹 대학 비교 (SciVal)", render_benchmark_scival_tab),
    ],
    "학문분야별 연구성과": [],
    "우수연구성과 선정": [],
    "연구지원 전략제언": [],
}

with st.sidebar:
    st.markdown('<div class="sidebar-nav-title">기준 연구영역</div>', unsafe_allow_html=True)
    primary_section = st.selectbox(
        "기준 연구영역",
        list(NAV_STRUCTURE.keys()),
        label_visibility="collapsed",
    )
    st.markdown('<div class="sidebar-nav-title">세부 페이지</div>', unsafe_allow_html=True)
    secondary_options = NAV_STRUCTURE[primary_section]
    if secondary_options:
        secondary_labels = [label for label, _ in secondary_options]
        secondary_label = st.radio(
            "세부 페이지",
            secondary_labels,
            label_visibility="collapsed",
            key=f"secondary-{primary_section}",
        )
    else:
        secondary_label = None
        st.markdown("준비 중입니다.", unsafe_allow_html=True)

st.subheader(
    f"{primary_section} · {secondary_label}" if secondary_label else primary_section
)

if secondary_label:
    renderer_map = {label: renderer for label, renderer in secondary_options}
    renderer_map[secondary_label]()
else:
    render_placeholder(primary_section)
