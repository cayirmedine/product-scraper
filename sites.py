# One entry per site. To add a new site, copy an entry and change the values.
#
# Required keys:
#   category_urls : list of listing pages to scrape
#   selectors     : CSS selectors for that site
#       card      -> product links on the listing page
#       name      -> product name on the product page
#       gallery   -> product images on the product page
# Optional selectors:
#       description -> left empty in the CSV if missing
#       next_page          -> "next" link for pagination (omit if no pagination)
#       cookie_button      -> cookie consent button to click once

SITES = {
    "nuova_fima": {
        "category_urls": [
            "https://www.nuovafima.com/en/categoria/bourdon-tube-pressure-gauge-en/",
            "https://www.nuovafima.com/en/categoria/special-pressure-gauge/",
            "https://www.nuovafima.com/en/categoria/pressure-switches/",
            "https://www.nuovafima.com/en/categoria/diaphragm-seals-en/",
            "https://www.nuovafima.com/en/categoria/components-and-accessories/",
            "https://www.nuovafima.com/en/categoria/thermometers/",
            "https://www.nuovafima.com/en/categoria/electronic-transmitters/",
            "https://www.nuovafima.com/en/categoria/thermowells/"
        ],
        "image_url_remove": r"-\d+x\d+(?=\.\w+$)",
        "selectors": {
            "card": "#output > article > h2 > a",
            "name": "#content > article > section > header > h1",
            "description": "#content > article > section > header > p",
            "gallery": "#thumbs img, #content > article > aside > figure > a > img",
            "cookie_button": "#onetrust-accept-btn-handler",
            "next_page": ".pagenav.top a.next",
            "files": {
                "row": "#files tbody tr",
                "title": "td:nth-child(2)",
                "link": "td:nth-child(3) a.file",
                "filter_cell": "td:nth-child(1)",      # NAME column
                "filter_prefix": "Data Sheet",         # keep only rows whose NAME starts with this
            },
        },
    },
}