import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

def plot_gauge(score):
    """
    Creates a speedometer-style gauge chart using Plotly.
    Input: Integer score (0-100)
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "", 'font': {'size': 24,}}, # White Title
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"}, # White ticks
            'bar': {'color': "#8b5cf6"}, # Your Theme Purple
            'bgcolor': "#1f2937", # Dark Gray background for the empty part of gauge
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [0, 50], 'color': "#360100"},  # Deep Red
                {'range': [50, 75], 'color': "#454502"}, # Deep Yellow
                {'range': [75, 100], 'color': "#064e3b"} # Deep Green
            ],
        }
    ))
    
    # Resize and make background TRANSPARENT to match the black app
    fig.update_layout(
        paper_bgcolor = "rgba(0,0,0,0)", # Transparent background
        plot_bgcolor = "rgba(0,0,0,0)",  # Transparent plot area
        font = {'color': "white", 'family': "Arial"}, # All text white
        width=300, 
        height=250, 
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_keyword_bar(found_count, missing_count):

    labels = ['Found Skills', 'Missing Skills']
    values = [found_count, missing_count]
    colors = ["#035606", "#740505"] 
    
    fig, ax = plt.subplots(figsize=(4, 3))
    bars = ax.bar(labels, values, color=colors, edgecolor='black', alpha=0.7)

    ax.tick_params(axis='x', colors="#e8f7f7ff", labelsize=8)
    
    ax.bar_label(bars,color = "#e8f7f7ff",fontsize = 10, padding=3)
    ax.set_facecolor("#000000ff")
    fig.set_facecolor("#000000ff")
    

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_yticks([]) 
   
    st.pyplot(fig, width='stretch')