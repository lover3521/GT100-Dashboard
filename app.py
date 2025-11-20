"""GT100 진입전략 대시보드 메인 애플리케이션."""

import streamlit as st
import pandas as pd
from pathlib import Path


# 기본 페이지 타이틀과 레이아웃을 지정해 전체 앱의 모습을 통일한다.
st.set_page_config(
    page_title="GT100 진입전략 대시보드",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 사이드바 스타일을 커스터마이즈해 대시보드 톤앤매너를 맞춘다.
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
            padding: 0.25rem 0;
            border-bottom: 1px solid #f0f0f0;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label p {
            color: #c1121f;
            font-weight: 600;
            margin-left: 0.1rem;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label p::before {
            content: "• ";
            margin-right: 0.25rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 메인 헤더와 요약 설명으로 대시보드 목적을 명확히 안내합니다.
st.title("GT100 진입전략 대시보드")
st.caption("전북대학교의 GT100 진입전략 수립을 지원하는 내부용 모니터링 페이지입니다.")

summary_cols = st.columns(4)
summary_metrics = [
    ("THE 2026 순위", "801-1000위", "+0단계"),
    ("QS 2026 순위", "701-710위", "-10단계"),
    ("논문 수 (최근 5년)", "12,095편", "+15.5%"),
    ("피인용 수 (최근 5년)", "158,624회", "2020-2024"),
]
# KPI 카드들을 반복문으로 렌더링해 상단 요약을 구성한다.
for col, (label, value, delta) in zip(summary_cols, summary_metrics):
    col.metric(label, value, delta)

# 구분선을 사용해 KPI 영역과 이하 콘텐츠를 분리한다.
st.divider()

# 배포 디렉터리 내 엑셀 파일을 기본 데이터 소스로 참조한다.
FACT_SHEET_FILE = Path(__file__).with_name("\ud1b5\ud569 \ubb38\uc11c1.xlsx")

# 엑셀 미제공 시에도 데모가 가능하도록 하드코딩된 Fact Sheet 데이터.
EMBEDDED_FACT_SHEET = {
    "\uc601\ud5a5\ub825(Impact)": [
        {
            "label": "\ub17c\ubb38\uc218",
            "unit": "",
            "values": {2020: 2180.0, 2021: 2434.0, 2022: 2433.0, 2023: 2530.0, 2024: 2518.0},
        },
        {
            "label": "\ucd1d\uc778\uc6a9\uc218",
            "unit": "",
            "values": {2020: 48108.0, 2021: 44630.0, 2022: 31855.0, 2023: 23535.0, 2024: 10496.0},
        },
        {
            "label": "\ub17c\ubb38\ub2f9 \ud3c9\uade0 \uc778\uc6a9\uc218",
            "unit": "",
            "values": {2020: 22.07, 2021: 18.34, 2022: 13.09, 2023: 9.3, 2024: 4.17},
        },
        {
            "label": "FWCI",
            "unit": "",
            "values": {2020: 1.06, 2021: 1.08, 2022: 1.11, 2023: 1.13, 2024: 1.09},
        },
        {
            "label": "\ud53c\uc778\uc6a9 \ub17c\ubb38 \ube44\uc728",
            "unit": "",
            "values": {2020: 94.2, 2021: 93.8, 2022: 92.7, 2023: 88.6, 2024: 77.8},
        },
        {
            "label": "\ub9e4\uccb4 \ub178\ucd9c \ubc0f \ubd84\uc57c \ub2e4\uc591\uc131",
            "unit": "",
            "values": {2020: 390.0, 2021: 183.0, 2022: 115.0, 2023: 159.0},
        },
    ],
    "\uc6b0\uc218\uc131(Excellence)": [
        {
            "label": "\uc0c1\uc704 1% \ub17c\ubb38 \uc218",
            "unit": "",
            "values": {2020: 14.0, 2021: 29.0, 2022: 24.0, 2023: 34.0, 2024: 32.0},
        },
        {
            "label": "\uc0c1\uc704 1% \ub17c\ubb38 \ube44\uc728",
            "unit": "",
            "values": {2020: 0.7, 2021: 1.3, 2022: 1.1, 2023: 1.5, 2024: 1.4},
        },
        {
            "label": "\uc0c1\uc704 10% \ub17c\ubb38 \uc218",
            "unit": "",
            "values": {2020: 269.0, 2021: 263.0, 2022: 309.0, 2023: 331.0, 2024: 315.0},
        },
        {
            "label": "\uc0c1\uc704 10% \ub17c\ubb38 \ube44\uc728",
            "unit": "",
            "values": {2020: 13.3, 2021: 11.7, 2022: 13.6, 2023: 14.2, 2024: 13.5},
        },
        {
            "label": "\uc0c1\uc704 10% \uc800\ub110 \ub17c\ubb38 \uc218",
            "unit": "",
            "values": {2020: 560.0, 2021: 732.0, 2022: 696.0, 2023: 821.0, 2024: 884.0},
        },
        {
            "label": "\uc0c1\uc704 10% \uc800\ub110 \ub17c\ubb38 \ube44\uc728",
            "unit": "",
            "values": {2020: 28.4, 2021: 33.0, 2022: 30.9, 2023: 35.6, 2024: 38.0},
        },
        {
            "label": "Q1 \uc800\ub110 \ub17c\ubb38 \uc218",
            "unit": "",
            "values": {2020: 1048.0, 2021: 1274.0, 2022: 1374.0, 2023: 1498.0, 2024: 1590.0},
        },
        {
            "label": "Q1 \uc800\ub110 \ub17c\ubb38 \ube44\uc728",
            "unit": "",
            "values": {2020: 53.1, 2021: 57.5, 2022: 61.1, 2023: 65.0, 2024: 68.3},
        },
    ],
    "\uacf5\ub3d9\ud611\ub825(Collaboration)": [
        {
            "label": "\uad6d\uc81c \uacf5\ub3d9\uc5f0\uad6c \ub17c\ubb38 \uc218",
            "unit": "",
            "values": {2020: 618.0, 2021: 700.0, 2022: 706.0, 2023: 768.0, 2024: 768.0},
        },
        {
            "label": "\uad6d\uc81c \uacf5\ub3d9\uc5f0\uad6c \ub17c\ubb38 \ube44\uc728",
            "unit": "",
            "values": {2020: 30.5, 2021: 31.1, 2022: 31.0, 2023: 33.0, 2024: 32.8},
        },
        {
            "label": "\uad6d\uc81c \uacf5\ub3d9\uc5f0\uad6c FWCI",
            "unit": "",
            "values": {2020: 0.67, 2021: 0.7, 2022: 0.71, 2023: 0.75, 2024: 0.75},
        },
        {
            "label": "\uad6d\ub0b4 \uacf5\ub3d9\uc5f0\uad6c \ub17c\ubb38 \uc218",
            "unit": "",
            "values": {2020: 898.0, 2021: 1005.0, 2022: 993.0, 2023: 1017.0, 2024: 1018.0},
        },
        {
            "label": "\uad6d\ub0b4 \uacf5\ub3d9\uc5f0\uad6c \ub17c\ubb38 \ube44\uc728",
            "unit": "",
            "values": {2020: 44.3, 2021: 44.7, 2022: 43.6, 2023: 43.7, 2024: 43.5},
        },
        {
            "label": "\uc778\uc6a9 \uad6d\uac00 \uc218",
            "unit": "",
            "values": {2020: 166.0, 2021: 165.0, 2022: 161.0, 2023: 159.0, 2024: 141.0},
        },
    ],
    "\uacf5\uacf5\uc131 \ubc0f \uac1c\ubc29\uc131\n(Public Engagement and Openness)": [
        {
            "label": "\uc624\ud508 \uc561\uc138\uc2a4 \ub17c\ubb38 \uc218",
            "unit": "",
            "values": {2020: 1076.0, 2021: 1297.0, 2022: 1310.0, 2023: 1340.0, 2024: 1282.0},
        },
        {
            "label": "\uc624\ud508 \uc561\uc138\uc2a4 \ub17c\ubb38 \ube44\uc728",
            "unit": "",
            "values": {2020: 49.36, 2021: 53.29, 2022: 53.84, 2023: 52.96, 2024: 50.91},
        },
        {
            "label": "\uc5f4\ub78c \uc218",
            "unit": "",
            "values": {2020: 58142.0, 2021: 70857.0, 2022: 54029.0, 2023: 55552.0, 2024: 36628.0},
        },
        {
            "label": "\ubbf8\ub514\uc5b4 \uc778\uc6a9 \uc218",
            "unit": "",
            "values": {2020: 15.0, 2021: 17.0, 2022: 9.0, 2023: 19.0, 2024: 8.0},
        },
        {
            "label": "\uc8fc\uc81c \ubd84\uc57c \uc218",
            "unit": "",
            "values": {2020: 277.0, 2021: 281.0, 2022: 284.0, 2023: 292.0, 2024: 285.0},
        },
    ],
}


def _looks_like_year(label: object) -> bool:
    """단순한 규칙을 이용해 컬럼명이 연도인지 판별한다."""
    label_str = str(label)
    return label_str.isdigit() and 1900 <= int(label_str) <= 2100


def build_fact_sheet_df_from_embedded() -> pd.DataFrame:
    """EMBEDDED_FACT_SHEET 딕셔너리를 DataFrame 형태로 가공한다."""
    records: list[dict[str, object]] = []
    for indicator_group, entries in EMBEDDED_FACT_SHEET.items():
        for entry in entries:
            row: dict[str, object] = {
                "indicator_group": indicator_group,
                "????": entry["label"],
                "??": entry.get("unit", "") or "-",
            }
            for year, value in entry["values"].items():
                try:
                    year_key = int(year)
                except (TypeError, ValueError):
                    continue
                row[year_key] = value
            records.append(row)
    return pd.DataFrame(records)


@st.cache_data
def load_fact_sheet_data(xlsx_path: str) -> pd.DataFrame:
    """로컬 엑셀 파일을 읽고, 실패하면 임베디드 데이터를 반환한다."""
    try:
        raw_df = pd.read_excel(xlsx_path)
    except Exception:
        return build_fact_sheet_df_from_embedded()
    if raw_df.empty:
        return build_fact_sheet_df_from_embedded()

    category_col, indicator_col = raw_df.columns[:2]
    trimmed_df = raw_df.copy()
    sustainability_mask = trimmed_df[indicator_col].astype(str).str.contains(
        "Sustainability", case=False, na=False
    )
    if sustainability_mask.any():
        stop_idx = int(sustainability_mask[sustainability_mask].index[0])
        trimmed_df = trimmed_df.loc[: stop_idx - 1]

    fact_df = trimmed_df.rename(
        columns={category_col: "indicator_group", indicator_col: "????"}
    )
    fact_df["indicator_group"] = fact_df["indicator_group"].ffill()

    candidate_years = [col for col in fact_df.columns if _looks_like_year(col)]
    year_columns: list[int] = []
    for column in candidate_years:
        year = int(column)
        fact_df[year] = pd.to_numeric(fact_df[column], errors="coerce")
        if year not in year_columns:
            year_columns.append(year)
        if column != year:
            fact_df = fact_df.drop(columns=[column])
    year_columns = sorted(set(year_columns))

    total_column = next(
        (
            col
            for col in fact_df.columns
            if isinstance(col, str) and "5" in col and ("?" in col or "?" in col)
        ),
        None,
    )

    base_columns = ["indicator_group", "????"] + year_columns
    if total_column:
        base_columns.append(total_column)
    fact_df = fact_df[base_columns].dropna(subset=["????"])
    fact_df["??"] = "-"

    ordered_columns = ["indicator_group", "????", "??"] + year_columns
    if total_column:
        ordered_columns.append(total_column)
    fact_df = fact_df[ordered_columns]
    if year_columns:
        valid_mask = fact_df[year_columns].notna().any(axis=1)
        fact_df = fact_df[valid_mask]
    if fact_df.empty:
        return build_fact_sheet_df_from_embedded()
    return fact_df.reset_index(drop=True)


def get_fact_sheet_dataframe() -> pd.DataFrame:
    """엑셀 파일 존재 여부에 따라 Fact Sheet DataFrame을 확보한다."""
    if not FACT_SHEET_FILE.exists():
        return build_fact_sheet_df_from_embedded()
    return load_fact_sheet_data(str(FACT_SHEET_FILE))


def get_fact_sheet_year_columns(fact_df: pd.DataFrame) -> list[int]:
    """연도로 해석되는 컬럼만 모아 정렬된 리스트를 만든다."""
    return sorted(col for col in fact_df.columns if isinstance(col, int))


def get_fact_sheet_extra_columns(fact_df: pd.DataFrame) -> list[str]:
    """추가 메타데이터 컬럼명을 추출해 테이블 표시 순서를 제어한다."""
    return [
        col
        for col in fact_df.columns
        if isinstance(col, str) and col not in {"indicator_group", "????", "??"}
    ]


def build_indicator_dataframe(fact_df: pd.DataFrame, indicator: str) -> pd.DataFrame:
    """선택한 indicator_group에 해당하는 지표 행들만 필터링한다."""
    if fact_df.empty:
        return pd.DataFrame()
    year_columns = get_fact_sheet_year_columns(fact_df)
    extra_columns = get_fact_sheet_extra_columns(fact_df)
    display_columns = ["????", "??"] + year_columns + extra_columns
    subset = fact_df[fact_df["indicator_group"] == indicator][display_columns].copy()
    return subset.reset_index(drop=True)


# 가상의 비교 대학 배수를 정의해 SciVal 벤치마킹 시뮬레이션을 만든다.
SCIVAL_BENCHMARK_MULTIPLIERS = {
    "전북대": 1.00,
    "University A": 1.12,
    "University B": 0.94,
}


def build_scival_benchmark_dataframe(year: int, fact_df: pd.DataFrame) -> pd.DataFrame:
    """연도별 Fact Sheet 값을 가중치와 함께 피벗해 비교 테이블을 만든다."""
    columns = []
    data = {uni: [] for uni in SCIVAL_BENCHMARK_MULTIPLIERS}
    for _, row in fact_df.iterrows():
        unit = row.get("??", "")
        label = row["????"]
        label_with_unit = f"{label} ({unit})" if unit and unit != "-" else label
        columns.append((row["indicator_group"], label_with_unit))
        base_value = row.get(year)
        for uni, multiplier in SCIVAL_BENCHMARK_MULTIPLIERS.items():
            if pd.notna(base_value):
                value = round(float(base_value) * multiplier, 2)
            else:
                value = None
            data[uni].append(value)
    multi_columns = pd.MultiIndex.from_tuples(columns, names=["????", "????"])
    universities = list(SCIVAL_BENCHMARK_MULTIPLIERS.keys())
    values = [data[uni] for uni in universities]
    df = pd.DataFrame(values, columns=multi_columns, index=universities)
    df.index.name = "??"
    return df


def render_global_ranking_tab() -> None:
    """THE/QS 순위를 간단한 지표와 라인차트로 보여준다."""
    st.subheader("Global Ranking")
    ranking_df = pd.DataFrame(
        {
            "연도": [2020, 2021, 2022, 2023, 2024],
            "THE": [601, 601, 551, 501, 475],
            "QS": [651, 601, 571, 551, 505],
        }
    )
    source = st.selectbox("평가 체계 선택", ["THE", "QS"])
    cols = st.columns(2)
    the_latest = ranking_df.iloc[-1]["THE"]
    qs_latest = ranking_df.iloc[-1]["QS"]
    cols[0].metric("THE 2024", f"{int(the_latest)}위", "-26 단계 개선")
    cols[1].metric("QS 2024", f"{int(qs_latest)}위", "-46 단계 개선")
    st.line_chart(ranking_df.set_index("연도")[["THE", "QS"]])
    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True,
    )
    st.info(f"{source} 상세 분석과 세부 지표는 추후 연동 예정입니다.")


def render_fact_sheet_tab() -> None:
    """Fact Sheet 데이터의 요약, 상세 테이블, 추이 차트를 렌더링한다."""
    st.subheader("Fact Sheet")
    metric_cols = st.columns(3)
    summary_metrics = [
        ("학생 수", "28,450명", "+1.2%"),
        ("교원 수", "1,760명", "+0.9%"),
        ("연구비", "4,280억원", "+3.9%"),
    ]
    for col, (label, value, delta) in zip(metric_cols, summary_metrics):
        col.metric(label, value, delta)

    try:
        fact_df = get_fact_sheet_dataframe()
    except Exception as exc:
        st.error(f"Fact Sheet 데이터를 불러오지 못했습니다: {exc}")
        return

    if fact_df.empty:
        st.warning("Fact Sheet 데이터를 준비할 수 없습니다.")
        return

    if not FACT_SHEET_FILE.exists():
        st.info("통합 문서1.xlsx 연결에 실패하여 내장 데이터를 사용 중입니다.")

    indicator_groups = fact_df["indicator_group"].dropna().unique().tolist()
    year_columns = get_fact_sheet_year_columns(fact_df)
    if not indicator_groups or not year_columns:
        st.warning("Fact Sheet 지표 구성이 올바르지 않습니다.")
        return

    st.markdown("#### 지표 상세 보기")
    detail_indicator = st.selectbox(
        "지표(Indicator) 선택",
        indicator_groups,
        key="fact-detail-indicator",
    )
    detail_df = build_indicator_dataframe(fact_df, detail_indicator)
    st.dataframe(detail_df, use_container_width=True, hide_index=True)

    st.markdown("#### 지표 추이 차트")
    chart_indicator = st.selectbox(
        "차트용 지표 그룹",
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
        metric_multi = st.multiselect(
            "차트 지표 선택",
            chart_df["????"],
            default=list(chart_df["????"][: min(2, len(chart_df))]),
        )
        if metric_multi:
            plot_df = (
                chart_df[chart_df["????"].isin(metric_multi)]
                .set_index("????")[numeric_years]
                .T
            )
            filtered_plot = plot_df.loc[
                (plot_df.index >= year_range[0]) & (plot_df.index <= year_range[1])
            ]
            st.line_chart(filtered_plot)
        else:
            st.info("차트로 보고 싶은 지표를 선택해 주세요.")
    else:
        st.info("표에 연도 데이터가 없어 차트를 그릴 수 없습니다.")

    st.markdown("#### 전체 Fact Sheet")
    combined_df = []
    for indicator_name in indicator_groups:
        df = build_indicator_dataframe(fact_df, indicator_name)
        if df.empty:
            continue
        df = df.copy()
        if "????" in df.columns:
            df = df.drop(columns=["????"])
        df.insert(0, "????", indicator_name)
        combined_df.append(df)
    if combined_df:
        master_df = pd.concat(combined_df, ignore_index=True)
        st.dataframe(master_df, use_container_width=True, hide_index=True)
    else:
        st.info("표시할 Fact Sheet 데이터가 없습니다.")
    st.caption("※ 지표·세부지표 단위는 컬럼명에 괄호로 표기되어 있습니다.")


def render_publications_tab() -> None:
    """?? ?? ???? ??????? ???? ????."""
    st.subheader("전북대 논문 목록")
    sample_papers = pd.DataFrame(
        [
            {
                "논문명": "Smart Agriculture using AI",
                "저널": "Nature Food",
                "발행연도": 2024,
                "분야": "농생명",
                "피인용수": 42,
            },
            {
                "논문명": "Energy Storage Materials",
                "저널": "Advanced Energy Materials",
                "발행연도": 2023,
                "분야": "공학",
                "피인용수": 55,
            },
            {
                "논문명": "Carbon Neutral Cities",
                "저널": "Renewable Energy",
                "발행연도": 2022,
                "분야": "환경",
                "피인용수": 33,
            },
            {
                "논문명": "Precision Medicine Pipeline",
                "저널": "Lancet Digital Health",
                "발행연도": 2024,
                "분야": "의생명",
                "피인용수": 29,
            },
        ]
    )
    year_range = st.slider("발행연도", 2020, 2024, (2022, 2024))
    fields = st.multiselect(
        "연구 분야",
        options=sorted(sample_papers["분야"].unique()),
        default=sorted(sample_papers["분야"].unique()),
    )
    filtered = sample_papers[
        sample_papers["발행연도"].between(year_range[0], year_range[1])
        & sample_papers["분야"].isin(fields)
    ]
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button(
        "CSV 다운로드",
        filtered.to_csv(index=False).encode("utf-8-sig"),
        file_name="jbnu_publications.csv",
        mime="text/csv",
    )


def render_benchmark_the_qs_tab() -> None:
    """THE/QS 지표를 기준으로 경쟁 대학과 막대 차트를 비교한다."""
    st.subheader("벤치마킹 대학 비교 (THE/QS)")
    comparison_df = pd.DataFrame(
        [
            {"대학": "전북대", "지표": "교육(Teaching)", "THE": 25.1, "QS": 18.4},
            {"대학": "University A", "지표": "교육(Teaching)", "THE": 38.3, "QS": 32.1},
            {"대학": "전북대", "지표": "연구(Research)", "THE": 24.3, "QS": 21.4},
            {"대학": "University A", "지표": "연구(Research)", "THE": 40.2, "QS": 36.8},
        ]
    )
    indicator = st.selectbox("평가 지표", sorted(comparison_df["지표"].unique()))
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
    """Fact Sheet 기반으로 SciVal 스타일 벤치마킹 표를 구성한다."""
    st.subheader("???? ???? (SciVal)")
    try:
        fact_df = get_fact_sheet_dataframe()
    except Exception as exc:
        st.error(f"Fact Sheet ???? ???? ?????: {exc}")
        return

    year_options = get_fact_sheet_year_columns(fact_df)
    if not year_options:
        st.warning("??? Fact Sheet ???? ?? ????? ??? ? ????.")
        return

    selected_year = st.selectbox(
        "?? ??",
        year_options,
        format_func=lambda y: f"{y}?",
        key="scival-year",
    )
    scival_df = build_scival_benchmark_dataframe(selected_year, fact_df)
    st.dataframe(scival_df, use_container_width=True)
    st.download_button(
        "CSV ????",
        scival_df.to_csv(encoding="utf-8-sig"),
        file_name=f"scival_benchmark_{selected_year}.csv",
        mime="text/csv",
    )
    st.caption("? ??????? ??? ???? ??? ???? ????.")


def render_placeholder(section_name: str) -> None:
    """준비되지 않은 섹션에 대한 안내 메시지를 보여준다."""
    st.info(f"{section_name} 섹션은 추후 구현 예정입니다.")


# 사이드바 내비게이션 구성을 정의(레이블, 렌더 함수 매핑)한다.
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
    # 좌측 내비게이션에서 1·2차 영역을 선택하도록 구성한다.
    st.markdown('<div class="sidebar-nav-title">기관 연구역량</div>', unsafe_allow_html=True)
    primary_section = st.selectbox(
        "기관 연구역량",
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
        st.markdown("• 준비 중", unsafe_allow_html=True)

# 본문 상단에 현재 선택한 섹션/페이지를 제목으로 표시한다.
st.subheader(
    f"{primary_section} · {secondary_label}"
    if secondary_label
    else primary_section
)

# 세부 페이지가 선택되면 대응하는 렌더 함수를 호출한다.
if secondary_label:
    renderer_map = {label: renderer for label, renderer in secondary_options}
    renderer_map[secondary_label]()
else:
    render_placeholder(primary_section)
