import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Agricultural Data Dashboard",
    page_icon="🌾",
    layout="wide"
)

# Main title
st.title("🌾 Agricultural Data Dashboard")
st.markdown("Interactive visualizations of crop prices, cropland values, and price received index")

# Function to load and process crop prices data
@st.cache_data
def load_crop_prices():
    df = pd.read_csv("Crop Prices.csv")
    # Filter for national data and the three crops we want
    crops_of_interest = ['CORN', 'SOYBEANS', 'WHEAT']
    df_filtered = df[
        (df['Geo Level'] == 'NATIONAL') & 
        (df['Commodity'].isin(crops_of_interest))
    ].copy()
    
    # Clean and convert data types
    df_filtered['Value'] = pd.to_numeric(df_filtered['Value'], errors='coerce')
    df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')
    
    # Filter for years 1975-2025
    df_filtered = df_filtered[(df_filtered['Year'] >= 1975) & (df_filtered['Year'] <= 2025)]
    
    return df_filtered

# Function to load and process cropland value data
@st.cache_data
def load_cropland_values():
    df = pd.read_csv("Cropland Value.csv")
    # Filter for the four states we want
    states_of_interest = ['KENTUCKY', 'INDIANA', 'OHIO', 'TENNESSEE']
    df_filtered = df[df['State'].isin(states_of_interest)].copy()
    
    # Clean and convert data types - remove commas from Value column
    df_filtered['Value'] = df_filtered['Value'].astype(str).str.replace(',', '').astype(float)
    df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')
    
    # Filter for years 1997-2025
    df_filtered = df_filtered[(df_filtered['Year'] >= 1997) & (df_filtered['Year'] <= 2025)]
    
    return df_filtered

# Function to load and process price received index data
@st.cache_data
def load_price_received_index():
    df = pd.read_csv("PriceReceivedIndex.csv")
    # Filter for national data
    df_filtered = df[df['Geo Level'] == 'NATIONAL'].copy()
    
    # Clean and convert data types
    df_filtered['Value'] = pd.to_numeric(df_filtered['Value'], errors='coerce')
    df_filtered['Year'] = pd.to_numeric(df_filtered['Year'], errors='coerce')
    
    # Filter for years 1990-2025
    df_filtered = df_filtered[(df_filtered['Year'] >= 1990) & (df_filtered['Year'] <= 2025)]
    
    return df_filtered

# Load all data
crop_prices_df = load_crop_prices()
cropland_values_df = load_cropland_values()
price_index_df = load_price_received_index()

# Create tabs for each chart
tab1, tab2, tab3, tab4 = st.tabs(["🌾 Crop Prices", "🏞️ Cropland Values", "📊 Price Index", "📈 Combined View"])

# Tab 1: Crop Prices
with tab1:
    st.header("National Crop Prices (1975-2025)")
    st.markdown("*Wheat, Corn, and Soybeans prices in dollars per bushel*")
    
    # Interactive controls for crop prices
    col1, col2, col3, col4 = st.columns([2, 2, 1, 2])
    
    with col1:
        crop_start_year = st.selectbox(
            "Start Year", 
            options=sorted(crop_prices_df['Year'].unique()),
            index=0,
            key="crop_start"
        )
    
    with col2:
        crop_end_year = st.selectbox(
            "End Year", 
            options=sorted(crop_prices_df['Year'].unique()),
            index=len(sorted(crop_prices_df['Year'].unique()))-1,
            key="crop_end"
        )
    
    with col3:
        crop_zoom = st.selectbox(
            "Zoom Level",
            options=["Full View", "Last 10 Years", "Last 20 Years", "Custom Range"],
            index=0,
            key="crop_zoom"
        )
    
    with col4:
        selected_crops = st.multiselect(
            "Select Crops to Display",
            options=['CORN', 'SOYBEANS', 'WHEAT'],
            default=['CORN', 'SOYBEANS', 'WHEAT'],
            key="selected_crops"
        )
    
    # Apply zoom and date filters
    if crop_zoom == "Last 10 Years":
        crop_start_year = max(crop_prices_df['Year']) - 9
        crop_end_year = max(crop_prices_df['Year'])
    elif crop_zoom == "Last 20 Years":
        crop_start_year = max(crop_prices_df['Year']) - 19
        crop_end_year = max(crop_prices_df['Year'])
    elif crop_zoom == "Full View":
        crop_start_year = min(crop_prices_df['Year'])
        crop_end_year = max(crop_prices_df['Year'])
    
    # Filter data based on selected date range and selected crops
    crop_filtered = crop_prices_df[
        (crop_prices_df['Year'] >= crop_start_year) & 
        (crop_prices_df['Year'] <= crop_end_year) &
        (crop_prices_df['Commodity'].isin(selected_crops))
    ]
    
    if not crop_prices_df.empty and len(selected_crops) > 0:
        fig1 = px.line(
            crop_filtered, 
            x='Year', 
            y='Value', 
            color='Commodity',
            title=f"Crop Prices - Dollars per Bushel ({crop_start_year}-{crop_end_year})",
            labels={
                'Value': 'Price ($/bushel)',
                'Year': 'Year',
                'Commodity': 'Crop'
            },
            height=600
        )
        
        fig1.update_layout(
            xaxis_title="Year",
            yaxis_title="Price ($/bushel)",
            legend_title="Crop",
            hovermode='x unified',
            font=dict(size=14),
            xaxis=dict(range=[crop_start_year, crop_end_year])
        )
        
        # Customize line colors
        color_map = {'CORN': '#FFD700', 'SOYBEANS': '#228B22', 'WHEAT': '#DEB887'}
        for i, commodity in enumerate(['CORN', 'SOYBEANS', 'WHEAT']):
            if commodity in crop_filtered['Commodity'].values:
                commodity_data = crop_filtered[crop_filtered['Commodity'] == commodity]
                if not commodity_data.empty:
                    for trace in fig1.data:
                        if trace.name == commodity:
                            trace.line.color = color_map[commodity]
                            trace.line.width = 3
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # Add summary statistics for filtered data
        st.subheader(f"Summary Statistics ({crop_start_year}-{crop_end_year})")
        
        # Dynamic statistics based on selected crops
        if len(selected_crops) == 0:
            st.warning("Please select at least one crop to display data and statistics.")
        elif len(selected_crops) == 1:
            # Single crop view
            crop = selected_crops[0]
            crop_data = crop_filtered[crop_filtered['Commodity'] == crop]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                latest_price = crop_data['Value'].iloc[0] if len(crop_data) > 0 else 0
                st.metric(
                    label=f"{crop.title()} - Latest Price",
                    value=f"${latest_price:.2f}/bushel",
                    delta=f"Year: {crop_data['Year'].iloc[0] if len(crop_data) > 0 else 'N/A'}"
                )
            
            with col2:
                avg_price = crop_data['Value'].mean()
                st.metric(
                    label=f"{crop.title()} - Average Price",
                    value=f"${avg_price:.2f}/bushel",
                    delta=f"Period: {crop_start_year}-{crop_end_year}"
                )
            
            with col3:
                price_range = f"${crop_data['Value'].min():.2f} - ${crop_data['Value'].max():.2f}"
                volatility = crop_data['Value'].std()
                st.metric(
                    label=f"{crop.title()} - Price Range",
                    value=price_range,
                    delta=f"Volatility: ${volatility:.2f}"
                )
                
            # Additional insights for single crop
            st.info(f"📊 **{crop.title()} Analysis**: Showing detailed statistics for {crop.lower()} only. "
                   f"Click other crops in the legend above to compare, or click {crop.lower()} again to hide it.")
                   
        else:
            # Multi-crop view - only show selected crops
            if len(selected_crops) <= 3 and len(selected_crops) > 0:
                cols = st.columns(len(selected_crops))
            else:
                cols = st.columns(3)
            
            for i, crop in enumerate(selected_crops):
                crop_data = crop_filtered[crop_filtered['Commodity'] == crop]
                if not crop_data.empty:
                    with cols[i % len(cols)]:
                        latest_price = crop_data['Value'].iloc[0] if len(crop_data) > 0 else 0
                        st.metric(
                            label=f"{crop.title()} ($/bushel)",
                            value=f"${latest_price:.2f}",
                            delta=f"Latest in range"
                        )
                        st.caption(f"Avg: ${crop_data['Value'].mean():.2f} | Range: ${crop_data['Value'].min():.2f}-${crop_data['Value'].max():.2f}")
        
        # Instructions
        st.markdown("💡 **Tip**: Use the 'Select Crops to Display' dropdown above to focus on specific crops. Statistics will update automatically!")
    else:
        st.error("No crop price data available for the specified time period.")

# Tab 2: Cropland Values
with tab2:
    st.header("Cropland Values (1997-2025)")
    st.markdown("*Kentucky, Indiana, Ohio, and Tennessee cropland values in dollars per acre*")
    
    # Interactive controls for cropland values
    col1, col2, col3, col4 = st.columns([2, 2, 1, 2])
    
    with col1:
        land_start_year = st.selectbox(
            "Start Year", 
            options=sorted(cropland_values_df['Year'].unique()),
            index=0,
            key="land_start"
        )
    
    with col2:
        land_end_year = st.selectbox(
            "End Year", 
            options=sorted(cropland_values_df['Year'].unique()),
            index=len(sorted(cropland_values_df['Year'].unique()))-1,
            key="land_end"
        )
    
    with col3:
        land_zoom = st.selectbox(
            "Zoom Level",
            options=["Full View", "Last 5 Years", "Last 10 Years", "Custom Range"],
            index=0,
            key="land_zoom"
        )
    
    with col4:
        selected_states = st.multiselect(
            "Select States to Display",
            options=['KENTUCKY', 'INDIANA', 'OHIO', 'TENNESSEE'],
            default=['KENTUCKY', 'INDIANA', 'OHIO', 'TENNESSEE'],
            key="selected_states"
        )
    
    # Apply zoom and date filters
    if land_zoom == "Last 5 Years":
        land_start_year = max(cropland_values_df['Year']) - 4
        land_end_year = max(cropland_values_df['Year'])
    elif land_zoom == "Last 10 Years":
        land_start_year = max(cropland_values_df['Year']) - 9
        land_end_year = max(cropland_values_df['Year'])
    elif land_zoom == "Full View":
        land_start_year = min(cropland_values_df['Year'])
        land_end_year = max(cropland_values_df['Year'])
    
    # Filter data based on selected date range and selected states
    land_filtered = cropland_values_df[
        (cropland_values_df['Year'] >= land_start_year) & 
        (cropland_values_df['Year'] <= land_end_year) &
        (cropland_values_df['State'].isin(selected_states))
    ]
    
    if not cropland_values_df.empty and len(selected_states) > 0:
        fig2 = px.line(
            land_filtered, 
            x='Year', 
            y='Value', 
            color='State',
            title=f"Cropland Values - Dollars per Acre ({land_start_year}-{land_end_year})",
            labels={
                'Value': 'Value ($/acre)',
                'Year': 'Year',
                'State': 'State'
            },
            height=600
        )
        
        fig2.update_layout(
            xaxis_title="Year",
            yaxis_title="Value ($/acre)",
            legend_title="State",
            hovermode='x unified',
            font=dict(size=14),
            xaxis=dict(range=[land_start_year, land_end_year])
        )
        
        # Customize line colors
        color_map = {'KENTUCKY': '#FF6B6B', 'INDIANA': '#4ECDC4', 'OHIO': '#45B7D1', 'TENNESSEE': '#96CEB4'}
        for state in ['KENTUCKY', 'INDIANA', 'OHIO', 'TENNESSEE']:
            if state in land_filtered['State'].values:
                for trace in fig2.data:
                    if trace.name == state:
                        trace.line.color = color_map[state]
                        trace.line.width = 3
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Add summary statistics for filtered data
        st.subheader(f"Summary Statistics ({land_start_year}-{land_end_year})")
        
        # Dynamic statistics based on selected states
        if len(selected_states) == 0:
            st.warning("Please select at least one state to display data and statistics.")
        elif len(selected_states) == 1:
            # Single state view
            state = selected_states[0]
            state_data = land_filtered[land_filtered['State'] == state]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                latest_value = state_data['Value'].iloc[0] if len(state_data) > 0 else 0
                st.metric(
                    label=f"{state.title()} - Latest Value",
                    value=f"${latest_value:,.0f}/acre",
                    delta=f"Year: {state_data['Year'].iloc[0] if len(state_data) > 0 else 'N/A'}"
                )
            
            with col2:
                avg_value = state_data['Value'].mean()
                st.metric(
                    label=f"{state.title()} - Average Value",
                    value=f"${avg_value:,.0f}/acre",
                    delta=f"Period: {land_start_year}-{land_end_year}"
                )
            
            with col3:
                growth_rate = ((state_data['Value'].iloc[0] - state_data['Value'].iloc[-1]) / state_data['Value'].iloc[-1] * 100) if len(state_data) > 1 else 0
                st.metric(
                    label=f"{state.title()} - Growth Rate",
                    value=f"{growth_rate:+.1f}%",
                    delta=f"Over period"
                )
            
            # Additional insights for single state
            st.info(f"🏞️ **{state.title()} Analysis**: Showing detailed statistics for {state.title()} only. "
                   f"Click other states in the legend above to compare, or click {state.title()} again to hide it.")
                   
        else:
            # Multi-state view - only show selected states
            if len(selected_states) <= 4 and len(selected_states) > 0:
                cols = st.columns(len(selected_states))
            else:
                cols = st.columns(4)
            
            for i, state in enumerate(selected_states):
                state_data = land_filtered[land_filtered['State'] == state]
                if not state_data.empty:
                    with cols[i % len(cols)]:
                        latest_value = state_data['Value'].iloc[0] if len(state_data) > 0 else 0
                        st.metric(
                            label=f"{state.title()} ($/acre)",
                            value=f"${latest_value:,.0f}",
                            delta=f"Latest in range"
                        )
                        st.caption(f"Avg: ${state_data['Value'].mean():,.0f} | Range: ${state_data['Value'].min():,.0f}-${state_data['Value'].max():,.0f}")
        
        # Instructions
        st.markdown("💡 **Tip**: Use the 'Select States to Display' dropdown above to focus on specific states. Statistics will update automatically!")
    else:
        st.error("No cropland value data available for the specified time period.")

# Tab 3: Price Received Index
with tab3:
    st.header("Price Received Index (1990-2025)")
    st.markdown("*National index of price received (2011 = 100)*")
    
    # Interactive controls for price index
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        index_start_year = st.selectbox(
            "Start Year", 
            options=sorted(price_index_df['Year'].unique()),
            index=0,
            key="index_start"
        )
    
    with col2:
        index_end_year = st.selectbox(
            "End Year", 
            options=sorted(price_index_df['Year'].unique()),
            index=len(sorted(price_index_df['Year'].unique()))-1,
            key="index_end"
        )
    
    with col3:
        index_zoom = st.selectbox(
            "Zoom Level",
            options=["Full View", "Last 5 Years", "Last 10 Years", "Since 2010", "Custom Range"],
            index=0,
            key="index_zoom"
        )
    
    # Apply zoom and date filters
    if index_zoom == "Last 5 Years":
        index_start_year = max(price_index_df['Year']) - 4
        index_end_year = max(price_index_df['Year'])
    elif index_zoom == "Last 10 Years":
        index_start_year = max(price_index_df['Year']) - 9
        index_end_year = max(price_index_df['Year'])
    elif index_zoom == "Since 2010":
        index_start_year = 2010
        index_end_year = max(price_index_df['Year'])
    elif index_zoom == "Full View":
        index_start_year = min(price_index_df['Year'])
        index_end_year = max(price_index_df['Year'])
    
    # Filter data based on selected date range
    index_filtered = price_index_df[
        (price_index_df['Year'] >= index_start_year) & 
        (price_index_df['Year'] <= index_end_year)
    ]
    
    if not price_index_df.empty:
        fig3 = px.line(
            index_filtered, 
            x='Year', 
            y='Value',
            title=f"National Price Received Index ({index_start_year}-{index_end_year})",
            labels={
                'Value': 'Price Index (2011 = 100)',
                'Year': 'Year'
            },
            height=600
        )
        
        fig3.update_layout(
            xaxis_title="Year",
            yaxis_title="Price Index (2011 = 100)",
            hovermode='x',
            font=dict(size=14),
            xaxis=dict(range=[index_start_year, index_end_year])
        )
        
        # Customize line color and add markers
        fig3.update_traces(line_color='#E74C3C', line_width=3, mode='lines+markers', marker_size=4)
        
        st.plotly_chart(fig3, use_container_width=True)
        
        # Add summary statistics for filtered data
        st.subheader(f"Summary Statistics ({index_start_year}-{index_end_year})")
        col1, col2, col3 = st.columns(3)
        
        if len(index_filtered) > 0:
            with col1:
                latest_index = index_filtered['Value'].iloc[0]
                st.metric(
                    label=f"Latest Index ({index_filtered['Year'].iloc[0]:.0f})",
                    value=f"{latest_index:.1f}",
                    delta=f"{latest_index - 100:.1f} vs 2011 baseline"
                )
            
            with col2:
                avg_index = index_filtered['Value'].mean()
                st.metric(
                    label="Average Index",
                    value=f"{avg_index:.1f}",
                    delta=f"Range: {index_start_year}-{index_end_year}"
                )
            
            with col3:
                peak_index = index_filtered['Value'].max()
                peak_year = index_filtered.loc[index_filtered['Value'].idxmax(), 'Year']
                st.metric(
                    label="Peak Index",
                    value=f"{peak_index:.1f}",
                    delta=f"Year: {peak_year:.0f}"
                )
    else:
        st.error("No price received index data available for the specified time period.")

# Tab 4: Combined View
with tab4:
    st.header("Combined Agricultural Data Analysis")
    st.markdown("*All datasets combined with multiple Y-axes for comprehensive analysis*")
    
    # Interactive controls for combined view
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        combined_start_year = st.selectbox(
            "Start Year", 
            options=list(range(1990, 2026)),  # Common range for meaningful comparison
            index=7,  # Start at 1997
            key="combined_start"
        )
    
    with col2:
        combined_end_year = st.selectbox(
            "End Year", 
            options=list(range(1990, 2026)),
            index=35,  # End at 2025
            key="combined_end"
        )
    
    with col3:
        combined_zoom = st.selectbox(
            "Time Period",
            options=["Custom Range", "Last 10 Years", "Last 15 Years", "Since 2000", "Full Range (1997-2025)"],
            index=0,
            key="combined_zoom"
        )
    
    # Apply zoom and date filters
    if combined_zoom == "Last 10 Years":
        combined_start_year = 2015
        combined_end_year = 2025
    elif combined_zoom == "Last 15 Years":
        combined_start_year = 2010
        combined_end_year = 2025
    elif combined_zoom == "Since 2000":
        combined_start_year = 2000
        combined_end_year = 2025
    elif combined_zoom == "Full Range (1997-2025)":
        combined_start_year = 1997
        combined_end_year = 2025
    
    # Filter all datasets to the common time range
    crop_combined = crop_prices_df[
        (crop_prices_df['Year'] >= combined_start_year) & 
        (crop_prices_df['Year'] <= combined_end_year)
    ]
    
    land_combined = cropland_values_df[
        (cropland_values_df['Year'] >= combined_start_year) & 
        (cropland_values_df['Year'] <= combined_end_year)
    ]
    
    index_combined = price_index_df[
        (price_index_df['Year'] >= combined_start_year) & 
        (price_index_df['Year'] <= combined_end_year)
    ]
    
    if not crop_combined.empty and not land_combined.empty and not index_combined.empty:
        # Create subplot with secondary y-axes using plotly.graph_objects
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        
        # Create figure with secondary y-axis
        fig_combined = make_subplots(
            specs=[[{"secondary_y": True}]],
            subplot_titles=[f"Combined Agricultural Data ({combined_start_year}-{combined_end_year})"]
        )
        
        # Add crop prices (primary y-axis)
        colors_crops = {'CORN': '#FFD700', 'SOYBEANS': '#228B22', 'WHEAT': '#DEB887'}
        for crop in ['CORN', 'SOYBEANS', 'WHEAT']:
            crop_data = crop_combined[crop_combined['Commodity'] == crop]
            if not crop_data.empty:
                fig_combined.add_trace(
                    go.Scatter(
                        x=crop_data['Year'],
                        y=crop_data['Value'],
                        mode='lines+markers',
                        name=f"{crop.title()} Price",
                        line=dict(color=colors_crops[crop], width=3),
                        marker=dict(size=4),
                        yaxis='y'
                    ),
                    secondary_y=False
                )
        
        # Add price index (secondary y-axis - left side)
        if not index_combined.empty:
            fig_combined.add_trace(
                go.Scatter(
                    x=index_combined['Year'],
                    y=index_combined['Value'],
                    mode='lines+markers',
                    name='Price Index',
                    line=dict(color='#E74C3C', width=3, dash='dash'),
                    marker=dict(size=4),
                    yaxis='y2'
                ),
                secondary_y=True
            )
        
        # Calculate average cropland value for secondary axis
        land_avg_by_year = land_combined.groupby('Year')['Value'].mean().reset_index()
        land_avg_by_year.columns = ['Year', 'Avg_Value']
        
        if not land_avg_by_year.empty:
            fig_combined.add_trace(
                go.Scatter(
                    x=land_avg_by_year['Year'],
                    y=land_avg_by_year['Avg_Value'],
                    mode='lines+markers',
                    name='Avg Cropland Value',
                    line=dict(color='#9B59B6', width=3, dash='dot'),
                    marker=dict(size=4),
                    yaxis='y3'
                ),
                secondary_y=True
            )
        
        # Update layout with multiple y-axes
        fig_combined.update_layout(
            title=f"Comprehensive Agricultural Analysis ({combined_start_year}-{combined_end_year})",
            xaxis_title="Year",
            height=700,
            hovermode='x unified',
            font=dict(size=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Set y-axes titles
        fig_combined.update_yaxes(title_text="Crop Prices ($/bushel)", secondary_y=False, side='left')
        fig_combined.update_yaxes(title_text="Price Index (2011=100) / Cropland Value ($/acre)", secondary_y=True, side='right')
        
        # Adjust y-axis ranges for better visualization
        if not land_avg_by_year.empty and not index_combined.empty:
            # Scale the cropland values to fit with price index
            land_max = land_avg_by_year['Avg_Value'].max()
            index_max = index_combined['Value'].max()
            scale_factor = index_max / land_max * 100  # Adjust scaling
            
            fig_combined.update_yaxes(
                range=[0, crop_combined['Value'].max() * 1.1], 
                secondary_y=False
            )
            fig_combined.update_yaxes(
                range=[0, max(index_combined['Value'].max(), land_avg_by_year['Avg_Value'].max() * scale_factor) * 1.1], 
                secondary_y=True
            )
        
        st.plotly_chart(fig_combined, use_container_width=True)
        
        # Add explanatory text
        st.info("""
        **📊 Reading the Combined Chart:**
        - **Left Y-axis (Crop Prices)**: Shows wheat, corn, and soybean prices in $/bushel
        - **Right Y-axis (Dual Scale)**: Shows both Price Index (2011=100) and Average Cropland Value ($/acre)
        - **Line Styles**: Solid lines = Crop prices, Dashed line = Price Index, Dotted line = Cropland values
        """)
        
        # Summary statistics for combined view
        st.subheader(f"Comparative Analysis ({combined_start_year}-{combined_end_year})")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if not crop_combined.empty:
                avg_corn = crop_combined[crop_combined['Commodity'] == 'CORN']['Value'].mean()
                st.metric(
                    label="Avg Corn Price",
                    value=f"${avg_corn:.2f}/bu",
                    delta="Primary axis"
                )
        
        with col2:
            if not index_combined.empty:
                avg_index = index_combined['Value'].mean()
                current_index = index_combined['Value'].iloc[0] if len(index_combined) > 0 else 0
                st.metric(
                    label="Avg Price Index", 
                    value=f"{avg_index:.1f}",
                    delta=f"Current: {current_index:.1f}"
                )
        
        with col3:
            if not land_avg_by_year.empty:
                avg_land = land_avg_by_year['Avg_Value'].mean()
                current_land = land_avg_by_year['Avg_Value'].iloc[-1] if len(land_avg_by_year) > 0 else 0
                st.metric(
                    label="Avg Cropland Value",
                    value=f"${avg_land:,.0f}/acre",
                    delta=f"Current: ${current_land:,.0f}"
                )
        
        with col4:
            # Correlation analysis
            if len(crop_combined[crop_combined['Commodity'] == 'CORN']) > 0 and len(index_combined) > 0:
                corn_data = crop_combined[crop_combined['Commodity'] == 'CORN'].set_index('Year')['Value']
                index_data = index_combined.set_index('Year')['Value']
                
                # Find common years for correlation
                common_years = corn_data.index.intersection(index_data.index)
                if len(common_years) > 1:
                    correlation = corn_data.loc[common_years].corr(index_data.loc[common_years])
                    st.metric(
                        label="Corn-Index Correlation",
                        value=f"{correlation:.3f}",
                        delta="Relationship strength"
                    )
        
        # Additional insights
        st.subheader("📈 Market Insights")
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.markdown("""
            **🌾 Crop Price Trends:**
            - Track seasonal and cyclical price patterns
            - Compare relative price movements between crops
            - Identify price volatility periods
            """)
            
        with insights_col2:
            st.markdown("""
            **🏞️ Land Value & Economic Indicators:**
            - Observe how land values respond to crop prices
            - Monitor price index as economic health indicator
            - Analyze long-term agricultural investment trends
            """)
            
    else:
        st.warning("Insufficient data overlap between datasets for the selected time period. Try selecting a range between 1997-2025.")

# Add some spacing and additional information
st.markdown("---")
st.markdown("### 📈 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(f"**🌾 Crop Prices**\n\n"
            f"• **Records**: {len(crop_prices_df)}\n\n"
            f"• **Crops**: Corn, Soybeans, Wheat\n\n"
            f"• **Time Range**: 1975-2025\n\n"
            f"• **Unit**: Dollars per bushel")

with col2:
    st.info(f"**🏞️ Cropland Values**\n\n"
            f"• **Records**: {len(cropland_values_df)}\n\n"
            f"• **States**: KY, IN, OH, TN\n\n"
            f"• **Time Range**: 1997-2025\n\n"
            f"• **Unit**: Dollars per acre")

with col3:
    st.info(f"**📊 Price Index**\n\n"
            f"• **Records**: {len(price_index_df)}\n\n"
            f"• **Scope**: National index\n\n"
            f"• **Time Range**: 1990-2025\n\n"
            f"• **Base Year**: 2011 = 100")

with col4:
    st.info(f"**📈 Combined View**\n\n"
            f"• **Multi-axis**: All data combined\n\n"
            f"• **Correlations**: Cross-dataset analysis\n\n"
            f"• **Time Range**: 1997-2025\n\n"
            f"• **Features**: Secondary Y-axes")

# Interactive features information
st.markdown("### 🎯 Interactive Features")
st.markdown("""
- **📱 Tab Navigation**: Click on the tabs above to switch between different charts
- **� Date Range Controls**: Use the Start Year and End Year dropdowns to customize the time period displayed
- **🔍 Zoom Level Presets**: Quick zoom options like "Last 10 Years", "Last 5 Years", or "Full View"
- **�🖱️ Hover**: Hover over data points to see exact values and year information
- **🔍 Chart Zoom**: Click and drag on the chart to zoom into specific areas
- **↔️ Pan**: Hold Shift and drag to pan across the chart horizontally
- **👁️ Legend**: Click legend items to show/hide specific lines in the chart
- **📷 Download**: Use the camera icon in the chart toolbar to save charts as PNG files
- **🔄 Reset**: Double-click anywhere on the chart to reset zoom to the original view
- **📊 Dynamic Statistics**: Summary statistics automatically update based on your selected date range
- **⚡ Real-time Updates**: Charts and statistics update instantly when you change date ranges or zoom levels
""")
