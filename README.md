# Engagement-platform-webapp

## Setup

  It is recommended to setup this project using the [engagement-platform](https://github.com/digital-land/engagement-platform) core repo that contains all required repos as submodules

### Prerequisites
- [engagement-platform-cms](https://github.com/digital-land/engagement-platform-cms)

## Initialisation
- After cloning this repo, run the following command:
    ```
    make init
    ```

## Start Server
- To start the server run the following command:
    ```
    make server
    ```

## Adding new dependencies
- Project dependencies are managed via pip-tools
- to add a dependency, write it on a new line in ` /requirements/requirements.in ` or ` /requirements/dev-requirements.in `
- Then to compile your requirements file and produce a requirements.txt file run: 
    ```
    make piptool-compile
    ```
- Finally, to install the requirements from your requirements.txt file run:
    ```
    make dependencies
    ```


## Testing
Testing is done using `pytest` with `playwrite` also being used for the acceptance tests.
- To run unit tests run:
    ```
    make test-unit
    ```
- To run integration tests run:
    ```
    make test-integration
    ```
- To run acceptance tests run:
    ```
    make test-acceptance
    ```

## Linting
We use [flake8](https://flake8.pycqa.org/en/latest/) for linting, combined with [black](https://black.readthedocs.io/en/stable/) for automatic code formatting
- To run the linting checks and code formatter run:
    ```
    make lint
    ```