import argparse
import json
import time
from pathlib import Path

import config
from sites import SITES
from scraper import (create_driver, collect_product_links, scrape_product,
                     download_images, download_files)


def scrape_site(driver, site_name, site):
    selectors = site["selectors"]
    site_dir = Path(config.OUTPUT_DIR) / site_name
    image_dir = site_dir / "images"
    file_dir = site_dir / "files"
    json_file = site_dir / "products.json"
    site_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== {site_name} ===")
    links = []
    for category_url in site["category_urls"]:
        print(f"Category: {category_url}")
        for link in collect_product_links(driver, category_url, selectors, site.get("pagination")):
            if link not in links:
                links.append(link)
    print(f"{len(links)} products found")
    if config.MAX_PRODUCTS:
        links = links[:config.MAX_PRODUCTS]

    # utf-8-sig: Turkish characters display correctly when opened in Excel
    products = []
    for i, link in enumerate(links, start=1):
        try:
            product = scrape_product(driver, link, selectors, site.get("image_url_remove"))
            images = download_images(driver, product, image_dir)
            files = download_files(driver, product, file_dir)
            products.append({
                "name": product["name"],
                "url": product["url"],
                "image_names": images,
                "file_names": files,
            })
            json_file.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  [{i}/{len(links)}] {product['name']} ({len(images)} images, {len(files)} files)")
        except Exception as e:
            print(f"  [{i}/{len(links)}] Failed: {link} -> {e}")
        time.sleep(config.DELAY)

    print(f"Done: {json_file}")


def main():
    parser = argparse.ArgumentParser(description="Product scraper")
    parser.add_argument("sites", nargs="*", help="site names from sites.py (empty = all)")
    args = parser.parse_args()

    names = args.sites or list(SITES)
    unknown = [n for n in names if n not in SITES]
    if unknown:
        print(f"Unknown site(s): {', '.join(unknown)}")
        print(f"Available: {', '.join(SITES)}")
        return

    driver = create_driver()
    try:
        for name in names:
            try:
                scrape_site(driver, name, SITES[name])
            except Exception as e:
                print(f"Site {name} failed: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user. Rows scraped so far are saved in the CSV.")
    finally:
        try:
            driver.quit()
        except Exception:
            pass  # driver may already be closed after Ctrl+C


if __name__ == "__main__":
    main()