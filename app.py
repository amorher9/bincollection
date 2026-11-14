"""Use a privately configured address to display the council's collection results."""

from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import streamlit as st
import streamlit.components.v1 as components

from collection_lookup import lookup_collections

st.title("My bin collection day")

# st.secrets reads Cloud app settings or the local .streamlit/secrets.toml file.
try:
    saved_address = st.secrets["address"]
    postcode = saved_address["postcode"].strip()
    house = saved_address["house"].strip()
except (FileNotFoundError, KeyError):
    st.error(
        "Configure an [address] section with postcode and house values in "
        "Streamlit Community Cloud's app settings > Secrets, or in "
        ".streamlit/secrets.toml when running locally."
    )
    st.stop()

refresh = st.button("Check collection dates")
# Use UK dates even when the hosting server's clock is set to UTC.
today = datetime.now(ZoneInfo("Europe/London")).date()
lookup_key = (postcode, house, today)
# Reuse results within this session until refresh, an address change, or a new day.
if (
    refresh
    or st.session_state.get("lookup_key") != lookup_key
    or "council_street_page" not in st.session_state
):
    # Clear old results first so a failed refresh cannot display a stale schedule.
    st.session_state.pop("collection_result", None)
    st.session_state.pop("council_street_page", None)
    st.session_state.pop("lookup_key", None)
    try:
        with st.spinner("Finding your address and checking collection dates..."):
            result = lookup_collections(postcode, house)
    except requests.RequestException:
        st.error(
            "Could not retrieve collection dates from the council. Check your "
            "internet connection or try again later."
        )
        st.stop()
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    address, collections, council_page = result
    st.session_state.collection_result = (address, collections)
    st.session_state.council_street_page = council_page
    st.session_state.lookup_key = lookup_key
    st.session_state.checked_at = datetime.now(ZoneInfo("Europe/London"))

# Ignore past collections when calculating today's status and the next pickup.
address, collections = st.session_state.collection_result
upcoming = [(day, service) for day, service in collections if day >= today]
st.subheader(address)
st.caption(
    "Consultation date: "
    f"{st.session_state.checked_at:%A %d/%m/%Y %H:%M:%S %Z}."
)

if not upcoming:
    st.warning(
        "The council returned no dates for today or later. Check its website "
        "for the latest schedule."
    )
else:
    due_today = [service for day, service in upcoming if day == today]
    if due_today:
        st.success("Collection scheduled today: " + ", ".join(due_today))
    else:
        st.info("No collection is listed for today.")

    next_date = upcoming[0][0]
    next_services = [service for day, service in upcoming if day == next_date]
    st.write(
        f"**Next collection: {next_date:%A %d/%m/%Y}** - "
        + ", ".join(next_services)
    )

st.caption(
    "Council results fetched at the time shown above, displayed with the "
    "council's layout. Use 'Check collection dates' to reload them."
)
# Keep the council's layout separate from Streamlit's page styles.
components.html(st.session_state.council_street_page, height=1050, scrolling=True)
