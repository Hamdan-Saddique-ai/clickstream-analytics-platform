import sqlite3
import pandas as pd
from datetime import datetime
import streamlit as st

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('data/clickstream.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            session_id TEXT,
            page_name TEXT,
            button_name TEXT,
            element_type TEXT,
            click_time TIMESTAMP,
            user_agent TEXT,
            ip_address TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            total_clicks INTEGER,
            user_id TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_click(user_id, session_id, page_name, button_name, element_type, user_agent, ip_address):
    """Save click event to database"""
    conn = sqlite3.connect('data/clickstream.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO clicks (user_id, session_id, page_name, button_name, element_type, click_time, user_agent, ip_address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, session_id, page_name, button_name, element_type, datetime.now(), user_agent, ip_address))
    
    conn.commit()
    conn.close()

def update_session(session_id, user_id):
    """Update or create session"""
    conn = sqlite3.connect('data/clickstream.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (session_id,))
    session = cursor.fetchone()
    
    if session:
        cursor.execute('''
            UPDATE sessions 
            SET end_time = ?, total_clicks = total_clicks + 1
            WHERE session_id = ?
        ''', (datetime.now(), session_id))
    else:
        cursor.execute('''
            INSERT INTO sessions (session_id, start_time, end_time, total_clicks, user_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (session_id, datetime.now(), datetime.now(), 1, user_id))
    
    conn.commit()
    conn.close()

def get_analytics():
    """Get analytics data"""
    conn = sqlite3.connect('data/clickstream.db')
    
    clicks_df = pd.read_sql_query("SELECT * FROM clicks ORDER BY click_time DESC", conn)
    sessions_df = pd.read_sql_query("SELECT * FROM sessions ORDER BY start_time DESC", conn)
    
    conn.close()
    return clicks_df, sessions_df

def get_click_stats():
    """Get click statistics"""
    conn = sqlite3.connect('data/clickstream.db')
    
    # Total clicks
    total_clicks = pd.read_sql_query("SELECT COUNT(*) as count FROM clicks", conn)['count'][0]
    
    # Clicks by page
    clicks_by_page = pd.read_sql_query("""
        SELECT page_name, COUNT(*) as count 
        FROM clicks 
        GROUP BY page_name 
        ORDER BY count DESC
    """, conn)
    
    # Clicks by button
    clicks_by_button = pd.read_sql_query("""
        SELECT button_name, COUNT(*) as count 
        FROM clicks 
        WHERE button_name IS NOT NULL
        GROUP BY button_name 
        ORDER BY count DESC
    """, conn)
    
    # Hourly clicks
    hourly_clicks = pd.read_sql_query("""
        SELECT strftime('%H', click_time) as hour, COUNT(*) as count 
        FROM clicks 
        GROUP BY hour 
        ORDER BY hour
    """, conn)
    
    # Unique users
    unique_users = pd.read_sql_query("SELECT COUNT(DISTINCT user_id) as count FROM clicks", conn)['count'][0]
    
    conn.close()
    
    return {
        'total_clicks': total_clicks,
        'unique_users': unique_users,
        'clicks_by_page': clicks_by_page,
        'clicks_by_button': clicks_by_button,
        'hourly_clicks': hourly_clicks
    }