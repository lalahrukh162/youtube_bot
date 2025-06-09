import streamlit as st
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random

st.title("📺 YouTube View Bot")
st.write("Automate watching YouTube videos using Selenium with Proxies!")

# Load proxies from file
proxies = []
with open('Webshare 250 proxies.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            ip, port, username, password = line.split(':')
            proxy_str = f"{username}:{password}@{ip}:{port}"
            proxies.append(proxy_str)

YOUTUBE_VIDEO_URL = st.text_input("🔗 Enter YouTube Video URL:", "https://www.youtube.com/watch?v=d9L37Xv96gU")
WATCH_TIME = st.number_input("⏳ Watch Time (seconds):", min_value=10, max_value=600, value=120)
NUM_VIEWS = st.number_input("👀 Number of Views:", min_value=1, max_value=50, value=5)

def get_chrome_options(proxy_str=None):
    options = Options()
    options.add_argument('--disable-notifications')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    if proxy_str:
        options.add_argument(f'--proxy-server=http://{proxy_str}')
    
    return options

def watch_video(proxy_str):
    try:
        driver = uc.Chrome(
            driver_executable_path='C:\\Users\\SHANI\\chromedriver.exe',
            options=get_chrome_options(proxy_str),
            headless=False,
        )
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.delete_all_cookies()

        driver.get(YOUTUBE_VIDEO_URL)
        time.sleep(random.uniform(5, 10))

        try:
            play_button = driver.find_element(By.CSS_SELECTOR, "#movie_player > div.ytp-cued-thumbnail-overlay > button")
            play_button.click()
            st.success("▶️ Clicked Play button!")
        except Exception:
            st.info("🎬 Video is already playing.")

        st.write(f"⏳ Watching the video for {WATCH_TIME} seconds...")
        time.sleep(WATCH_TIME)
        st.success("✅ Done watching!")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if st.button("🚀 Start Watching"):
    if not proxies:
        st.error("No proxies loaded! Check your proxy file.")
    else:
        for i in range(int(NUM_VIEWS)):
            current_proxy = proxies[i % len(proxies)]
            st.write(f"🔄 Starting view {i+1} of {NUM_VIEWS} with proxy: {current_proxy.split('@')[1]}")
            watch_video(current_proxy)
            time.sleep(random.uniform(5, 10))