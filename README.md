# Proyek Analisis Data Dicoding

This project is a data analysis project that uses a Streamlit web application for visualization. The project contains a series of Python scripts and data files used to analyze and display insights interactively.

## Table of Contents

- [Installation](#installation)
- [Running the App](#running-the-app)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [License](#license)

## Installation

To run the Streamlit app locally, follow these steps:

### 1. Clone the repository

First, clone the repository to your local machine using the following command:

```bash
git clone https://github.com/rezaubaidillah/proyek-analisis-data-dicoding.git
```

Then navigate into the project directory:

```bash
cd proyek-analisis-data-dicoding
```

### 2. Create a Virtual Environment (optional)

It's a good practice to create a virtual environment to manage your dependencies. You can create and activate a virtual environment as follows:

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

Make sure the `requirements.txt` file contains the necessary packages to run Streamlit and other dependencies for the project. If the file is missing, you can install `streamlit` and other common libraries manually:

```bash
pip install streamlit pandas numpy matplotlib seaborn
```

## Running the App

To run the Streamlit app, execute the following command in the project directory:

```bash
streamlit run app.py
```

This will launch the Streamlit application in your default web browser. You will see the data analysis dashboard and interactive visualizations in the browser.

### Note:
Make sure the `app.py` file contains the Streamlit application logic. If the file is named differently, update the command with the correct filename.

## Project Structure

The typical structure of this project might look like:

```
├── LICENSE
├── README.md
├── dashboard
│   ├── day.csv
│   ├── hour.csv
│   └── streamlit_app.py
├── data
│   ├── Readme.txt
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
└── requirements.txt
```
## Dependencies

Ensure the following Python libraries are installed:

- `streamlit`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`

You can install these libraries by running:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
