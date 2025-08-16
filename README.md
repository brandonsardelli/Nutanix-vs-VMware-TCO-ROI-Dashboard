# Nutanix-vs-VMware-TCO-ROI-Dashboard
Interactive dashboard comparing Nutanix and VMware costs using real-world data patterns. 


Overview

Interactive dashboard comparing Nutanix and VMware costs using real-world data patterns. Visualizes:
3-year TCO comparison
ROI projections
Deal registration impact
Features
Adjust cost parameters dynamically
Save comparison scenarios
Generate shareable reports

Setup
pip install streamlit pandas matplotlib
streamlit run tco_calculator.py

Usage
Adjust the sliders in the sidebar to match customer environment parameters. View savings metrics in real-time.

graph TD
    A[User Inputs Parameters] --> B[Calculate VMware Costs]
    A --> C[Calculate Nutanix Costs]
    B --> D[Generate Comparison Metrics]
    C --> D
    D --> E[Visualize Cost Breakdown]
    D --> F[Calculate Partner Incentives]
    F --> G[Output PDF/Shareable Report]
