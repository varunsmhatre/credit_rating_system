# Credit Rating System

## Overview
This project is a **Credit Rating System** that processes mortgage applications and assigns risk scores. It supports parallel processing for large datasets and includes **robust validation, risk computation, and logging**.

## Features
- Validates mortgage applications based on credit scores, loan amounts, and other financial factors.
- Computes **total risk score** based on mortgage data.
- Supports **parallel processing** for efficient large-scale data handling.
- Includes **comprehensive unit tests** and a **stress test** for handling 100,000+ mortgage records.

## Installation
### Prerequisites
- Python **3.8+**
- Virtual Environment (recommended)

### Steps
```sh
# Clone the repository
$ git clone https://github.com/varunsmhatre/credit_rating_system.git
$ cd credit_rating_system

# Create a virtual environment
$ python -m venv venv
$ source venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt
```

## Usage
To run the credit rating system:
```sh
$ python demo_run.py
```

## Running Tests
To run all unit tests:
```sh
$ python -m unittest discover tests
```

## Stress Testing
A built-in **stress test** ensures performance on large datasets:
```sh
$ python -m unittest tests.test_credit_rating.TestCreditRating.test_stress_large_data
```

## Debugging with VS Code
Use the **launch.json** to debug and run tests in **VS Code**.

## Key Design Decisions
1. **Parallel Processing**:
   - Utilizes `multiprocessing.Pool` to process large datasets efficiently.
   - Automatically determines optimal worker count using `WorkerManager.get_optimal_workers()`.
   - **Problem Solved**: Without parallel processing, large JSON files would take significantly longer to process due to the sequential execution of mortgage risk calculations. Using multiple workers speeds up processing by distributing the workload across CPU cores.

2. **Batch Reading of JSON File**:
   - Reads mortgage data in chunks instead of loading the entire file into memory.
   - Ensures efficient handling of **large datasets** without memory overflow.
   - **Problem Solved**: Loading a massive JSON file at once can cause memory errors and slow performance. By processing the file in batches, the system remains efficient and avoids unnecessary memory consumption.

3. **Logging & Debugging**:
   - Centralized logging in `credit_rating/utils.py`.
   - `logging.error` used for invalid data tracking.

4. **Test Coverage**:
   - **Unit Tests**: Validate individual functions.
   - **Stress Tests**: Ensure scalability with large datasets.