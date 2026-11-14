import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="效用概率决策智能体", layout="wide")
st.title("效用概率决策智能体")
st.caption("Expected Utility Decision Agent · 规避风险还是追求刺激？")

# ---------- 侧边栏：参数输入 ----------
with st.sidebar:
    st.header("1. 方案收益与概率设定")
    st.markdown("**方案 A（高风险高收益）**")
    a_prob = st.slider("A 获得高收益的概率", 0.0, 1.0, 0.10, step=0.05)
    a_high = st.number_input("A 高收益金额（万元）", value=100.0, step=10.0)
    a_low = st.number_input("A 低收益金额（万元）", value=0.0, step=10.0)
    
    st.markdown("**方案 B（稳健低风险）**")
    b_prob = st.slider("B 获得高收益的概率", 0.0, 1.0, 1.00, step=0.05)
    b_high = st.number_input("B 高收益金额（万元）", value=8.0, step=10.0)
    b_low = st.number_input("B 低收益金额（万元）", value=8.0, step=10.0)

    st.header("2. 决策者风险态度")
    alpha = st.slider("风险态度参数 α (0.1~2.0)", 0.1, 2.0, 1.0, step=0.1)
    st.caption("α=1 风险中性；α<1 风险厌恶；α>1 风险偏好")

# ---------- 核心决策计算层 ----------
def utility(x, alpha):
    return np.where(x >= 0, x ** alpha, 0.0)

emv_a = a_prob * a_high + (1 - a_prob) * a_low
emv_b = b_prob * b_high + (1 - b_prob) * b_low

eu_a = a_prob * utility(a_high, alpha) + (1 - a_prob) * utility(a_low, alpha)
eu_b = b_prob * utility(b_high, alpha) + (1 - b_prob) * utility(b_low, alpha)

# ---------- 输出层：指标卡片 ----------
st.subheader("决策数据对比")
c1, c2, c3 = st.columns(3)
c1.metric("方案 A 期望货币值 (EMV)", f"{emv_a:.2f} 万元")
c2.metric("方案 B 期望货币值 (EMV)", f"{emv_b:.2f} 万元")

if alpha == 1.0:
    risk_attitude = "风险中性"
elif alpha < 1.0:
    risk_attitude = "风险厌恶"
else:
    risk_attitude = "风险偏好"
c3.metric("当前决策者偏好", risk_attitude)

# ---------- 智能决策诊断 ----------
st.subheader("智能体决策建议")

if eu_a > eu_b:
    best_plan = "方案 A"
    reason = f"方案 A 的期望效用（{eu_a:.2f}）大于方案 B（{eu_b:.2f}）。"
    st.success(f"**推荐选择：{best_plan}**。{reason}")
elif eu_b > eu_a:
    best_plan = "方案 B"
    reason = f"方案 B 的期望效用（{eu_b:.2f}）大于方案 A（{eu_a:.2f}）。"
    st.success(f"**推荐选择：{best_plan}**。{reason}")
else:
    st.info("两个方案的期望效用相同，可根据其他非量化因素进行决策。")

if (emv_a > emv_b and eu_b > eu_a) or (emv_b > emv_a and eu_a > eu_b):
    st.warning(
        "**决策冲突提示**：单纯看期望收益（EMV）和看期望效用（EU）得出的最优方案不同！"
        "这说明当前的风险态度（α）显著影响了决策。效用理论纠正了只看金钱数字的盲区。"
    )

# ---------- 图表可视化 ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 效用曲线与方案分布")
    max_val = max(a_high, b_high, 10) * 1.2
    xs = np.linspace(0, max_val, 100)
    ys = utility(xs, alpha)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name=f"效用函数 (α={alpha})"))
    fig.add_trace(go.Scatter(x=[emv_a], y=[eu_a], mode="markers+text",
                             marker=dict(size=12, color="red"), text=["方案A"],
                             textposition="top center", name="方案 A 期望点"))
    fig.add_trace(go.Scatter(x=[emv_b], y=[eu_b], mode="markers+text",
                             marker=dict(size=12, color="blue"), text=["方案B"],
                             textposition="top center", name="方案 B 期望点"))
    fig.update_layout(xaxis_title="收益金额（万元）", yaxis_title="效用值 U(x)", height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### 期望货币值 vs 期望效用 对比")
    fig2 = go.Figure(data=[
        go.Bar(name='期望货币值 EMV', x=['方案 A', '方案 B'], y=[emv_a, emv_b], marker_color='lightgrey'),
        go.Bar(name='期望效用 EU', x=['方案 A', '方案 B'], y=[eu_a, eu_b], marker_color='lightblue')
    ])
    fig2.update_layout(barmode='group', height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.caption("效用概率决策智能体")
