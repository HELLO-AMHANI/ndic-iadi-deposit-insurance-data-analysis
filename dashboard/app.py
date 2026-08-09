# =============================================================
# NDIC + IADI DEPOSIT INSURANCE ANALYSIS — DASHBOARD
# Author: Promise O. Amhanesi
# =============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="NDIC + IADI Analysis",
    page_icon="🏦",
    layout="wide"
)

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df   = pd.read_csv('dataclean/model_dataset.csv')
    iadi = pd.read_csv('dataclean/iadi_survey.csv')
    return df, iadi

df, iadi = load_data()

# ── Header ────────────────────────────────────────────────────
st.title("🏦 NDIC + IADI Deposit Insurance Analysis")
st.markdown(
    "**Research question:** How does NDIC's fund adequacy, coverage ratio, "
    "and premium system compare against IADI Core Principles and peer member DICs?"
)
st.markdown("---")

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.header("Controls")

yr = st.sidebar.slider(
    "Select Year", min_value=2010, max_value=2024, value=2020, step=1
)

metric_options = {
    "Fund Adequacy Ratio"  : "local_fund_adequacy_ratio",
    "Claims Intensity"     : "claims_intensity",
    "Coverage Ratio"       : "coverage_ratio",
    "NPL Ratio (%)"        : "npl_ratio_pct",
    "CAR (%)"              : "car_pct",
    "ROA (%)"              : "roa_pct",
    "Liquidity Ratio (%)"  : "liquidity_ratio_pct",
}
selected_label  = st.sidebar.selectbox("Select Metric", list(metric_options.keys()))
selected_metric = metric_options[selected_label]

show_iadi = st.sidebar.toggle("Show IADI Benchmark Panel", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**Author:** Promise O. Amhanesi")
st.sidebar.markdown("**Data:** NDIC Annual Reports 2010–2024 · IADI Annual Survey · World Bank")

# ── Row 1: KPI cards ──────────────────────────────────────────
row_data = df[df['year'] == yr]

if row_data.empty:
    st.warning(f"No data found for year {yr}.")
    st.stop()

row = row_data.iloc[0]
iadi_yr_avg = iadi[iadi['year'] == yr]['fund_adequacy_ratio'].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Fund Adequacy Ratio (Local)",
    f"{row['local_fund_adequacy_ratio']:.4f}",
    delta=f"IADI avg: {iadi_yr_avg:.4f}"
)
col2.metric(
    "Claims Intensity",
    f"{row['claims_intensity']:.4f}",
    delta="Low = good"
)
col3.metric(
    "Coverage Ratio",
    f"{row['coverage_ratio']:.4f}",
    delta="Coverage / GDP per capita"
)
col4.metric(
    "NPL Ratio (%)",
    f"{row['npl_ratio_pct']:.2f}%",
    delta="Lower = healthier"
)
col5.metric(
    "CAR (%)",
    f"{row['car_pct']:.2f}%",
    delta="Min IADI: 10%"
)

st.markdown("---")

# ── Row 2: Time-series + benchmark bar ───────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📈 Fund Balance & Claims Paid Over Time")
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(
        x=df['year'], y=df['fund_balance_bn'],
        mode='lines+markers', name='Fund Balance (₦bn)',
        line=dict(color='#1D9E75', width=3), marker=dict(size=7)
    ))
    fig_ts.add_trace(go.Scatter(
        x=df['year'], y=df['claims_paid_bn'],
        mode='lines+markers', name='Claims Paid (₦bn)',
        line=dict(color='#C0392B', width=2, dash='dot'), marker=dict(size=7)
    ))
    fig_ts.add_vline(x=yr, line_dash='dash', line_color='orange',
                     annotation_text=f"Selected: {yr}")
    for stress_yr in [2016, 2020]:
        fig_ts.add_vline(x=stress_yr, line_dash='dot',
                         line_color='grey', line_width=1)
    fig_ts.update_layout(
        height=380, template='plotly_white',
        legend=dict(x=0.01, y=0.99),
        margin=dict(t=20, b=30),
        hovermode='x unified'
    )
    st.plotly_chart(fig_ts, use_container_width=True)

with col_right:
    st.subheader(f"📊 {selected_label} — Trend")
    fig_metric = px.bar(
        df, x='year', y=selected_metric,
        color=selected_metric,
        color_continuous_scale='RdYlGn',
        title=None
    )
    fig_metric.add_vline(x=yr, line_dash='dash', line_color='orange')
    fig_metric.update_layout(
        height=380, template='plotly_white',
        margin=dict(t=20, b=30),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_metric, use_container_width=True)

st.markdown("---")

# ── Row 3: IADI Benchmark Panel ──────────────────────────────
if show_iadi:
    st.subheader("🌍 IADI Benchmark Panel")
    col_iadi1, col_iadi2 = st.columns(2)

    with col_iadi1:
        # NDIC vs IADI average FAR trend
        iadi_avg_yr = iadi.groupby('year')['fund_adequacy_ratio'].mean().reset_index()
        iadi_avg_yr.columns = ['year','iadi_avg_far']
        merged_far = df[['year','local_fund_adequacy_ratio',
                          'fund_adequacy_ratio']].merge(iadi_avg_yr, on='year')

        fig_far = go.Figure()
        fig_far.add_trace(go.Scatter(
            x=merged_far['year'], y=merged_far['local_fund_adequacy_ratio'],
            mode='lines+markers', name='NDIC Local FAR',
            line=dict(color='#1D9E75', width=3)
        ))
        fig_far.add_trace(go.Scatter(
            x=merged_far['year'], y=merged_far['fund_adequacy_ratio'],
            mode='lines+markers', name='IADI-Reported FAR (Nigeria)',
            line=dict(color='#E67E22', width=2, dash='dash')
        ))
        fig_far.add_trace(go.Scatter(
            x=merged_far['year'], y=merged_far['iadi_avg_far'],
            mode='lines+markers', name='IADI Peer Average',
            line=dict(color='#2980B9', width=2, dash='dot')
        ))
        fig_far.update_layout(
            title='Fund Adequacy Ratio: NDIC vs IADI',
            height=360, template='plotly_white',
            legend=dict(x=0.01, y=0.99),
            hovermode='x unified', margin=dict(t=40, b=30)
        )
        st.plotly_chart(fig_far, use_container_width=True)

    with col_iadi2:
        # Country comparison bar for selected year and selected metric
        iadi_yr = iadi[iadi['year'] == yr].copy()
        iadi_yr['is_nigeria'] = iadi_yr['country'].apply(
            lambda x: '★ Nigeria' if x == 'Nigeria' else x
        )
        iadi_yr_sorted = iadi_yr.sort_values('fund_adequacy_ratio', ascending=True)
        colors_bar = [
            '#F39C12' if c == 'Nigeria' else '#7F8C8D'
            for c in iadi_yr_sorted['country']
        ]
        fig_peer = go.Figure(go.Bar(
            x=iadi_yr_sorted['fund_adequacy_ratio'],
            y=iadi_yr_sorted['country'],
            orientation='h',
            marker_color=colors_bar,
            text=[f"{v:.4f}" for v in iadi_yr_sorted['fund_adequacy_ratio']],
            textposition='outside'
        ))
        fig_peer.update_layout(
            title=f'Fund Adequacy Ratio — All IADI Members ({yr})',
            height=360, template='plotly_white',
            margin=dict(t=40, b=30, r=80)
        )
        st.plotly_chart(fig_peer, use_container_width=True)

    st.markdown("---")

# ── Row 4: Full data table ───────────────────────────────────
with st.expander("📋 View full model dataset"):
    display_cols = [
        'year','fund_balance_bn','insured_deposits_bn','claims_paid_bn',
        'local_fund_adequacy_ratio','fund_adequacy_ratio',
        'iadi_avg_fund_adequacy','coverage_ratio',
        'npl_ratio_pct','car_pct','roa_pct',
        'gdp_growth','inflation','exchange_rate'
    ]
    available = [c for c in display_cols if c in df.columns]
    st.dataframe(df[available].set_index('year').style.format("{:.4f}"),
                 use_container_width=True)

st.markdown("---")
st.caption(
    "Data: NDIC Annual Reports 2010–2024 · IADI Annual Survey · "
    "World Bank GFDD · CBN Statistical Bulletin | "
    "Author: Promise O. Amhanesi | "
    "Repo: github.com/HELLO-AMHANI/ndic-iadi-deposit-insurance-analysis"
)
