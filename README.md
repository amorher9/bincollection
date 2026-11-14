# My bin collection day

A Streamlit app that automatically looks up a privately configured address on
Cheshire East Council's website. It shows the street name, consultation date and
time, next collection, and the council's original collection details.

The postcode and house number are not entered or displayed on the main screen.
They are read from Streamlit Secrets and sent to the council for the lookup.

## What each file does

| File | Purpose | Upload to GitHub? |
| --- | --- | --- |
| [app.py](app.py) | Streamlit entry point. Reads private address settings, handles refreshes and errors, and displays the results. | Required |
| [collection_lookup.py](collection_lookup.py) | Searches for the address, refuses ambiguous matches, retrieves collection dates, and prepares the council HTML with street-only headings and without its scripts. | Required |
| [requirements.txt](requirements.txt) | Pins the three direct Python dependencies installed by Streamlit Community Cloud. | Required |
| [.gitignore](.gitignore) | Excludes local address settings, the virtual environment, and Python/test caches from Git. | Strongly recommended |
| [README.md](README.md) | This file: explains the application, files, setup, and deployment. | Recommended |
| [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) | Safe template with placeholders; contains no real address. | Recommended |
| [test_collection_lookup.py](test_collection_lookup.py) | Offline tests for lookup requests, HTML rendering, street-only headings, refreshes, dates, and errors. | Recommended; not required to run the app |
| `.streamlit/secrets.toml` | Your real postcode and house number for local use. | **Never upload** |
| `.venv/` | Locally installed Python interpreter and packages. Cloud creates its own environment. | **Do not upload** |
| `__pycache__/`, `.pytest_cache/` | Generated Python and test caches. | **Do not upload** |

The old `packages.txt` has been removed. The app does not need additional Linux
packages: Chromium, Firefox, browser drivers, and Selenium are no longer used.
Do not upload an old copy of that file.

## Files to put in the GitHub repository

Keep this structure at the repository root:

```text
your-repository/
|-- app.py
|-- collection_lookup.py
|-- requirements.txt
|-- .gitignore
|-- README.md
|-- test_collection_lookup.py
`-- .streamlit/
    `-- secrets.toml.example
```

Only the first three files are needed to run the app; the others make the
repository safer and easier to maintain. GitHub's file list may not show
`.gitignore` or `.streamlit/` in some local file pickers because their names
start with a dot. Make sure to include them.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository, preferably private because this is a personal
   address lookup. Upload the files listed above. Do not upload your real
   `secrets.toml` file, even to a private repository.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and connect
   your GitHub account.
3. Choose **Create app**, select your repository and branch, and set the main
   file path to `app.py`.
4. Open **Advanced settings** and choose **Python 3.12**, matching the Python
   version used for this application.
5. In **Secrets**, paste the following and replace the placeholders:

   ```toml
   [address]
   postcode = "YOUR_POSTCODE"
   house = "YOUR_HOUSE_NUMBER_OR_NAME"
   ```

   Keep both values in quotes, including a numeric house number. You can also
   copy your existing local secrets file into this private settings field.
   Do not paste the real values into GitHub files or the README.
6. Save the settings and deploy. Cloud installs the pinned Python dependencies.
   A separate browser installation and `packages.txt` are not needed.
7. Check the app's **Settings > Sharing** and restrict viewing to specific
   people if you do not want the results to be public.

You can change the address later in the deployed app's **Settings > Secrets**.
After saving changes, reload the app and check the new results.

### Privacy when publishing

Keeping the address in Secrets protects its configuration, not the information
the app sends to viewers. Anyone allowed to view the app sees collection results
for the configured property. Although visible headings show only the street,
the embedded council HTML and calendar download can still contain property
identifiers or the full address. **This app is not an anonymisation tool.**
Use restricted app access for a personal lookup.

## Run locally

Use Python 3.12. From the repository directory:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

For a new checkout, copy `.streamlit/secrets.toml.example` to
`.streamlit/secrets.toml` and replace its placeholders with your real values.
If you already have a local secrets file, keep it; do not overwrite it with
the template.

```bash
python -m streamlit run app.py
```

The existing local virtual environment is not uploaded or reused by Cloud.
For a clean dependency check, use a new virtual environment instead of one
containing the old Selenium packages.

## How the app works

1. Reads `postcode` and `house` from the private `[address]` settings.
2. Sends the same address search request used by the council's website.
3. Continues only if exactly one address matches; it never guesses a property.
4. Retrieves and parses the council's collection dates.
5. Calculates today's status and the next collection using UK time.
6. Displays a fetched copy of the council's results with its layout and
   street-only headings, rather than opening a separate browser.

Results are kept only in the current Streamlit session. **Check collection
dates** fetches fresh results. A rerun on a new UK date also refreshes them.
Leaving a tab open does not continuously poll the council or automatically
update at midnight.

This depends on the council website remaining available and retaining its
current form and HTML structure. Errors are displayed instead of substituting
old results. The embedded page uses the council's external styles and images;
it is a fetched view, not a fully interactive copy of the council website.

## Dependencies and tests

- **Streamlit** provides the web app, private settings, session state, and
  embedded results view.
- **Requests** makes the council lookup requests with timeouts and HTTP checks.
- **Beautiful Soup** reads the HTML, extracts dates, and prepares the results
  for display.

Python's `datetime`, `zoneinfo`, `re`, `pathlib`, and `unittest` modules are built
in and do not belong in `requirements.txt`. Dependencies required internally
by Streamlit, such as pandas, are installed automatically.

Run the offline tests after installing the application requirements:

```bash
python -m unittest -v test_collection_lookup
```

The tests use made-up addresses and mocked council responses, so they do not
need your real secrets or contact the council.

## Official deployment references

- [Cloud dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)
- [Cloud secrets management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Deploy a Community Cloud app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Control app sharing](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app)
