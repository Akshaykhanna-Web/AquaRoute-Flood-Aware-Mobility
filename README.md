# AquaRoute 🌧️

**Hyperlocal flood-aware mobility and road-condition reporting**

AquaRoute is a student innovation project exploring how community-submitted, geo-tagged waterlogging observations and optional future sensor data could help commuters understand local road conditions during heavy rainfall.

## Current status

**Prototype / demonstration stage.** This repository contains a working local web demonstration with illustrative sample reports and locally stored user-submitted reports. It is not connected to live flood sensors, official warning systems, or verified real-time road-condition feeds.

## Features in this version

- Interactive Chennai map with severity-coloured report markers.
- Form to submit a location, coordinates, severity, estimated depth and notes.
- Local CSV storage for submitted reports.
- Dashboard metrics and a report register.
- Clear labelling of illustrative and unverified data.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL printed in the terminal (usually `http://localhost:8501`).

## Project structure

```text
AquaRoute/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Data and safety

- Rows marked `Sample data` are illustrative and must not be interpreted as real flood observations.
- User-submitted reports are unverified and stored locally in `reports.csv`.
- Coordinates are entered by the reporter; the app does not independently validate that a road is flooded.
- This prototype does not provide verified safe-route navigation or emergency warnings. Follow official instructions and local authorities.

## Planned next steps

- Validate reports with timestamps, moderation and expiry rules.
- Evaluate suitable public rainfall and flood data sources.
- Explore low-cost water-level sensor integration.
- Build a documented road-segment risk-scoring method.
- Test usability and classification performance using independently verified observations.

## Technology

Python, Streamlit, Pandas, Folium and Streamlit-Folium.

## Contribution and originality

This is an early-stage student project. Existing flood mapping and citizen-reporting solutions should be reviewed before making claims of novelty. No patent, deployment, user validation or measured impact is claimed.
