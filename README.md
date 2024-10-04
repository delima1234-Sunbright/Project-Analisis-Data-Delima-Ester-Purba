# Air-Quality Dashboard

This project is a **Streamlit-based air-quality dashboard** that visualizes pollutant data PM2.5 and provides AQI forecasts for a given date range.

## Setup Environment

### Prerequisites

1. **Python**: Ensure Python is installed on your machine. You can download it from the official [Python website](https://www.python.org/downloads/).
2. **VSCode**: Install Visual Studio Code for coding and development. Download it [here](https://code.visualstudio.com/).
3. **Streamlit**: Install Streamlit via pip:

    ```bash
    pip install streamlit
    ```

4. **Other Dependencies**: Install additional libraries required for the project by running:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Dashboard

To run the air-quality dashboard, follow these steps:

1. In VSCode, open the terminal and activate your Python virtual environment (recommended but optional):

    ```bash
    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

2. Change the directory to the `dashboard` folder:

    ```bash
    cd dashboard
    ```

3. Run the Streamlit app using the following command:

    ```bash
    streamlit run AQIDashboard.py
    ```

4. Open your browser and navigate to:

    ```
    http://localhost:8501
    ```

   The dashboard will be available locally at this address.

### Features

- Select a **date range** and **station** to view the average pollutant data.
- Visualize pollutant concentration charts with the title *"Pollutant and Concentration."*
- Get AQI category forecasts along with **temperature** and **pressure** data.
