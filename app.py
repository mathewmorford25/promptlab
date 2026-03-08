import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import json
import csv
import io
import html
from datetime import datetime


load_dotenv()

api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="PromptLab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #06111f 0%, #081424 100%);
        color: #f8fafc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        letter-spacing: -0.02em;
    }

    p, li, label, span, div {
        color: #dbe4f0;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #f3f4f6 !important;
    }

    .hero {
        background:
            radial-gradient(circle at top right, rgba(56,189,248,0.22), transparent 30%),
            radial-gradient(circle at bottom left, rgba(99,102,241,0.16), transparent 28%),
            linear-gradient(135deg, #111827 0%, #0f172a 55%, #08101d 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 14px 40px rgba(0,0,0,0.28);
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.35rem;
        letter-spacing: -0.03em;
    }

    .hero-subtitle {
        font-size: 1.02rem;
        color: #cbd5e1;
        max-width: 760px;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    .hero-badges {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-top: 0.6rem;
    }

    .hero-badge {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        color: #dbeafe;
        font-size: 0.88rem;
        font-weight: 600;
    }

    .small-muted {
        color: #94a3b8 !important;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
    }

    .card-wrap {
        background: rgba(15,23,42,0.85);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        overflow: hidden;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        height: 100%;
    }

    .card-header {
        background: linear-gradient(180deg, rgba(30,41,59,0.95) 0%, rgba(15,23,42,0.95) 100%);
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding: 0.8rem 1rem;
        font-weight: 800;
        font-size: 1rem;
        color: #f8fafc;
    }

    .card-header.best {
        background: linear-gradient(90deg, rgba(16,185,129,0.26), rgba(34,197,94,0.12));
        color: #ecfdf5;
        border-bottom: 1px solid rgba(16,185,129,0.45);
    }

    .card-body {
        padding: 1rem;
    }

    .section-label {
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94a3b8 !important;
        margin-bottom: 0.45rem;
    }

    .score-chip {
        display: inline-block;
        margin: 0.18rem 0.3rem 0.18rem 0;
        padding: 0.36rem 0.6rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        color: #e2e8f0;
        font-size: 0.86rem;
        font-weight: 600;
    }

    .stButton > button {
        border-radius: 14px !important;
        padding: 0.72rem 1rem !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: linear-gradient(180deg, #132033 0%, #0f172a 100%) !important;
        color: #f8fafc !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.18);
    }

    .stButton > button:hover {
        border-color: rgba(56,189,248,0.45) !important;
        transform: translateY(-1px);
    }

    .stDownloadButton > button {
        border-radius: 14px !important;
        font-weight: 700 !important;
    }

    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: rgba(15,23,42,0.88) !important;
        color: #f8fafc !important;
    }

    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
    }

    .streamlit-expanderHeader {
        border-radius: 14px !important;
        background: rgba(15,23,42,0.75) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
    }

    div[data-testid="stMarkdownContainer"] p {
        margin-top: 0.15rem;
        margin-bottom: 0.35rem;
        line-height: 1.45;
    }

    .text-block {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 0.9rem;
    }
    
    .prompt-version-block {
    min-height: 260px;
}

.copy-box textarea {
    font-size: 0.9rem !important;
    line-height: 1.45 !important;
    border-radius: 12px !important;
}

.prompt-version-block pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    line-height: 1.75;
    font-size: 0.95rem;
}

    .text-block pre {
        margin: 0;
        white-space: pre-wrap;
        word-wrap: break-word;
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 0.96rem;
        line-height: 1.55;
        color: #e5edf7;
    }
</style>
""", unsafe_allow_html=True)

client = OpenAI(api_key=api_key) if api_key else None


def reset_app():
    st.session_state.user_prompt = ""
    st.session_state.category = "General"
    st.session_state.optimized_text = ""
    st.session_state.prompt_versions = []
    st.session_state.test_outputs = []
    st.session_state.scores = ""
    st.session_state.parsed_scores = {}
    st.session_state.best_version = ""
    st.session_state.best_reason = ""


def clear_history():
    st.session_state.history = []


def add_to_history():
    history_item = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": st.session_state.category,
        "prompt": st.session_state.user_prompt,
        "best_version": st.session_state.best_version,
        "best_reason": st.session_state.best_reason
    }
    st.session_state.history.insert(0, history_item)


def generate_optimized_prompts(prompt_text: str, prompt_category: str) -> tuple[str, list[str]]:
    system_prompt = f"""
    You are an expert prompt engineer.

    The user is working in this category: {prompt_category}.

    Your job is to create 3 improved PROMPTS that the user could copy and paste into another AI tool.

    IMPORTANT RULES:
    - Do NOT answer the user's request.
    - Do NOT complete the task.
    - Do NOT write the final email, recipe, response, guide, or content.
    - ONLY write improved prompts that instruct another AI what to do.
    - Each version must clearly read like a prompt/request, not like the final finished output.

    Make each version meaningfully different:
    - Version 1: simple and clear
    - Version 2: more structured and detailed
    - Version 3: expert-level with constraints, formatting instructions, tone guidance, and quality improvements

    If the user's request is "write an email", your output should be a better prompt such as:
    "Write a professional email to my manager explaining that I will be out of the office tomorrow due to a personal reason. Keep the tone respectful and concise."

    If the user's request is "make a burger recipe", your output should be a better prompt such as:
    "Write a step-by-step recipe for a homemade cheeseburger, including ingredients, prep instructions, cook time, and serving suggestions."

    Format the response exactly like this:

    Version 1
    [improved prompt only]

    Version 2
    [improved prompt only]

    Version 3
    [improved prompt only]
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_text}
        ]
    )

    full_text = response.choices[0].message.content
    versions = []
    current_lines = []

    for line in full_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Version 1") or stripped.startswith("Version 2") or stripped.startswith("Version 3"):
            if current_lines:
                versions.append("\n".join(current_lines).strip())
                current_lines = []
        else:
            if stripped:
                current_lines.append(stripped)

    if current_lines:
        versions.append("\n".join(current_lines).strip())

    return full_text, versions


def run_prompt_test(test_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": test_prompt}]
    )
    return response.choices[0].message.content


def score_outputs(original_prompt: str, output_1: str, output_2: str, output_3: str) -> str:
    scoring_prompt = f"""
You are evaluating 3 AI-generated outputs based on the user's original request.

Original request:
{original_prompt}

Score each output from 1 to 10 in these categories:
- Clarity
- Completeness
- Professionalism
- Overall Quality

Then choose the best version.

Format the response exactly like this:

Version 1
Clarity: X/10
Completeness: X/10
Professionalism: X/10
Overall Quality: X/10

Version 2
Clarity: X/10
Completeness: X/10
Professionalism: X/10
Overall Quality: X/10

Version 3
Clarity: X/10
Completeness: X/10
Professionalism: X/10
Overall Quality: X/10

Best Version: Version X
Reason: [short explanation]

Here are the outputs to score:

Version 1 Output:
{output_1}

Version 2 Output:
{output_2}

Version 3 Output:
{output_3}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert AI output evaluator."},
            {"role": "user", "content": scoring_prompt}
        ]
    )
    return response.choices[0].message.content


def parse_score_text(score_text: str):
    parsed = {"Version 1": {}, "Version 2": {}, "Version 3": {}}
    best_version = ""
    best_reason = ""

    version_pattern = r"(Version [123])\s+Clarity:\s*(\d+/10)\s+Completeness:\s*(\d+/10)\s+Professionalism:\s*(\d+/10)\s+Overall Quality:\s*(\d+/10)"
    matches = re.findall(version_pattern, score_text, re.DOTALL)

    for match in matches:
        version_name, clarity, completeness, professionalism, overall_quality = match
        parsed[version_name] = {
            "Clarity": clarity,
            "Completeness": completeness,
            "Professionalism": professionalism,
            "Overall Quality": overall_quality
        }

    best_match = re.search(r"Best Version:\s*(Version [123])", score_text)
    if best_match:
        best_version = best_match.group(1)

    reason_match = re.search(r"Reason:\s*(.*)", score_text, re.DOTALL)
    if reason_match:
        best_reason = reason_match.group(1).strip()

    return parsed, best_version, best_reason


def build_export_data():
    return {
        "original_prompt": st.session_state.user_prompt,
        "category": st.session_state.category,
        "optimized_prompts": {
            "Version 1": st.session_state.prompt_versions[0] if len(st.session_state.prompt_versions) > 0 else "",
            "Version 2": st.session_state.prompt_versions[1] if len(st.session_state.prompt_versions) > 1 else "",
            "Version 3": st.session_state.prompt_versions[2] if len(st.session_state.prompt_versions) > 2 else ""
        },
        "test_outputs": {
            "Version 1": st.session_state.test_outputs[0] if len(st.session_state.test_outputs) > 0 else "",
            "Version 2": st.session_state.test_outputs[1] if len(st.session_state.test_outputs) > 1 else "",
            "Version 3": st.session_state.test_outputs[2] if len(st.session_state.test_outputs) > 2 else ""
        },
        "scores": st.session_state.parsed_scores,
        "best_version": st.session_state.best_version,
        "best_reason": st.session_state.best_reason
    }


def build_json_export():
    return json.dumps(build_export_data(), indent=4)


def build_csv_export():
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Field", "Value"])
    writer.writerow(["Original Prompt", st.session_state.user_prompt])
    writer.writerow(["Category", st.session_state.category])
    writer.writerow(["Best Version", st.session_state.best_version])
    writer.writerow(["Best Reason", st.session_state.best_reason])

    writer.writerow([])
    writer.writerow(["Optimized Prompt - Version 1", st.session_state.prompt_versions[0] if len(st.session_state.prompt_versions) > 0 else ""])
    writer.writerow(["Optimized Prompt - Version 2", st.session_state.prompt_versions[1] if len(st.session_state.prompt_versions) > 1 else ""])
    writer.writerow(["Optimized Prompt - Version 3", st.session_state.prompt_versions[2] if len(st.session_state.prompt_versions) > 2 else ""])

    writer.writerow([])
    writer.writerow(["Output - Version 1", st.session_state.test_outputs[0] if len(st.session_state.test_outputs) > 0 else ""])
    writer.writerow(["Output - Version 2", st.session_state.test_outputs[1] if len(st.session_state.test_outputs) > 1 else ""])
    writer.writerow(["Output - Version 3", st.session_state.test_outputs[2] if len(st.session_state.test_outputs) > 2 else ""])

    writer.writerow([])
    for version_name in ["Version 1", "Version 2", "Version 3"]:
        score_data = st.session_state.parsed_scores.get(version_name, {})
        writer.writerow([f"{version_name} Clarity", score_data.get("Clarity", "")])
        writer.writerow([f"{version_name} Completeness", score_data.get("Completeness", "")])
        writer.writerow([f"{version_name} Professionalism", score_data.get("Professionalism", "")])
        writer.writerow([f"{version_name} Overall Quality", score_data.get("Overall Quality", "")])
        writer.writerow([])

    return output.getvalue()


def render_text_block(text: str):
    safe_text = html.escape(text)
    st.markdown(
        f'<div class="text-block"><pre>{safe_text}</pre></div>',
        unsafe_allow_html=True
    )


def render_prompt_version_block(text: str):
    safe_text = html.escape(text)

    # Add a little visual spacing for common prompt patterns
    safe_text = safe_text.replace(". ", ".\n\n")
    safe_text = safe_text.replace(": ", ":\n")
    safe_text = safe_text.replace("1. ", "\n1. ")
    safe_text = safe_text.replace("2. ", "\n2. ")
    safe_text = safe_text.replace("3. ", "\n3. ")
    safe_text = safe_text.replace("4. ", "\n4. ")
    safe_text = safe_text.replace("5. ", "\n5. ")
    safe_text = safe_text.replace("- ", "\n- ")

    st.markdown(
        f'<div class="text-block prompt-version-block"><pre>{safe_text}</pre></div>',
        unsafe_allow_html=True
    )

defaults = {
    "user_prompt": "",
    "category": "General",
    "optimized_text": "",
    "prompt_versions": [],
    "test_outputs": [],
    "scores": "",
    "parsed_scores": {},
    "best_version": "",
    "best_reason": "",
    "history": []
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

with st.sidebar:
    st.markdown("## PromptLab")
    st.caption("Prompt testing workspace")

    st.markdown("### Workflow")
    st.markdown("""
1. Pick a category  
2. Enter your prompt  
3. Optimize it  
4. Run test + score  
5. Download results  
""")

    if st.button("Clear History", use_container_width=True):
        clear_history()
        st.rerun()

    st.markdown("### Prompt History")
    if st.session_state.history:
        for item in st.session_state.history:
            with st.expander(f"{item['timestamp']} · {item['category']}", expanded=False):
                st.write(f"**Prompt:** {item['prompt']}")
                st.write(f"**Best Version:** {item['best_version']}")
                st.write(f"**Reason:** {item['best_reason']}")
    else:
        st.caption("No history yet.")

st.markdown("""
<div class="hero">
    <div class="hero-title">PromptLab 🧪</div>
    <div class="hero-subtitle">
        A polished AI workspace for prompt optimization, output comparison, scoring, and exportable evaluation results.
    </div>
    <div class="hero-badges">
        <div class="hero-badge">Prompt Optimization</div>
        <div class="hero-badge">A/B/C Testing</div>
        <div class="hero-badge">Output Scoring</div>
        <div class="hero-badge">Exportable Results</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="small-muted">Workspace</div>', unsafe_allow_html=True)
st.subheader("Create and refine your prompt")

left_col, right_col = st.columns([2, 1])

category_options = [
    "General",
    "Blog Writing",
    "Customer Support",
    "Marketing",
    "Technical Troubleshooting",
    "Data Analysis"
]

with left_col:
    selected_category = st.selectbox(
        "Choose a prompt category",
        category_options,
        index=category_options.index(st.session_state.category)
    )
    st.session_state.category = selected_category

with right_col:
    st.caption("Choose the task type before optimization.")

entered_prompt = st.text_area(
    "Enter your prompt",
    value=st.session_state.user_prompt,
    height=150,
    placeholder="Example: Write a professional customer support reply for a delayed shipment."
)
st.session_state.user_prompt = entered_prompt

button_col1, button_col2 = st.columns(2)
with button_col1:
    optimize_clicked = st.button("✨ Optimize Prompt", use_container_width=True)
with button_col2:
    new_prompt_clicked = st.button("🧹 Start New", use_container_width=True)

if new_prompt_clicked:
    reset_app()
    st.rerun()

if optimize_clicked:
    if not api_key:
        st.error("OpenAI API key not found. Please check your .env file.")
    elif not st.session_state.user_prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        try:
            with st.spinner("Optimizing prompt..."):
                optimized_text, versions = generate_optimized_prompts(
                    st.session_state.user_prompt,
                    st.session_state.category
                )
                st.session_state.optimized_text = optimized_text
                st.session_state.prompt_versions = versions
                st.session_state.test_outputs = []
                st.session_state.scores = ""
                st.session_state.parsed_scores = {}
                st.session_state.best_version = ""
                st.session_state.best_reason = ""
        except Exception as error:
            error_text = str(error)
            if "insufficient_quota" in error_text or "429" in error_text:
                st.error("Your OpenAI API account does not currently have available quota or billing set up. Check your OpenAI billing settings and then try again.")
            else:
                st.error(f"Something went wrong: {error_text}")

if st.session_state.optimized_text:
    st.markdown("## Optimized Prompts")

    prompt_col1, prompt_col2, prompt_col3 = st.columns(3)

    with prompt_col1:
        st.markdown(
            '<div class="card-wrap"><div class="card-header">Version 1</div><div class="card-body">',
            unsafe_allow_html=True
        )
        render_prompt_version_block(st.session_state.prompt_versions[0])
        st.markdown("**Copy Prompt**")
        st.code(
            st.session_state.prompt_versions[0],
            language="text",
        )
        st.markdown('</div></div>', unsafe_allow_html=True)

    with prompt_col2:
        st.markdown(
            '<div class="card-wrap"><div class="card-header">Version 2</div><div class="card-body">',
            unsafe_allow_html=True
        )
        render_prompt_version_block(st.session_state.prompt_versions[1])
        st.markdown("**Copy Prompt**")
        st.code(
            st.session_state.prompt_versions[1],
            language="text",
        )
        st.markdown('</div></div>', unsafe_allow_html=True)

    with prompt_col3:
        st.markdown(
            '<div class="card-wrap"><div class="card-header">Version 3</div><div class="card-body">',
            unsafe_allow_html=True
        )
        render_prompt_version_block(st.session_state.prompt_versions[2])
        st.markdown("**Copy Prompt**")
        st.code(
            st.session_state.prompt_versions[2],
            language="text",
        )
        st.markdown('</div></div>', unsafe_allow_html=True)

    if len(st.session_state.prompt_versions) == 3:
        if st.button("🚀 Run Test + Score", use_container_width=True):
            try:
                with st.spinner("Running prompt test and scoring outputs..."):
                    outputs = [run_prompt_test(version_prompt) for version_prompt in st.session_state.prompt_versions]
                    st.session_state.test_outputs = outputs

                    score_text = score_outputs(
                        st.session_state.user_prompt,
                        st.session_state.test_outputs[0],
                        st.session_state.test_outputs[1],
                        st.session_state.test_outputs[2]
                    )
                    st.session_state.scores = score_text
                    parsed_scores, best_version, best_reason = parse_score_text(score_text)
                    st.session_state.parsed_scores = parsed_scores
                    st.session_state.best_version = best_version
                    st.session_state.best_reason = best_reason
                    add_to_history()
            except Exception as error:
                st.error(f"Prompt test failed: {error}")

if st.session_state.test_outputs:
    st.markdown("## Prompt Test Results")

    cols = st.columns(3)
    version_names = ["Version 1", "Version 2", "Version 3"]

    for i, col in enumerate(cols):
        version_name = version_names[i]
        output_text = st.session_state.test_outputs[i]
        score_data = st.session_state.parsed_scores.get(version_name, {})

        with col:
            header_class = "card-header best" if st.session_state.best_version == version_name else "card-header"
            header_text = f"🏆 Best Version · {version_name}" if st.session_state.best_version == version_name else version_name

            st.markdown(f'<div class="card-wrap"><div class="{header_class}">{header_text}</div><div class="card-body">', unsafe_allow_html=True)

            st.markdown("**Output**")
            render_text_block(output_text)

            if score_data:
                st.markdown("**Scores**")
                st.markdown(
                    f"""
                    <span class="score-chip">Clarity: {score_data.get('Clarity', 'N/A')}</span>
                    <span class="score-chip">Completeness: {score_data.get('Completeness', 'N/A')}</span>
                    <span class="score-chip">Professionalism: {score_data.get('Professionalism', 'N/A')}</span>
                    <span class="score-chip">Overall: {score_data.get('Overall Quality', 'N/A')}</span>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown('</div></div>', unsafe_allow_html=True)

if st.session_state.best_version:
    st.markdown("## Best Result Summary")
    st.markdown(f"""
    <div class="card-wrap">
        <div class="card-header best">Best Result Summary</div>
        <div class="card-body">
    """, unsafe_allow_html=True)
    st.write(f"**Best Version:** {st.session_state.best_version}")
    if st.session_state.best_reason:
        st.write(f"**Reason:** {st.session_state.best_reason}")
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("## Download Results")
    download_col1, download_col2 = st.columns(2)

    json_data = build_json_export()
    csv_data = build_csv_export()

    with download_col1:
        st.download_button(
            label="⬇ Download JSON",
            data=json_data,
            file_name="promptlab_results.json",
            mime="application/json",
            use_container_width=True
        )

    with download_col2:
        st.download_button(
            label="⬇ Download CSV",
            data=csv_data,
            file_name="promptlab_results.csv",
            mime="text/csv",
            use_container_width=True
        )