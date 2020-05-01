# CS 170 Project Spring 2020

# By KruskalKrew - Angela Liu, Kevin Liu, and Jenny Wang

### Dependencies
python
networkx

### Running all solvers
```
python parallel_runner_v1.py our_inputs/<type of graph> our_outputs/<type of graph> <cache type>
```
type of graph - small, medium, large
cache type - none, some, all

For example, to run on medium-sized outputs without pulling past outputs from the cache:
```
python parallel_runner_v1.py our_inputs/medium our_outputs/medium none
```

### Gathering the submission data

```
python submission.py 

<at the prompt "Please enter a solver name.">
combined_solver
```
Be sure to remove all DS_Store files


### Project Start Info

Take a look at the project spec before you get started!

Requirements:

You'll only need to install networkx to work with the starter code. For installation instructions, follow: https://networkx.github.io/documentation/stable/install.html

Files:
- `parse.py`: functions to read/write inputs and outputs
- `solver.py`: where you should be writing your code to solve inputs
- `utils.py`: contains functions to compute cost and validate NetworkX graphs

When writing inputs/outputs:
- Make sure you use the functions `write_input_file` and `write_output_file` provided
- Run the functions `read_input_file` and `read_output_file` to validate your files before submitting!
  - These are the functions run by the autograder to validate submissions
