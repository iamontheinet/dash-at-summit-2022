## Setup

### Step 1 -- Conda Environment
`pip install conda`
  * NOTE: The other option is to use [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

`conda create --name snowpark -c https://repo.anaconda.com/pkgs/snowflake python=3.8`

`conda activate snowpark`

### Step 2 -- Install Snowpark for Python
`pip install "snowflake-snowpark-python[pandas]"`

### Step 3 -- Install Other packages
`pip install ipykernel`

`pip install cachetools`

`pip install scikit-learn`

## Usage

### Step 1 -- Update [connection.json](https://github.com/iamontheinet/dash-at-summit-2022/blob/main/SnowparkForPythonIn20/connection.json) with your Snowflake account details

### Step 2 -- Run through the [Jupyter notebook](https://github.com/iamontheinet/dash-at-summit-2022/blob/main/SnowparkForPythonIn20/Snowpark_For_Python.ipynb)
