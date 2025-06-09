# youtube_bot
A Streamlit-based YouTube view bot using undetected ChromeDriver and rotating HTTP proxies. Users can input a video URL, set custom watch time and number of views. The bot loads proxies from a file and automates views by mimicking human behavior with randomized delays and stealth browsing.


## 📺 YouTube View Bot (Streamlit + Selenium + Proxies)

This project is a **YouTube View Bot** built with **Streamlit** for the frontend and **Selenium with Undetected ChromeDriver** for browser automation. It enables automated viewing of a YouTube video using rotating HTTP proxies, simulating human behavior with randomized actions and configurable watch times.

---

### 🚀 Features

* **Streamlit Interface**: A simple and interactive web UI for inputting the video URL, watch time, and number of views.
* **Proxy Support**: Loads proxies (IP\:Port\:Username\:Password) from a local text file to rotate across multiple sessions.
* **Human-like Behavior**:

  * Waits a random time before/after each view.
  * Attempts to click the play button manually.
  * Bypasses bot detection using `undetected_chromedriver`.
* **Custom Watch Duration**: Allows setting a specific watch time (10 to 600 seconds).
* **Configurable View Count**: Choose how many views to simulate (1 to 50).
* **Error Handling**: Displays user-friendly status and error messages in the Streamlit UI.

---

### 🧰 Tech Stack

* **Python 3**
* **Streamlit** – For building the web UI.
* **Selenium & Undetected ChromeDriver** – For browser automation.
* **Webshare Proxies (or similar)** – For IP rotation.

---

### 📁 Proxy File Format

The proxy list should be stored in a text file with each line in the following format:

```
ip:port:username:password
```

Example:

```
123.45.67.89:8080:user1:pass1
```


### ⚠️ Disclaimer

This project is intended for **educational purposes only**. Automating views may violate YouTube’s terms of service. Use responsibly.


