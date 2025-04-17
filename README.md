# Pathfinder App
**Get there, no matter where.**

## About Us - Pathfinder
Pathfinder app was developed with a clear purpose: to enhance the VGI-Flexi transportation model for the Ingolstadt Regional Area, making on-demand transit more efficient and accessible. Our mission is to provide the best data-driven solutions to public transportation systems to improve mobility, reduce wait times, and promote sustainability.

## Our Vision
The **Pathfinder app** leverages cutting-edge machine learning models and data analysis to predict transportation demand, optimize bus placement, and streamline routing for better service. Our goal is to provide real-time insights into the demand for public transportation pickups in rural areas, helping to make mobility easier and more efficient.

## Our Services
With VGI-provided data, we've visualized essential insights, including:
- **High-demand zones**
- **Hotspots**
- **Patterns behind canceled and completed trips**

Through analyzing these data points and recognizing high cancellation rates, we've developed a fully integrated solution to improve the VGI-Flexi transportation system.

## Key Features
### 1. **Demand Prediction**
"We use the **Prophet model** to forecast demand trends, empowering operators to anticipate needs for the next day, week, and peak periods. This predictive capability helps reduce service gaps and improve scheduling."

### 2. **Strategic Bus Repositioning**
"Since **Flexi buses** lack static positioning, our algorithm strategically places buses closer to anticipated pickup areas. This readiness reduces wait times and minimizes cancellations, ensuring resources are aligned where they're needed most."

### 3. **Optimized Routing**
"Pathfinder calculates **fast and carbon-efficient routes**, supporting timely pickups while reducing emissions—a crucial aspect for sustainable rural mobility."

### 4. **Pre-positioning Algorithm**
"Our **pre-positioning algorithm** dynamically adjusts bus placements based on demand predictions, ensuring buses are stationed in areas with the highest expected demand. This helps ensure buses are ready and in place when passengers need them, minimizing delays and cancellations."

### 5. **DaRP (Dial-a-Route Solution)**
"Pathfinder implements a **Dial-a-Route Solution (DaRP)** with **time-sensitive pickup scheduling**. This solution allows customers to request a ride within a specific time window, ensuring more flexible and efficient pickups. The DaRP solution optimizes routes based on real-time requests, improving service reliability and reducing wait times."

## Products
### Demand Forecasting & Actual Demand
This product predicts the demand for public transportation pickups in the **VGI region**. Using machine learning, it forecasts future demand based on historical data. 

It also helps visualize actual demand for pickups in the **VGI region**. It shows the real-time or historical demand data, allowing you to analyze patterns.

The link to the product:
[Demand Forecasting](https://pathfinders.streamlit.app/)

### Prepositioning & DaRP

The link to the product:
[Pre-positioning and DaRP](https://pathfinders2.streamlit.app/)

## Installation
### 1. Clone the Repository
Start by cloning the repository to your local machine:
```bash
git clone https://github.com/yourusername/Pathfinders.git
cd pathfinder-app
```

### 2. Install Core Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Additional Packages for Notebooks
```bash
pip install numpy matplotlib ydata_profiling
```

### 4. Configure API Keys
Create a `.env` file in the root directory or set environment variables to store your API key:

```bash
# Example .env file
ORS_API_KEY=your_api_key_here
```

In your code, access the API key like this:
```python
ors_client = openrouteservice.Client(key=os.getenv('ORS_API_KEY'))
```
