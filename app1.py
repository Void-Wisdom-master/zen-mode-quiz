"""Zen Mode Quiz - Main application UI orchestration."""
import copy
from typing import Any

import streamlit as st

from styles import ZEN_CSS
from data_manager import process_excel, export_wrong_questions, save_state, load_state
from quiz_utils import normalize_answer

# --- Page config ---
st.set_page_config(
    page_title="ZenMode Ultimate",
    layout="wide",
    page_icon=":crescent_moon:",
    initial_sidebar_state="expanded"
)

st.markdown(ZEN_CSS, unsafe_allow_html=True)

# --- Session state init ---
if 'init' not in st.session_state:
    st.session_state.banks = {}
    st.session_state.progress = {}
    st.session_state.active_bank = None
    st.session_state.filters = {}
    st.session_state.feedback_state = None
    load_state()
    st.session_state.init = True


def reset_feedback() -> None:
    st.session_state.feedback_state = None


def get_filtered_questions(bank_name: str) -> list[dict[str, Any]]:
    full_qs = st.session_state.banks.get(bank_name, [])
    active_filters = st.session_state.filters.get(bank_name, [])
    return [q for q in full_qs if q['type'] in active_filters]


def _fmt_ao(ans: str) -> str:
    return "正确" if ans == "A" else "错误" if ans == "B" else ans


def _persist() -> None:
    save_state()


# --- Sidebar ---
with st.sidebar:
    st.header(":wrench: 控制台")

    st.subheader(":books: 题库")
    bank_names = list(st.session_state.banks.keys())
    if bank_names:
        curr_idx = bank_names.index(st.session_state.active_bank) if st.session_state.active_bank in bank_names else 0
        selected = st.selectbox("切换题库", bank_names, index=curr_idx)
        if selected != st.session_state.active_bank:
            st.session_state.active_bank = selected
            reset_feedback()
            _persist()
            st.rerun()

        if st.session_state.active_bank:
            curr_q_list = st.session_state.banks[st.session_state.active_bank]
            all_types = list(set(q['type'] for q in curr_q_list))
            default_sel = st.session_state.filters.get(st.session_state.active_bank, all_types)
            st.markdown("---")
            st.subheader(":dart: 筛选")
            selected_types = st.multiselect("只刷:", all_types, default=default_sel)
            if selected_types != default_sel:
                st.session_state.filters[st.session_state.active_bank] = selected_types
                st.session_state.progress[st.session_state.active_bank]["current_idx"] = 0
                reset_feedback()
                _persist()
                st.rerun()
    else:
        st.warning("暂无题库")

    if st.session_state.active_bank:
        prog = st.session_state.progress[st.session_state.active_bank]
        wrong_cnt = len(prog['wrong'])
        if wrong_cnt > 0:
            st.divider()
            st.subheader(f":package: 错题 ({wrong_cnt})")
            c1, c2 = st.columns(2)
            xls = export_wrong_questions(prog['wrong'])
            c1.download_button("导出", xls, "错题.xlsx", use_container_width=True)
            with c2.popover("清空"):
                if st.button("确认", type="primary"):
                    prog['wrong'] = []
                    _persist()
                    st.rerun()
            if st.button(":floppy_disk: 存为新题库", use_container_width=True):
                new_name = f"{st.session_state.active_bank}_错题本"
                import time as _time
                if new_name in st.session_state.banks:
                    new_name += f"_{int(_time.time())}"
                new_qs = [copy.deepcopy(wq) for wq in prog['wrong']]
                for nq in new_qs:
                    nq['user_answer'] = None
                st.session_state.banks[new_name] = new_qs
                st.session_state.progress[new_name] = {"history": {}, "wrong": [], "current_idx": 0}
                st.session_state.active_bank = new_name
                st.session_state.filters[new_name] = list(set(q['type'] for q in new_qs))
                reset_feedback()
                _persist()
                st.rerun()

    st.divider()
    with st.expander(":heavy_plus_sign: 导入", expanded=(not bank_names)):
        f = st.file_uploader("Excel", type=['xlsx', 'xls'])
        n = st.text_input("命名")
        if f and st.button("导入", type="primary"):
            with st.spinner("解析中..."):
                qs, err = process_excel(f)
            if err:
                st.error(err)
            else:
                final_n = n.strip() if n else f.name.split('.')[0]
                import time as _time
                if final_n in st.session_state.banks:
                    final_n += f"_{int(_time.time())}"
                st.session_state.banks[final_n] = qs
                st.session_state.progress[final_n] = {"history": {}, "wrong": [], "current_idx": 0}
                st.session_state.active_bank = final_n
                st.session_state.filters[final_n] = list(set(q['type'] for q in qs))
                reset_feedback()
                _persist()
                st.rerun()

    if st.session_state.active_bank:
        st.divider()
        with st.popover(":wastebasket: 删除", use_container_width=True):
            if st.button(":red_circle: 确认"):
                del st.session_state.banks[st.session_state.active_bank]
                del st.session_state.progress[st.session_state.active_bank]
                del st.session_state.filters[st.session_state.active_bank]
                st.session_state.active_bank = (
                    list(st.session_state.banks.keys())[0] if st.session_state.banks else None
                )
                reset_feedback()
                _persist()
                st.rerun()

# --- Main area ---
if not st.session_state.active_bank:
    st.markdown(
        """<div class="welcome-container">
            <div class="welcome-title">👋 欢迎使用</div>
            <p class="welcome-subtitle">ZenMode 专注刷题模式</p>
            <p style="color:#666; margin-bottom: 30px;">请点击左上角箭头，打开侧边栏导入题库开始学习</p>
            <div><span class="arrow-hint">👈</span><span class="welcome-hint">点击这里展开菜单</span></div>
        </div>""",
        unsafe_allow_html=True)
else:
    bk = st.session_state.active_bank
    qs = get_filtered_questions(bk)
    full_qs = st.session_state.banks[bk]

    if not qs:
        st.warning("⚠️ 无题目，请检查筛选。")
    else:
        pg = st.session_state.progress[bk]
        idx = pg['current_idx']
        total_q = len(qs)

        # Handle completion
        if idx >= total_q:
            pg['current_idx'] = total_q
            st.balloons()
            st.markdown(
                f"""<div class="completion-card">
                    <h2 style="font-size: 36px; margin-bottom: 20px;">🎉 恭喜完成!</h2>
                    <p style="font-size: 18px; color: #a0a0b0;">本轮共 <span style="color: var(--accent-color); font-weight: bold;">{total_q}</span> 题</p>
                    <p style="font-size: 18px; color: #a0a0b0;">错题 <span style="color: var(--error-color); font-weight: bold;">{len(pg['wrong'])}</span> 道</p>
                </div>""",
                unsafe_allow_html=True)
            if st.button(":repeat: 再刷一次", type="primary", use_container_width=True):
                pg['current_idx'] = 0
                pg['history'] = {}
                reset_feedback()
                _persist()
                st.rerun()
        else:
            # --- HUD ---
            wrong_q_count = len(pg['wrong'])
            pct = int((idx + 1) / total_q * 100)
            st.markdown(f"""
            <div class="hud-container">
                <div class="hud-item" style="max-width: 35%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{bk}">{bk}</div>
                <div style="display:flex; gap: 18px; align-items: center;">
                    <div class="hud-item">进度 <span class="hud-value hud-accent">{idx + 1}</span><span style="color:var(--text-muted)">/{total_q}</span></div>
                    <div class="hud-item" style="font-size:0.8rem;color:var(--text-muted)">{pct}%</div>
                    <div class="hud-item">错题 <span class="hud-value hud-warn">{wrong_q_count}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- Question card ---
            q = qs[idx]
            st.markdown(f"""
            <div class="zen-card">
                <span class="tag">{q['type']}</span>
                <div class="question-text">{q['content']}</div>
            </div>
            """, unsafe_allow_html=True)

            saved = pg['history'].get(idx)
            is_answered = idx in pg['history']
            reveal_key = f"reveal_{bk}_{idx}"
            is_revealed = st.session_state.get(reveal_key, False)

            # --- Answer input (always rendered so selection stays visible) ---
            user_choice: Any = None

            if q['code'] == 'AO':
                sel = 0 if saved == 'A' else (1 if saved == 'B' else None)
                user_choice = st.radio(
                    "判断题", ['A', 'B'],
                    index=sel,
                    format_func=lambda x: "正确" if x == 'A' else "错误",
                    horizontal=True,
                    key=f"{bk}_{idx}",
                    label_visibility="collapsed"
                )

            elif q['code'] == 'BO':
                if q['options']:
                    ks = list(q['options'].keys())
                    ds = [f"{k}. {v}" for k, v in q['options'].items()]
                    sel = ks.index(saved) if saved in ks else None
                    val = st.radio(
                        "单选题", ds, index=sel,
                        key=f"{bk}_{idx}",
                        label_visibility="collapsed"
                    )
                    if val:
                        user_choice = val.split('.')[0]
                else:
                    user_choice = st.text_input(
                        "输入答案:", value=saved or "",
                        key=f"tx_{bk}_{idx}"
                    ).strip().upper()

            elif q['code'] == 'CO':
                st.markdown(
                    '<div style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:8px;font-weight:600;">'
                    '📋 多选题（可多选）</div>', unsafe_allow_html=True)
                if q['options']:
                    selected_opts = []
                    for k, v in q['options'].items():
                        chk = (k in saved) if saved else False
                        if st.checkbox(f"{k}. {v}", value=chk, key=f"{bk}_{idx}_{k}"):
                            selected_opts.append(k)
                    if selected_opts:
                        user_choice = "".join(sorted(selected_opts))
                else:
                    user_choice = st.text_input(
                        "输入答案:", value=saved or "",
                        key=f"tx_{bk}_{idx}"
                    ).strip().upper()

            # --- Unified submit button ---
            if not is_answered and not is_revealed:
                st.write("")
                if st.button("提交", type="primary", use_container_width=True):
                    if not user_choice:
                        st.toast("请先作答", icon=":warning:")
                    else:
                        pg['history'][idx] = user_choice
                        if normalize_answer(user_choice) != normalize_answer(q.get('answer', '')):
                            if not any(w.get('raw_content') == q.get('raw_content') for w in pg['wrong']):
                                wq = copy.deepcopy(q)
                                wq['user_answer'] = user_choice
                                pg['wrong'].append(wq)
                        _persist()
                        st.rerun()

            # --- Result feedback ---
            if is_answered:
                ans = q.get('answer', '')
                correct = normalize_answer(saved) == normalize_answer(ans)
                display_ans = _fmt_ao(ans) if q['code'] == 'AO' else ans
                if correct:
                    st.markdown(
                        '<div class="feedback-box feedback-success">正确!</div>',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="feedback-box feedback-error">错误! 正确答案: <strong>{display_ans}</strong></div>',
                        unsafe_allow_html=True)

            if is_revealed:
                ans = q.get('answer', '')
                display_ans = _fmt_ao(ans) if q['code'] == 'AO' else ans
                st.markdown(
                    f'<div class="feedback-box feedback-info">答案: <strong>{display_ans}</strong></div>',
                    unsafe_allow_html=True)

            # --- Continue button ---
            if is_answered or is_revealed:
                st.write("")
                if st.button("继续", type="primary", use_container_width=True):
                    pg['current_idx'] += 1
                    st.session_state[reveal_key] = False
                    _persist()
                    st.rerun()

            # --- Navigation ---
            st.write("")
            c1, c2, c3 = st.columns([1, 1, 1])
            if c1.button(":arrow_backward:", disabled=(idx == 0), use_container_width=True):
                pg['current_idx'] -= 1
                st.session_state[reveal_key] = False
                _persist()
                st.rerun()
            if c2.button(":eye: 答案", use_container_width=True):
                st.session_state[reveal_key] = True
                _persist()
                st.rerun()
            if c3.button(":arrow_forward:", use_container_width=True):
                pg['current_idx'] += 1
                st.session_state[reveal_key] = False
                _persist()
                st.rerun()
