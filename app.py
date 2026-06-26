import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sentiment_model import analyze_sentiment, get_sentence_sentiments

# Page config 
st.set_page_config(
    page_title="Text Sentiment Analyzer",
    page_icon="🧠",
    layout="wide",
)

# Custom CSS 
st.markdown(
    """
    <style>
    .main { background-color: #0F1117; }
    .result-card {
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        margin: 12px 0;
    }
    .sentence-row {
        padding: 10px 16px;
        border-radius: 10px;
        margin: 6px 0;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header 
st.markdown("## 🧠 Text Sentiment Analyzer")
st.markdown("Analyze the emotional tone of any text using **TextBlob NLP**.")
st.divider()

# Session state init
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

# Clear buttons (BEFORE text_area so value is set first) 
col_input, col_result = st.columns([3, 2], gap="large")

with col_input:
    st.markdown("#### 💡 Try an example:")
    examples = {
        "😊 Positive": "I absolutely loved this product! It exceeded all my expectations and the customer service was outstanding.",
        "😞 Negative": "This was a terrible experience. The product broke within a week and support was completely unhelpful.",
        "😐 Neutral":  "The package arrived on Tuesday. It contained the items listed on the website.",
    }
    ex_cols = st.columns(3)
    for i, (label, ex_text) in enumerate(examples.items()):
        with ex_cols[i]:
            if st.button(label, use_container_width=True):
                st.session_state["input_text"] = ex_text
                st.rerun()

    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state["input_text"] = ""
        st.rerun()

    # Text area uses value= (not key=) to avoid the session_state conflict 
    st.markdown("#### ✍️ Enter your text")
    text_input = st.text_area(
        label="",
        placeholder="Type or paste any text here — a review, tweet, feedback, paragraph...",
        height=200,
        value=st.session_state["input_text"],
    )

    analyze_btn = st.button("🔍 Analyze Sentiment", use_container_width=True, type="primary")

# Analysis 
if analyze_btn and text_input.strip():
    result = analyze_sentiment(text_input)
    sentence_results = get_sentence_sentiments(text_input)

    with col_result:
        st.markdown("#### 📊 Overall Result")

        bg = result["color"] + "22"
        border = result["color"]
        st.markdown(
            f"""
            <div class="result-card" style="background:{bg}; border: 2px solid {border};">
                <div style="font-size:52px">{result['emoji']}</div>
                <div style="font-size:32px; font-weight:800; color:{border}">
                    {result['sentiment']}
                </div>
                <div style="color:#ccc; font-size:13px; margin-top:6px;">
                    {result['word_count']} words analyzed
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Polarity gauge
        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=result["polarity"],
                number={"font": {"size": 28, "color": "white"}},
                gauge={
                    "axis": {"range": [-1, 1], "tickcolor": "#aaa"},
                    "bar": {"color": result["color"]},
                    "bgcolor": "#1E1E2E",
                    "steps": [
                        {"range": [-1, -0.05], "color": "#3B1A1A"},
                        {"range": [-0.05, 0.05], "color": "#2A2A1A"},
                        {"range": [0.05, 1],    "color": "#1A3B1A"},
                    ],
                },
                title={"text": "Polarity Score", "font": {"color": "#ccc", "size": 14}},
            )
        )
        fig_gauge.update_layout(
            height=220,
            margin=dict(t=40, b=0, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        subj = result["subjectivity"]
        subj_label = "Very Objective" if subj < 0.3 else ("Mixed" if subj < 0.6 else "Very Subjective")
        st.markdown(f"**Subjectivity:** {subj:.2f} — *{subj_label}*")
        st.progress(subj)

    # Sentence breakdown
    if len(sentence_results) > 1:
        st.divider()
        st.markdown("#### 🔬 Sentence-by-Sentence Breakdown")

        sent_df_data = []
        for sr in sentence_results:
            bg_color = sr["color"] + "33"
            st.markdown(
                f"""
                <div class="sentence-row" style="background:{bg_color}; border-left: 4px solid {sr['color']};">
                    {sr['emoji']} &nbsp; <b>{sr['sentiment']}</b> &nbsp;
                    <span style="color:#aaa">(polarity: {sr['polarity']})</span><br/>
                    <span style="color:#ddd">{sr['sentence']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            sent_df_data.append({
                "Sentence": sr["sentence"],
                "Sentiment": sr["sentiment"],
                "Polarity": sr["polarity"],
                "Subjectivity": sr["subjectivity"],
            })

        if len(sent_df_data) > 1:
            df_sent = pd.DataFrame(sent_df_data)
            colors = [
                "#2ECC71" if p > 0.05 else ("#E74C3C" if p < -0.05 else "#F39C12")
                for p in df_sent["Polarity"]
            ]
            fig_bar = go.Figure(
                go.Bar(
                    x=[f"S{i+1}" for i in range(len(df_sent))],
                    y=df_sent["Polarity"],
                    marker_color=colors,
                    text=df_sent["Polarity"],
                    textposition="outside",
                )
            )
            fig_bar.update_layout(
                title="Polarity per Sentence",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                height=280,
                margin=dict(t=40, b=20, l=20, r=20),
                yaxis=dict(range=[-1.1, 1.1], gridcolor="#333"),
                xaxis=dict(gridcolor="#333"),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

elif analyze_btn and not text_input.strip():
    with col_result:
        st.warning("⚠️ Please enter some text before analyzing.")
else:
    with col_result:
        st.info("👈 Enter text on the left and click **Analyze Sentiment**.")

# Footer
st.divider()
st.markdown(
    "<p style='text-align:center; color:#555; font-size:12px;'>"
    "Understanding Emotions Through AI"
    "</p>",
    unsafe_allow_html=True,
)