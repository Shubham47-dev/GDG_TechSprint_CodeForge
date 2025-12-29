# visuals.py
import plotly.graph_objects as go
import streamlit as st

def plot_gauge(score):
    """
    Creates a speedometer style gauge chart for the resume score.
    Input: score (0-100)
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Resume Match Score"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps' : [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "green"}
            ],
        }
    ))
    
    # Make it look clean # 
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    
    # Display it in Streamlit
    st.plotly_chart(fig, use_container_width=True)