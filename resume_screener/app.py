import streamlit as st
from screener import ResumeScreener
from visualizer import plot_match_scores, plot_skill_gap

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🔍",
    layout="wide"
)

# ── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: #1e2130;
        border-radius: 10px;
        padding: 16px 20px;
        border-left: 4px solid #4f8ef7;
    }
    .score-high  { color: #22c55e; font-size: 2rem; font-weight: 700; }
    .score-mid   { color: #f59e0b; font-size: 2rem; font-weight: 700; }
    .score-low   { color: #ef4444; font-size: 2rem; font-weight: 700; }
    .tag {
        display: inline-block;
        background: #2d3a5e;
        color: #93b4ff;
        border-radius: 20px;
        padding: 2px 12px;
        margin: 3px;
        font-size: 0.8rem;
    }
    .tag-miss {
        background: #3b1f1f;
        color: #f87171;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🔍 AI Resume Screener")
st.caption("Paste a job description and one or more resumes to get instant match scores, skill gap analysis, and candidate rankings.")
st.divider()

# ── Inputs ───────────────────────────────────────────────────────────────────
col_jd, col_res = st.columns([1, 1], gap="large")

with col_jd:
    st.subheader("Job Description")
    job_desc = st.text_area(
        "Paste the full job description here",
        height=280,
        placeholder="e.g. We are looking for a Python developer with experience in Django, REST APIs, SQL, and Docker..."
    )

with col_res:
    st.subheader("Candidate Resumes")
    num_candidates = st.number_input("Number of candidates", min_value=1, max_value=8, value=2, step=1)
    resumes = {}
    for i in range(int(num_candidates)):
        name = st.text_input(f"Candidate {i+1} name", value=f"Candidate {i+1}", key=f"name_{i}")
        text = st.text_area(f"Resume text for {name}", height=100, key=f"resume_{i}",
                            placeholder="Paste resume text here...")
        if text.strip():
            resumes[name] = text

# ── Run ───────────────────────────────────────────────────────────────────────
if st.button("⚡ Screen Candidates", use_container_width=True, type="primary"):
    if not job_desc.strip():
        st.warning("Please enter a job description.")
    elif not resumes:
        st.warning("Please enter at least one resume.")
    else:
        with st.spinner("Analyzing resumes..."):
            screener = ResumeScreener()
            results  = screener.screen_all(job_desc, resumes)

        st.divider()
        st.subheader("📊 Results")

        # ── Rankings ─────────────────────────────────────────────────────────
        st.markdown("#### Candidate Rankings")
        ranked = sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)

        cols = st.columns(len(ranked))
        for idx, (col, (name, data)) in enumerate(zip(cols, ranked)):
            score = data["score"]
            score_class = "score-high" if score >= 70 else ("score-mid" if score >= 45 else "score-low")
            medal = ["🥇", "🥈", "🥉"] + [""] * 10
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size:0.85rem;color:#9ca3af;">#{idx+1} {medal[idx]}</div>
                    <div style="font-weight:600;font-size:1rem;margin:4px 0;">{name}</div>
                    <div class="{score_class}">{score}%</div>
                    <div style="font-size:0.75rem;color:#6b7280;margin-top:4px;">Match Score</div>
                </div>
                """, unsafe_allow_html=True)

        st.write("")

        # ── Charts ───────────────────────────────────────────────────────────
        ch1, ch2 = st.columns(2)
        with ch1:
            fig_bar = plot_match_scores(ranked)
            st.plotly_chart(fig_bar, use_container_width=True)
        with ch2:
            top_name, top_data = ranked[0]
            fig_gap = plot_skill_gap(top_name, top_data)
            st.plotly_chart(fig_gap, use_container_width=True)

        # ── Per-candidate detail ──────────────────────────────────────────────
        st.markdown("#### Detailed Breakdown")
        for name, data in ranked:
            with st.expander(f"**{name}** — {data['score']}% match"):
                d1, d2 = st.columns(2)
                with d1:
                    st.markdown("**✅ Matched Skills**")
                    if data["matched"]:
                        tags = " ".join(f'<span class="tag">{s}</span>' for s in data["matched"])
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.caption("No skills matched.")
                with d2:
                    st.markdown("**❌ Missing Skills**")
                    if data["missing"]:
                        tags = " ".join(f'<span class="tag tag-miss">{s}</span>' for s in data["missing"])
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.caption("No skill gaps found.")

                st.write("")
                st.markdown(f"**📝 Summary**")
                st.info(data["summary"])
