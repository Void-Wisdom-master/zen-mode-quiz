"""CSS styles for the Zen Mode Quiz application."""

ZEN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-deep: #0c0e14;
        --bg-surface: #12141c;
        --bg-card: #181b28;
        --bg-elevated: #1e2235;
        --border-subtle: #262a3f;
        --border-accent: #383d5c;
        --text-primary: #e8edf5;
        --text-secondary: #8b92a9;
        --text-muted: #5c6278;
        --accent: #6366f1;
        --accent-glow: rgba(99, 102, 241, 0.25);
        --accent-soft: #818cf8;
        --success: #22c55e;
        --success-bg: rgba(34, 197, 94, 0.12);
        --error: #ef4444;
        --error-bg: rgba(239, 68, 68, 0.12);
        --info: #3b82f6;
        --info-bg: rgba(59, 130, 246, 0.12);
        --tag-gradient: linear-gradient(135deg, #6366f1, #8b5cf6);
        --card-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 1px 3px rgba(0, 0, 0, 0.2);
        --font-stack: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                       "PingFang SC", "Microsoft YaHei", "Hiragino Sans GB",
                       "Noto Sans CJK SC", sans-serif;
    }

    /* ── Reset ── */
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stHeader"] { background: transparent !important; }
    .stApp { background: var(--bg-deep); color: var(--text-primary); }
    .stApp > header { background: transparent !important; }

    *, html, body, [class*="css"], [class*="st-"] {
        font-family: var(--font-stack) !important;
    }

    .main > .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: var(--bg-surface);
        border-right: 1px solid var(--border-subtle);
    }
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }
    [data-testid="stSidebar"] h2 {
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: var(--text-primary) !important;
        margin: 1rem 0 0.75rem !important;
    }
    [data-testid="stSidebar"] h3 {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0.75rem 0 0.5rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {
        color: var(--text-secondary) !important;
        font-size: 0.85rem;
    }
    [data-testid="stSidebar"] hr {
        border-color: var(--border-subtle) !important;
        margin: 1rem 0 !important;
    }

    /* ── Selectbox / Multiselect ── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        transition: border-color 0.2s;
    }
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover {
        border-color: var(--accent) !important;
    }
    .stSelectbox [data-baseweb="select"] span,
    .stMultiSelect [data-baseweb="select"] span {
        color: var(--text-primary) !important;
    }

    /* ── HUD ── */
    .hud-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: var(--bg-card);
        padding: 14px 22px;
        border-radius: 14px;
        border: 1px solid var(--border-subtle);
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .hud-item {
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--text-secondary);
    }
    .hud-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-left: 6px;
    }
    .hud-accent { color: var(--accent-soft) !important; }
    .hud-warn { color: var(--error) !important; }

    /* ── Question Card ── */
    .zen-card {
        background: var(--bg-card);
        padding: 32px 36px;
        border-radius: 18px;
        border: 1px solid var(--border-subtle);
        margin-bottom: 20px;
        box-shadow: var(--card-shadow);
        position: relative;
        overflow: hidden;
    }
    .zen-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 3px;
        background: var(--tag-gradient);
    }
    .question-text {
        font-size: 1.15rem;
        font-weight: 500;
        color: var(--text-primary);
        line-height: 1.75;
        letter-spacing: 0.01em;
    }

    .tag {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 5px 14px;
        background: var(--tag-gradient);
        color: #fff;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin-bottom: 18px;
        box-shadow: 0 2px 12px rgba(99, 102, 241, 0.3);
    }

    /* ── Radio Buttons ── */
    .stRadio {
        margin: 10px 0;
    }
    .stRadio > div {
        gap: 0 !important;
    }
    .stRadio div[role='radiogroup'] {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    .stRadio div[role='radiogroup'] > label {
        background: var(--bg-elevated) !important;
        border: 2px solid var(--border-subtle) !important;
        color: var(--text-primary) !important;
        font-size: 1.25rem !important;
        font-weight: 500;
        padding: 24px 32px;
        border-radius: 16px;
        margin: 0 !important;
        transition: all 0.2s ease;
        cursor: pointer;
        opacity: 1 !important;
        display: flex !important;
        align-items: center;
        min-height: 72px;
    }
    .stRadio div[role='radiogroup'] > label:hover {
        border-color: var(--accent) !important;
        background: rgba(99, 102, 241, 0.06) !important;
        transform: translateX(4px);
    }
    .stRadio div[role='radiogroup'] > label[data-checked="true"],
    .stRadio div[role='radiogroup'] > label:has(input:checked) {
        border-color: var(--accent) !important;
        background: rgba(99, 102, 241, 0.1) !important;
        box-shadow: 0 0 0 1.5px var(--accent), 0 4px 20px rgba(99, 102, 241, 0.2);
    }
    div[role="radiogroup"] div[data-testid="stMarkdownContainer"] p {
        color: var(--text-primary) !important;
        font-size: 1.25rem !important;
    }
    /* Radio circle styling */
    .stRadio div[role='radiogroup'] input[type="radio"] {
        accent-color: var(--accent);
        width: 24px;
        height: 24px;
        margin-right: 16px;
        flex-shrink: 0;
    }

    /* ── Checkboxes ── */
    .stCheckbox {
        margin: 6px 0;
    }
    .stCheckbox label {
        background: var(--bg-elevated) !important;
        border: 2px solid var(--border-subtle) !important;
        border-radius: 16px !important;
        padding: 22px 28px !important;
        color: var(--text-primary) !important;
        font-size: 1.25rem !important;
        font-weight: 500;
        transition: all 0.2s ease;
        gap: 16px;
        min-height: 68px;
    }
    .stCheckbox label:hover {
        border-color: var(--accent) !important;
        background: rgba(99, 102, 241, 0.06) !important;
    }
    .stCheckbox input:checked ~ div:first-child {
        border-color: var(--accent) !important;
        background: var(--accent) !important;
    }
    .stCheckbox input:checked ~ p {
        color: var(--accent-soft) !important;
    }
    .stCheckbox [data-testid="stMarkdownContainer"] p {
        font-size: 1.25rem !important;
    }
    .stCheckbox input[type="checkbox"] {
        accent-color: var(--accent);
        width: 22px;
        height: 22px;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: var(--bg-elevated) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
        height: auto !important;
    }
    .stButton > button:hover {
        border-color: var(--accent) !important;
        background: rgba(99, 102, 241, 0.08) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.15) !important;
    }
    .stButton > button:active {
        transform: translateY(0);
    }
    .stButton > button:disabled {
        opacity: 0.35 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }

    button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: #fff !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 12px 28px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 18px rgba(99, 102, 241, 0.3) !important;
        letter-spacing: 0.01em;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.45) !important;
    }

    /* ── Text Input ── */
    .stTextInput input {
        background: var(--bg-elevated) !important;
        border: 1.5px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-size: 0.95rem !important;
        padding: 12px 16px !important;
        transition: border-color 0.2s;
    }
    .stTextInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-glow) !important;
    }

    /* ── Feedback Boxes ── */
    .feedback-box {
        padding: 16px 24px;
        border-radius: 12px;
        margin: 16px 0;
        font-weight: 600;
        text-align: center;
        font-size: 1.05rem;
        border: 1px solid transparent;
        animation: fadeSlideIn 0.3s ease;
    }
    .feedback-success {
        background: var(--success-bg);
        color: var(--success);
        border-color: rgba(34, 197, 94, 0.3);
    }
    .feedback-error {
        background: var(--error-bg);
        color: var(--error);
        border-color: rgba(239, 68, 68, 0.3);
    }
    .feedback-info {
        background: var(--info-bg);
        color: var(--info);
        border-color: rgba(59, 130, 246, 0.3);
    }

    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(-8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Completion Card ── */
    .completion-card {
        text-align: center;
        padding: 60px 40px;
        background: var(--bg-card);
        border-radius: 20px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--card-shadow);
        max-width: 520px;
        margin: 40px auto;
    }
    .completion-card h2 {
        background: var(--tag-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ── Welcome Screen ── */
    .welcome-container {
        text-align: center;
        padding: 100px 20px;
        max-width: 500px;
        margin: 0 auto;
    }
    .welcome-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: var(--tag-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
    }
    .welcome-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 32px;
    }
    .welcome-hint {
        color: var(--accent-soft);
        font-size: 0.95rem;
        font-weight: 500;
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateX(0); }
        40% { transform: translateX(-8px); }
        60% { transform: translateX(-4px); }
    }
    .arrow-hint {
        animation: bounce 2s infinite;
        font-size: 1.5rem;
        color: var(--accent);
        display: inline-block;
        margin-right: 10px;
    }

    /* ── Alert / Toast ── */
    .stAlert {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    div[data-baseweb="toast"] {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border-subtle) !important;
    }

    /* ── Misc ── */
    hr { border-color: var(--border-subtle) !important; margin: 1.25rem 0 !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: var(--bg-elevated) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-subtle) !important;
        color: var(--text-primary) !important;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .streamlit-expanderContent {
        border: 1px solid var(--border-subtle) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        background: var(--bg-card) !important;
        padding: 1rem !important;
    }

    /* ── Progress bar in sidebar ── */
    .stProgress > div > div {
        background: var(--bg-elevated) !important;
        border-radius: 10px !important;
        height: 6px !important;
    }
    .stProgress > div > div > div {
        background: var(--tag-gradient) !important;
        border-radius: 10px !important;
    }

    /* ── Download button ── */
    .stDownloadButton > button {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        border-color: var(--accent) !important;
        background: rgba(99, 102, 241, 0.08) !important;
    }

    /* ── Popover ── */
    div[data-testid="stPopoverBody"] {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        box-shadow: var(--card-shadow) !important;
    }
    div[data-testid="stPopoverBody"] button {
        width: 100%;
    }

    /* ── File uploader ── */
    section[data-testid="stFileUploader"] {
        background: var(--bg-elevated) !important;
        border: 1.5px dashed var(--border-subtle) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        transition: border-color 0.2s;
    }
    section[data-testid="stFileUploader"]:hover {
        border-color: var(--accent) !important;
    }
    section[data-testid="stFileUploader"] button {
        background: var(--accent) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-deep);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border-subtle);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--border-accent);
    }

    /* ── Responsive tweaks ── */
    @media (max-width: 768px) {
        .zen-card { padding: 24px 20px; }
        .question-text { font-size: 1rem; }
        .hud-container { flex-direction: column; gap: 8px; }
    }
</style>
"""
