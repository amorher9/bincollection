from datetime import date, datetime
import re

import requests
from bs4 import BeautifulSoup

COLLECTION_URL = "https://online.cheshireeast.gov.uk/mycollectionday/"
SEARCH_URL = "https://online.cheshireeast.gov.uk/MyCollectionDay/SearchByAjax/Search"
RESULTS_URL = (
    "https://online.cheshireeast.gov.uk/MyCollectionDay/SearchByAjax/GetBartecJobList"
)


def lookup_collections(
    postcode: str, house: str
) -> tuple[str, list[tuple[date, str]], str]:
    if not postcode.strip() or not house.strip():
        raise ValueError("Enter both a postcode and a house number or name.")

    with requests.Session() as session:
        response = session.get(
            SEARCH_URL,
            params={"postcode": postcode.strip(), "propertyname": house.strip()},
            timeout=(10, 60),
        )
        response.raise_for_status()
        search = BeautifulSoup(response.text, "html.parser")
        error = search.select_one(".bg-danger")
        if error is not None:
            raise ValueError(error.get_text(" ", strip=True))

        addresses = search.select(
            ".get-job-details[data-uprn][data-onelineaddress]"
        )
        if not addresses:
            raise ValueError(
                "The council did not return an address. Check your details or "
                "open the council website to check whether its form has changed."
            )
        if len(addresses) != 1:
            raise ValueError(
                "More than one address matched. Enter the full house number "
                "or name so the app does not select the wrong property."
            )

        address = addresses[0]
        address_label = str(address["data-onelineaddress"])
        street_name = re.sub(
            rf"^{re.escape(house.strip())}(?:\s+|,\s*)",
            "",
            address_label,
            count=1,
            flags=re.IGNORECASE,
        ).split(",")[0].strip()
        response = session.get(
            RESULTS_URL,
            params={
                "uprn": str(address["data-uprn"]),
                "onelineaddress": address_label,
            },
            timeout=(10, 60),
        )
        response.raise_for_status()
        results_html = response.text
        response = session.get(COLLECTION_URL, timeout=(10, 60))
        response.raise_for_status()
        page_html = response.text

    results = BeautifulSoup(results_html, "html.parser")
    error = results.select_one(".bg-danger")
    if error is not None:
        raise ValueError(error.get_text(" ", strip=True))

    for heading in results.select("h3"):
        if heading.get_text(" ", strip=True) == address_label:
            heading.string = street_name

    rows = results.select("table.job-details tr.data-row")
    if not rows:
        raise ValueError(
            "The council returned no collection dates. Open its website to "
            "check for service notices or try again later."
        )

    collections = []
    for row in rows:
        labels = row.select("td.visible-cell label")
        if len(labels) != 3:
            raise ValueError("The council's collection table format has changed.")
        try:
            collection_date = datetime.strptime(
                labels[1].get_text(strip=True), "%d/%m/%Y"
            ).date()
        except ValueError as exc:
            raise ValueError(
                "The council returned an unrecognised collection date."
            ) from exc
        service = labels[2].get_text(" ", strip=True)
        if not service:
            raise ValueError("The council returned a collection without a bin type.")
        collections.append((collection_date, service))

    page = BeautifulSoup(page_html, "html.parser")
    panel = page.select_one(".results-div")
    if page.head is None or panel is None:
        raise ValueError(
            "The council's page layout has changed and could not be displayed."
        )
    base = page.new_tag("base", href=COLLECTION_URL)
    page.head.insert(0, base)
    article = page.select_one("article")
    if article is not None:
        article.decompose()
    panel.clear()
    panel["style"] = "display: block;"
    panel.append(results)
    # Display the fetched results without running the site's search or analytics.
    for script in page.select("script"):
        script.decompose()

    return street_name, sorted(collections), str(page)
