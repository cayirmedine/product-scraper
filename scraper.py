import re
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import config

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")

def create_driver():
    options = Options()
    if config.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)


def lazy_scroll(driver, step=800, pause=0.7):
    """Scrolls to the bottom so lazy-loaded content gets loaded."""
    last = -1
    while True:
        driver.execute_script(f"window.scrollBy(0, {step});")
        time.sleep(pause)
        position = driver.execute_script("return window.scrollY + window.innerHeight")
        if position == last:
            break
        last = position


def accept_cookies(driver, selectors):
    """Clicks the cookie banner if the site defines one."""
    selector = selectors.get("cookie_button")
    if not selector:
        return
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        ).click()
    except TimeoutException:
        pass


def collect_product_links(driver, url, selectors):
    links = []
    driver.get(url)
    accept_cookies(driver, selectors)

    for page in range(1, config.MAX_PAGES + 1):
        try:
            WebDriverWait(driver, config.TIMEOUT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selectors["card"]))
            )
        except TimeoutException:
            print(f"  Page {page}: no product cards found")
            break

        lazy_scroll(driver)
        for a in driver.find_elements(By.CSS_SELECTOR, selectors["card"]):
            href = a.get_attribute("href")
            if href and href not in links:
                links.append(href)
        print(f"  Page {page} done, {len(links)} links in total")

        next_selector = selectors.get("next_page")
        if not next_selector:
            break
        next_links = driver.find_elements(By.CSS_SELECTOR, next_selector)
        href = next_links[0].get_attribute("href") if next_links else None
        if not href:
            break
        driver.get(href)
        time.sleep(config.DELAY)

    return links


def _text(driver, selector):
    if not selector:
        return ""
    elements = driver.find_elements(By.CSS_SELECTOR, selector)
    return elements[0].text.strip() if elements else ""


def _image_url(img):
    # Lazy-loading sites usually keep the real URL in data-src or srcset
    for attr in ("href","data-src", "data-original", "data-zoom-image", "src"):
        url = img.get_attribute(attr)
        if url and not url.startswith("data:"):
            return url
    srcset = img.get_attribute("srcset")
    if srcset:
        return srcset.split(",")[-1].strip().split(" ")[0]  # largest size
    return None


def scrape_product(driver, url, selectors):
    driver.get(url)
    WebDriverWait(driver, config.TIMEOUT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selectors["name"]))
    )
    lazy_scroll(driver)

    image_urls = []
    for img in driver.find_elements(By.CSS_SELECTOR, selectors["gallery"]):
        image_url = _image_url(img)
        if image_url and image_url not in image_urls:
            image_urls.append(image_url)

    return {
        "name": _text(driver, selectors["name"]),
        "price": _text(driver, selectors.get("price")),
        "description": _text(driver, selectors.get("description")),
        "url": url,
        "image_urls": image_urls,
    }


def safe_filename(name):
    """Keeps the product name readable, only removes characters Windows doesn't allow."""
    name = re.sub(r'[\\/:*?"<>|]', "", name)
    name = re.sub(r"\s+", " ", name).strip().rstrip(".")
    return name[:100] or "product"


def download_images(driver, product, folder):
    """Saves images as '<product name>.jpg', '<product name> 2.jpg', ..."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie["name"], cookie["value"])
    session.headers.update({
        "User-Agent": driver.execute_script("return navigator.userAgent"),
        "Referer": driver.current_url,
    })

    base = safe_filename(product["name"])
    files = []
    for i, url in enumerate(product["image_urls"], start=1):
        ext = Path(urlparse(url).path).suffix.lower()
        if ext not in IMAGE_EXTENSIONS:
            ext = ".jpg"
        filename = f"{base}{ext}" if i == 1 else f"{base} {i}{ext}"
        try:
            response = session.get(url, timeout=20)
            response.raise_for_status()
            (folder / filename).write_bytes(response.content)
            files.append(filename)
        except Exception as e:
            print(f"    Could not download image {url}: {e}")
    return files