import streamlit as st

CSS = """
<style>
@font-face {
  font-family: 'Vazirmatn';
  src: url('app/static/Vazirmatn-Regular.ttf') format('truetype');
  font-weight: 100 900;
  font-display: swap;
}

.stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp button, .stApp input, .stApp textarea,
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] p,
.stTabs [data-baseweb="tab"] {
  font-family: 'Vazirmatn', sans-serif !important;
}

/* راست‌چین */
.stApp, [data-testid="stSidebar"] { direction: rtl; }
.stMarkdown, label, h1, h2, h3, h4, [data-testid="stMetric"] { text-align: right; }
input[type=number] { direction: ltr; text-align: left; }
.js-plotly-plot { direction: ltr; }

/* چیدمان */
.block-container { padding-top: 2rem; max-width: 1200px; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

/* کارت‌های عددی */
[data-testid="stMetric"] {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 16px;
  padding: 16px 20px;
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.06);
}
[data-testid="stMetricValue"] { font-size: 1.5rem; font-weight: 700; }
[data-testid="stMetricLabel"] p { color: #64748B; }

/* فرم‌ها و سایدبار */
[data-testid="stForm"] {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 16px;
}
[data-testid="stSidebar"] { background: #FFFFFF; border-left: 1px solid #E5E7EB; }

/* تب‌ها */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
  padding: 10px 18px;
  border-radius: 10px 10px 0 0;
  font-weight: 600;
}

/* دکمه‌ها */
.stButton > button, .stDownloadButton > button {
  border-radius: 10px;
  font-weight: 600;
}

/* بنر بالای صفحه */
.hero {
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
  color: #fff;
  padding: 28px 32px;
  border-radius: 20px;
  margin-bottom: 20px;
}
.hero h1 { color: #fff; margin: 0; font-size: 1.8rem; }
.hero p { color: rgba(255,255,255,0.85); margin: 6px 0 0 0; }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)