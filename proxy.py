import streamlit as st
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
import base64
import zipfile
import os


st.title("📺 YouTube View Bot")
st.write("Automate watching YouTube videos using Selenium with Proxies!")

# Load proxies from file
proxies = []
with open('Webshare 250 proxies.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            proxies.append(line)  # Format: ip:port:username:password

# User Inputs
YOUTUBE_VIDEO_URL = st.text_input("🔗 Enter YouTube Video URL:", "https://www.youtube.com/watch?v=6hlDGVv1_Hs")
WATCH_TIME = st.number_input("⏳ Watch Time (seconds):", min_value=10, max_value=600, value=20)
NUM_VIEWS = st.number_input("👀 Number of Views:", min_value=1, max_value=50, value=2)

def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password, plugin_path):
    manifest_json = """
    {
      "version": "1.0.0",
      "manifest_version": 2,
      "name": "Chrome Proxy Auth Extension",
      "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
      ],
      "background": {
        "scripts": ["background.js"]
      }
    }
    """

    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
          singleProxy: {{
            scheme: "http",
            host: "{proxy_host}",
            port: parseInt({proxy_port})
          }},
          bypassList: ["localhost"]
        }}
      }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{proxy_username}",
                password: "{proxy_password}"
            }}
        }};
    }}

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {{urls: ["<all_urls>"]}},
        ['blocking']
    );
    """

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)


# Chrome Options with proxy
def get_chrome_options(proxy_address=None):
    options = Options()
    options.add_argument('--disable-notifications')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    if proxy_address:
        options.add_argument(f'--proxy-server=http://{proxy_address}')
    return options

# Function to watch a video using a proxy
def watch_video(proxy_line):
    try:
        ip, port, username, password = proxy_line.split(':')
        proxy_plugin_path = 'proxy_auth_plugin.zip'
        create_proxy_auth_extension(ip, port, username, password, proxy_plugin_path)

        options = get_chrome_options()
        options.add_extension(proxy_plugin_path)

        driver = uc.Chrome(
            driver_executable_path='C:\\Users\\SHANI\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe',
            options=options,
            headless=False,
        )

        driver.get(YOUTUBE_VIDEO_URL)
        time.sleep(random.uniform(5, 10))

        try:
            play_button = driver.find_element(By.CSS_SELECTOR, "#movie_player > div.ytp-cued-thumbnail-overlay > button")
            play_button.click()
            st.success("▶️ Clicked Play button!")
        except:
            st.info("🎬 Video is already playing.")

        st.write(f"⏳ Watching for {WATCH_TIME} seconds...")
        time.sleep(WATCH_TIME)
        st.success("✅ Done watching!")

    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass
        if os.path.exists('proxy_auth_plugin.zip'):
            os.remove('proxy_auth_plugin.zip')

# Run bot for N views
if st.button("🚀 Start Watching"):
    if not proxies:
        st.error("No proxies loaded! Check your proxy file.")
    else:
        for i in range(int(NUM_VIEWS)):
            current_proxy = proxies[i % len(proxies)]
            ip_port = current_proxy.split(':')
            st.write(f"🔄 Starting view {i+1} using proxy: {ip_port[0]}:{ip_port[1]}")
            watch_video(current_proxy)
            time.sleep(random.uniform(5, 10))
