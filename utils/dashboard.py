"""
Analytics Dashboard Module

This module uses Plotly to render beautiful, responsive, and professional
charts for the Premium AI Resume Analyzer.
"""
import plotly.graph_objects as go
import streamlit as st
from typing import Dict, List

# Define global theme colors to ensure consistency (White background, no dark mode)
THEME = {
    "bg_color": "#ffffff",
    "font_color": "#333333",
    "grid_color": "#e9ecef",
    "primary": "#4CAF50",
    "warning": "#ff9800",
    "danger": "#f44336"
}

def display_ats_gauge(score: int):
    """
    Renders an ATS Score gauge chart.
    0-40 Red, 40-70 Orange, 70-100 Green.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>ATS Compatibility Score</b>", 'font': {'size': 18, 'color': THEME["font_color"]}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': THEME["font_color"]},
            'bar': {'color': "#ffffff", 'thickness': 0.15},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': THEME["grid_color"],
            'steps': [
                {'range': [0, 40], 'color': THEME["danger"]},
                {'range': [40, 70], 'color': THEME["warning"]},
                {'range': [70, 100], 'color': THEME["primary"]}],
            'threshold': {
                'line': {'color': "#212529", 'width': 4},
                'thickness': 0.75,
                'value': score}
        }
    ))
    fig.update_layout(
        paper_bgcolor=THEME["bg_color"],
        font={'color': THEME["font_color"], 'family': "Arial"},
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

def display_section_chart(sections: Dict[str, bool]):
    """
    Renders a Donut Chart showing Present vs Missing sections.
    """
    present_count = sum(1 for v in sections.values() if v)
    missing_count = len(sections) - present_count
    
    labels = ['Present Sections', 'Missing Sections']
    values = [present_count, missing_count]
    colors = [THEME["primary"], THEME["danger"]]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    fig.update_traces(
        hoverinfo='label+percent', 
        textinfo='value', 
        textfont_size=16,
        marker=dict(colors=colors, line=dict(color=THEME["bg_color"], width=2))
    )
    fig.update_layout(
        title={'text': "<b>Resume Sections</b>", 'x': 0.5, 'xanchor': 'center'},
        paper_bgcolor=THEME["bg_color"],
        font={'color': THEME["font_color"]},
        margin=dict(l=20, r=20, t=40, b=20),
        height=300,
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

def display_skills_chart(skills: str):
    """
    Renders a Horizontal Bar Chart for the Top 10 skills.
    """
    if not skills or skills == "Not Found":
        st.info("No skills extracted to display.")
        return
        
    skill_list = [s.strip() for s in skills.split(',')]
    top_skills = skill_list[:10]
    top_skills.reverse()
    
    # Assign descending arbitrary score for visual horizontal stack
    scores = list(range(len(top_skills), 0, -1))
    
    fig = go.Figure(go.Bar(
        x=scores,
        y=top_skills,
        orientation='h',
        marker_color=THEME["primary"],
        marker_line_color=THEME["font_color"],
        marker_line_width=1,
        opacity=0.8
    ))
    
    fig.update_layout(
        title={'text': "<b>Top 10 Detected Skills</b>", 'x': 0.5, 'xanchor': 'center'},
        xaxis_title="Relevance",
        yaxis_title="Skills",
        paper_bgcolor=THEME["bg_color"],
        plot_bgcolor=THEME["bg_color"],
        font={'color': THEME["font_color"]},
        margin=dict(l=20, r=20, t=40, b=20),
        height=350,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid_color"], showticklabels=False)
    )
    st.plotly_chart(fig, use_container_width=True)

def display_missing_skills(missing: List[str]):
    """
    Renders a Bar Chart for missing skills in Red Color.
    """
    if not missing:
        st.success("No missing key skills!")
        return
        
    top_missing = missing[:10]
    top_missing.reverse()
    scores = list(range(len(top_missing), 0, -1))
    
    fig = go.Figure(go.Bar(
        x=scores,
        y=top_missing,
        orientation='h',
        marker_color=THEME["danger"],
        marker_line_color=THEME["font_color"],
        marker_line_width=1,
        opacity=0.8
    ))
    
    fig.update_layout(
        title={'text': "<b>Missing Industry Skills</b>", 'x': 0.5, 'xanchor': 'center'},
        xaxis_title="Priority",
        yaxis_title="Skills",
        paper_bgcolor=THEME["bg_color"],
        plot_bgcolor=THEME["bg_color"],
        font={'color': THEME["font_color"]},
        margin=dict(l=20, r=20, t=40, b=20),
        height=350,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid_color"], showticklabels=False)
    )
    st.plotly_chart(fig, use_container_width=True)

def display_match_score(match_score: int):
    """
    Renders a Circular Progress Gauge for JD match score.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=match_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>JD Match Percentage</b>", 'font': {'size': 18, 'color': THEME["font_color"]}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': THEME["font_color"]},
            'bar': {'color': THEME["primary"], 'thickness': 0.25},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': THEME["grid_color"]
        }
    ))
    fig.update_layout(
        paper_bgcolor=THEME["bg_color"],
        font={'color': THEME["font_color"], 'family': "Arial"},
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

def display_summary_cards(ats_score: int, match_score: int, skills_found_count: int, missing_skills_count: int, has_projects: bool, has_experience: bool):
    """
    Displays professional KPI Cards using Streamlit columns and custom HTML/CSS.
    """
    st.markdown("""
        <style>
        .kpi-card {
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            text-align: center;
            margin-bottom: 20px;
        }
        .kpi-card h4 {
            margin: 0;
            color: #6c757d;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .kpi-card h2 {
            margin: 10px 0 0 0;
            color: #333333;
            font-size: 32px;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>ATS Score</h4>
            <h2>{ats_score}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>JD Match</h4>
            <h2>{match_score}%</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>Skills Found</h4>
            <h2>{skills_found_count}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>Skills Missing</h4>
            <h2 style="color: #f44336;">{missing_skills_count}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col5:
        p_color = "#4CAF50" if has_projects else "#f44336"
        p_text = "Yes" if has_projects else "No"
        st.markdown(f"""
        <div class="kpi-card">
            <h4>Projects</h4>
            <h2 style="color: {p_color};">{p_text}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col6:
        e_color = "#4CAF50" if has_experience else "#f44336"
        e_text = "Yes" if has_experience else "No"
        st.markdown(f"""
        <div class="kpi-card">
            <h4>Experience</h4>
            <h2 style="color: {e_color};">{e_text}</h2>
        </div>
        """, unsafe_allow_html=True)
