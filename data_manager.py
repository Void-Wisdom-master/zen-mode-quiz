"""Data management: Excel parsing, state persistence, and export utilities."""
import io
import json
import os
from typing import Any, Optional

import pandas as pd
import streamlit as st

from quiz_utils import normalize_text, normalize_answer, parse_options_zen

DATA_FILE = "user_data.json"


def find_column(df: pd.DataFrame, keywords: list[str]) -> Optional[str]:
    """Find a column in the DataFrame by keywords (case-insensitive)."""
    for c in df.columns:
        c_lower = c.lower()
        for kw in keywords:
            if kw.lower() in c_lower:
                return c
    return None


def process_excel(file) -> tuple[Optional[list[dict[str, Any]]], Optional[str]]:
    """Process Excel file and extract questions. Returns (questions_list, error_message)."""
    try:
        df = pd.read_excel(file)
        if df.empty:
            return None, "Excel文件为空"

        df.columns = [str(c).strip() for c in df.columns]

        col_type = find_column(df, ['类型', 'Type', '题型', 'type', 'kind'])
        col_content = find_column(df, ['内容', 'Content', '题目', '问题', 'question', 'content'])
        col_answer = find_column(df, ['答案', 'Answer', '结果', '正确答案', 'answer', 'result'])

        missing_cols = []
        if not col_type:
            missing_cols.append("类型/Type/题型")
        if not col_content:
            missing_cols.append("内容/Content/题目")
        if not col_answer:
            missing_cols.append("答案/Answer/结果")

        if missing_cols:
            return None, f"缺少必要列: {', '.join(missing_cols)}。可用列: {', '.join(df.columns)}"

        df[col_type] = df[col_type].fillna("").astype(str)
        df[col_content] = df[col_content].fillna("").astype(str)
        df[col_answer] = df[col_answer].fillna("").astype(str)

        records = df.to_dict('records')
        total_rows = len(records)

        if total_rows == 0:
            return None, "Excel文件中没有数据行"

        progress_bar = st.progress(0)
        skipped_count = 0
        questions: list[dict[str, Any]] = []

        for i, row in enumerate(records):
            try:
                if i % (max(1, total_rows // 10)) == 0:
                    progress_bar.progress((i + 1) / total_rows)

                raw_type = normalize_text(row.get(col_type, "")).upper()
                raw_content = row.get(col_content, "")
                raw_answer = row.get(col_answer, "")

                if not raw_content or not raw_content.strip():
                    skipped_count += 1
                    continue

                if not raw_type:
                    skipped_count += 1
                    continue

                if any(x in raw_type for x in ['A0', 'AO', '判断', 'TRUE', 'FALSE', 'TF', '对错', '是非']):
                    q_code, q_name = 'AO', '判断题'
                elif any(x in raw_type for x in ['B0', 'BO', '单选', 'SINGLE', '单项', 'RADIO']):
                    q_code, q_name = 'BO', '单选题'
                elif any(x in raw_type for x in ['C0', 'CO', '多选', 'MULTI', '多项', 'CHECKBOX']):
                    q_code, q_name = 'CO', '多选题'
                else:
                    q_code, q_name = 'UNK', '未知'

                q_text, q_options = parse_options_zen(raw_content)
                normalized_answer = normalize_answer(raw_answer)

                questions.append({
                    "id": i, "code": q_code, "type": q_name,
                    "content": q_text, "options": q_options, "answer": normalized_answer,
                    "user_answer": None, "raw_content": raw_content
                })
            except Exception:
                skipped_count += 1

        progress_bar.empty()

        if not questions:
            return None, f"未能解析出任何有效题目 (跳过了 {skipped_count} 行)"

        return questions, None
    except Exception as e:
        return None, f"解析错误: {str(e)}"


def export_wrong_questions(q_list: list[dict[str, Any]]) -> Optional[bytes]:
    """Export wrong questions to Excel format. Returns bytes or None."""
    if not q_list:
        return None
    data = []
    for q in q_list:
        data.append({
            "题目类型": q.get('type', '未知'),
            "题目内容": q.get('raw_content', ''),
            "正确答案": q.get('answer', ''),
            "你的误选": q.get('user_answer', '')
        })
    df = pd.DataFrame(data)
    out = io.BytesIO()
    try:
        with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        return out.getvalue()
    except Exception:
        return None


def save_state() -> None:
    """Persist session state to JSON file."""
    import streamlit as st
    data = {
        "banks": st.session_state.banks,
        "progress": st.session_state.progress,
        "active_bank": st.session_state.active_bank,
        "filters": st.session_state.filters,
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except (OSError, TypeError):
        pass


def load_state() -> bool:
    """Load persisted state from JSON file. Returns True if data was loaded."""
    import streamlit as st
    if not os.path.exists(DATA_FILE):
        return False
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        st.session_state.banks = data.get("banks", {})
        st.session_state.progress = data.get("progress", {})
        st.session_state.active_bank = data.get("active_bank", None)
        st.session_state.filters = data.get("filters", {})
        # JSON only supports string keys; convert history keys back to int
        for prog in st.session_state.progress.values():
            prog["history"] = {int(k): v for k, v in prog.get("history", {}).items()}
        return True
    except (OSError, json.JSONDecodeError):
        return False


