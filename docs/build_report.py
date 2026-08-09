# BUILD REPORT — report.pdf
# NDIC + IADI Deposit Insurance Analysis
# Author: Promise O. Amhanesi

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import pandas as pd
import os

OUTPUT = 'docs/report.pdf'
FIGS   = 'resultsfigs'
doc    = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=2.2*cm, leftMargin=2.2*cm,
    topMargin=2.2*cm, bottomMargin=2.2*cm
)

# Styles 
styles = getSampleStyleSheet()

DARK_BLUE = colors.HexColor('#1B3A6B')
MID_BLUE  = colors.HexColor('#2E6BAD')
GREEN     = colors.HexColor('#1D9E75')
LIGHT_BG  = colors.HexColor('#F2F5F9')

title_style = ParagraphStyle('Title', parent=styles['Title'],
    fontSize=22, textColor=DARK_BLUE, leading=28,
    spaceAfter=8, alignment=TA_CENTER)

subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
    fontSize=12, textColor=MID_BLUE, leading=16,
    spaceAfter=6, alignment=TA_CENTER)

h1_style = ParagraphStyle('H1', parent=styles['Heading1'],
    fontSize=15, textColor=DARK_BLUE, leading=20,
    spaceBefore=18, spaceAfter=6,
    borderPad=4)

h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
    fontSize=12, textColor=MID_BLUE, leading=16,
    spaceBefore=12, spaceAfter=4)

body_style = ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=10.5, leading=16, spaceAfter=8, alignment=TA_JUSTIFY)

caption_style = ParagraphStyle('Caption', parent=styles['Normal'],
    fontSize=9, textColor=colors.grey, leading=13,
    spaceAfter=12, alignment=TA_CENTER, italics=1)

bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'],
    fontSize=10.5, leading=15, spaceAfter=4,
    leftIndent=14, firstLineIndent=-14)

def h(text, style=h1_style):
    return Paragraph(text, style)

def p(text, style=body_style):
    return Paragraph(text, style)

def sp(n=1):
    return Spacer(1, n * 0.3 * cm)

def hr():
    return HRFlowable(width='100%', thickness=0.8,
                      color=MID_BLUE, spaceAfter=6, spaceBefore=6)

def fig(fname, w=14, caption=''):
    path = os.path.join(FIGS, fname)
    elems = []
    if os.path.exists(path):
        elems.append(Image(path, width=w*cm, height=w*0.55*cm))
        if caption:
            elems.append(Paragraph(caption, caption_style))
    else:
        elems.append(p(f'[Chart not found: {fname}]', caption_style))
    return elems

def table_style_base(data, col_widths=None):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_BG, colors.white]),
        ('GRID',       (0,0), (-1,-1), 0.4, colors.HexColor('#BBCDE0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

# Load data for tables 
df       = pd.read_csv('dataclean/model_dataset.csv')
metrics  = pd.read_csv('results/model_metrics.csv')
gap      = pd.read_csv('results/gap_table.csv')
peer     = pd.read_csv('results/peer_comparison.csv')

# Build content 
story = []

# COVER PAGE 
story += [
    sp(4),
    Paragraph("NDIC + IADI DEPOSIT INSURANCE ANALYSIS", title_style),
    Paragraph(
        "Benchmarking Nigeria's Deposit Insurance System<br/>"
        "Against IADI Core Principles and Peer Member DICs (2010–2024)",
        subtitle_style
    ),
    sp(2),
    Paragraph("Promise O. Amhanesi", ParagraphStyle('Author', parent=styles['Normal'],
        fontSize=12, textColor=DARK_BLUE, leading=18, alignment=TA_CENTER)),
    Paragraph(
        "Banking and Finance · Philomath University Abuja, Nigeria<br/>"
        "Founder, AMHANi Enterprise",
        ParagraphStyle('Affil', parent=styles['Normal'],
            fontSize=10, textColor=colors.grey, leading=16, alignment=TA_CENTER)
    ),
    sp(2),
    Paragraph(
        "Repository: github.com/HELLO-AMHANI/ndic-iadi-deposit-insurance-analysis",
        ParagraphStyle('Repo', parent=styles['Normal'],
            fontSize=9, textColor=MID_BLUE, alignment=TA_CENTER)
    ),
    PageBreak()
]

# 1. EXECUTIVE SUMMARY 
story += [
    h("1. Executive Summary"),
    hr(),
    p(
        "Nigeria's National Deposit Insurance Corporation (NDIC) has maintained a fund adequacy "
        "ratio (FAR) substantially above the IADI 14-country peer average over the 2010–2024 "
        "period, averaging 0.47 locally compared to an IADI peer mean of approximately 0.06. "
        "This reflects a well-capitalised, ex-ante deposit insurance fund supported by consistent "
        "premium collection from a growing banking sector. However, 2024 data reveals a critical "
        "structural vulnerability: claims paid surged from a stable ₦8.3bn baseline to ₦63.2bn, "
        "coinciding with severe Naira devaluation (₦1,479/USD) and an upward revision of the "
        "statutory coverage limit to ₦5 million. Predictive modeling using XGBoost with SHAP "
        "explainability identifies lagged exchange rate depreciation, GDP contraction, and elevated "
        "NPL ratios as the three primary macro drivers of fund stress. Against IADI Core Principles, "
        "NDIC scores above the peer average on mandate, fund management, and safety-net coordination, "
        "but below average on governance independence and public awareness. These findings carry "
        "direct policy implications for NDIC's medium-term fund adequacy strategy, premium "
        "recalibration, and cross-border coordination under the IADI framework."
    ),
    sp()
]

# 2. CONTEXT
story += [
    h("2. Context & IADI Framework"),
    hr(),
    p(
        "The International Association of Deposit Insurers (IADI), headquartered at the Bank for "
        "International Settlements (BIS) in Basel, Switzerland, publishes the Core Principles for "
        "Effective Deposit Insurance Systems — a globally recognised benchmark adopted by the G20 "
        "and Financial Stability Board (FSB). NDIC, established under the NDIC Act 2006 (amended "
        "2019), is a full IADI member and is expected to align its operations with these principles."
    ),
    p(
        "This project benchmarks NDIC's quantitative performance — fund adequacy, coverage, "
        "claims intensity, and premium efficiency — against IADI annual survey data for 14 member "
        "countries across 15 years (2010–2024). The analysis is cross-functional: data was ingested "
        "via SQL (SQLite), cleaned and analysed in Python (pandas, scikit-learn, XGBoost, SHAP), "
        "validated in Microsoft Excel, and visualised using Plotly and Matplotlib."
    ),
    sp()
]

# 3. DATA & METHODS
story += [
    h("3. Data & Methods"),
    hr(),
    h("3.1 Data Sources", h2_style),
    table_style_base([
        ['Source', 'Coverage', 'Key Variables'],
        ['NDIC Annual Reports', 'Nigeria 2010–2024', 'fund_balance, insured_deposits, claims_paid, premium_rate, num_banks'],
        ['IADI Annual Survey', '14 countries 2010–2024', 'fund_adequacy_ratio, coverage_limit_usd, insured_deposits_usd'],
        ['World Bank GFDD', '14 countries 2010–2024', 'gdp_growth, inflation, exchange_rate, gdp_per_capita'],
    ], col_widths=[4.5*cm, 4*cm, 8.5*cm]),
    sp(),
    h("3.2 Key Computed Metrics", h2_style),
    p("Five primary ratios were engineered from raw data:"),
    p("• <b>Local Fund Adequacy Ratio:</b> fund_balance_bn / insured_deposits_bn"),
    p("• <b>Coverage Ratio:</b> coverage_limit_usd / gdp_per_capita (USD)"),
    p("• <b>Claims Intensity:</b> claims_paid_bn / fund_balance_bn"),
    p("• <b>Premium Efficiency:</b> mean_premium_rate_pct / 100"),
    p("• <b>IADI Benchmark Gap:</b> NDIC local FAR minus IADI 14-country peer average"),
    p("All macro variables were lagged by one year to prevent data leakage in predictive models."),
    sp()
]

# 4. NDIC PERFORMANCE 
story += [
    h("4. NDIC Performance Analysis (2010–2024)"),
    hr(),
]
story += fig('01_fund_vs_claims_timeseries.png', 15,
             'Figure 1: NDIC Fund Balance vs Claims Paid 2010–2024 (₦ billion). '
             'Stress years 2016 and 2020 annotated.')
story += [
    p(
        "NDIC's insurance fund grew from ₦295.7bn in 2010 to ₦2,279.4bn in 2024 — "
        "a 7.7x nominal increase over 15 years. Premium collection remained stable at "
        "0.40–0.64% of total deposits. Claims paid were flat at approximately ₦8.3bn "
        "annually from 2012 to 2023, then spiked to ₦63.2bn in 2024 — the clearest "
        "signal of structural stress in the dataset."
    ),
    sp()
]

# 5. BENCHMARKING 
story += [
    h("5. IADI Benchmarking Results"),
    hr(),
]
story += fig('05_far_trend_comparison.png', 15,
             'Figure 2: NDIC Fund Adequacy Ratio vs IADI Peer Average 2010–2024. '
             'Three series: local calculation, IADI-reported, and 14-country average.')
story += [
    p(
        "Nigeria's NDIC consistently outperforms the IADI 14-country peer average on "
        "fund adequacy — by a factor of approximately 8x in recent years. However, the "
        "IADI-reported FAR for Nigeria diverges sharply from the local calculation in 2024 "
        "(IADI: 0.47 vs local: 0.09), driven by the mid-year timing of IADI's survey snapshot "
        "relative to the Naira devaluation event. This divergence is itself a key finding: "
        "exchange-rate methodology materially affects how Nigeria's fund adequacy is perceived "
        "in international benchmarking."
    ),
    sp()
]
story += fig('06_radar_iadi_benchmarking.png', 13,
             'Figure 3: NDIC scored against IADI Core Principles across 6 dimensions. '
             'Scale 1–5. NDIC overall average: 3.57 / 5.')
story += [sp()]

story += fig('07_peer_comparison_table.png', 15,
             'Figure 4: Peer comparison — Nigeria vs African and emerging-market DIC members.')
story += [sp()]

# 6. MODEL FINDINGS 
story += [
    h("6. Predictive Modeling & SHAP Explainability"),
    hr(),
    p(
        "A fund stress classification model was built using an out-of-time test design: "
        "trained on 2011–2019, tested on 2020–2024. Given the small sample (n=14 usable rows), "
        "Leave-One-Out cross-validation was used to maximise reliability. XGBoost outperformed "
        "Logistic Regression on LOO CV F1 score."
    ),
    sp()
]

# Metrics table
met_data = [['Model','AUC-ROC','Precision','Recall','F1 Score','LOO CV F1']]
for _, r in metrics.iterrows():
    met_data.append([
        r['model'], str(r['auc_roc']), str(r['precision']),
        str(r['recall']), str(r['f1_score']), str(r['loo_cv_f1_mean'])
    ])
story.append(table_style_base(met_data, [6*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2.5*cm]))
story.append(sp())

story += fig('11_shap_feature_importance.png', 15,
             'Figure 5: SHAP feature importance — top predictors of fund stress. '
             'Mean absolute SHAP value across all years.')
story += [
    p(
        "The SHAP analysis identifies <b>lagged exchange rate</b>, <b>lagged GDP growth</b>, "
        "and <b>lagged inflation</b> as the three strongest predictors of fund stress — "
        "all macro variables. This confirms that NDIC's fund stress risk is primarily "
        "driven by external macroeconomic shocks rather than internal banking sector "
        "deterioration, a critical insight for policy calibration."
    ),
    sp()
]

# 7. LIMITATIONS 
story += [
    h("7. Limitations"),
    hr(),
    p("• <b>Small sample:</b> 15 annual observations limit statistical power. Results are indicative, not definitive."),
    p("• <b>NDIC data extraction:</b> Financial figures were manually extracted from PDF annual reports. Minor transcription variance is possible."),
    p("• <b>IADI 2024 divergence:</b> IADI-reported FAR for Nigeria differs from local calculation due to mid-year snapshot timing and currency methodology."),
    p("• <b>NDIC loan/deposit ratio:</b> Four years show a >5% gap between computed and reported figures because NDIC uses net loans (after provisions) while raw data uses gross loans."),
    p("• <b>Peer selection:</b> Only 14 IADI member countries were available in the public annual survey. A full 82-member benchmark would strengthen conclusions."),
    sp()
]

# 8. POLICY RECOMMENDATIONS 
story += [
    h("8. Policy Recommendations"),
    hr(),
    p("<b>1. Anchor the fund adequacy ratio target in statute.</b> NDIC currently has no legislated FAR floor. A minimum of 0.20 (local calculation) would provide a defensible buffer against macro shocks."),
    p("<b>2. Index coverage limit to GDP per capita annually.</b> The 2024 revision to ₦5mn was long overdue. Automatic annual indexation prevents the coverage ratio from eroding during inflationary periods."),
    p("<b>3. Introduce a formal exchange-rate stress test.</b> The SHAP analysis shows FX depreciation as the primary stress driver. NDIC should publish an annual scenario showing fund adequacy under a 30%, 50%, and 70% Naira devaluation."),
    p("<b>4. Strengthen governance independence.</b> NDIC scored below the IADI peer average on CP3 (Governance). Amending the NDIC Act to establish a board with fixed, staggered terms and a supermajority removal threshold would improve independence."),
    p("<b>5. Invest in depositor awareness in rural and informal sectors.</b> CP7 (Public Awareness) is the weakest dimension. A targeted awareness programme — particularly for microfinance bank depositors — would improve system trust and reduce bank-run risk."),
    sp()
]

# BUILD
doc.build(story)
print(f"✅  report.pdf built: {OUTPUT}")
