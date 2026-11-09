import streamlit as st

CSS = """
<style>
@font-face {
  font-family: 'Vazirmatn';
  src: url('app/static/Vazirmatn-Regular.ttf') format('truetype');
  font-weight: 100 900;
  font-display: swap;
}

/* فونت */
.stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp button, .stApp input, .stApp textarea,
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] p,
.stTabs [data-baseweb="tab"] {
  font-family: 'Vazirmatn', sans-serif !important;
}

/* پس‌زمینه */
.stApp {
  background:
    radial-gradient(ellipse 60% 50% at 85% 0%, rgba(139, 92, 246, 0.28), transparent 60%),
    radial-gradient(ellipse 50% 40% at 0% 30%, rgba(6, 182, 212, 0.18), transparent 60%),
    radial-gradient(ellipse 60% 50% at 70% 100%, rgba(236, 72, 153, 0.14), transparent 60%),
    linear-gradient(160deg, #0B1020 0%, #0F1530 50%, #0B1020 100%);
  background-attachment: fixed;
}
[data-testid="stHeader"] { background: transparent; }

/* راست‌چین: فقط روی محتوا، نه روی کانتینر اصلی سایدبار */
[data-testid="stMain"] .block-container { direction: rtl; }
[data-testid="stSidebarUserContent"] { direction: rtl; }

.stMarkdown, label, h1, h2, h3, h4,
[data-testid="stMetric"], [data-testid="stWidgetLabel"] { text-align: right; }

input[type=number] { direction: ltr; text-align: left; }
.js-plotly-plot { direction: ltr; }

/* چیدمان */
.block-container { padding-top: 2rem; max-width: 1200px; }
#MainMenu, footer { visibility: hidden; }

/* کارت‌های شیشه‌ای */
[data-testid="stMetric"] {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.10);
  border-radius: 16px;
  padding: 16px 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
[data-testid="stMetricValue"] { font-size: 1.5rem; font-weight: 700; color: #FFFFFF; }
[data-testid="stMetricLabel"] p { color: #94A3B8; }

/* فرم‌ها و کانتینرها */
[data-testid="stForm"],
[data-testid="stVerticalBlockBorderWrapper"] {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.10);
  border-radius: 16px;
}

/* سایدبار */
[data-testid="stSidebar"] {
  background: rgba(11, 16, 32, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

/* تب‌ها */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
  padding: 10px 18px;
  border-radius: 10px 10px 0 0;
  font-weight: 600;
}

/* دکمه‌ها */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
  border-radius: 10px;
  font-weight: 600;
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid rgba(139, 92, 246, 0.45);
  color: #E9D5FF;
  transition: all 0.2s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
  background: linear-gradient(135deg, #8B5CF6, #06B6D4);
  border-color: transparent;
  color: #FFFFFF;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(139, 92, 246, 0.35);
}

/* بنر بالای صفحه */
.hero {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.85) 0%, rgba(6, 182, 212, 0.75) 100%);
  color: #fff;
  padding: 28px 32px;
  border-radius: 20px;
  margin-bottom: 20px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 12px 40px rgba(139, 92, 246, 0.30);
}
.hero h1 { color: #fff; margin: 0; font-size: 1.8rem; }
.hero p { color: rgba(255, 255, 255, 0.90); margin: 6px 0 0 0; }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)