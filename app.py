import streamlit as st
import pandas as pd
import datetime
import os
import random

# --- 1. 页面配置 (网页标签名和炸虾尾图标) ---
st.set_page_config(page_title="萌物冬眠基地", page_icon="🍤", layout="wide")

# --- 2. 注入超级美化 CSS (萌物专属皮肤) ---
st.markdown("""
    <style>
    /* 全局背景：粉、紫、黄梦幻渐变 */
    .stApp {
        background: linear-gradient(120deg, #fff5f5 0%, #f3e5f5 50%, #fffde7 100%);
    }
    
    /* 主标题样式：炸虾尾同款暖黄 */
    .main-title {
        color: #FFB300;
        text-align: center;
        font-family: 'Microsoft YaHei', sans-serif;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 20px;
    }
    
    /* 侧边栏样式：库洛米紫色调 */
    [data-testid="stSidebar"] {
        background-color: #f3e5f5 !important;
        border-right: 2px solid #ce93d8;
    }
    
    /* 按钮样式：库洛米同款酷炫紫 */
    div.stButton > button {
        width: 100%;
        border-radius: 25px;
        background-color: #ba68c8;
        color: white;
        border: none;
        height: 3.5em;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #7b1fa2;
        transform: scale(1.05);
    }
    
    /* 图表选项卡美化 */
    .stTabs [data-baseweb="tab"] {
        color: #7b1fa2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 数据初始化 ---
FILE_NAME = "sleep_data.csv"
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["日期", "姓名", "睡觉时间", "起床时间", "睡眠时长(小时)", "心情"])
    df.to_csv(FILE_NAME, index=False)

# --- 4. 左侧：库洛米监督打卡区 ---
with st.sidebar:
    st.markdown("### 😈 库洛米盯着你打卡")
    # 这里去掉了他，只保留你们三个人的名字
    name = st.selectbox("是谁在记录？", ["子末", "小智", "宇彤"])
    date = st.date_input("日期", datetime.date.today())
    
    col_s, col_w = st.columns(2)
    with col_s:
        sleep_time = st.time_input("睡觉时间", datetime.time(23, 30))
    with col_w:
        wake_time = st.time_input("起床时间", datetime.time(7, 30))
    
    mood = st.select_slider("起床状态", options=["😫", "🥱", "😐", "🙂", "🤩"])
    
    if st.button("✨ 存入梦境"):
        sleep_dt = datetime.datetime.combine(date, sleep_time)
        wake_dt = datetime.datetime.combine(date, wake_time)
        if sleep_time > wake_time:
            sleep_dt -= datetime.timedelta(days=1) 
        duration = round((wake_dt - sleep_dt).total_seconds() / 3600, 1)

        new_record = pd.DataFrame([[date, name, sleep_time.strftime("%H:%M"), 
                                   wake_time.strftime("%H:%M"), duration, mood]])
        new_record.to_csv(FILE_NAME, mode='a', header=False, index=False)
        
        st.success(f"记录成功！昨晚睡了 {duration} 小时 🎵")
        st.balloons() # 撒花特效

# --- 5. 右侧：炸虾尾 & 小猪数据区 ---
st.markdown("<h1 class='main-title'>🍤 202 萌物冬眠基地 🍤</h1>", unsafe_allow_html=True)

greetings = [
    "🍤 炸虾尾裹紧了小被子：早安！昨晚梦到好吃的了吗？", 
    "😈 库洛米说：今天也要保持酷酷的好心情哦！", 
    "🐷 呼噜噜...是谁还在赖床呀？"
]
st.write(f"> **{random.choice(greetings)}**")

data = pd.read_csv(FILE_NAME)

if not data.empty:
    # 顶部小猪粉色指标卡
    avg_s = round(data['睡眠时长(小时)'].mean(), 1)
    max_s = data['睡眠时长(小时)'].max()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("💤 宿舍平均", f"{avg_s}h")
    m2.metric("🐷 睡神最高", f"{max_s}h")
    m3.metric("📅 打卡天数", f"{len(data)}天")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📈 每一天的睡眠", "📅 按月看汇总", "📑 翻看记账本"])

    with tab1:
        st.subheader("看看大家的睡眠起伏~")
        chart_data = data.pivot_table(index="日期", columns="姓名", values="睡眠时长(小时)")
        st.line_chart(chart_data)

    with tab2:
        data['日期'] = pd.to_datetime(data['日期'])
        data['月份'] = data['日期'].dt.month
        st.subheader("谁是这个月的冬眠冠军？")
        monthly_avg = data.groupby(['月份', '姓名'])['睡眠时长(小时)'].mean().unstack()
        st.bar_chart(monthly_avg)

    with tab3:
        st.dataframe(data.sort_values(by="日期", ascending=False), use_container_width=True)

else:
    st.info("👈正在等你填入第一笔梦境数据哦！")