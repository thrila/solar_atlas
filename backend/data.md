⚡ ~19 panels (6.65 kW system)
🌞 Produces ~9,700 kWh/year (~810/month)
📦 Roof area: ~32 m²
💵 Estimated cost: $13,965 (after 30% ITC)
📉 Payback: ~9–10 years at $0.15/kWh
🌍 Saves 3.9 tons CO₂/year (~97 trees or 9,360 miles)
Austin gets ~5.3 full sun hours/day. Data is based on NREL averages.


source to find data per country: https://ourworldindata.org/
Average Mean of Electricity a US house consumes anually = 10,791 kWh/year

| Component              | Qty | Unit Price | Estimated Total       |
| ---------------------- | --- | ---------- | --------------------- |
| 300 W Solar Panel      | 2   | \$161.79   | **\$323.58**          |
| 30 A MPPT Controller   | 1   | \$139.99   | **\$139.99**          |
| Battery Bank (≥ 5 kWh) | —   | \~\$4,000  | **\$4,000** (approx.) |
| Pure Sine Inverter     | 1   | \~\$800    | **\$800** (approx.)   |
| Mounting & Wiring Kit  | —   | \~\$300    | **\$300** (approx.)   |
| **Total Estimate**     | —   | —          | **≈ \$5,500**         |


app/
├── api/
│   ├── v1/
│   │   ├── endpoints.py     # All routes
│   │   └── __init__.py
│   └── __init__.py
├── core/
│   ├── logic.py             # Business logic (solar calcs, etc)
│   └── geo_utils.py         # Geocoding helper (get_lon_lat)
├── db/
│   ├── db_utils.py          # SQLite connection logic
│   └── __init__.py
├── main.py                  # App entrypoint
└── __init__.py

## User Input
- Location 
- Panel power output
- number of panels.

add output per panel  in response
