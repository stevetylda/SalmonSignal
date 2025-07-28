# SalmonSignal

**A spatiotemporal framework for modeling and forecasting salmon abundance in Puget Sound and the Pacific Northwest**

---

## Overview

**SalmonSignal** is a modular, data-driven system designed to estimate and predict salmon abundance and distribution on a fine temporal scale across spatial grids using the H3 hexagonal indexing system. The project integrates multiple data sources, including creel and catch card reports, environmental covariates, and spatial masking of restricted fishing areas, to provide robust and actionable predictions relevant for fisheries management and ecological research.

---

## Features

- **Spatiotemporal modeling** of salmon abundance at H3 grid resolution  
- Temporal prediction aggregated by **day-parts** (morning, afternoon, evening, night)  
- Forecasting horizon up to **7 days** into the future  
- Integration of heterogeneous data:  
  - Fishery-dependent data (creel and catch card surveys)  
  - Environmental covariates (sea surface temperature, salinity, bathymetry, etc.)  
  - Spatial masking for **restricted fishing zones** to address observation bias  
- Modular design allowing easy incorporation of new covariates or datasets  
- Compatibility with related ecosystem modeling projects (e.g., orca prey dynamics)  

---

## Data Sources

- **Fishery Data:** Washington Department of Fish and Wildlife (WDFW) creel and catch card datasets  
- **Environmental Data:** Remote sensing, ROMS model outputs (planned), in situ sensor data  
- **Spatial Framework:** Uber’s H3 grid system for spatial aggregation and indexing  
- **Regulatory Data:** Fishing closure zones and marine area regulations from WDFW  

---

## Installation

```bash
git clone https://github.com/your-org/salmon-signal.git
cd salmon-signal
conda create -n salmon-signal python=3.9
conda activate salmon-signal
pip install -r requirements.txt
```

---

## Usage
Data Preparation:
1. Ingest and preprocess fishery catch and creel data
    - Download and align environmental covariates with H3 grid cells
    - Apply spatial masks for fishing restrictions
2. Model Training:
    - Train predictive models using historical data filtered for observation bias
    - Utilize environmental and temporal features for abundance forecasting
3. Forecasting:
    - Generate 7-day ahead salmon abundance predictions
    - Aggregate predictions by day-part (morning, afternoon, evening, night)
4. Visualization & Analysis:
    - Export results for integration into dashboards or research tools
    - Support spatial and temporal uncertainty quantification

## Contributing

Contributions are welcome! Please follow standard GitHub pull request and code review protocols. Ensure all new code includes appropriate tests and documentation.

## License

MIT License

## Contact
Tyler (Data Scientist) — stevetylda@example.com
Project hosted by OrcaSound