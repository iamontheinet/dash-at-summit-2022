### Step 1 -- Conda Environment
`pip install conda`
  * NOTE: The other option is to use [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

`conda create --name snowpark -c https://repo.anaconda.com/pkgs/snowflake python=3.8`

`conda activate snowpark`

### Step 2 -- Install Snowpark for Python
`pip install "snowflake-snowpark-python[pandas]"`

### Step 3 -- Install Other packages
`pip install ipykernel`

`pip install scikit-learn`

### Step 4 -- Create stages required for creating Snowpark Stored Proc, User-Defined Function, and uploading ML model

* `CREATE OR REPLACE STAGE dash_sprocs`
  * NOTE: If you use a different name, update code in the [Jupyter notebook](https://github.com/iamontheinet/dash-at-summit-2022/blob/main/SnowparkForPythonAndStreamlit/Snowpark_For_Python.ipynb)

* `CREATE OR REPLACE STAGE dash_models`
  * NOTE: If you use a different name, update code in the [Jupyter notebook](https://github.com/iamontheinet/dash-at-summit-2022/blob/main/SnowparkForPythonAndStreamlit/Snowpark_For_Python.ipynb)

* `CREATE OR REPLACE STAGE dash_udfs`
  * NOTE: If you use a different name, update code in the [Jupyter notebook](https://github.com/iamontheinet/dash-at-summit-2022/blob/main/SnowparkForPythonAndStreamlit/Snowpark_For_Python.ipynb)

### Step 5 -- Create table BUDGET_ALLOCATIONS_AND_ROI that holds the last six months of budget allocations and ROI.

```sql
CREATE or REPLACE TABLE BUDGET_ALLOCATIONS_AND_ROI (
  MONTH varchar(30),
  SEARCHENGINE integer,
  SOCIALMEDIA integer,
  VIDEO integer,
  EMAIL integer,
  ROI float
);

INSERT INTO BUDGET_ALLOCATIONS_AND_ROI (MONTH, SEARCHENGINE, SOCIALMEDIA, VIDEO, EMAIL, ROI)
VALUES
('January',35,50,35,85,8.22),
('February',75,50,35,85,13.90),
('March',15,50,35,15,7.34),
('April',25,80,40,90,13.23),
('May',95,95,10,95,6.246),
('June',35,50,35,85,8.22);
```

## Usage

### Step 1 -- Run through the [Jupyter notebook](https://github.com/iamontheinet/dash-at-summit-2022/blob/main/SnowparkForPythonAndStreamlit/Snowpark_For_Python.ipynb)

NOTE: You will need to create a couple of tables using `campaign_spend.csv` and `monthly_revenue.csv` files. The other option is to load data from the files instead of from tables.

The notebook... 

* Performs Exploratory Data Analysis (EDA)
* Creates features for training a model and writes them to a Snowflake table
* Creates a Stored Proc for training a ML model and uploading it to a stage
* Calls the Stored Proc to train the model
* Creates a User-Defined Function (UDF) that uses the model for inference on new data points passed in as parameters
  * NOTE: This UDF is called from the Streamlit app

### Step 2 -- Run Streamlit app

In a terminal window, run the [Streamlit app](https://github.com/iamontheinet/dash-at-summit-2022/blob/main/SnowparkForPythonAndStreamlit/Snowpark_Streamlit_Revenue_Prediction.py) by executing `streamlit run Snowpark_Streamlit_Revenue_Prediction.py` 

If all goes well, you should the following app in your browser window.

https://user-images.githubusercontent.com/1723932/175127637-9149b9f3-e12a-4acd-a271-4650c47d8e34.mp4

