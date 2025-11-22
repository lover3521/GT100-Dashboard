"""GT100 진입전략 대시보드 메인 애플리케이션."""

import math
from pathlib import Path

import altair as alt
import pandas as pd
from pandas.io.formats.style import Styler
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
        [data-testid="stSidebar"] div[role="radiogroup"] label p {
            color: #c1121f;
            font-weight: 600;
            margin-left: 0.1rem;
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
SCIVAL_BENCHMARK_FILE = Path(__file__).with_name("GT100_비교대상 대학_SciVal.xlsx")
THE_BENCHMARK_PATTERN = "GT100_*THE*.xlsx"
QS_BENCHMARK_PATTERN = "GT100_*QS*.xlsx"

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

def _find_first_matching_file(pattern: str) -> Path | None:
    base_dir = Path(__file__).parent
    matches = sorted(base_dir.glob(pattern))
    return matches[0] if matches else None

@st.cache_data
def load_scival_benchmark_excel(path: Path) -> dict[str, pd.DataFrame]:
    if not path.exists():
        return {}
    df_raw = pd.read_excel(path, header=None)
    if df_raw.empty:
        return {}

    def _parse_block(header_row_idx: int, data_start_idx: int, data_end_idx: int) -> pd.DataFrame:
        raw_header = df_raw.iloc[header_row_idx].ffill()
        raw_group = df_raw.iloc[header_row_idx - 1].ffill() if header_row_idx > 0 else None
        seen: dict[tuple[str, str], int] = {}
        group_names: list[str] = []
        base_names: list[str] = []
        for idx, col in enumerate(raw_header):
            base_name = str(col) if pd.notna(col) else f"항목{idx}"
            if idx == 0:
                base_name = "대학"
            group_label = ""
            if raw_group is not None and idx < len(raw_group):
                gl = raw_group.iloc[idx]
                if pd.notna(gl):
                    group_label = str(gl).strip()
            key = (group_label, base_name)
            count = seen.get(key, 0)
            seen[key] = count + 1
            if count:
                base_name = f"{base_name}_{count}"
            group_names.append(group_label)
            base_names.append(base_name)
        data = df_raw.iloc[data_start_idx:data_end_idx].reset_index(drop=True)
        columns = pd.MultiIndex.from_tuples(list(zip(group_names, base_names)), names=["지표 그룹", "지표"])
        data.columns = columns
        data = data.dropna(subset=[("", "대학")])
        for idx in range(1, len(data.columns)):
            numeric = pd.to_numeric(data.iloc[:, idx], errors="coerce")
            if numeric.notna().sum() >= max(1, len(data) // 3):
                data.iloc[:, idx] = numeric
        return data.reset_index(drop=True)

    # 첫 번째 블록(예: 2024년)
    first_header_idx = 1
    # 두 번째 블록(예: 최근 5개년) 시작 행 찾기
    first_col_series = df_raw.iloc[:, 0].astype(str)
    five_header_idx = None
    for idx, val in first_col_series.items():
        if isinstance(val, str) and "5" in val:
            five_header_idx = idx
            break

    sections: dict[str, pd.DataFrame] = {}
    if five_header_idx is None:
        sections["2024년"] = _parse_block(first_header_idx, first_header_idx + 1, len(df_raw))
    else:
        sections["2024년"] = _parse_block(first_header_idx, first_header_idx + 1, five_header_idx)
        sections["최근 5개년"] = _parse_block(five_header_idx, five_header_idx + 1, len(df_raw))
    return sections

def _parse_the_qs_benchmark_excel(path: Path) -> pd.DataFrame:
    """첫 두 행을 헤더로 사용하는 THE/QS 벤치마킹 엑셀 파서."""
    try:
        df_raw = pd.read_excel(path, header=None)
    except Exception:
        return pd.DataFrame()
    if df_raw.empty or len(df_raw) < 3:
        return pd.DataFrame()

    header_top = df_raw.iloc[0].ffill()
    header_sub = df_raw.iloc[1].fillna("")

    columns: list[str] = []
    for top, sub in zip(header_top, header_sub):
        top_str = "" if pd.isna(top) else str(top).strip()
        sub_str = "" if pd.isna(sub) else str(sub).strip()
        if top_str and sub_str:
            col_name = f"{top_str} - {sub_str}"
        else:
            col_name = top_str or sub_str or "항목"
        columns.append(col_name)

    df = df_raw.iloc[2:].reset_index(drop=True)
    df.columns = columns

    if "Year" in df.columns:
        df = df[pd.to_numeric(df["Year"], errors="coerce").notna()].copy()
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype(int)

    def _likely_numeric(series: pd.Series) -> bool:
        numeric = pd.to_numeric(series, errors="coerce")
        return numeric.notna().sum() >= max(1, len(series) // 3)

    for col in df.columns:
        if col in {"Year", "Institution Name"}:
            continue
        if _likely_numeric(df[col]):
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

@st.cache_data
def load_benchmark_the_qs_data() -> dict[str, pd.DataFrame]:
    files = {
        "THE": _find_first_matching_file(THE_BENCHMARK_PATTERN),
        "QS": _find_first_matching_file(QS_BENCHMARK_PATTERN),
    }
    datasets: dict[str, pd.DataFrame] = {}
    for scheme, path in files.items():
        if path and path.exists():
            parsed = _parse_the_qs_benchmark_excel(path)
            if not parsed.empty:
                datasets[scheme] = parsed
    return datasets


def _get_benchmark_score_for_jbnu(scheme: str) -> tuple[int | None, str | None, float | None]:
    """THE/QS 벤치마킹 데이터에서 전북대 점수를 추출."""
    datasets = load_benchmark_the_qs_data()
    df = datasets.get(scheme)
    if df is None or df.empty or "Institution Name" not in df.columns:
        return (None, None, None)

    name_mask = (
        df["Institution Name"]
        .astype(str)
        .str.contains("전북|Jeonbuk|JBNU", case=False, na=False)
    )
    df_jbnu = df[name_mask]
    if df_jbnu.empty:
        return (None, None, None)

    if "Year" in df_jbnu.columns:
        df_jbnu = df_jbnu.sort_values("Year", ascending=False)
    latest_row = df_jbnu.iloc[0]
    year_value = int(latest_row["Year"]) if "Year" in latest_row and pd.notna(latest_row["Year"]) else None

    candidate_cols = [col for col in df_jbnu.columns if col not in {"Year", "Institution Name"}]
    if not candidate_cols:
        return (year_value, None, None)

    def _choose_metric(cols: list[str]) -> str:
        score_cols = [c for c in cols if "score" in c.lower()]
        if score_cols:
            return score_cols[0]
        numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df_jbnu[c])]
        if numeric_cols:
            return numeric_cols[0]
        return cols[0]

    metric_col = _choose_metric(candidate_cols)
    raw_value = latest_row.get(metric_col)
    try:
        numeric_value = float(raw_value)
    except (TypeError, ValueError):
        numeric_value = None
    return (year_value, metric_col, numeric_value)


def _get_jbnu_latest_benchmark_row(scheme: str) -> pd.DataFrame:
    """전북대(Jeonbuk/JBNU) 최신 연도 행만 반환."""
    datasets = load_benchmark_the_qs_data()
    df = datasets.get(scheme)
    if df is None or df.empty or "Institution Name" not in df.columns:
        return pd.DataFrame()

    mask = df["Institution Name"].astype(str).str.contains("전북|Jeonbuk|JBNU", case=False, na=False)
    df_jbnu = df[mask].copy()
    if df_jbnu.empty:
        return pd.DataFrame()

    if "Year" in df_jbnu.columns:
        df_jbnu["Year"] = pd.to_numeric(df_jbnu["Year"], errors="coerce")
        df_jbnu = df_jbnu.sort_values("Year", ascending=False)
    return df_jbnu.head(1).reset_index(drop=True)


def format_scival_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """표시용: NaN은 '-', 수치는 콤마와 소수 둘째자리까지."""
    display = df.copy()
    for col in display.columns:
        series = display[col]
        if pd.api.types.is_numeric_dtype(series):
            display[col] = series.apply(
                lambda v: "-"
                if pd.isna(v)
                else (f"{int(v):,}" if float(v).is_integer() else f"{float(v):,.2f}")
            )
        else:
            display[col] = series.fillna("-")
    return display


def style_scival_table(df: pd.DataFrame, highlight_university: str | None = "전북대") -> Styler:
    def _fmt(v: object) -> str:
        if pd.isna(v):
            return "-"
        try:
            fv = float(v)
            return f"{int(fv):,}" if fv.is_integer() else f"{fv:,.2f}"
        except Exception:
            return str(v)

    styler = df.style.format(_fmt)

    if highlight_university and ("", "대학") in df.columns:
        def _highlight(row: pd.Series) -> list[str]:
            uni_name = row.get(("", "대학"))
            if pd.isna(uni_name):
                return [""] * len(row)
            is_target = str(uni_name).strip() == highlight_university
            style = "background-color: #fff3f5; font-weight: 600;" if is_target else ""
            return [style] * len(row)

        styler = styler.apply(_highlight, axis=1)

    return styler

def style_the_qs_table(df: pd.DataFrame, keywords: tuple[str, ...] = ("전북", "Jeonbuk", "JBNU")) -> Styler:
    """벤치마킹 표에서 전북대 행을 강조하고 숫자 포맷을 적용."""
    styler = df.style

    def _fmt(v: object) -> str:
        if pd.isna(v):
            return "-"
        try:
            num = float(v)
        except Exception:
            return str(v)
        return f"{int(num):,}" if num.is_integer() else f"{num:,.2f}"
    year_cols = [col for col in df.columns if "year" in str(col).lower()]
    other_cols = [col for col in df.columns if col not in year_cols]
    if other_cols:
        styler = styler.format(_fmt, subset=other_cols)
    if year_cols:
        styler = styler.format(
            lambda v: "-" if pd.isna(v) else f"{int(float(v))}", subset=year_cols
        )

    def _highlight(row: pd.Series) -> list[str]:
        name = str(row.get("Institution Name", "") or "")
        is_target = any(keyword in name or keyword in name.upper() for keyword in keywords)
        style = "background-color: #fff3f5; font-weight: 600;" if is_target else ""
        return [style] * len(row)

    return styler.apply(_highlight, axis=1)


def _scival_group_order_key(group_name: str) -> tuple[int, str]:
    """그룹 정렬: 영향력/우수성/협력/공공성 및 개방성/지속성 순."""
    g_lower = (group_name or "").lower()
    g_orig = group_name or ""
    if "영향" in g_orig or "impact" in g_lower:
        order = 0
    elif "우수" in g_orig or "excellence" in g_lower:
        order = 1
    elif "협력" in g_orig or "collaboration" in g_lower:
        order = 2
    elif "공공" in g_orig or "개방" in g_orig or "public" in g_lower or "openness" in g_lower:
        order = 3
    elif "지속" in g_orig or "sustainability" in g_lower or "sdg" in g_lower:
        order = 4
    else:
        order = 5
    return (order, group_name)

def render_global_ranking_tab(show_heading: bool = True) -> None:
    if show_heading:
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

    st.markdown("#### 전북대 점수 (THE/QS)")
    jbnu_the = _get_jbnu_latest_benchmark_row("THE")
    jbnu_qs = _get_jbnu_latest_benchmark_row("QS")
    if jbnu_the.empty and jbnu_qs.empty:
        st.info("벤치마킹 데이터에서 전북대 행을 찾지 못했습니다.")
    else:
        if not jbnu_the.empty:
            st.markdown("##### THE")
            st.dataframe(style_the_qs_table(jbnu_the), use_container_width=True, hide_index=True)
        if not jbnu_qs.empty:
            st.markdown("##### QS")
            st.dataframe(style_the_qs_table(jbnu_qs), use_container_width=True, hide_index=True)

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
        palette_cycle = ["#fde9f4", "#eef6ff", "#fef5e5", "#f3f9ef", "#f1e9ff"]
        group_palette = {g: palette_cycle[i % len(palette_cycle)] for i, g in enumerate(indicator_groups)}
        detail_display = detail_df.copy()
        if "단위" in detail_display.columns:
            detail_display["지표명"] = detail_display.apply(
                lambda row: (
                    row["지표명"] if row.get("단위") in ("", "-", None) else f"{row['지표명']} ({row['단위']})"
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
        range_state_key = f"fact_chart_year_range_{chart_indicator}"
        start_key = f"fact-chart-year-start-{chart_indicator}"
        end_key = f"fact-chart-year-end-{chart_indicator}"

        stored_range = st.session_state.get(range_state_key, (year_min, year_max))
        default_start = min(max(int(stored_range[0]), year_min), year_max)
        default_end = min(max(int(stored_range[1]), year_min), year_max)
        if default_start > default_end:
            default_start, default_end = default_end, default_start
        st.session_state[range_state_key] = (default_start, default_end)
        if start_key not in st.session_state:
            st.session_state[start_key] = default_start
        if end_key not in st.session_state:
            st.session_state[end_key] = default_end

        current_start, current_end = st.session_state[range_state_key]
        start_col, end_col = st.columns(2)
        with start_col:
            start_input = st.number_input(
                "시작 연도",
                min_value=year_min,
                max_value=year_max,
                value=current_start,
                step=1,
                key=start_key,
            )
        with end_col:
            end_input = st.number_input(
                "종료 연도",
                min_value=year_min,
                max_value=year_max,
                value=current_end,
                step=1,
                key=end_key,
            )

        selected_range = tuple(sorted((int(start_input), int(end_input))))
        selected_range = (max(year_min, selected_range[0]), min(year_max, selected_range[1]))
        if selected_range != st.session_state[range_state_key]:
            st.session_state[range_state_key] = selected_range

        year_range = st.session_state[range_state_key]
        metric_multi = st.multiselect(
            "차트 지표 선택",
            chart_df["지표명"],
            default=list(chart_df["지표명"][: min(2, len(chart_df))]),
        )
        if metric_multi:
            plot_df = chart_df[chart_df["지표명"].isin(metric_multi)].set_index("지표명")[numeric_years].T
            filtered_plot = plot_df.loc[(plot_df.index >= year_range[0]) & (plot_df.index <= year_range[1])]
            line_data = (
                filtered_plot.reset_index()
                .rename(columns={"index": "year"})
                .melt(id_vars="year", var_name="지표명", value_name="value")
                .dropna(subset=["value"])
            )

            turning_rows: list[dict[str, object]] = []
            for metric_name, series in filtered_plot.items():
                series_clean = series.dropna()
                if len(series_clean) < 3:
                    continue
                years = series_clean.index.astype(int).tolist()
                values = series_clean.values.tolist()
                for i in range(1, len(values) - 1):
                    prev_val, curr_val, next_val = values[i - 1], values[i], values[i + 1]
                    if (curr_val - prev_val) * (next_val - curr_val) < 0:
                        turning_rows.append({"year": years[i], "지표명": metric_name, "value": curr_val})
            turning_df = pd.DataFrame(turning_rows)

            base_chart = (
                alt.Chart(line_data)
                .mark_line(point=True)
                .encode(
                    x=alt.X("year:O", title="연도"),
                    y=alt.Y("value:Q", title="값"),
                    color=alt.Color("지표명:N", title="지표"),
                    tooltip=["year:O", "지표명:N", alt.Tooltip("value:Q", title="값")],
                )
                .properties(height=320)
            )
            chart = base_chart
            if not turning_df.empty:
                turning_layer = (
                    alt.Chart(turning_df)
                    .mark_point(shape="diamond", size=80, color="#222")
                    .encode(
                        x="year:O",
                        y="value:Q",
                        color=alt.Color("지표명:N", title="지표"),
                        tooltip=["year:O", "지표명:N", alt.Tooltip("value:Q", title="값")],
                    )
                )
                chart = base_chart + turning_layer
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("차트로 보고 싶은 지표를 선택해 주세요")
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

        display_df["지표 그룹 표시"] = display_df["지표 그룹"].where(
            ~display_df["지표 그룹"].duplicated(), ""
        )
        display_df = display_df.drop(columns=["지표 그룹"]).rename(
            columns={"지표 그룹 표시": "지표 그룹"}
        )

        palette_cycle = ["#fde9f4", "#eef6ff", "#fef5e5", "#f3f9ef", "#f1e9ff"]
        group_palette = {g: palette_cycle[i % len(palette_cycle)] for i, g in enumerate(indicator_groups)}
        color_series = master_df["지표 그룹"].map(group_palette).fillna("#fafafa")

        def highlight_group(row: pd.Series) -> list[str]:
            color = color_series[row.name]
            return [f"background-color: {color}"] * len(row)

        styled_df = (
            display_df.style.apply(highlight_group, axis=1)
            .set_properties(subset=["지표 그룹"], **{"font-weight": "600"})
        )
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("표시할 Fact Sheet 데이터가 없습니다.")
    st.caption("지표명 뒤 괄호 안에 단위를 표시했습니다.")

def load_publication_csv(csv_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(csv_path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(csv_path, encoding="cp949")

def get_publications_dataframe() -> pd.DataFrame:
    if SCOPUS_EXPORT_FILE.exists():
        try:
            df = load_publication_csv(str(SCOPUS_EXPORT_FILE))
        except Exception:
            df = pd.DataFrame()
    else:
        df = pd.DataFrame()
    if df.empty:
        return pd.DataFrame(
            [
                {"논문명": "Smart Agriculture using AI", "저널": "Nature Food", "발행연도": 2024, "분야": "생명", "피인용수": 42, "논문 유형": "Article", "저자": "Ahn J.; Kim S."},
                {"논문명": "Energy Storage Materials", "저널": "Advanced Energy Materials", "발행연도": 2023, "분야": "공학", "피인용수": 55, "논문 유형": "Review", "저자": "Lee H.; Park K."},
                {"논문명": "Carbon Neutral Cities", "저널": "Renewable Energy", "발행연도": 2022, "분야": "환경", "피인용수": 33, "논문 유형": "Article", "저자": "Choi M.; Seo G."},
                {"논문명": "Precision Medicine Pipeline", "저널": "Lancet Digital Health", "발행연도": 2024, "분야": "의생명", "피인용수": 29, "논문 유형": "Article", "저자": "Jung Y.; Lee J."},
            ]
        )
    subject_columns = [
        "All Science Journal Classification (ASJC) field name",
        "Quacquarelli Symonds (QS) Subject field name",
        "Times Higher Education (THE) field name",
    ]
    subject_series = pd.Series([None] * len(df))
    for col in subject_columns:
        if col in df.columns:
            if subject_series.isna().all():
                subject_series = df[col]
            else:
                subject_series = subject_series.fillna(df[col])

    doc_type_col = None
    for col in df.columns:
        normalized = col.strip().lower().replace(" ", "")
        if normalized in {"publicationtype", "documenttype"}:
            doc_type_col = col
            break

    mapped = pd.DataFrame(
        {
            "논문명": df.get("Title"),
            "저널": df.get("Scopus Source title"),
            "발행연도": pd.to_numeric(df.get("Year"), errors="coerce"),
            "분야": subject_series,
            "피인용수": pd.to_numeric(df.get("Citations"), errors="coerce"),
            "논문 유형": df.get(doc_type_col) if doc_type_col else None,
            "저자": df.get("Authors"),
        }
    )
    mapped = mapped.dropna(subset=["발행연도"])
    mapped["발행연도"] = mapped["발행연도"].astype(int)
    mapped["피인용수"] = mapped["피인용수"].fillna(0).astype(int)
    mapped["저널"] = mapped["저널"].fillna("-")
    mapped["분야"] = mapped["분야"].fillna("-")
    mapped["논문 유형"] = mapped["논문 유형"].fillna("미분류")
    mapped["저자"] = mapped["저자"].fillna("-")
    return mapped.reset_index(drop=True)

def render_publications_tab() -> None:
    st.subheader("Scopus 5년치 연구성과")
    publications_df = get_publications_dataframe()
    if publications_df.empty:
        st.info("표시할 논문 데이터가 없습니다.")
        return

    year_min, year_max = int(publications_df["발행연도"].min()), int(publications_df["발행연도"].max())
    start_col, end_col = st.columns(2)
    with start_col:
        start_year = st.number_input("시작 연도", min_value=year_min, max_value=year_max, value=year_min, step=1, key="pub-year-start")
    with end_col:
        end_year = st.number_input("종료 연도", min_value=year_min, max_value=year_max, value=year_max, step=1, key="pub-year-end")
    selected_years = tuple(sorted((int(start_year), int(end_year))))

    doc_types = sorted(publications_df["논문 유형"].dropna().unique())
    selected_types = st.multiselect("논문 유형", options=doc_types, default=doc_types)

    search_query = st.text_input("논문 검색 (제목/저자/저널)", value="", key="pub-search").strip().lower()

    filtered = publications_df[
        publications_df["발행연도"].between(selected_years[0], selected_years[1])
        & publications_df["논문 유형"].isin(selected_types)
    ]

    if search_query:
        mask = (
            filtered["논문명"].fillna("").str.lower().str.contains(search_query)
            | filtered["저자"].fillna("").str.lower().str.contains(search_query)
            | filtered["저널"].fillna("").str.lower().str.contains(search_query)
        )
        filtered = filtered[mask]

    if filtered.empty:
        st.info("조건에 맞는 논문이 없습니다.")
        return

    # 기본 표시 순서를 맞춰서 저자를 저널 앞에 배치
    display_order = ["논문명", "저자", "저널", "발행연도", "분야", "논문 유형", "피인용수"]
    ordered_cols = [col for col in display_order if col in filtered.columns] + [
        col for col in filtered.columns if col not in display_order
    ]
    filtered = filtered[ordered_cols]

    page_size = 50
    total_rows = len(filtered)
    total_pages = max(1, math.ceil(total_rows / page_size))
    if "pub-page" not in st.session_state:
        st.session_state["pub-page"] = 1
    current_page = min(st.session_state["pub-page"], total_pages)
    if current_page != st.session_state["pub-page"]:
        st.session_state["pub-page"] = current_page

    def _set_page(page: int) -> None:
        st.session_state["pub-page"] = max(1, min(total_pages, page))

    # 페이지 번호 버튼 구성 (현재 페이지 주변으로 5개까지)
    start_page = max(1, current_page - 2)
    end_page = min(total_pages, start_page + 4)
    start_page = max(1, end_page - 4)
    page_numbers = list(range(start_page, end_page + 1))

    if total_pages > 1:
        cols = st.columns(len(page_numbers) + 2)
        with cols[0]:
            st.button("← 이전", disabled=current_page == 1, on_click=_set_page, args=(current_page - 1,))
        for idx, page_num in enumerate(page_numbers, start=1):
            with cols[idx]:
                st.button(
                    str(page_num),
                    on_click=_set_page,
                    args=(page_num,),
                    type="primary" if page_num == current_page else "secondary",
                )
        with cols[-1]:
            st.button("다음 →", disabled=current_page == total_pages, on_click=_set_page, args=(current_page + 1,))

    start_idx = (current_page - 1) * page_size
    end_idx = start_idx + page_size
    page_df = filtered.iloc[start_idx:end_idx]

    st.dataframe(page_df, use_container_width=True, hide_index=True, height=600)
    st.caption(f"총 {total_rows}건 · 페이지 {current_page}/{total_pages} · 페이지당 {page_size}건")
    st.download_button(
        "CSV 다운로드",
        filtered.to_csv(index=False).encode("utf-8-sig"),
        file_name="jbnu_publications.csv",
        mime="text/csv",
    )


def render_wos_performance_tab() -> None:
    st.subheader("WoS 5년치 연구성과")
    st.info("WoS 5년치 연구성과 데이터는 추후 업데이트될 예정입니다.")

def render_benchmark_the_qs_tab(show_heading: bool = True) -> None:
    if show_heading:
        st.subheader("벤치마킹 대학비교 (THE/QS)")
    datasets = load_benchmark_the_qs_data()
    if not datasets:
        st.warning("벤치마킹 엑셀 파일을 찾을 수 없습니다. 폴더의 THE/QS 파일을 확인해 주세요.")
        return

    available_schemes = [scheme for scheme, df in datasets.items() if not df.empty]
    scheme = st.radio(
        "평가 체계 선택",
        available_schemes,
        horizontal=True,
        index=0 if available_schemes else None,
    )
    if not scheme:
        st.info("선택할 수 있는 평가 체계가 없습니다.")
        return

    df = datasets.get(scheme, pd.DataFrame())
    if df.empty:
        st.warning(f"{scheme} 데이터가 비어 있습니다.")
        return

    if "Year" not in df.columns or "Institution Name" not in df.columns:
        st.warning(f"{scheme} 데이터에 Year 또는 Institution Name 열이 없습니다.")
        return

    sorted_years = sorted(df["Year"].dropna().unique(), reverse=True)
    if not sorted_years:
        st.info("데이터에 연도 정보가 없습니다.")
        return
    selected_year = st.selectbox("연도 선택", sorted_years, index=0 if sorted_years else None)
    df_year = df[df["Year"] == selected_year]
    if df_year.empty:
        st.info("선택한 연도에 데이터가 없습니다.")
        return

    excluded_cols = {"Year", "Institution Name"}
    metrics = [col for col in df.columns if col not in excluded_cols]
    if not metrics:
        st.info("표시할 지표가 없습니다.")
        return

    def _choose_metric(cols: list[str]) -> str:
        score_cols = [c for c in cols if "score" in c.lower()]
        if score_cols:
            return score_cols[0]
        numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df_year[c])]
        if numeric_cols:
            return numeric_cols[0]
        return cols[0]

    selected_metric = _choose_metric(metrics)

    chart_data = df_year[["Institution Name", selected_metric]].dropna(subset=[selected_metric]).copy()
    chart_data[selected_metric] = pd.to_numeric(chart_data[selected_metric], errors="coerce")
    chart_data = chart_data.dropna(subset=[selected_metric])
    if chart_data.empty:
        st.info("선택한 지표에 표시할 값이 없습니다.")
        return

    chart_data["is_jbnu"] = chart_data["Institution Name"].astype(str).apply(
        lambda name: ("전북" in name) or ("Jeonbuk" in name) or ("JBNU" in name.upper())
    )

    highlight_color = "#c1121f"
    default_color = "#9db7e0"

    bar_chart = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X("Institution Name:N", sort="-y", title="대학"),
            y=alt.Y(f"{selected_metric}:Q", title=selected_metric),
            color=alt.condition("is_jbnu == true", alt.value(highlight_color), alt.value(default_color)),
            tooltip=["Institution Name:N", alt.Tooltip(f"{selected_metric}:Q", title="값")],
        )
        .properties(height=340)
    )
    st.altair_chart(bar_chart, use_container_width=True)

    st.markdown("#### 표 보기")
    display_cols = ["Institution Name", "Year", selected_metric, "RANK"] if "RANK" in df.columns else ["Institution Name", "Year", selected_metric]
    # 포함되지 않은 열은 뒤쪽에 배치
    display_cols = [col for col in display_cols if col in df_year.columns] + [
        col for col in df_year.columns if col not in display_cols
    ]
    display_df = df_year[display_cols]
    st.dataframe(
        style_the_qs_table(display_df),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "CSV 다운로드",
        df_year.to_csv(index=False, encoding="utf-8-sig"),
        file_name=f"benchmark_{scheme}_{selected_year}.csv",
        mime="text/csv",
    )

    st.divider()
    st.markdown("#### 전체 연도 테이블")
    st.dataframe(
        style_the_qs_table(df),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "전체 데이터 CSV 다운로드",
        df.to_csv(index=False, encoding="utf-8-sig"),
        file_name=f"benchmark_{scheme}_all_years.csv",
        mime="text/csv",
    )

def render_benchmark_scival_tab(show_heading: bool = True) -> None:
    if show_heading:
        st.subheader("벤치마킹 대학비교 (SciVal)")
    scival_sections = load_scival_benchmark_excel(SCIVAL_BENCHMARK_FILE)
    if not scival_sections:
        st.warning("SciVal 벤치마킹 데이터를 불러올 수 없습니다. 엑셀 파일을 확인해 주세요.")
        return

    period_options = list(scival_sections.keys())
    selected_period = st.radio("기간 선택", period_options, horizontal=True)
    scival_df = scival_sections[selected_period]

    universities = scival_df[("", "대학")].tolist()
    selected_unis = st.multiselect("비교 대학 선택", options=universities, default=universities)
    df_filtered = scival_df[scival_df[("", "대학")].isin(selected_unis)] if selected_unis else scival_df

    # 그룹 선택 -> 그룹별 표
    groups = sorted(
        {g for g, n in scival_df.columns if g and n != "대학"},
        key=_scival_group_order_key,
    )
    selected_group = st.selectbox("지표 그룹 선택", groups, index=0 if groups else None)
    group_metrics = [(g, n) for g, n in scival_df.columns if g == selected_group and n != "대학"]
    group_cols = [("", "대학")] + group_metrics
    group_df = df_filtered[group_cols]
    st.markdown("#### 선택한 그룹 표")
    st.dataframe(
        style_scival_table(group_df, highlight_university="전북대"),
        use_container_width=True,
        hide_index=True,
    )

    # 그룹 내 세부 지표 차트
    metric_names = [name for _, name in group_metrics]
    if not group_metrics:
        st.warning("선택한 그룹에 표시할 지표가 없습니다.")
        return
    selected_metric_name = st.selectbox("세부 지표 선택", metric_names, index=0)
    metric = (selected_group, selected_metric_name)
    chart_df = group_df[[("", "대학"), metric]].copy()
    chart_df.columns = ["대학", "값"]
    bar_data = chart_df.dropna(subset=["값"]).reset_index(drop=True)
    highlight_color = "#c1121f"
    default_color = "#9db7e0"
    st.markdown("#### 세부 지표 차트")
    bar_chart = (
        alt.Chart(bar_data)
        .mark_bar()
        .encode(
            x=alt.X("대학:N", sort="-y", title="대학"),
            y=alt.Y("값:Q", title="값"),
            color=alt.condition(
                alt.FieldEqualPredicate(field="대학", equal="전북대"),
                alt.value(highlight_color),
                alt.value(default_color),
            ),
            tooltip=["대학:N", alt.Tooltip("값:Q", title="값")],
        )
        .properties(height=340)
    )
    st.altair_chart(bar_chart, use_container_width=True)

    # 전체 표 및 다운로드
    st.markdown("#### 전체 테이블")
    st.dataframe(
        style_scival_table(df_filtered, highlight_university="전북대"),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "CSV 다운로드",
        df_filtered.to_csv(index=False, encoding="utf-8-sig"),
        file_name="scival_benchmark_filtered.csv",
        mime="text/csv",
    )
    st.caption("GT100 비교대상 대학의 SciVal 지표를 시각화하고 다운로드할 수 있습니다.")

def render_placeholder(section_name: str) -> None:
    st.info(f"{section_name} 섹션은 추후 구현 예정입니다.")






def render_global_benchmark_tab() -> None:
    st.markdown("### 글로벌 랭킹")
    render_global_ranking_tab(show_heading=False)
    st.divider()
    st.markdown("### 벤치마킹")
    st.markdown("#### THE/QS")
    render_benchmark_the_qs_tab(show_heading=False)
    st.markdown("#### SciVal")
    render_benchmark_scival_tab(show_heading=False)

NAV_STRUCTURE = {
    "전북대학교 현황": [
        ("글로벌 랭킹/벤치마킹", render_global_benchmark_tab),
        ("Fact Sheet", render_fact_sheet_tab),
    ],
    "전북대 연구성과": [
        ("Scopus 5년치 연구성과", render_publications_tab),
        ("WoS 5년치 연구성과", render_wos_performance_tab),
    ],
    "논문분야별 연구성과": [],
    "우수연구성과 확정": [],
    "연구지원·전략제언": [],
}

# 사이드바 네비게이션 (아코디언 스타일)
with st.sidebar:
    st.markdown(
        '''
        <style>
        [data-testid="stSidebar"] div.stButton > button {
            width: 100%;
            text-align: left;
            border-radius: 12px;
            border: 1px solid #dce2ec;
            background: linear-gradient(135deg, #f9fbff 0%, #f5f7fb 100%);
            color: #1f2d4d;
            box-shadow: 0 3px 10px rgba(0,0,0,0.04);
        }
        [data-testid="stSidebar"] div.stButton > button:hover {
            border-color: #c7d2e8;
            background: #f2f5fa;
        }
        </style>
        ''',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-nav-title">기준 연구영역</div>', unsafe_allow_html=True)
    primary_options = list(NAV_STRUCTURE.keys())
    current_primary = st.session_state.get("nav-expanded", primary_options[0] if primary_options else "")
    if current_primary not in primary_options and primary_options:
        current_primary = primary_options[0]
        st.session_state["nav-expanded"] = current_primary

    secondary_label = st.session_state.get("nav-secondary")

    with st.container():
        for primary in primary_options:
            is_open = primary == current_primary
            arrow = "\u25bc" if is_open else "\u25b6"
            btn_type = "primary" if is_open else "secondary"
            if st.button(f"{arrow} {primary}", key=f"nav-primary-{primary}", type=btn_type):
                st.session_state["nav-expanded"] = primary
                current_primary = primary
                secondary_label = None

            if is_open:
                secondary_options = NAV_STRUCTURE.get(primary, [])
                if secondary_options:
                    available_labels = [label for label, _ in secondary_options]
                    if secondary_label not in available_labels:
                        secondary_label = available_labels[0]
                        st.session_state["nav-secondary"] = secondary_label
                    for label, _ in secondary_options:
                        btn_type = "primary" if label == secondary_label else "secondary"
                        if st.button(f"\u00b7 {label}", key=f"nav-secondary-{primary}-{label}", type=btn_type):
                            secondary_label = label
                            st.session_state["nav-secondary"] = label
                            st.session_state["nav-expanded"] = primary
                else:
                    st.markdown('<div style="margin-left: 0.5rem; color: #888;">준비 중입니다.</div>', unsafe_allow_html=True)

primary_section = st.session_state.get("nav-expanded", primary_options[0] if primary_options else "")
secondary_options = NAV_STRUCTURE.get(primary_section, [])
secondary_label = st.session_state.get("nav-secondary") if secondary_options else None

st.subheader(
    f"{primary_section} \u00b7 {secondary_label}" if secondary_label else primary_section
)

if secondary_label:
    renderer_map = {label: renderer for label, renderer in secondary_options}
    renderer_map.get(secondary_label, secondary_options[0][1])()
else:
    render_placeholder(primary_section)