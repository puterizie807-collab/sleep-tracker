import streamlit as st
import pandas as pd
import datetime
import os

# 1. 告诉软件我们的“记账本”存在哪里
FILE_NAME = "sleep_data.csv"

# 2. 如果之前没有记账本，就新建一个，并写上表头
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["日期", "姓名", "睡觉时间", "起床时间", "睡眠时长(小时)"])
    df.to_csv(FILE_NAME, index=False)

# ====== 界面部分开始 ======
st.title("🛏️ 宿舍睡眠记录分析仪")

# 3. 记录新数据的区域
st.header("📝 添加今日记录")
# 左右分栏让界面更好看
col1, col2 = st.columns(2)

with col1:
    name = st.selectbox("是谁在记录？", ["我自己", "舍友"])
    date = st.date_input("日期", datetime.date.today())

with col2:
    # 默认昨晚 23:30 睡，今早 07:30 起
    sleep_time = st.time_input("睡觉时间", datetime.time(23, 30))
    wake_time = st.time_input("起床时间", datetime.time(7, 30))

# 点击按钮后的动作
if st.button("💾 保存记录"):
    # 简单算一下睡了多久 (小白先不用深究这段时间计算的魔法逻辑)
    sleep_dt = datetime.datetime.combine(date, sleep_time)
    wake_dt = datetime.datetime.combine(date, wake_time)
    # 如果是跨越午夜的睡眠（比如晚上11点到早上7点）
    if sleep_time > wake_time:
        sleep_dt -= datetime.timedelta(days=1) 
    
    duration = (wake_dt - sleep_dt).total_seconds() / 3600
    duration = round(duration, 1) # 保留一位小数

    # 把新数据打包
    new_record = pd.DataFrame({
        "日期": [date],
        "姓名": [name],
        "睡觉时间": [sleep_time.strftime("%H:%M")],
        "起床时间": [wake_time.strftime("%H:%M")],
        "睡眠时长(小时)": [duration]
    })
    
    # 存入 CSV 文件
    new_record.to_csv(FILE_NAME, mode='a', header=False, index=False)
    st.success(f"太棒了！{name} 的睡眠数据已保存。昨晚睡了 {duration} 小时！")

# 4. 数据展示与分析区域
st.header("📊 数据分析")
# 读取我们存好的数据
data = pd.read_csv(FILE_NAME)

if not data.empty:
    st.write("最近的记录：")
    st.dataframe(data.tail(5)) # 只显示最后 5 条记录

    st.subheader("📈 睡眠时长趋势图")
    # 把数据转换成画图需要的格式：按日期作横轴，姓名为图例
    chart_data = data.pivot(index="日期", columns="姓名", values="睡眠时长(小时)")
    # 一行代码画出折线图！
    st.line_chart(chart_data)
else:
    st.info("还没有数据哦，赶紧在上面记录第一笔吧！")
   
