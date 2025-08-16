import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = []

st.title("Nutanix Competitive Displacement Dashboard")
st.caption("Real-time TCO/ROI Analysis vs VMware")

# Input parameters
with st.sidebar:
    st.header("Environment Parameters")
    vm_count = st.slider("Virtual Machines", 50, 1000, 250)
    storage_tb = st.slider("Storage (TB)", 10, 500, 100)
    admin_count = st.slider("IT Admins", 2, 20, 5)
    st.divider()
    deal_size = st.number_input("Deal Size ($)", 50000, 10000000, 500000)
    partner_tier = st.selectbox("Partner Tier", ["Authorized", "Premier", "Elite"])

# TCO Calculation Logic
def calculate_tco(vm_count, storage_tb, admin_count):
    vmware_costs = {
        'licensing': vm_count * 3500,
        'hardware': vm_count * 4000,
        'storage': storage_tb * 2500,
        'admin': admin_count * 120000,
        'maint': vm_count * 1000
    }
    nutanix_costs = {
        'licensing': vm_count * 2000,
        'hardware': vm_count * 3500,
        'storage': storage_tb * 1800,
        'admin': admin_count * 75000,
        'maint': vm_count * 600
    }
    return sum(vmware_costs.values()) * 3, sum(nutanix_costs.values()) * 3

vmware_tco, nutanix_tco = calculate_tco(vm_count, storage_tb, admin_count)
savings = vmware_tco - nutanix_tco
roi = (savings / vmware_tco) * 100

# Deal Registration Impact
tier_multipliers = {"Authorized": 0.05, "Premier": 0.10, "Elite": 0.15}
partner_incentive = deal_size * tier_multipliers[partner_tier]

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("3-Yr VMware TCO", f"${vmware_tco/1000000:.1f}M")
col2.metric("3-Yr Nutanix TCO", f"${nutanix_tco/1000000:.1f}M", f"-{roi:.1f}%")
col3.metric("Partner Incentive", f"${partner_incentive:,.0f}", partner_tier)

# Visualization
fig, ax = plt.subplots()
categories = ['Licensing', 'Hardware', 'Storage', 'Admin', 'Maintenance']
vmware_breakdown = [vm_count * 3500, vm_count * 4000, storage_tb * 2500, admin_count * 120000, vm_count * 1000]
nutanix_breakdown = [vm_count * 2000, vm_count * 3500, storage_tb * 1800, admin_count * 75000, vm_count * 600]
ax.bar(categories, vmware_breakdown, label='VMware')
ax.bar(categories, nutanix_breakdown, label='Nutanix', alpha=0.7)
ax.set_ylabel('Annual Cost')
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
