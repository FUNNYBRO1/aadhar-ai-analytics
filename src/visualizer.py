# src/visualizer.py

import streamlit as st
import matplotlib.pyplot as plt

def generate_graph(df, graph_type, title):
    # ---------- FIG SETUP ----------
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("#0b0f19")   # dark bg
    ax.set_facecolor("#0b0f19")

    x = df.iloc[:, 0].astype(str)
    y = df.iloc[:, 1]

    # ---------- BAR GRAPH ----------
    if graph_type == "bar":
        bars = ax.bar(
            x,
            y,
            color="#4f7cff",     # primary blue
            edgecolor="#9b5cff",
            linewidth=0.6
        )

        # value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{int(height):,}",
                ha="center",
                va="bottom",
                fontsize=9,
                color="#e5e7eb"
            )

    # ---------- TITLE ----------
    ax.set_title(
        title,
        fontsize=14,
        color="#e5e7eb",
        pad=15
    )

    # ---------- AXIS STYLING ----------
    ax.tick_params(axis="x", colors="#9ca3af", rotation=45)
    ax.tick_params(axis="y", colors="#9ca3af")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(
        axis="y",
        linestyle="--",
        linewidth=0.4,
        alpha=0.3
    )

    plt.tight_layout()

    # ---------- STREAMLIT RENDER ----------
    st.pyplot(fig, use_container_width=True)
