# 🌾 Agricultural Data Dashboard

An interactive Streamlit application that visualizes agricultural data including crop prices, cropland values, and price received indices. Built for comprehensive agricultural market analysis with dynamic filtering and correlation insights.

## 🚀 Live Demo

**Access the live dashboard at:** [Coming Soon - Will be deployed to Streamlit Cloud]

## 📊 Features

### Four Interactive Dashboards:
1. **🌾 Crop Prices (1975-2025)** - National prices for wheat, corn, and soybeans
2. **🏞️ Cropland Values (1997-2025)** - Land values for Kentucky, Indiana, Ohio, and Tennessee  
3. **📊 Price Received Index (1990-2025)** - National agricultural price index (2011=100)
4. **📈 Combined Analysis** - Multi-axis view with correlation analysis

### Interactive Controls:
- **Date Range Selection** - Custom start/end years for focused analysis
- **Zoom Presets** - Quick access to recent trends (Last 5/10/20 years)
- **Data Series Selection** - Choose specific crops or states to display
- **Dynamic Statistics** - Auto-updating metrics based on selections
- **Export Capabilities** - Download charts as PNG files

### Advanced Analytics:
- **Correlation Analysis** - Statistical relationships between datasets
- **Volatility Metrics** - Price variation and market stability indicators
- **Growth Rate Calculations** - Land value appreciation over time
- **Comparative Insights** - Side-by-side analysis across different metrics

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly (interactive charts with secondary axes)
- **Data Processing**: Pandas
- **Deployment**: Streamlit Community Cloud

## 📁 Project Structure

```
BAE599Homework2/
├── streamlit_app.py          # Main application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── Crop Prices.csv          # National crop price data
├── Cropland Value.csv       # State-level land value data
└── PriceReceivedIndex.csv   # National price index data
```

## 🔧 Local Development

### Prerequisites
- Python 3.9+
- pip package manager

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [repository-url]
   cd BAE599Homework2
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access locally:**
   Open your browser to `http://localhost:8501`

## 📈 Data Sources

- **Crop Prices**: USDA National Agricultural Statistics Service (NASS)
- **Cropland Values**: USDA NASS Agricultural Land Values
- **Price Index**: USDA NASS Price Received Index (2011 baseline)

### Data Coverage:
- **Geographic**: National (crops/index) and state-level (land values)
- **Temporal**: 1975-2025 (crops), 1997-2025 (land), 1990-2025 (index)
- **Frequency**: Annual data points

## 🎯 Use Cases

- **Academic Research** - Agricultural economics and policy analysis
- **Market Analysis** - Investment decisions and trend identification  
- **Educational Tool** - Teaching agricultural market dynamics
- **Policy Planning** - Government and industry strategic planning

## 🔄 Interactive Features Guide

### Tab Navigation
- Click tabs to switch between different analytical views
- Each tab maintains independent settings and zoom levels

### Data Selection
- Use dropdowns to select specific crops or states
- Statistics automatically update to reflect visible data
- Single-selection mode provides enhanced detailed analysis

### Date Range Controls
- **Custom Range**: Set specific start/end years
- **Quick Presets**: "Last 10 Years", "Since 2000", etc.
- **Smart Filtering**: Charts and statistics update instantly

### Chart Interactions
- **Hover**: View exact values and dates
- **Zoom**: Click and drag to focus on specific periods
- **Pan**: Shift+drag to navigate across time
- **Legend**: Click to show/hide data series
- **Download**: Export charts as high-quality images

## 📊 Statistical Features

### Single-Item Analysis (when one crop/state selected):
- Latest values with timestamps
- Historical averages over selected period
- Price ranges and volatility metrics
- Growth rates and trend analysis

### Multi-Item Comparison:
- Side-by-side metric comparisons
- Relative performance analysis
- Cross-dataset correlations (Combined View)

## 🚀 Deployment

This application is deployed on Streamlit Community Cloud for free public access. 

### Deployment Benefits:
- ✅ **Free Hosting** - No cost for public repositories
- ✅ **Automatic Updates** - Syncs with GitHub commits
- ✅ **SSL Certificate** - Secure HTTPS access
- ✅ **Custom URLs** - Professional web addresses
- ✅ **Analytics** - Usage tracking and monitoring

## 🤝 Contributing

This project was developed for BAE 599 coursework. For suggestions or improvements:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

## 📄 License

This project is for educational purposes as part of BAE 599 coursework.

## 📞 Contact

For questions about this agricultural dashboard or data analysis:
- Course: BAE 599
- Project: Homework 2 - Agricultural Data Visualization

---

**Built with ❤️ for agricultural data analysis and education**
