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
    "senseca": {
        "category_urls": [
            "https://www.senseca.com/en/products/process-automation/flow",
            "https://www.senseca.com/en/products/process-automation/level",
            "https://www.senseca.com/en/products/process-automation/pressure",
            "https://www.senseca.com/en/products/process-automation/temperature",
            "https://www.senseca.com/en/products/process-automation/liquid-analysis",
            "https://www.senseca.com/en/products/process-automation/gas-analysis",
            "https://www.senseca.com/en/products/process-automation/electronics",
            "https://www.senseca.com/en/products/process-automation/digital-communication",
            "https://www.senseca.com/en/products/process-automation/monitoring-data-acquisition-systems",
            "https://www.senseca.com/en/products/process-automation/apps-software",
            "https://www.senseca.com/en/products/process-automation/filters",
            "https://www.senseca.com/en/products/process-automation/accessories",
        ],
        "selectors": {
            "card": "#products > div > div.product-teaser-grid__grid > a",
            "name": ".product-hero__content h1",
            "gallery": ".media-gallery__main-slide img",
            "cookie_button": "#onetrust-accept-btn-handler",
            "next_page": ".load-more__button-wrapper button",
            "files": {
                "row": "[id$='-panel-downloads'] ul > li",           # each download item
                "title": ".object-list-item__meta-title",            # "Data sheet" -> used in file name
                "filter_cell": ".object-list-item__meta-title",      # keep only rows where this...
                "filter_prefix": "Data sheet",                       # ...starts with "Data sheet"
                "lang_cell": ".object-list-item__list > h5",         # "(EN)" in this text -> "en"
                "link": "a",                                         # download link inside the item
            },
        }
    },
    "holmatro": {
        "category_urls": [
            "https://www.holmatro.com/hydraulic-solutions/lifting/hydraulic-cylinders/",
            "https://www.holmatro.com/hydraulic-solutions/lifting/hydraulic-pumps/",
            "https://www.holmatro.com/hydraulic-solutions/lifting/flowpanels-valve-blocks/",
            "https://www.holmatro.com/hydraulic-solutions/lifting/hydraulic-hoses/",
            "https://www.holmatro.com/hydraulic-solutions/lifting/hydraulic-system-components/",
            "https://www.holmatro.com/hydraulic-solutions/lifting/other-lifting-tools/",
            "https://www.holmatro.com/hydraulic-solutions/heavy-lifting-transportation-systems/skidding-systems/",
            "https://www.holmatro.com/hydraulic-solutions/heavy-lifting-transportation-systems/ring-climbing-cylinder-set/",
            "https://www.holmatro.com/hydraulic-solutions/heavy-lifting-transportation-systems/step-jacks/",
            "https://www.holmatro.com/hydraulic-solutions/heavy-lifting-transportation-systems/split-flow-pump-4-outlets/",
            "https://www.holmatro.com/hydraulic-solutions/heavy-lifting-transportation-systems/offshore-wind-systems-services/",
            "https://www.holmatro.com/hydraulic-solutions/rerailing-vehicle-recovery/lifting-sliding-components/",
            "https://www.holmatro.com/hydraulic-solutions/rerailing-vehicle-recovery/operational-components/",
            "https://www.holmatro.com/hydraulic-solutions/rerailing-vehicle-recovery/compact-rerailing-unit/",
            "https://www.holmatro.com/hydraulic-solutions/cutting/hydraulic-cutters/",
            "https://www.holmatro.com/hydraulic-solutions/cutting/hydraulic-pumps/",
            "https://www.holmatro.com/hydraulic-solutions/cutting/hydraulic-hoses/",
            "https://www.holmatro.com/hydraulic-solutions/cutting/accessories/"
        ],
        "selectors": {
            "card": ".product-card-wrapper a",
            "name": ".product-hero h1",
            "gallery": ".swiper-thumbs__slide img",
            "cookie_button": "#onetrust-accept-btn-handler",
            "next_page": ".archive-product__pagination a.next",
            "image_url_remove": r"-\d+x\d+(?=\.\w+$)",
            "files": {
                "row": "#downloads > div > div",
                "filter_cell": ".asset__title",
                "filter_suffix": "Spec sheet, A4 metric",
                "link": ".asset__content a",
                "label": "Spec_sheet",
            },
        }
    }
}