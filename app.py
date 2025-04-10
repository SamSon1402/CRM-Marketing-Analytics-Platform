import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import matplotlib.pyplot as plt
import base64
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="ESG Arcade: Real Estate Edition",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set the background color for the entire app
st.markdown("""
<style>
    .stApp {
        background-color: #FF69B4;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS for retro gaming aesthetic
def add_retro_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&family=Press+Start+2P&family=Space+Mono&display=swap');
        
        /* Base styling */
        html, body, [class*="css"] {
            font-family: 'Space Mono', monospace;
        }
        
        h1, h2, h3 {
            font-family: 'Press Start 2P', cursive;
            text-transform: uppercase;
            color: #000000;
            text-shadow: 2px 2px 0px #FFFFFF;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        /* Header styling */
        h1 {
            font-size: 2.5em;
            color: #6B0075;
            border-bottom: 5px solid #00AA00;
            padding-bottom: 10px;
        }
        
        /* Card styling */
        .pixel-card {
            border: 4px solid #FFFFFF;
            background-color: #FF69B4;
            border-radius: 0px;
            padding: 20px;
            box-shadow: 10px 10px 0px #8B0053;
            margin-bottom: 30px;
        }
        
        /* Button styling */
        .stButton button {
            font-family: 'Press Start 2P', cursive;
            border: 3px solid #FFFFFF;
            border-radius: 0px;
            background-color: #6B0075;
            color: white;
            box-shadow: 4px 4px 0px #000000;
            transition: all 0.1s;
        }
        
        .stButton button:hover {
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px #000000;
        }
        
        /* Select box styling */
        .stSelectbox div[data-baseweb="select"] {
            font-family: 'VT323', monospace;
            border: 3px solid #6B0075;
            border-radius: 0px;
            background-color: #FFFFFF;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #FF69B4;
        }
        
        [data-testid=stSidebar] {
            background-color: #FF69B4;
            border-right: 3px solid #FFFFFF;
        }
        
        [data-testid=stSidebar] h2 {
            color: #6B0075;
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background-color: #6B0075;
        }
        
        /* Main area styling */
        .main {
            background-color: #FF69B4;
        }
        
        .reportview-container {
            background-color: #FF69B4;
        }
        
        /* Text styling */
        p, li, div {
            font-family: 'VT323', monospace;
            font-size: 20px;
            color: #000000;
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-family: 'Press Start 2P', cursive;
            color: #6B0075;
        }
        
        /* Custom retro progress bar */
        .retro-progress-container {
            width: 100%;
            background-color: #333333;
            border: 3px solid #FFFFFF;
            height: 30px;
            margin-bottom: 15px;
        }
        .retro-progress-bar {
            height: 100%;
            background-color: #00FF00;
            text-align: center;
            line-height: 30px;
            color: white;
            font-family: 'Press Start 2P', cursive;
            font-size: 12px;
        }
        
        /* Property card */
        .property-card {
            border: 4px solid #FFFFFF;
            background-color: #000080;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 5px 5px 0px #000000;
        }
        
        /* For tables */
        .dataframe {
            font-family: 'VT323', monospace;
            border: 3px solid #6B0075;
        }
        .dataframe th {
            background-color: #6B0075;
            color: white;
            padding: 8px;
            font-family: 'Press Start 2P', cursive;
            font-size: 14px;
        }
        .dataframe td {
            padding: 8px;
            border: 2px solid #6B0075;
            background-color: #FFFFFF;
        }
        
        /* Plotly charts styling */
        .js-plotly-plot {
            border: 3px solid #6B0075;
            box-shadow: 8px 8px 0px #8B0053;
            background-color: #FFFFFF;
        }
        
        /* Text input styling */
        .stTextInput input {
            font-family: 'VT323', monospace;
            border: 3px solid #6B0075;
            border-radius: 0px;
            background-color: #FFFFFF;
            color: #000000;
        }
        
        /* For specific color coding */
        .green-text {
            color: #008800;
        }
        .red-text {
            color: #880000;
        }
        .yellow-text {
            color: #6B0075;
        }
    </style>
    """, unsafe_allow_html=True)

# Function to create retro progress bar
def retro_progress_bar(percentage, label="", color="#00FF00"):
    return f"""
    <div class="retro-progress-container">
        <div class="retro-progress-bar" style="width:{percentage}%; background-color:{color};">
            {label} {int(percentage)}%
        </div>
    </div>
    """

# Function to create pixel art building icon (simple ASCII representation)
def pixel_building(score):
    if score >= 80:
        color = "#00FF00"  # Green
    elif score >= 50:
        color = "#FFFF00"  # Yellow
    else:
        color = "#FF0000"  # Red
        
    building = f"""
    <div style="text-align: center; color: {color}; font-family: monospace; font-size: 18px; margin: 10px 0;">
    <pre>
      /\\
     /  \\
    /____\\
    |    |
    |____|
    |    |
    |    |
    |____|
    </pre>
    <p style="margin-top: -10px; font-family: 'Press Start 2P', cursive; font-size: 14px; color: {color};">
    ESG SCORE: {score}%
    </p>
    </div>
    """
    return building

# Generate sample data
def generate_sample_data():
    property_types = ["Office", "Retail", "Residential", "Industrial", "Mixed-Use"]
    cities = ["Paris", "London", "Berlin", "Madrid", "Amsterdam", "Milan", "Brussels"]
    certification_types = ["BREEAM", "HQE", "LEED", "None"]
    certification_levels = ["Outstanding", "Excellent", "Very Good", "Good", "Pass", "None"]
    
    data = []
    for i in range(1, 16):
        property_type = random.choice(property_types)
        city = random.choice(cities)
        certification = random.choice(certification_types)
        
        # For properties with no certification
        if certification == "None":
            certification_level = "None"
        else:
            # Skip "None" if there's a certification
            possible_levels = certification_levels.copy()
            if "None" in possible_levels:
                possible_levels.remove("None")
            certification_level = random.choice(possible_levels)
        
        # Random ESG metrics
        energy_score = random.randint(20, 100)
        carbon_footprint = random.randint(50, 250)
        water_usage = random.randint(500, 2000)
        waste_recycling = random.randint(10, 95)
        
        # Social and governance metrics
        tenant_satisfaction = random.randint(50, 100)
        community_impact = random.randint(30, 100)
        governance_compliance = random.randint(40, 100)
        
        # Calculate overall ESG score (weighted)
        env_score = (energy_score * 0.4 + (100 - carbon_footprint/2.5) * 0.4 + 
                    waste_recycling * 0.2)
        social_score = (tenant_satisfaction * 0.6 + community_impact * 0.4)
        gov_score = governance_compliance
        
        overall_esg_score = env_score * 0.5 + social_score * 0.3 + gov_score * 0.2
        
        # Random coordinates within Europe
        lat = random.uniform(36.0, 60.0)
        lon = random.uniform(-5.0, 30.0)
        
        # Create property entry
        property_data = {
            "Property ID": f"PROP-{i:03d}",
            "Property Name": f"{city} {property_type} {i}",
            "Type": property_type,
            "Location": city,
            "Size (sqm)": random.randint(1000, 50000),
            "Year Built": random.randint(1970, 2023),
            "Certification": certification,
            "Certification Level": certification_level,
            "Energy Score": energy_score,
            "Carbon Footprint (kgCO2e/sqm/yr)": carbon_footprint,
            "Water Usage (L/sqm/yr)": water_usage,
            "Waste Recycling (%)": waste_recycling,
            "Tenant Satisfaction": tenant_satisfaction,
            "Community Impact": community_impact,
            "Governance Compliance": governance_compliance,
            "Environmental Score": env_score,
            "Social Score": social_score,
            "Governance Score": gov_score,
            "Overall ESG Score": overall_esg_score,
            "Latitude": lat,
            "Longitude": lon
        }
        
        data.append(property_data)
    
    return pd.DataFrame(data)

# Function to generate random target data
def generate_target_data():
    current_year = datetime.now().year
    targets = [
        {
            "Target Name": "Carbon Neutrality",
            "Category": "Environmental",
            "Current Value": random.randint(50, 80),
            "Target Value": 100,
            "Target Year": current_year + 5,
            "Regulation": "EU Climate Law",
            "Priority": "High"
        },
        {
            "Target Name": "Energy Efficiency",
            "Category": "Environmental",
            "Current Value": random.randint(30, 70),
            "Target Value": 90,
            "Target Year": current_year + 3,
            "Regulation": "EPBD",
            "Priority": "High"
        },
        {
            "Target Name": "Water Conservation",
            "Category": "Environmental",
            "Current Value": random.randint(40, 60),
            "Target Value": 80,
            "Target Year": current_year + 4,
            "Regulation": "EU Water Framework",
            "Priority": "Medium"
        },
        {
            "Target Name": "Waste Reduction",
            "Category": "Environmental",
            "Current Value": random.randint(30, 50),
            "Target Value": 90,
            "Target Year": current_year + 3,
            "Regulation": "EU Circular Economy Package",
            "Priority": "Medium"
        },
        {
            "Target Name": "Certification Coverage",
            "Category": "Environmental",
            "Current Value": random.randint(20, 40),
            "Target Value": 100,
            "Target Year": current_year + 5,
            "Regulation": "Market Standards",
            "Priority": "High"
        },
        {
            "Target Name": "Tenant Wellbeing",
            "Category": "Social",
            "Current Value": random.randint(50, 70),
            "Target Value": 95,
            "Target Year": current_year + 2,
            "Regulation": "Internal Policy",
            "Priority": "Medium"
        },
        {
            "Target Name": "Community Engagement",
            "Category": "Social",
            "Current Value": random.randint(30, 60),
            "Target Value": 85,
            "Target Year": current_year + 4,
            "Regulation": "CSR Framework",
            "Priority": "Low"
        },
        {
            "Target Name": "ESG Reporting",
            "Category": "Governance",
            "Current Value": random.randint(50, 70),
            "Target Value": 100,
            "Target Year": current_year + 2,
            "Regulation": "SFDR",
            "Priority": "High"
        },
        {
            "Target Name": "ESG Risk Management",
            "Category": "Governance",
            "Current Value": random.randint(40, 70),
            "Target Value": 90,
            "Target Year": current_year + 3,
            "Regulation": "TCFD",
            "Priority": "High"
        }
    ]
    
    return pd.DataFrame(targets)

# Generate retrofit data
def generate_retrofit_options():
    options = [
        {
            "Retrofit": "Solar Panel Installation",
            "Category": "Energy Generation",
            "Cost (€/sqm)": 120,
            "ROI (Years)": 7,
            "Carbon Reduction (%)": 30,
            "Energy Saving (%)": 25,
            "Implementation Time (Months)": 3,
            "Complexity": "Medium"
        },
        {
            "Retrofit": "HVAC Upgrade",
            "Category": "Energy Efficiency",
            "Cost (€/sqm)": 80,
            "ROI (Years)": 5,
            "Carbon Reduction (%)": 20,
            "Energy Saving (%)": 30,
            "Implementation Time (Months)": 4,
            "Complexity": "Medium"
        },
        {
            "Retrofit": "Building Envelope Insulation",
            "Category": "Energy Efficiency",
            "Cost (€/sqm)": 95,
            "ROI (Years)": 8,
            "Carbon Reduction (%)": 25,
            "Energy Saving (%)": 35,
            "Implementation Time (Months)": 5,
            "Complexity": "High"
        },
        {
            "Retrofit": "LED Lighting Upgrade",
            "Category": "Energy Efficiency",
            "Cost (€/sqm)": 15,
            "ROI (Years)": 2,
            "Carbon Reduction (%)": 5,
            "Energy Saving (%)": 10,
            "Implementation Time (Months)": 1,
            "Complexity": "Low"
        },
        {
            "Retrofit": "Smart Building Management System",
            "Category": "Energy Management",
            "Cost (€/sqm)": 50,
            "ROI (Years)": 4,
            "Carbon Reduction (%)": 15,
            "Energy Saving (%)": 20,
            "Implementation Time (Months)": 3,
            "Complexity": "High"
        },
        {
            "Retrofit": "Water Efficiency Measures",
            "Category": "Water Conservation",
            "Cost (€/sqm)": 25,
            "ROI (Years)": 3,
            "Carbon Reduction (%)": 2,
            "Energy Saving (%)": 5,
            "Implementation Time (Months)": 2,
            "Complexity": "Low"
        },
        {
            "Retrofit": "Green Roof Installation",
            "Category": "Biodiversity",
            "Cost (€/sqm)": 110,
            "ROI (Years)": 12,
            "Carbon Reduction (%)": 5,
            "Energy Saving (%)": 8,
            "Implementation Time (Months)": 4,
            "Complexity": "High"
        },
        {
            "Retrofit": "Waste Management Systems",
            "Category": "Waste Reduction",
            "Cost (€/sqm)": 10,
            "ROI (Years)": 2,
            "Carbon Reduction (%)": 3,
            "Energy Saving (%)": 0,
            "Implementation Time (Months)": 2,
            "Complexity": "Low"
        }
    ]
    
    return pd.DataFrame(options)

# Apply the custom CSS
add_retro_css()

# Initialize session state for the "game"
if 'properties_df' not in st.session_state:
    st.session_state.properties_df = generate_sample_data()

if 'targets_df' not in st.session_state:
    st.session_state.targets_df = generate_target_data()
    
if 'retrofit_df' not in st.session_state:
    st.session_state.retrofit_df = generate_retrofit_options()

if 'game_score' not in st.session_state:
    st.session_state.game_score = 0
    
if 'level' not in st.session_state:
    st.session_state.level = 1

# Title with retro gaming aesthetic
st.markdown("""
<div style="text-align: center; padding: 20px; margin-bottom: 30px; 
            background-color: #FF69B4; border: 5px solid #FFFFFF; box-shadow: 10px 10px 0px #8B0053;">
    <h1 style="font-size: 3em; margin-bottom: 0; color: #6B0075; text-shadow: 2px 2px 0px #FFFFFF;">ESG ARCADE</h1>
    <p style="font-family: 'Press Start 2P', cursive; color: #6B0075; font-size: 1.2em; margin-top: 10px;">
        REAL ESTATE EDITION
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h2 style="font-size: 1.5em; margin-bottom: 5px; color: #6B0075; text-shadow: 2px 2px 0px #FFFFFF;">GAME MENU</h2>
</div>
""", unsafe_allow_html=True)

# Game stats in sidebar
st.sidebar.markdown(f"""
<div style="padding: 15px; border: 3px solid #FFFFFF; margin-bottom: 20px; background-color: #FF69B4;">
    <p style="font-family: 'Press Start 2P', cursive; color: #6B0075; font-size: 1em; margin-bottom: 10px;">PLAYER STATS</p>
    <p style="font-family: 'VT323', monospace; font-size: 1.2em; color: #000000;">LEVEL: {st.session_state.level}</p>
    <p style="font-family: 'VT323', monospace; font-size: 1.2em; color: #000000;">SCORE: {st.session_state.game_score}</p>
</div>
""", unsafe_allow_html=True)

# Navigation options
nav_options = ["Portfolio Map", "ESG Assessment", "Target Tracking", "Retrofit Simulator", "ESG Reports"]
nav_icons = ["🗺️", "📊", "🎯", "🔧", "📜"]

nav_selection = st.sidebar.radio(
    "Select Your Quest",
    [f"{icon} {option}" for icon, option in zip(nav_icons, nav_options)]
)

# Extract the section name without the icon
current_section = nav_selection.split(" ", 1)[1]

# Increase game score when changing sections
if 'last_section' not in st.session_state:
    st.session_state.last_section = current_section
elif st.session_state.last_section != current_section:
    st.session_state.game_score += 100
    st.session_state.last_section = current_section
    # Level up for every 1000 points
    st.session_state.level = (st.session_state.game_score // 1000) + 1

# Custom section header
st.markdown(f"""
<div style="padding: 15px; border: 3px solid #FFFFFF; margin-bottom: 20px; 
           background-color: #FF69B4; box-shadow: 5px 5px 0px #8B0053;">
    <h2 style="font-size: 1.8em; margin: 0; color: #6B0075; text-shadow: 2px 2px 0px #FFFFFF;">[ {current_section} ]</h2>
</div>
""", unsafe_allow_html=True)

# Section content
if current_section == "Portfolio Map":
    st.markdown("""
    <div class="pixel-card">
        <p>Explore your property portfolio and ESG performance across different locations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Map of properties
        df = st.session_state.properties_df
        
        # Create color scale based on ESG score
        fig = px.scatter_mapbox(
            df, 
            lat="Latitude", 
            lon="Longitude", 
            color="Overall ESG Score",
            size=[30] * len(df),  # Fixed size for pixel art feel
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[0, 100],
            hover_name="Property Name",
            hover_data={
                "Property ID": True,
                "Type": True,
                "Location": True,
                "Overall ESG Score": True,
                "Certification": True,
                "Latitude": False,
                "Longitude": False
            },
            zoom=3,
            height=500
        )
        
        fig.update_layout(
            mapbox_style="carto-positron",  # Lighter map style for better visibility
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(family="VT323", size=16, color="#000000"),
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=dict(
                title="ESG Score",
                tickfont=dict(family="VT323", size=14, color="#000000"),
                titlefont=dict(family="Press Start 2P", size=12, color="#6B0075"),
                len=0.8
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #FF69B4; border: 3px solid #FFFFFF; padding: 15px; 
                   box-shadow: 5px 5px 0px #8B0053; height: 480px; overflow-y: auto;">
            <h3 style="font-size: 1.2em; margin-bottom: 15px; color: #6B0075; text-shadow: 2px 2px 0px #FFFFFF;">TOP PROPERTIES</h3>
        """, unsafe_allow_html=True)
        
        # Sort by ESG score and get top 5
        top_properties = df.sort_values("Overall ESG Score", ascending=False).head(5)
        
        for _, prop in top_properties.iterrows():
            score = int(prop["Overall ESG Score"])
            st.markdown(f"""
            <div class="property-card">
                <p style="font-family: 'Press Start 2P', cursive; font-size: 0.9em; margin-bottom: 10px;">
                    {prop["Property Name"]}
                </p>
                {pixel_building(score)}
                <p>TYPE: {prop["Type"]}</p>
                <p>LOCATION: {prop["Location"]}</p>
                <p>CERT: {prop["Certification"]}</p>
                {retro_progress_bar(score, "ESG", "#00FF00" if score >= 80 else "#FFFF00" if score >= 50 else "#FF0000")}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Game-like action buttons
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("ADD PROPERTY"):
                st.session_state.game_score += 50
                st.session_state.level = (st.session_state.game_score // 1000) + 1
                st.toast("New property added! +50 points", icon="🏆")
        with col2:
            if st.button("ANALYZE MAP"):
                st.session_state.game_score += 30
                st.session_state.level = (st.session_state.game_score // 1000) + 1
                st.toast("Map analyzed! +30 points", icon="🏆")

elif current_section == "ESG Assessment":
    st.markdown("""
    <div class="pixel-card">
        <p>Conduct baseline ESG assessment of your portfolio and analyze performance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Property selector
    df = st.session_state.properties_df
    property_options = df["Property Name"].tolist()
    
    selected_property = st.selectbox("SELECT PROPERTY", property_options)
    property_data = df[df["Property Name"] == selected_property].iloc[0]
    
    # Display property ESG stats in a game-like stat card
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #FF69B4; border: 3px solid #FFFFFF; padding: 20px; 
                   box-shadow: 5px 5px 0px #8B0053; margin-bottom: 20px;">
            <h3 style="font-size: 1.2em; margin-bottom: 15px; color: #6B0075; text-shadow: 2px 2px 0px #FFFFFF;">PROPERTY STATS</h3>
            <p style="font-family: 'Press Start 2P', cursive; font-size: 1.1em; margin-bottom: 15px; 
                      color: #6B0075;">{selected_property}</p>
            <p style="color: #000000;">ID: {property_data["Property ID"]}</p>
            <p style="color: #000000;">TYPE: {property_data["Type"]}</p>
            <p style="color: #000000;">LOCATION: {property_data["Location"]}</p>
            <p style="color: #000000;">SIZE: {property_data["Size (sqm)"]} sqm</p>
            <p style="color: #000000;">YEAR BUILT: {property_data["Year Built"]}</p>
            <p style="color: #000000;">CERTIFICATION: {property_data["Certification"]} 
               ({property_data["Certification Level"]})</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        env_score = property_data["Environmental Score"]
        social_score = property_data["Social Score"]
        gov_score = property_data["Governance Score"]
        overall_score = property_data["Overall ESG Score"]
        
        st.markdown(f"""
        <div style="background-color: #FF69B4; border: 3px solid #FFFFFF; padding: 20px; 
                   box-shadow: 5px 5px 0px #8B0053; margin-bottom: 20px;">
            <h3 style="font-size: 1.2em; margin-bottom: 15px; color: #6B0075; text-shadow: 2px 2px 0px #FFFFFF;">ESG POWER LEVELS</h3>
            
            <p style="margin-bottom: 5px; color: #000000;">ENVIRONMENTAL</p>
            {retro_progress_bar(env_score, "", "#6B0075")}
            
            <p style="margin-bottom: 5px; color: #000000;">SOCIAL</p>
            {retro_progress_bar(social_score, "", "#8B0053")}
            
            <p style="margin-bottom: 5px; color: #000000;">GOVERNANCE</p>
            {retro_progress_bar(gov_score, "", "#6B0075")}
            
            <p style="margin-top: 15px; margin-bottom: 5px; font-family: 'Press Start 2P', cursive; color: #6B0075;">
                OVERALL POWER
            </p>
            {retro_progress_bar(overall_score, "", "#8B0053")}
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed metrics in pixel-art style
    st.markdown("""
    <div style="background-color: #000080; border: 3px solid #FFFFFF; padding: 20px; 
               box-shadow: 5px 5px 0px #000000; margin-bottom: 20px;">
        <h3 style="font-size: 1.2em; margin-bottom: 15px;">DETAILED METRICS</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="border: 2px solid #FFFFFF; padding: 15px; margin-bottom: 15px;">
            <p style="font-family: 'Press Start 2P', cursive; font-size: 0.9em; color: #00FF00;">
                ENVIRONMENTAL
            </p>
            <p>ENERGY: {property_data["Energy Score"]}/100</p>
            <p>CARBON: {property_data["Carbon Footprint (kgCO2e/sqm/yr)"]} kg/sqm/yr</p>
            <p>WATER: {property_data["Water Usage (L/sqm/yr)"]} L/sqm/yr</p>
            <p>WASTE RECYCLING: {property_data["Waste Recycling (%)"]}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="border: 2px solid #FFFFFF; padding: 15px; margin-bottom: 15px;">
            <p style="font-family: 'Press Start 2P', cursive; font-size: 0.9em; color: #FFFF00;">
                SOCIAL
            </p>
            <p>TENANT SATISFACTION: {property_data["Tenant Satisfaction"]}/100</p>
            <p>COMMUNITY IMPACT: {property_data["Community Impact"]}/100</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div style="border: 2px solid #FFFFFF; padding: 15px; margin-bottom: 15px;">
            <p style="font-family: 'Press Start 2P', cursive; font-size: 0.9em; color: #FF0000;">
                GOVERNANCE
            </p>
            <p>COMPLIANCE: {property_data["Governance Compliance"]}/100</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Comparison chart
    st.markdown("""
    <h3 style="font-size: 1.2em; margin-top: 30px; margin-bottom: 15px;">COMPARISON RADAR</h3>
    """, unsafe_allow_html=True)
    
    # Create a radar chart comparing this property to portfolio average
    avg_env = df["Environmental Score"].mean()
    avg_social = df["Social Score"].mean()
    avg_gov = df["Governance Score"].mean()
    
    categories = ['Environmental', 'Social', 'Governance']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[env_score, social_score, gov_score],
        theta=categories,
        fill='toself',
        name='Selected Property',
        line=dict(color='#00FFFF'),
        fillcolor='rgba(0, 255, 255, 0.2)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[avg_env, avg_social, avg_gov],
        theta=categories,
        fill='toself',
        name='Portfolio Average',
        line=dict(color='#FF00FF'),
        fillcolor='rgba(255, 0, 255, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        legend=dict(
            font=dict(
                family="VT323",
                size=16,
                color="white"
            )
        ),
        paper_bgcolor="#000080",
        plot_bgcolor="#000080",
        font=dict(
            family="VT323",
            size=16,
            color="white"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Game-like action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("IMPROVE BUILDING"):
            st.session_state.game_score += 150
            st.session_state.level = (st.session_state.game_score // 1000) + 1
            st.toast("Building improved! +150 points", icon="🏆")
    with col2:
        if st.button("GENERATE REPORT"):
            st.session_state.game_score += 100
            st.session_state.level = (st.session_state.game_score // 1000) + 1
            st.toast("Report generated! +100 points", icon="🏆")
    with col3:
        if st.button("CERTIFICATION UPGRADE"):
            st.session_state.game_score += 200
            st.session_state.level = (st.session_state.game_score // 1000) + 1
            st.toast("Certification upgraded! +200 points", icon="🏆")

elif current_section == "Target Tracking":
    st.markdown("""
    <div class="pixel-card">
        <p>Track progress against ESG targets and regulatory requirements.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Target data
    targets_df = st.session_state.targets_df
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        category_filter = st.selectbox(
            "FILTER BY CATEGORY",
            ["All Categories"] + list(targets_df["Category"].unique())
        )
    with col2:
        priority_filter = st.selectbox(
            "FILTER BY PRIORITY",
            ["All Priorities"] + list(targets_df["Priority"].unique())
        )
    
    # Apply filters
    filtered_df = targets_df.copy()
    if category_filter != "All Categories":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]
    if priority_filter != "All Priorities":
        filtered_df = filtered_df[filtered_df["Priority"] == priority_filter]
    
    # Display targets as "quests"
    st.markdown("""
    <h3 style="font-size: 1.2em; margin-top: 20px; margin-bottom: 15px;">ESG QUESTS</h3>
    """, unsafe_allow_html=True)
    
    for _, target in filtered_df.iterrows():
        current_value = target["Current Value"]
        target_value = target["Target Value"]
        progress = (current_value / target_value) * 100
        
        # Determine color based on progress
        if progress >= 80:
            color = "#00FF00"  # Green
        elif progress >= 50:
            color = "#FFFF00"  # Yellow
        else:
            color = "#FF0000"  # Red
            
        years_left = target["Target Year"] - datetime.now().year
        
        st.markdown(f"""
        <div style="background-color: #000080; border: 3px solid #FFFFFF; padding: 15px; 
                   box-shadow: 5px 5px 0px #000000; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <p style="font-family: 'Press Start 2P', cursive; font-size: 1em; color: #FFFF00;">
                    {target["Target Name"]}
                </p>
                <p style="background-color: {
                    "#FF0000" if target["Priority"] == "High" else 
                    "#FFFF00" if target["Priority"] == "Medium" else "#00FF00"
                }; padding: 5px 10px; font-family: 'VT323', monospace; font-size: 16px;">
                    {target["Priority"]}
                </p>
            </div>
            
            <p style="margin-top: 10px;">CATEGORY: {target["Category"]}</p>
            <p>REGULATION: {target["Regulation"]}</p>
            <p>TARGET YEAR: {target["Target Year"]} ({years_left} years left)</p>
            
            <div style="display: flex; margin-top: 15px; margin-bottom: 10px;">
                <p style="width: 50%; text-align: left;">CURRENT: {current_value}%</p>
                <p style="width: 50%; text-align: right;">TARGET: {target_value}%</p>
            </div>
            
            {retro_progress_bar(progress, "PROGRESS", color)}
            
            <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
                <div style="background-color: #0000AA; border: 2px solid #FFFFFF; padding: 5px 10px; 
                           font-family: 'Press Start 2P', cursive; font-size: 0.8em; cursor: pointer;">
                    UPDATE QUEST
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Summary chart
    st.markdown("""
    <h3 style="font-size: 1.2em; margin-top: 30px; margin-bottom: 15px;">QUEST PROGRESS</h3>
    """, unsafe_allow_html=True)
    
    # Calculate progress for each category
    env_targets = targets_df[targets_df["Category"] == "Environmental"]
    social_targets = targets_df[targets_df["Category"] == "Social"]
    gov_targets = targets_df[targets_df["Category"] == "Governance"]
    
    env_progress = env_targets["Current Value"].sum() / env_targets["Target Value"].sum() * 100
    social_progress = social_targets["Current Value"].sum() / social_targets["Target Value"].sum() * 100
    gov_progress = gov_targets["Current Value"].sum() / gov_targets["Target Value"].sum() * 100
    
    categories = ["Environmental", "Social", "Governance"]
    progress_values = [env_progress, social_progress, gov_progress]
    
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        x=categories,
        y=progress_values,
        text=[f"{val:.1f}%" for val in progress_values],
        textposition='auto',
        marker=dict(
            color=['#00FF00', '#FFFF00', '#FF0000'],
            line=dict(color='#FFFFFF', width=2)
        )
    ))
    
    # Add a horizontal line at 100%
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=100,
        x1=2.5,
        y1=100,
        line=dict(
            color="#FFFFFF",
            width=2,
            dash="dash",
        )
    )
    
    fig.update_layout(
        xaxis=dict(
            title="ESG Categories",
            title_font=dict(family="Press Start 2P", size=12),
            tickfont=dict(family="VT323", size=14),
            tickmode='array',
            tickvals=[0, 1, 2],
            ticktext=categories
        ),
        yaxis=dict(
            title="Progress (%)",
            title_font=dict(family="Press Start 2P", size=12),
            tickfont=dict(family="VT323", size=14),
            range=[0, 110]
        ),
        paper_bgcolor="#000080",
        plot_bgcolor="#000080",
        font=dict(
            family="VT323",
            size=16,
            color="white"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Game-like action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("ADD NEW TARGET"):
            st.session_state.game_score += 100
            st.session_state.level = (st.session_state.game_score // 1000) + 1
            st.toast("New target added! +100 points", icon="🏆")
    with col2:
        if st.button("PROGRESS UPDATE"):
            st.session_state.game_score += 75
            st.session_state.level = (st.session_state.game_score // 1000) + 1
            st.toast("Progress updated! +75 points", icon="🏆")
    with col3:
        if st.button("REGULATORY SCAN"):
            st.session_state.game_score += 150
            st.session_state.level = (st.session_state.game_score // 1000) + 1
            st.toast("Regulatory scan complete! +150 points", icon="🏆")

elif current_section == "Retrofit Simulator":
    st.markdown("""
    <div class="pixel-card">
        <p>Plan and prioritize retrofitting projects for maximum ESG impact.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Property selector
    df = st.session_state.properties_df
    property_options = df["Property Name"].tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_property = st.selectbox("SELECT PROPERTY FOR RETROFIT", property_options)
    with col2:
        budget = st.number_input("BUDGET (€)", min_value=10000, max_value=1000000, value=100000, step=10000)
    
    property_data = df[df["Property Name"] == selected_property].iloc[0]
    property_size = property_data["Size (sqm)"]
    
    # Display property current stats
    st.markdown(f"""
    <div style="background-color: #000080; border: 3px solid #FFFFFF; padding: 15px; 
               box-shadow: 5px 5px 0px #000000; margin-bottom: 20px;">
        <h3 style="font-size: 1.2em; margin-bottom: 15px;">CURRENT PROPERTY STATS</h3>
        <p style="font-family: 'Press Start 2P', cursive; font-size: 1em; margin-bottom: 15px; 
                 color: #FFFF00;">{selected_property}</p>
        
        <div style="display: flex; flex-wrap: wrap;">
            <div style="width: 33%; padding: 5px;">
                <p>SIZE: {property_size} sqm</p>
            </div>
            <div style="width: 33%; padding: 5px;">
                <p>ENERGY SCORE: {property_data["Energy Score"]}/100</p>
            </div>
            <div style="width: 33%; padding: 5px;">
                <p>CARBON: {property_data["Carbon Footprint (kgCO2e/sqm/yr)"]} kg/sqm/yr</p>
            </div>
            <div style="width: 33%; padding: 5px;">
                <p>ESG SCORE: {property_data["Overall ESG Score"]:.1f}/100</p>
            </div>
            <div style="width: 33%; padding: 5px;">
                <p>YEAR BUILT: {property_data["Year Built"]}</p>
            </div>
            <div style="width: 33%; padding: 5px;">
                <p>CERTIFICATION: {property_data["Certification"]}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display retrofit options
    st.markdown("""
    <h3 style="font-size: 1.2em; margin-top: 20px; margin-bottom: 15px;">AVAILABLE UPGRADES</h3>
    """, unsafe_allow_html=True)
    
    # Retrofit data
    retrofit_df = st.session_state.retrofit_df
    
    # Calculate total cost for each retrofit based on property size
    retrofit_df["Total Cost (€)"] = retrofit_df["Cost (€/sqm)"] * property_size
    retrofit_df["Affordable"] = retrofit_df["Total Cost (€)"] <= budget
    
    # Create columns for the retrofit options
    cols = st.columns(3)
    
    # Track selected retrofits
    if "selected_retrofits" not in st.session_state:
        st.session_state.selected_retrofits = []
    
    # Display retrofit cards
    for i, (_, retrofit) in enumerate(retrofit_df.iterrows()):
        col = cols[i % 3]
        
        # Calculate retrofit ID
        retrofit_id = f"retrofit_{i}"
        
        # Check if this retrofit is already selected
        is_selected = retrofit_id in st.session_state.selected_retrofits
        
        # Calculate affordability
        can_afford = retrofit["Affordable"]
        remaining_budget = budget - sum([retrofit_df.iloc[int(r.split('_')[1])]["Total Cost (€)"] 
                                        for r in st.session_state.selected_retrofits if r != retrofit_id])
        
        with col:
            border_color = "#00FF00" if is_selected else ("#FFFFFF" if can_afford else "#FF0000")
            bg_color = "#004400" if is_selected else "#000080"
            
            st.markdown(f"""
            <div style="background-color: {bg_color}; border: 3px solid {border_color}; 
                      padding: 15px; margin-bottom: 15px; cursor: pointer;"
                 onclick="this.style.backgroundColor='{
                     '#000080' if is_selected else '#004400'
                 }'; this.style.borderColor='{
                     '#FFFFFF' if is_selected else '#00FF00'
                 }';">
                <p style="font-family: 'Press Start 2P', cursive; font-size: 0.9em; 
                         color: {'#00FF00' if is_selected else '#FFFF00'}; margin-bottom: 10px;">
                    {retrofit["Retrofit"]}
                </p>
                <p>CATEGORY: {retrofit["Category"]}</p>
                <p>COST: €{int(retrofit["Total Cost (€)"]):,}</p>
                <p>ROI: {retrofit["ROI (Years)"]} years</p>
                <p>CARBON REDUCTION: {retrofit["Carbon Reduction (%)"]}%</p>
                <p>ENERGY SAVING: {retrofit["Energy Saving (%)"]}%</p>
                <p>TIME: {retrofit["Implementation Time (Months)"]} months</p>
                <p>COMPLEXITY: {retrofit["Complexity"]}</p>
                
                <div style="margin-top: 15px; text-align: center;">
                    <div style="display: inline-block; background-color: {
                        '#FF0000' if is_selected else '#00FF00'
                    }; border: 2px solid #FFFFFF; padding: 5px 10px; 
                             font-family: 'Press Start 2P', cursive; font-size: 0.7em;">
                        {
                            "REMOVE" if is_selected else 
                            ("SELECT" if can_afford else "INSUFFICIENT FUNDS")
                        }
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add button for selection (this will actually work, unlike the div click)
            button_label = "REMOVE" if is_selected else ("SELECT" if can_afford else "INSUFFICIENT FUNDS")
            button_disabled = not can_afford and not is_selected
            
            if st.button(button_label, key=f"btn_{retrofit_id}", disabled=button_disabled):
                if is_selected:
                    st.session_state.selected_retrofits.remove(retrofit_id)
                else:
                    st.session_state.selected_retrofits.append(retrofit_id)
                st.rerun()
    
    # Calculate impact of selected retrofits
    selected_retrofits_data = [retrofit_df.iloc[int(r.split('_')[1])] for r in st.session_state.selected_retrofits]
    
    total_cost = sum([r["Total Cost (€)"] for r in selected_retrofits_data])
    total_carbon_reduction = min(100, sum([r["Carbon Reduction (%)"] for r in selected_retrofits_data]))
    total_energy_saving = min(100, sum([r["Energy Saving (%)"] for r in selected_retrofits_data]))
    
    # Calculate new property metrics after retrofits
    new_carbon = max(0, property_data["Carbon Footprint (kgCO2e/sqm/yr)"] * (1 - total_carbon_reduction/100))
    new_energy_score = min(100, property_data["Energy Score"] + (total_energy_saving/2))
    
    # Estimate impact on overall ESG score
    env_improvement = (total_carbon_reduction + total_energy_saving) / 4  # Converting to ESG score impact
    new_env_score = min(100, property_data["Environmental Score"] + env_improvement)
    new_overall_score = min(100, property_data["Overall ESG Score"] + (env_improvement * 0.5))  # Environmental is 50% of overall
    
    # Display retrofit plan summary
    st.markdown(f"""
    <div style="background-color: #000080; border: 3px solid #FFFFFF; padding: 20px; 
               box-shadow: 5px 5px 0px #000000; margin-top: 30px; margin-bottom: 20px;">
        <h3 style="font-size: 1.2em; margin-bottom: 15px;">RETROFIT PLAN SUMMARY</h3>
        
        <div style="display: flex; flex-wrap: wrap; margin-bottom: 20px;">
            <div style="width: 33%; padding: 10px;">
                <p style="font-family: 'Press Start 2P', cursive; font-size: 0.9em; color: #FFFF00;">
                    UPGRADES SELECTED
                </p>
                <p style="font-size: 1.5em;">{len(selected_retrofits_data)}</p>
            </div>
            
            <div style="width: 33%; padding: 10px;">
                <p style="font-family: 'Press Start 2P', cursive; font-size: 0.9em; color: #FFFF00;">
                    TOTAL COST
                </p>
                <p style="font-size: 1.5em;">€{int(total_cost):,}</p>
            </div>
            
            <div style="width: 33%; padding: 10px;">
                <p style="font-family: 'Press Start 2P', cursive; font-size: 0.9em; color: #FFFF00;">
                    REMAINING BUDGET
                </p>
                <p style="font-size: 1.5em;">€{int(budget - total_cost):,}</p>
            </div>
        </div>
        
        <h3 style="font-size: 1em; margin-top: 20px; margin-bottom: 15px;">PROJECTED IMPROVEMENTS</h3>
        
        <div style="display: flex; flex-wrap: wrap;">
            <div style="width: 50%; padding: 10px;">
                <p>CARBON REDUCTION</p>
                {retro_progress_bar(total_carbon_reduction, "", "#00FF00")}
            </div>
            
            <div style="width: 50%; padding: 10px;">
                <p>ENERGY IMPROVEMENT</p>
                {retro_progress_bar(total_energy_saving, "", "#FFFF00")}
            </div>
        </div>
        
        <h3 style="font-size: 1em; margin-top: 20px; margin-bottom: 15px;">BEFORE & AFTER</h3>
        
        <div style="display: flex; flex-wrap: wrap;">
            <div style="width: 50%; padding: 10px;">
                <p>CARBON FOOTPRINT (kgCO2e/sqm/yr)</p>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <p>BEFORE: {property_data["Carbon Footprint (kgCO2e/sqm/yr)"]}</p>
                    <p>AFTER: {new_carbon:.1f}</p>
                </div>
                <div class="retro-progress-container" style="background-color: #333333; height: 20px;">
                    <div class="retro-progress-bar" style="width:100%; background-color:#FF0000; height: 20px;"></div>
                </div>
                <div class="retro-progress-container" style="background-color: #333333; height: 20px; margin-top: 5px;">
                    <div class="retro-progress-bar" style="width:{100-total_carbon_reduction}%; background-color:#00FF00; height: 20px;"></div>
                </div>
            </div>
            
            <div style="width: 50%; padding: 10px;">
                <p>ENERGY SCORE (/100)</p>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <p>BEFORE: {property_data["Energy Score"]}</p>
                    <p>AFTER: {new_energy_score:.1f}</p>
                </div>
                <div class="retro-progress-container" style="background-color: #333333; height: 20px;">
                    <div class="retro-progress-bar" style="width:{property_data["Energy Score"]}%; background-color:#FFFF00; height: 20px;"></div>
                </div>
                <div class="retro-progress-container" style="background-color: #333333; height: 20px; margin-top: 5px;">
                    <div class="retro-progress-bar" style="width:{new_energy_score}%; background-color:#00FF00; height: 20px;"></div>
                </div>
            </div>
            
            <div style="width: 100%; padding: 10px; margin-top: 15px;">
                <p>OVERALL ESG SCORE (/100)</p>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <p>BEFORE: {property_data["Overall ESG Score"]:.1f}</p>
                    <p>AFTER: {new_overall_score:.1f}</p>
                </div>
                <div class="retro-progress-container" style="background-color: #333333; height: 25px;">
                    <div class="retro-progress-bar" style="width:{property_data["Overall ESG Score"]}%; background-color:#0088FF; height: 25px;"></div>
                </div>
                <div class="retro-progress-container" style="background-color: #333333; height: 25px; margin-top: 5px;">
                    <div class="retro-progress-bar" style="width:{new_overall_score}%; background-color:#00FFFF; height: 25px;"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("RESET SELECTIONS"):
            st.session_state.selected_retrofits = []
            st.session_state.game_score += 20
            st.session_state.level = (st.session_state.game_score // 1000) + 1
            st.toast("Selections reset! +20 points", icon="🏆")
            st.rerun()
    with col2:
        if st.button("IMPLEMENT RETROFIT PLAN"):
            if len(selected_retrofits_data) > 0:
                st.session_state.game_score += 300
                st.session_state.level = (st.session_state.game_score // 1000) + 1
                st.toast(f"Retrofit plan implemented! +300 points", icon="🏆")
                st.balloons()
            else:
                st.warning("Please select at least one retrofit option first!")

elif current_section == "ESG Reports":
    st.markdown("""
    <div class="pixel-card">
        <p>Generate ESG reports and track compliance with reporting standards.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Report type selector
    report_types = {
        "GRESB": "Global Real Estate Sustainability Benchmark - Comprehensive assessment focused on real estate",
        "SFDR": "Sustainable Finance Disclosure Regulation - EU regulation for financial market transparency",
        "GRI": "Global Reporting Initiative - International standards for sustainability reporting",
        "TCFD": "Task Force on Climate-related Financial Disclosures - Framework for climate-related financial risk"
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_report = st.selectbox("SELECT REPORT TYPE", list(report_types.keys()))
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #000080; border: 2px solid #FFFFFF; padding: 10px; height: 80px;">
            <p style="font-family: 'VT323', monospace; font-size: 18px;">{report_types[selected_report]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Example report metrics
    # This would dynamically pull data from the property portfolio in a real application
    
    # Get portfolio-level statistics
    df = st.session_state.properties_df
    avg_energy_score = df["Energy Score"].mean()
    avg_carbon = df["Carbon Footprint (kgCO2e/sqm/yr)"].mean()
    avg_water = df["Water Usage (L/sqm/yr)"].mean()
    avg_recycling = df["Waste Recycling (%)"].mean()
    
    certified_buildings = df[df["Certification"] != "None"].shape[0]
    certification_percentage = (certified_buildings / df.shape[0]) * 100
    
    avg_env_score = df["Environmental Score"].mean()
    avg_social_score = df["Social Score"].mean()
    avg_gov_score = df["Governance Score"].mean()
    avg_overall_score = df["Overall ESG Score"].mean()
    
    # Display report overview
    st.markdown(f"""
    <div style="background-color: #000080; border: 3px solid #FFFFFF; padding: 20px; 
               box-shadow: 5px 5px 0px #000000; margin-top: 20px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="font-size: 1.2em; margin: 0;">{selected_report} REPORT OVERVIEW</h3>
            <p style="font-family: 'VT323', monospace; background-color: #00AA00; 
                     padding: 5px 10px; margin: 0;">READY TO GENERATE</p>
        </div>
        
        <div style="display: flex; flex-wrap: wrap; margin-bottom: 20px;">
            <div style="width: 50%; padding: 10px;">
                <p style="font-family: 'Press Start 2P', cursive; font-size: 0.9em; color: #FFFF00;">
                    REPORT PERIOD
                </p>
                <p>JAN 2025 - DEC 2025</p>
            </div>
            
            <div style="width: 50%; padding: 10px;">
                <p style="font-family: 'Press Start 2P', cursive; font-size: 0.9em; color: #FFFF00;">
                    COMPLIANCE STATUS
                </p>
                <p style="color: #00FF00;">IN COMPLIANCE</p>
            </div>
        </div>
        
        <h3 style="font-size: 1em; margin-top: 20px; margin-bottom: 15px;">KEY METRICS</h3>
        
        <div style="display: flex; flex-wrap: wrap;">
            <div style="width: 33%; padding: 10px;">
                <p>PROPERTIES ASSESSED</p>
                <p style="font-size: 1.5em; color: #00FFFF;">{df.shape[0]}</p>
            </div>
            
            <div style="width: 33%; padding: 10px;">
                <p>CERTIFIED PROPERTIES</p>
                <p style="font-size: 1.5em; color: #00FFFF;">{certified_buildings} ({certification_percentage:.1f}%)</p>
            </div>
            
            <div style="width: 33%; padding: 10px;">
                <p>AVG CARBON FOOTPRINT</p>
                <p style="font-size: 1.5em; color: #00FFFF;">{avg_carbon:.1f} kgCO2e/sqm/yr</p>
            </div>
            
            <div style="width: 33%; padding: 10px;">
                <p>AVG ENERGY SCORE</p>
                <p style="font-size: 1.5em; color: #00FFFF;">{avg_energy_score:.1f}/100</p>
            </div>
            
            <div style="width: 33%; padding: 10px;">
                <p>AVG WATER USAGE</p>
                <p style="font-size: 1.5em; color: #00FFFF;">{avg_water:.1f} L/sqm/yr</p>
            </div>
            
            <div style="width: 33%; padding: 10px;">
                <p>AVG WASTE RECYCLING</p>
                <p style="font-size: 1.5em; color: #00FFFF;">{avg_recycling:.1f}%</p>
            </div>
        </div>
        
        <h3 style="font-size: 1em; margin-top: 20px; margin-bottom: 15px;">ESG SCORES</h3>
        
        <div style="display: flex; flex-wrap: wrap;">
            <div style="width: 50%; padding: 10px;">
                <p>ENVIRONMENTAL SCORE</p>
                {retro_progress_bar(avg_env_score, "", "#00FF00")}
            </div>
            
            <div style="width: 50%; padding: 10px;">
                <p>SOCIAL SCORE</p>
                {retro_progress_bar(avg_social_score, "", "#FFFF00")}
            </div>
            
            <div style="width: 50%; padding: 10px;">
                <p>GOVERNANCE SCORE</p>
                {retro_progress_bar(avg_gov_score, "", "#FF0000")}
            </div>
            
            <div style="width: 50%; padding: 10px;">
                <p>OVERALL ESG SCORE</p>
                {retro_progress_bar(avg_overall_score, "", "#00FFFF")}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Report visualization
    st.markdown("""
    <h3 style="font-size: 1.2em; margin-top: 30px; margin-bottom: 15px;">REPORT VISUALIZATION</h3>
    """, unsafe_allow_html=True)
    
    # Create chart based on report type
    if selected_report == "GRESB":
        # Create a bubble chart for property comparison
        fig = px.scatter(
            df,
            x="Environmental Score",
            y="Social Score",
            size="Size (sqm)",
            color="Type",
            hover_name="Property Name",
            size_max=50,
            color_discrete_sequence=["#00FF00", "#FFFF00", "#FF0000", "#00FFFF", "#FF00FF"]
        )
        
        fig.update_layout(
            title=dict(
                text="Property ESG Performance Matrix",
                font=dict(family="Press Start 2P", size=16)
            ),
            paper_bgcolor="#000080",
            plot_bgcolor="#000080",
            font=dict(family="VT323", size=16, color="white"),
            xaxis=dict(
                title="Environmental Score",
                title_font=dict(family="Press Start 2P", size=12),
                gridcolor="#333333"
            ),
            yaxis=dict(
                title="Social Score",
                title_font=dict(family="Press Start 2P", size=12),
                gridcolor="#333333"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    elif selected_report == "SFDR":
        # Principal Adverse Impact indicators visualization
        categories = ["Carbon Emissions", "Biodiversity", "Water Usage", "Waste Management", 
                     "Social Issues", "Governance"]
        
        # Random values for demo
        values = [random.randint(30, 90) for _ in range(len(categories))]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker=dict(
                color=["#FF0000", "#FFFF00", "#00FFFF", "#00FF00", "#FF00FF", "#0000FF"],
                line=dict(color="#FFFFFF", width=2)
            )
        ))
        
        fig.update_layout(
            title=dict(
                text="Principal Adverse Impact Indicators",
                font=dict(family="Press Start 2P", size=16)
            ),
            paper_bgcolor="#000080",
            plot_bgcolor="#000080",
            font=dict(family="VT323", size=16, color="white"),
            xaxis=dict(
                title="Categories",
                title_font=dict(family="Press Start 2P", size=12),
                tickfont=dict(family="VT323", size=14)
            ),
            yaxis=dict(
                title="Mitigation Score",
                title_font=dict(family="Press Start 2P", size=12),
                tickfont=dict(family="VT323", size=14),
                gridcolor="#333333"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    elif selected_report == "GRI":
        # Create a stacked bar chart for GRI disclosures compliance
        categories = ["Economic", "Environmental", "Social", "Governance"]
        full_compliance = [random.randint(40, 90) for _ in range(len(categories))]
        partial_compliance = [random.randint(0, 100-v) for v in full_compliance]
        non_compliance = [100 - (full + partial) for full, partial in zip(full_compliance, partial_compliance)]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=full_compliance,
            name="Full Compliance",
            marker=dict(color="#00FF00", line=dict(color="#FFFFFF", width=1))
        ))
        
        fig.add_trace(go.Bar(
            x=categories,
            y=partial_compliance,
            name="Partial Compliance",
            marker=dict(color="#FFFF00", line=dict(color="#FFFFFF", width=1))
        ))
        
        fig.add_trace(go.Bar(
            x=categories,
            y=non_compliance,
            name="Non-Compliance",
            marker=dict(color="#FF0000", line=dict(color="#FFFFFF", width=1))
        ))
        
        fig.update_layout(
            barmode="stack",
            title=dict(
                text="GRI Disclosures Compliance",
                font=dict(family="Press Start 2P", size=16)
            ),
            paper_bgcolor="#000080",
            plot_bgcolor="#000080",
            font=dict(family="VT323", size=16, color="white"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(family="VT323", size=14)
            ),
            xaxis=dict(
                title="Categories",
                title_font=dict(family="Press Start 2P", size=12),
                tickfont=dict(family="VT323", size=14)
            ),
            yaxis=dict(
                title="Percentage",
                title_font=dict(family="Press Start 2P", size=12),
                tickfont=dict(family="VT323", size=14),
                gridcolor="#333333"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    elif selected_report == "TCFD":
        # Create a radar chart for TCFD compliance across dimensions
        categories = ["Governance", "Strategy", "Risk Management", "Metrics & Targets"]
        
        # Random values for demo
        values = [random.randint(50, 95) for _ in range(len(categories))]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current Compliance',
            line=dict(color="#00FFFF"),
            fillcolor="rgba(0, 255, 255, 0.2)"
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[100, 100, 100, 100],
            theta=categories,
            fill='toself',
            name='Target',
            line=dict(color="#FF00FF", dash="dash"),
            fillcolor="rgba(255, 0, 255, 0.1)"
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title=dict(
                text="TCFD Compliance by Dimension",
                font=dict(family="Press Start 2P", size=16)
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.1,
                xanchor="center",
                x=0.5,
                font=dict(family="VT323", size=14)
            ),
            paper_bgcolor="#000080",
            plot_bgcolor="#000080",
            font=dict(family="VT323", size=16, color="white")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Report export options
    st.markdown("""
    <h3 style="font-size: 1.2em; margin-top: 30px; margin-bottom: 15px;">EXPORT OPTIONS</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("GENERATE PDF"):
            st.session_state.game_score += 100
            st.session_state.level = (st.session_state.game_score // 1000) + 1
            st.toast("PDF report generated! +100 points", icon="🏆")
    
    with col2:
        if st.button("GENERATE EXCEL"):
            st.session_state.game_score += 100
            st.session_state.level = (st.session_state.game_score // 1000) + 1
            st.toast("Excel report generated! +100 points", icon="🏆")
    
    with col3:
        if st.button("SHARE REPORT"):
            st.session_state.game_score += 150
            st.session_state.level = (st.session_state.game_score // 1000) + 1
            st.toast("Report shared with stakeholders! +150 points", icon="🏆")