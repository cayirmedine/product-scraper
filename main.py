import argparse
import csv
import time
from pathlib import Path

import config
from sites import SITES
from scraper import create_driver, collect_product_links, scrape_product, download_images

COLUMNS = ["name", "description", "url", "image_urls", "image_files"]


def scrape_site(driver, site_name, site):
    selectors = site["selectors"]
    site_dir = Path(config.OUTPUT_DIR) / site_name
    image_dir = site_dir / "images"
    csv_file = site_dir / "products.csv"
    site_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== {site_name} ===")
    links = []
    for category_url in site["category_urls"]:
        print(f"Category: {category_url}")
        for link in collect_product_links(driver, category_url, selectors):
            if link not in links:
                links.append(link)
    print(f"{len(links)} products found")

    # utf-8-sig: Turkish characters display correctly when opened in Excel
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()

        for i, link in enumerate(links, start=1):
            try:
                product = scrape_product(driver, link, selectors, site.get("image_url_remove"))
                files = download_images(driver, product, image_dir)
                writer.writerow({
                    **product,
                    "image_urls": " | ".join(product["image_urls"]),
                    "image_files": " | ".join(files),
                })
                f.flush()  # write each row immediately, nothing lost on crash
                print(f"  [{i}/{len(links)}] {product['name']} ({len(files)} images)")
            except Exception as e:
                print(f"  [{i}/{len(links)}] Failed: {link} -> {e}")
            time.sleep(config.DELAY)

    print(f"Done: {csv_file}")


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
    finally:
        driver.quit()


if __name__ == "__main__":
    main()