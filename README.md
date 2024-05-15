# 🐜 Path finding in complex mazes 🐜

This project explores the Ant Colony Optimization algorithms, a nature-inspired approaches that mimic how ants find the shortest paths between their nest and food sources. We leverage this ingenious strategy to solve the challenging problem of finding paths out of randomly-generated complex mazes.

# How to contribute

1. Clone the repository
2. Download and install conda (necessary for virtual environments)
3. Create the environment from the YAML file `conda env create -f environment.yml`
4. Activate the environment before working on the project `conda activate complex-network`

# Coding guidelines

For coding guidelines refer to [Google's Python style guide](https://google.github.io/styleguide/pyguide.html) but always remember about the following before opening pull requests:

- Review your code for logic errors, typos, and adherence to Python
coding standards
- Execute all unit tests to ensure that the changes doesn't break
existing functionality
- Write new tests for any added features or modified code to maintain
comprehensive test coverage
- Use `pylint` to catch potential issues (`pylint <file_name>` or
`pylint --rcfile=<.pylintrc location> <file_name>` when run outside
of the main directory)
- Write docstrings for public modules, functions, classes and methods

When working with pull requests ensure to follow the project's branching rules:
- Never work directly on the main branch
    - Create a new branch for each feature or bug fix
    - Choose a descriptive branch name that reflects the purpose of your work
    e.g. `feature/add-visualization` or `bugfix/pheromone-calculation`
    - branch off from the latest main branch to ensure you're working with the
    most up-to-date code
- Open a pull request for every change you want to merge into `main`
    - Clearly explain the purpose of your changes
    - Include screenshots or examples if applicable
    - Request a review from at least one other team member
