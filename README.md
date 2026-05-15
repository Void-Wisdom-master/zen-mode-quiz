# Zen Mode Quiz 禅境刷题

A minimalist, dark-themed quiz app built with Streamlit. Upload Excel question banks and practice in a focused, zen-like environment.

基于 Streamlit 的极简暗色刷题工具。上传 Excel 题库即可开始专注刷题。

## Features 功能

- **Upload & Parse** — Import `.xlsx` question banks with auto-detection of question types (judgment, single-choice, multiple-choice)
- **Filtering** — Filter questions by type within a bank
- **Progress Tracking** — Per-bank history, wrong question collection, and progress HUD
- **Export Wrong Questions** — Download wrong questions as Excel for review
- **Focus-First UI** — Dark minimal design with zero distractions; keyboard-friendly navigation
- **错题导出** — 支持导出错题为 Excel 文件
- **多题库** — 可同时导入多个题库并切换

## Quick Start 快速开始

### Deploy on Streamlit Cloud

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io) and deploy
3. Upload your Excel file via the sidebar to start practicing

> **Note:** Streamlit Cloud has an ephemeral filesystem — `user_data.json` persistence is session-only. Data will be lost when the app restarts. For full persistence, run locally.

### Run Locally

```bash
pip install -r requirements.txt
streamlit run app1.py
```

## Excel Format 题库格式

The uploaded Excel file must contain these three columns:

| Column 列名 | Description 说明 |
|---|---|
| 类型 / Type | Question type: `A0/AO/判断` (judgment), `B0/BO/单选` (single), `C0/CO/多选` (multi) |
| 内容 / Content | Question text. Supports inline options in parentheses `()` for single/multi-choice |
| 答案 / Answer | Correct answer. For judgment: `A`=correct, `B`=wrong. For choice: uppercase letter(s) |

## Tech Stack

- [Streamlit](https://streamlit.io)
- Pandas / OpenPyXL / XlsxWriter
- Pure CSS dark theme (no framework)
