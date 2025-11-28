# 使用streamlit run output.py运行

import streamlit as st
import requests
import time
from datetime import datetime
import json

# 页面配置
st.set_page_config(
    page_title="Bitcoin Price Tracker",
    page_icon="₿",
    layout="centered"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .price-display {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    .positive-change {
        color: #00cc00;
    }
    .negative-change {
        color: #ff4b4b;
    }
    .last-updated {
        font-size: 0.8rem;
        color: #666;
        text-align: center;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# API配置
API_URL = "https://api.coingecko.com/api/v3/simple/price"
PARAMS = {
    "ids": "bitcoin",
    "vs_currencies": "usd",
    "include_24hr_change": "true"
}

# 初始化session state
if 'bitcoin_data' not in st.session_state:
    st.session_state.bitcoin_data = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'error' not in st.session_state:
    st.session_state.error = None
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

def fetch_bitcoin_data():
    """获取比特币价格数据"""
    try:
        response = requests.get(API_URL, params=PARAMS, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        
        data = response.json()
        if 'bitcoin' not in data:
            raise ValueError("Invalid API response format")
        
        return data['bitcoin']
        
    except requests.exceptions.RequestException as e:
        st.session_state.error = f"网络错误: {str(e)}"
        return None
    except ValueError as e:
        st.session_state.error = f"数据解析错误: {str(e)}"
        return None
    except Exception as e:
        st.session_state.error = f"未知错误: {str(e)}"
        return None

def refresh_data():
    """刷新数据函数"""
    st.session_state.is_loading = True
    st.session_state.error = None
    
    data = fetch_bitcoin_data()
    if data:
        st.session_state.bitcoin_data = data
        st.session_state.last_update = datetime.now()
        st.session_state.error = None
    else:
        # 保持上一次成功的数据，仅更新错误状态
        pass
    
    st.session_state.is_loading = False

# 应用标题
st.title("₿ Bitcoin Price Tracker")
st.markdown("实时比特币价格监控")

# 主内容区域
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 刷新按钮
    if st.button("🔄 刷新价格", 
                disabled=st.session_state.is_loading,
                use_container_width=True):
        refresh_data()
    
    # 显示加载状态
    if st.session_state.is_loading:
        st.spinner("正在获取最新数据...")
    
    # 显示错误信息
    if st.session_state.error:
        st.error(st.session_state.error)
    
    # 显示价格数据
    if st.session_state.bitcoin_data:
        data = st.session_state.bitcoin_data
        current_price = data['usd']
        price_change_24h = data['usd_24h_change']
        price_change_amount = (current_price * price_change_24h) / 100
        
        # 价格显示
        st.markdown(f'<div class="price-display">${current_price:,.2f}</div>', 
                   unsafe_allow_html=True)
        
        # 价格变化
        change_class = "positive-change" if price_change_24h >= 0 else "negative-change"
        change_icon = "📈" if price_change_24h >= 0 else "📉"
        
        st.markdown(f"""
        <div style="text-align: center;">
            <span class="{change_class}">
                {change_icon} {price_change_24h:+.2f}% (${price_change_amount:+.2f})
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # 显示最后更新时间
    if st.session_state.last_update:
        update_time = st.session_state.last_update.strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f'<div class="last-updated">最后更新: {update_time}</div>', 
                   unsafe_allow_html=True)
    
    # 如果没有数据且没有错误，显示提示
    if not st.session_state.bitcoin_data and not st.session_state.error:
        st.info("点击刷新按钮获取比特币价格数据")

# 页面加载时自动获取数据（仅第一次）
if st.session_state.bitcoin_data is None and not st.session_state.is_loading:
    refresh_data()

# 使用说明
with st.expander("使用说明"):
    st.markdown("""
    - **当前价格**: 显示比特币的实时美元价格
    - **24小时变化**: 显示过去24小时的价格变化百分比和金额
    - **颜色标识**: 
        - 📈 绿色: 价格上涨
        - 📉 红色: 价格下跌
    - **刷新按钮**: 手动获取最新价格数据
    - **数据源**: CoinGecko API
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>数据提供: <a href="https://www.coingecko.com/" target="_blank">CoinGecko</a></p>
    <p>更新时间间隔请遵守API限制（约30次/分钟）</p>
</div>
""", unsafe_allow_html=True)