
Follow these steps exactly to run the experiment on any machine:

Create a Virtual Environment
>> python -m venv venv

Activate it:
>> venv\Scripts\Activate.ps1

Install Requirements
pip install -r requirements.txt

Set the Python Path
This ensures experiment.py can access the src directory.

>> $env:PYTHONPATH = "$PWD\src"

Run the Experiment
From the project root, run:

>> python experiment.py

Configuration Options
Change which problems are tested

Open experiment.py, scroll to the bottom:

if __name__ == "__main__":
    problem_ids = [
        "reverse_pairs"
    ]

Replace or append IDs based on those in PROBLEM_MAP:

edit_distance
maximal_rectangle
reverse_pairs
median_two_arrays
search_rotated
decode_ways

You may add new problems by placing the file in src/problems/ and adding an entry to PROBLEM_MAP.

Change GA population size or generations

In run_comparison():
ga_params = {"population_size": 50, "generations": 5}

Change number of random baseline tests
random_params = {"n_inputs": 250}

Change number of trials
Bottom of experiment.py:
run_comparison(pid, trials=5)


Results are saved as CSV files in:

results/<problem_id>_comparison.csv

Each file includes:

Random search coverage + failures
GA search coverage + failures
Number of tests run
Per-trial data