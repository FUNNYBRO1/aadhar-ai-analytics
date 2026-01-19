# src/visualizer.py

import streamlit as st
import matplotlib.pyplot as plt

def generate_graph(df, graph_type, title):
    fig, ax = plt.subplots()

    x = df.iloc[:, 0]
    y = df.iloc[:, 1]

    if graph_type == "bar":
        ax.bar(x, y)

    ax.set_title(title)
    ax.set_xticklabels(x, rotation=45, ha="right")

    st.pyplot(fig)
