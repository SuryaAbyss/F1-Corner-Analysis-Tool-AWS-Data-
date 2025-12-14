# F1 Corner Analysis Tool (AWS Data)

A powerful, Python-based analysis suite designed to provide granular insights into Formula 1 driver performance through specific corners and track sectors. Leveraging the `FastF1` library to access AWS-powered F1 telemetry, this tool allows for comprehensive comparisons between drivers, visualizing speed differentials, braking points, and throttle application.

## 🚀 Overview

This project enables users to analyze how different drivers approach specific parts of an interactively selected track. By specifying a race session and a track segment (in meters), the tool retrieves telemetry data and generates a detailed visualization containing:
1.  **Speed Trace Comparison:** A line chart overlaying the speed profiles of two drivers, highlighting where one gains or loses time against the other.
2.  **Telemetry Action Map:** A horizontal bar chart decomposing driver inputs into three distinct states:
    *   🟢 **Full Throttle**
    *   🔴 **Brake**
    *   ⚪ **Cornering** (Partial throttle/Coasting)

## ✨ Features

*   **Multi-Mode Usage:** Run as a web application, a standalone script, or an interactive Jupyter Notebook.
*   **Live Data Integration:** Fetches real-time/historical data directly from F1's live timing API via `FastF1`.
*   **Dynamic Comparisons:** Compare any two drivers from any session (Practice, Qualifying, Race) from 2018 onwards.
*   **Custom Sector Analysis:** Focus on specific corners by defining start and end distances (e.g., "Silverstone Maggotts-Becketts" sector).
*   **Visual Analytics:**
    *   **Speed Deltas:** Automatically calculates and displays the average speed difference in the selected sector.
    *   **Action Breakdown:** visualizes exactly *where* and *for how long* drivers are braking or on throttle.

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **Web Framework:** Flask
*   **Data Analysis:** Pandas, NumPy, FastF1
*   **Visualization:** Matplotlib

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/F1-Corner-Analysis-Tool.git
    cd F1-Corner-Analysis-Tool
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

## 🖥️ Usage

You can use this tool in three different ways depending on your needs.

### 1. Web Application (Interactive UI)
The easiest way to explore data interactively.
*   Run the Flask app:
    ```bash
    python web/app.py
    ```
*   Open your browser and navigate to `http://127.0.0.1:5000/`.
*   Enter the details (Year, Grand Prix, Session, Drivers, Distance Range) and click "Analyze".

### 2. Standalone Script
Generate a quick static report image without a UI.
*   Open `run_analysis.py` and modify the configuration variables at the top:
    ```python
    driver_1, driver_2 = 'HAM', 'VER'
    distance_min, distance_max = 4800, 5500 
    ```
*   Run the script:
    ```bash
    python run_analysis.py
    ```
*   The output image will be saved as a `.png` file in the project root.

### 3. Jupyter Notebook
For deep-dive data science and experimental analysis.
*   Launch Jupyter:
    ```bash
    jupyter notebook
    ```
*   Open `AWS_Corner_Analysis.ipynb` to step through the data loading and processing logic cell by cell.

## 📂 Project Structure

```
.
├── web/
│   ├── app.py              # Main Flask application
│   └── templates/          # HTML templates for the web interface
├── AWS_Corner_Analysis.ipynb # Jupyter notebook for interactive analysis
├── run_analysis.py         # CLI script for generating static analysis plots
├── requirements.txt        # Python dependency list
├── vercel.json             # Vercel deployment configuration
└── README.md               # Project documentation
```

## ⚠️ Notes
*   **First Run:** The first time you run an analysis for a specific race, `FastF1` will download the cache. This may take a few seconds or minutes depending on your internet connection. Subsequent runs will be much faster.
*   **Distance Units:** The analysis relies on track distance in **meters**. You may need to experiment with the `min` and `max` distance values to isolate specific corners for different tracks.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/F1-Corner-Analysis-Tool/issues).
