import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid
import hashlib
from streamlit_option_menu import option_menu
import utils

# Page configuration
st.set_page_config(
    page_title="ClickStream Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
utils.init_database()

# Session state initialization
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'click_count' not in st.session_state:
    st.session_state.click_count = 0

# Custom CSS for better UI
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .page-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .click-button {
        margin: 10px 0;
    }
    .success-message {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        animation: fadein 0.5s, fadeout 0.5s 2.5s;
        z-index: 1000;
    }
    @keyframes fadein {
        from {bottom: 0; opacity: 0;}
        to {bottom: 20px; opacity: 1;}
    }
    @keyframes fadeout {
        from {bottom: 20px; opacity: 1;}
        to {bottom: 0; opacity: 0;}
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/click.png", width=80)
    st.title("ClickStream 📊")
    
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Dashboard", "Analytics", "Reports", "User Activity"],
        icons=["house", "bar-chart", "graph-up", "file-text", "people"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#1f77b4", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#1f77b4"},
        }
    )

# Track page view
def track_click(page_name, button_name, element_type):
    user_agent = st.context.headers.get('User-Agent', 'Unknown')
    ip_address = st.context.headers.get('X-Forwarded-For', '127.0.0.1')
    
    utils.save_click(
        st.session_state.user_id,
        st.session_state.session_id,
        page_name,
        button_name,
        element_type,
        user_agent,
        ip_address
    )
    utils.update_session(st.session_state.session_id, st.session_state.user_id)
    st.session_state.click_count += 1
    
    # Show success message
    st.toast(f"✅ Click tracked! Total: {st.session_state.click_count}", icon="🎯")

# Home Page
if selected == "Home":
    st.markdown("<h1 class='page-title'>🎯 ClickStream Analytics Platform</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Your Session Clicks", st.session_state.click_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        stats = utils.get_click_stats()
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Platform Clicks", stats['total_clicks'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Active Session ID", st.session_state.session_id[:8] + "...")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🎮 Interactive Demo Area")
    st.write("Click the buttons below to generate clickstream data!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View Dashboard", use_container_width=True):
            track_click("Home Page", "View Dashboard", "button")
            st.switch_page("app.py")
            st.rerun()
    
    with col2:
        if st.button("📈 Analytics Report", use_container_width=True):
            track_click("Home Page", "Analytics Report", "button")
            st.success("Analytics report requested!")
    
    with col3:
        if st.button("👥 User Activity", use_container_width=True):
            track_click("Home Page", "User Activity", "button")
            st.info("User activity tracked!")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("👍 Like", use_container_width=True):
            track_click("Home Page", "Like Button", "button")
            st.balloons()
    
    with action_col2:
        if st.button("💬 Comment", use_container_width=True):
            track_click("Home Page", "Comment Button", "button")
            st.snow()
    
    with action_col3:
        if st.button("📤 Share", use_container_width=True):
            track_click("Home Page", "Share Button", "button")
            st.toast("Share feature coming soon!")
    
    with action_col4:
        if st.button("🔔 Subscribe", use_container_width=True):
            track_click("Home Page", "Subscribe Button", "button")
            st.success("Subscribed successfully!")

# Dashboard Page
elif selected == "Dashboard":
    st.markdown("<h1 class='page-title'>📊 Live Dashboard</h1>", unsafe_allow_html=True)
    
    stats = utils.get_click_stats()
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Clicks", stats['total_clicks'], delta="+12%")
    with col2:
        st.metric("Unique Users", stats['unique_users'], delta="+5%")
    with col3:
        st.metric("Active Session", "Yes", delta="Active")
    with col4:
        st.metric("Click Rate", f"{stats['total_clicks']/max(stats['unique_users'],1):.1f}", delta="per user")
    
    st.markdown("---")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Clicks by Page")
        if not stats['clicks_by_page'].empty:
            fig = px.pie(stats['clicks_by_page'], values='count', names='page_name', 
                        title="Page Distribution", color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet. Click some buttons!")
    
    with col2:
        st.subheader("Clicks by Button")
        if not stats['clicks_by_button'].empty:
            fig = px.bar(stats['clicks_by_button'], x='button_name', y='count', 
                        title="Button Popularity", color='count', color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No button clicks recorded yet!")
    
    # Hourly Activity
    st.subheader("Hourly Click Activity")
    if not stats['hourly_clicks'].empty:
        fig = px.line(stats['hourly_clicks'], x='hour', y='count', 
                     title="24-Hour Activity Pattern", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Live Click Stream
    st.subheader("Live Click Stream")
    clicks_df, _ = utils.get_analytics()
    if not clicks_df.empty:
        st.dataframe(clicks_df[['user_id', 'page_name', 'button_name', 'click_time']].head(10), 
                    use_container_width=True)
    else:
        st.info("No click data available yet. Start clicking!")

# Analytics Page
elif selected == "Analytics":
    st.markdown("<h1 class='page-title'>📈 Advanced Analytics</h1>", unsafe_allow_html=True)
    
    stats = utils.get_click_stats()
    clicks_df, sessions_df = utils.get_analytics()
    
    if not clicks_df.empty:
        # Filters
        st.sidebar.subheader("Filters")
        pages = ['All'] + list(stats['clicks_by_page']['page_name'].unique())
        selected_page = st.sidebar.selectbox("Filter by Page", pages)
        
        if selected_page != 'All':
            clicks_df = clicks_df[clicks_df['page_name'] == selected_page]
        
        # User Engagement Metrics
        st.subheader("User Engagement Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_clicks = len(clicks_df) / clicks_df['user_id'].nunique()
            st.metric("Avg Clicks per User", f"{avg_clicks:.2f}")
        
        with col2:
            st.metric("Total Sessions", len(sessions_df))
        
        with col3:
            bounce_rate = len(sessions_df[sessions_df['total_clicks'] == 1]) / max(len(sessions_df), 1) * 100
            st.metric("Bounce Rate", f"{bounce_rate:.1f}%")
        
        # Click Heatmap
        st.subheader("Click Activity Heatmap")
        clicks_df['hour'] = pd.to_datetime(clicks_df['click_time']).dt.hour
        clicks_df['day'] = pd.to_datetime(clicks_df['click_time']).dt.day_name()
        
        heatmap_data = clicks_df.groupby(['hour', 'day']).size().reset_index(name='clicks')
        if not heatmap_data.empty:
            fig = px.density_heatmap(heatmap_data, x='hour', y='day', z='clicks',
                                     title="Click Activity Heatmap", color_continuous_scale='YlOrRd')
            st.plotly_chart(fig, use_container_width=True)
        
        # Funnel Analysis
        st.subheader("User Journey Funnel")
        funnel_stages = ['Home Page', 'Dashboard', 'Analytics', 'Reports', 'User Activity']
        funnel_data = []
        
        for stage in funnel_stages:
            count = len(clicks_df[clicks_df['page_name'] == stage])
            funnel_data.append(count)
        
        fig = go.Figure(go.Funnel(
            y=funnel_stages,
            x=funnel_data,
            textposition="inside",
            textinfo="value+percent initial",
            marker={"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"]}
        ))
        fig.update_layout(title="User Conversion Funnel")
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Data
        with st.expander("View Detailed Click Data"):
            st.dataframe(clicks_df, use_container_width=True)
    else:
        st.warning("No analytics data available. Start clicking buttons to generate data!")

# Reports Page
elif selected == "Reports":
    st.markdown("<h1 class='page-title'>📄 Reports & Exports</h1>", unsafe_allow_html=True)
    
    clicks_df, sessions_df = utils.get_analytics()
    
    if not clicks_df.empty:
        # Summary Report
        st.subheader("Executive Summary Report")
        
        # Create report metrics
        stats = utils.get_click_stats()
        
        report_data = {
            "Metric": ["Total Clicks", "Unique Users", "Total Sessions", "Click per User"],
            "Value": [
                stats['total_clicks'],
                stats['unique_users'],
                len(sessions_df),
                f"{stats['total_clicks']/max(stats['unique_users'],1):.2f}"
            ]
        }
        
        report_df = pd.DataFrame(report_data)
        st.table(report_df)
        
        # Download Options
        st.subheader("Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_clicks = clicks_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Click Data (CSV)",
                data=csv_clicks,
                file_name=f"click_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            csv_sessions = sessions_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Session Data (CSV)",
                data=csv_sessions,
                file_name=f"session_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Data Preview
        with st.expander("Preview Click Data"):
            st.dataframe(clicks_df.head(20), use_container_width=True)
        
        with st.expander("Preview Session Data"):
            st.dataframe(sessions_df.head(20), use_container_width=True)
    else:
        st.info("No data available to generate reports. Start clicking buttons first!")

# User Activity Page
elif selected == "User Activity":
    st.markdown("<h1 class='page-title'>👥 User Activity Tracking</h1>", unsafe_allow_html=True)
    
    st.info(f"Your User ID: `{st.session_state.user_id}` | Session ID: `{st.session_state.session_id[:8]}...`")
    
    # User-specific tracking
    st.subheader("Your Activity Feed")
    
    clicks_df, _ = utils.get_analytics()
    user_clicks = clicks_df[clicks_df['user_id'] == st.session_state.user_id] if not clicks_df.empty else pd.DataFrame()
    
    if not user_clicks.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Total Clicks", len(user_clicks))
        with col2:
            pages_visited = user_clicks['page_name'].nunique()
            st.metric("Pages Visited", pages_visited)
        
        st.subheader("Your Click History")
        st.dataframe(user_clicks[['page_name', 'button_name', 'click_time']], use_container_width=True)
        
        # User preference chart
        if not user_clicks.empty:
            user_pref = user_clicks['page_name'].value_counts().head(5)
            fig = px.bar(x=user_pref.index, y=user_pref.values, 
                        title="Your Most Visited Pages",
                        labels={'x': 'Page', 'y': 'Visit Count'})
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No activity recorded for your session yet. Click some buttons to see your activity!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>ClickStream Analytics Platform © 2024 | Real-time Click Tracking</div>",
    unsafe_allow_html=True
)