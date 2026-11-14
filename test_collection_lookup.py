from datetime import date, datetime, timedelta
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup
from streamlit.testing.v1 import AppTest

from collection_lookup import lookup_collections

ADDRESS_HTML = """
<a class="get-job-details" data-uprn="123"
   data-onelineaddress="Example address">View collections</a>
"""
COLLECTION_HTML = """
<table class="job-details">
  <tr class="spacer-row"><td></td></tr>
  <tr class="data-row"><td class="visible-cell">
    <label>Thursday</label><label>26/11/2026</label><label>General Waste</label>
  </td></tr>
  <tr class="data-row"><td class="visible-cell">
    <label>Thursday</label><label>19/11/2026</label><label>Mixed Recycling</label>
  </td></tr>
</table>
<table class="full-job-list-for-posting">
  <tr class="data-row"><td>Hidden historical data</td></tr>
</table>
"""
APP_PATH = Path(__file__).with_name("app.py")
PAGE_HTML = """
<html><head><link rel="stylesheet" href="/MyCollectionDay/Content/css">
<script src="/analytics.js"></script></head><body>
<header>Council header</header>
<article><form id="search-form">Find your address</form></article>
<div class="results-div" style="display:none"></div>
</body></html>
"""


class LookupTests(TestCase):
    def setUp(self):
        patcher = patch("collection_lookup.requests.Session")
        self.session = patcher.start().return_value.__enter__.return_value
        self.addCleanup(patcher.stop)

    def responses(self, *pages):
        self.session.get.side_effect = [Mock(text=page) for page in pages]

    def test_selects_unique_address_and_parses_visible_dates_in_order(self):
        self.responses(ADDRESS_HTML, COLLECTION_HTML, PAGE_HTML)
        address, collections, page_html = lookup_collections(" TEST ", " 12 ")
        self.assertEqual(address, "Example address")
        self.assertEqual(
            collections,
            [
                (date(2026, 11, 19), "Mixed Recycling"),
                (date(2026, 11, 26), "General Waste"),
            ],
        )
        self.assertEqual(
            self.session.get.call_args_list[0].kwargs["params"],
            {"postcode": "TEST", "propertyname": "12"},
        )
        self.assertEqual(
            self.session.get.call_args_list[1].kwargs["params"],
            {"uprn": "123", "onelineaddress": "Example address"},
        )
        page = BeautifulSoup(page_html, "html.parser")
        self.assertIn("Council header", page.get_text())
        self.assertEqual(
            page.select_one("base")["href"],
            "https://online.cheshireeast.gov.uk/mycollectionday/",
        )
        self.assertEqual(
            page.select_one("link[rel=stylesheet]")["href"],
            "/MyCollectionDay/Content/css",
        )
        self.assertEqual(len(page.select(".results-div .job-details .data-row")), 2)
        self.assertEqual(page.select_one(".results-div")["style"], "display: block;")
        self.assertFalse(page.select("script, #search-form"))

    def test_does_not_guess_an_ambiguous_address(self):
        self.responses(ADDRESS_HTML * 2)
        with self.assertRaisesRegex(ValueError, "More than one"):
            lookup_collections("TEST", "12")
        self.assertEqual(self.session.get.call_count, 1)

    def test_displays_only_street_but_uses_full_address_for_lookup(self):
        for house, full_address, street in [
            ("12", "12 EXAMPLE STREET, AB1 2CD", "EXAMPLE STREET"),
            ("12A", "12A 2ND AVENUE, AB1 2CD", "2ND AVENUE"),
            ("Rose Cottage", "ROSE COTTAGE, EXAMPLE ROAD, AB1 2CD", "EXAMPLE ROAD"),
        ]:
            with self.subTest(house=house):
                search = ADDRESS_HTML.replace("Example address", full_address)
                results = f"<h3>{full_address}</h3>" + COLLECTION_HTML
                self.responses(search, results, PAGE_HTML)
                label, _, page_html = lookup_collections("AB1 2CD", house)
                self.assertEqual(label, street)
                page = BeautifulSoup(page_html, "html.parser")
                self.assertEqual(page.select_one(".results-div h3").text, street)
                self.assertNotIn(full_address, page.get_text())
                self.assertEqual(
                    self.session.get.call_args_list[-2].kwargs["params"]
                    ["onelineaddress"],
                    full_address,
                )

    def test_reports_council_errors(self):
        self.responses('<p class="bg-danger">No Matches found</p>')
        with self.assertRaisesRegex(ValueError, "No Matches"):
            lookup_collections("TEST", "12")

    def test_rejects_missing_or_changed_collection_results(self):
        for result in ("<p>Unavailable</p>", COLLECTION_HTML.replace("19/11/2026", "bad")):
            with self.subTest(result=result):
                self.responses(ADDRESS_HTML, result, PAGE_HTML)
                with self.assertRaises(ValueError):
                    lookup_collections("TEST", "12")

    def test_changed_page_layout_is_reported(self):
        self.responses(ADDRESS_HTML, COLLECTION_HTML, "<html><head></head></html>")
        with self.assertRaisesRegex(ValueError, "page layout has changed"):
            lookup_collections("TEST", "12")

    def test_http_errors_are_not_treated_as_results(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("Unavailable")
        self.session.get.return_value = response
        with self.assertRaises(requests.HTTPError):
            lookup_collections("TEST", "12")

    def test_empty_input_is_not_sent(self):
        with self.assertRaisesRegex(ValueError, "Enter both"):
            lookup_collections(" ", "12")
        self.session.get.assert_not_called()


class AppTests(TestCase):
    def app(self):
        app = AppTest.from_file(str(APP_PATH), default_timeout=15)
        app.secrets["address"] = {"postcode": "TEST", "house": "12"}
        return app

    def test_missing_address_explains_cloud_and_local_configuration(self):
        app = self.app()
        app.secrets["address"] = {}
        with patch("collection_lookup.lookup_collections") as lookup:
            app.run()
            self.assertFalse(app.exception)
            self.assertIn("Cloud's app settings > Secrets", app.error[0].value)
            self.assertIn(".streamlit/secrets.toml", app.error[0].value)
            self.assertEqual(len(app.get("iframe")), 0)
            lookup.assert_not_called()

    def test_automatically_checks_today_and_refreshes(self):
        today = datetime.now(ZoneInfo("Europe/London")).date()
        with patch(
            "collection_lookup.lookup_collections",
            return_value=(
                "Example address", [(today, "Mixed Recycling")], PAGE_HTML
            ),
        ) as lookup:
            app = self.app().run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.text_input), 0)
            self.assertIn("Consultation date:", app.caption[0].value)
            self.assertIn(f"{today:%d/%m/%Y}", app.caption[0].value)
            self.assertIn("Collection scheduled today", app.success[0].value)
            self.assertIn(
                f"Next collection: {today:%A %d/%m/%Y}", app.markdown[0].value
            )
            self.assertEqual(len(app.table), 0)
            self.assertEqual(app.get("iframe")[0].proto.srcdoc, PAGE_HTML)
            lookup.assert_called_once_with("TEST", "12")
            app.run()
            self.assertEqual(lookup.call_count, 1)
            app.button[0].click().run()
            self.assertFalse(app.exception)
            self.assertEqual(lookup.call_count, 2)

    def test_network_failure_clears_previous_results(self):
        today = datetime.now(ZoneInfo("Europe/London")).date()
        with patch(
            "collection_lookup.lookup_collections",
            side_effect=[
                ("Example address", [(today, "Mixed Recycling")], PAGE_HTML),
                requests.Timeout("Unavailable"),
            ],
        ):
            app = self.app().run()
            app.button[0].click().run()
            self.assertFalse(app.exception)
            self.assertIn("Could not retrieve", app.error[0].value)
            self.assertEqual(len(app.table), 0)
            self.assertEqual(len(app.get("iframe")), 0)

    def test_past_dates_are_excluded_and_no_collection_today_is_explicit(self):
        today = datetime.now(ZoneInfo("Europe/London")).date()
        with patch(
            "collection_lookup.lookup_collections",
            return_value=(
                "Example address",
                [
                    (today - timedelta(days=1), "General Waste"),
                    (today + timedelta(days=1), "Mixed Recycling"),
                ],
                PAGE_HTML,
            ),
        ):
            app = self.app().run()
            self.assertFalse(app.exception)
            self.assertEqual(app.info[0].value, "No collection is listed for today.")
            self.assertIn("Mixed Recycling", app.markdown[-1].value)
            self.assertNotIn("General Waste", app.markdown[-1].value)
