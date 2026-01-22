# tools/logo_fetcher.py
import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings
from urllib.parse import urljoin, urlparse
from pathlib import Path
from loguru import logger
from src.utils.config import IntentHQConfig
intenthq_cfg = IntentHQConfig()

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# tools/logo_fetcher.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
from PIL import Image
from io import BytesIO

VALID_FORMATS = ["png", "jpeg", "jpg", "gif", "bmp", "tiff"]

def save_image_bytes(content, save_path):
    img = Image.open(BytesIO(content))
    img.save(save_path)
    return save_path

def fetch_logo(url, save_path):
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    # 1. favicon
    icon = soup.find("link", rel=lambda x: x and "icon" in x.lower())
    if icon and icon.get("href"):
        logo_url = urljoin(url, icon["href"])
    else:
        # 2. <img> with "logo"
        img = soup.find("img", src=lambda x: x and "logo" in x.lower())
        if img and img.get("src"):
            logo_url = urljoin(url, img["src"])
        else:
            return None

    # Download logo
    r = requests.get(logo_url, timeout=10)
    content_type = r.headers.get("Content-Type", "").lower()

    # ICO → convert to PNG
    if "ico" in content_type or logo_url.endswith(".ico"):
        return save_image_bytes(r.content, save_path)

    # Unsupported formats (SVG, WEBP)
    if not any(fmt in content_type for fmt in VALID_FORMATS):
        return None

    return save_image_bytes(r.content, save_path)

def fetch_prospect_logo(prospect_url: str, save_path: str = "presentations/logos/prospect_logo.png") -> str:
    try:
        logger.info(f"Fetching Prospect logo from {prospect_url}")
        logo_path = fetch_logo(prospect_url, save_path)
        if logo_path:
            return logo_path
    except Exception as e:
        logger.warning(f"Error fetching Prospect logo: {e}")
        logger.info("Using fallback IntentHQ logo")
    return intenthq_cfg.logo_path  # fallback to local logo

def fetch_intenthq_logo(save_path="presentations/logos/intenthq_logo.png") -> str:
    try:
        url = "https://intenthq.com/"
        logger.info(f"Fetching IntentHQ logo from {url}")
        logo_path = fetch_logo(url, save_path)
        if logo_path:
            return logo_path
    except Exception as e:
        logger.warning(f"Error fetching IntentHQ logo: {e}")
        logger.info("Using fallback IntentHQ logo")
    return intenthq_cfg.logo_path  # fallback to local logo