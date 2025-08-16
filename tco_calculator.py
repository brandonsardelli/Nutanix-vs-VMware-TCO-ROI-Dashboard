# pip install streamlit pandas matplotlib 
# streamlit run tco_calculator.py

import streamlit as st
import matplotlib.pyplot as plt

# Initialize session state
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = []

st.title("Nutanix Competitive Displacement Dashboard")
st.caption("Real-time TCO/ROI Analysis vs VMware")

with st.sidebar:
    st.header("Environment Parameters")
    vm_count = st.slider("Virtual Machines", 50, 1000, 250)
    storage_tb = st.slider("Storage (TB)", 10, 500, 100)
    admin_count = st.slider("IT Admins", 2, 20, 5)
    st.divider()
    deal_size = st.number_input("Deal Size ($)", 50000, 10000000, 500000)
    partner_tier = st.selectbox("Partner Tier", ["Authorized", "Premier", "Elite"])
    has_bdf = st.checkbox("Includes BDF Bonus?")  # NEW

# TCO Calculation Logic
def calculate_tco(vm_count, storage_tb, admin_count):
    vmware_annual = {
        'licensing': vm_count * 3500,
        'hardware': vm_count * 4000,
        'storage': storage_tb * 2500,
        'admin': admin_count * 120000,
        'maint': vm_count * 1000
    }
    nutanix_annual = {
        'licensing': vm_count * 2000,
        'hardware': vm_count * 3500,
        'storage': storage_tb * 1800,
        'admin': admin_count * 75000,
        'maint': vm_count * 600
    }
    # Return 3-year totals
    return sum(vmware_annual.values()) * 3, sum(nutanix_annual.values()) * 3

vmware_tco, nutanix_tco = calculate_tco(vm_count, storage_tb, admin_count)
savings = vmware_tco - nutanix_tco
roi = (savings / vmware_tco) * 100

# Deal Registration Impact - FIXED
tier_multipliers = {"Authorized": 0.05, "Premier": 0.10, "Elite": 0.15}
bdf_bonus = 0.03 if has_bdf else 0  # NEW
partner_incentive = deal_size * (tier_multipliers[partner_tier] + bdf_bonus)  # FIXED

# Display Metrics - STANDARDIZED
col1, col2, col3 = st.columns(3)
col1.metric("3-Yr VMware TCO", f"${vmware_tco/1000000:.1f}M")
col2.metric("3-Yr Nutanix TCO", f"${nutanix_tco/1000000:.1f}M", f"-{roi:.1f}%")
col3.metric("Partner Incentive", f"${partner_incentive/1000000:.1f}M")  # Now in millions

# Visualization - 3-YEAR COSTS
fig, ax = plt.subplots()
categories = ['Licensing', 'Hardware', 'Storage', 'Admin', 'Maintenance']

# Calculate 3-year costs per category
vmware_3yr = [
    vm_count * 3500 * 3,
    vm_count * 4000 * 3,
    storage_tb * 2500 * 3,
    admin_count * 120000 * 3,
    vm_count * 1000 * 3
]

nutanix_3yr = [
    vm_count * 2000 * 3,
    vm_count * 3500 * 3,
    storage_tb * 1800 * 3,
    admin_count * 75000 * 3,
    vm_count * 600 * 3
]

ax.bar(categories, vmware_3yr, label='VMware')
ax.bar(categories, nutanix_3yr, label='Nutanix', alpha=0.7)
ax.set_ylabel('3-Year Cost ($)')
ax.legend()
st.pyplot(fig)

# Save scenario
if st.button("Save Current Scenario"):
    scenario = {
        'vm_count': vm_count,
        'storage_tb': storage_tb,
        'savings': savings,
        'roi': roi
    }
    st.session_state.scenarios.append(scenario)
    st.success("Scenario saved!")
