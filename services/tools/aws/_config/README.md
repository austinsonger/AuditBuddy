
# Modules


## AWSHandler Python Module

This Python module provides functionality to collect evidence from AWS environments by running specified AWS CLI commands and saving the output to a JSON file. The `AWSHandler` class handles the main logic of collecting and storing the evidence.

### Overview

The `AWSHandler` class is designed to:

1. Initialize with the environment name and configuration.
2. Collect evidence by running a specified AWS CLI command.
3. Save the output of the command in JSON format to a specified file.

### Dependencies

The module requires the following Python standard libraries:

- `os`
- `json`

### Class Description

#### AWSHandler

##### `__init__(self, env_name, config)`

The constructor initializes the `AWSHandler` object with the provided environment name and configuration.

- `env_name` (str): The name of the AWS environment.
- `config` (dict): Configuration details for the AWS environment.

##### `collect_evidence(self, command_runner, aws_command, output_file)`

This method runs the specified AWS CLI command and saves the output to a JSON file.

- `command_runner` (object): An object that has a `run_command` method to execute the AWS CLI command.
- `aws_command` (str): The AWS CLI command to be executed.
- `output_file` (str): The file path where the JSON output will be saved.

#### Method Workflow

1. **Initialize Output List:** An empty list `output` is initialized to store the JSON output.

2. Run AWS CLI Command:

    The specified 

   ```
   aws_command
   ```

    is executed using the 

   ```
   command_runner
   ```

    object's 

   ```
   run_command
   ```

    method.

   - The output of the command is expected to be in JSON format, with each line representing a JSON object.
   - Each line of the command output is parsed and added to the `output` list.

3. **Error Handling:** If there is an error while running the command, an error message is printed, and the method returns without saving the output.

4. **Ensure Output Directory Exists:** The method ensures that the directory for the `output_file` exists. If not, it creates the necessary directories.

5. **Write JSON Output to File:** The `output` list is written to the specified `output_file` in JSON format, with an indentation of 4 spaces for readability.

6. **Confirmation Message:** A confirmation message is printed indicating that the evidence has been saved.


## CommandRunner Python Module

This Python module provides a utility class `CommandRunner` to execute system commands using the `subprocess` library. The class is designed to run commands and capture their output, handling errors appropriately.

### Overview

The `CommandRunner` class is a simple utility to:

1. Run a specified system command.
2. Capture the standard output and standard error of the command.
3. Handle any errors that occur during command execution.

### Dependencies

The module requires the following Python standard library:

- `subprocess`

### Class Description

#### CommandRunner

#### `run_command(command)`

This static method runs the specified system command and returns the output as a list of lines.

- `command` (str): The system command to be executed.

#### Method Workflow

1. Run the Command:

    The 

   ```
   subprocess.run
   ```

    method is used to execute the given 

   ```
   command
   ```

   - The `stdout` (standard output) and `stderr` (standard error) are captured using `subprocess.PIPE`.
   - The `text=True` argument ensures that the output is captured as a string.

2. Check for Errors:

    The method checks the 

   ```
   returncode
   ```

    of the executed command.

   - If the `returncode` is not `0`, it indicates that the command failed.
   - In case of failure, an exception is raised with the error message from `stderr`.

3. **Return Output:** If the command succeeds, the method returns the output split into lines.

#### Exception Handling

- If the command execution fails (i.e., `returncode` is not `0`), an exception is raised with a detailed error message.


## EnvironmentConfig Python Module

This Python module provides functionality for setting up AWS credentials as environment variables. It includes a class `EnvironmentConfig` that initializes with AWS access key, secret key, and region, and a method to set these credentials as environment variables. Additionally, the module initializes configurations for different environments.

### Overview

The `EnvironmentConfig` class is designed to:

1. Initialize with AWS credentials and region.
2. Set AWS credentials as environment variables.

The module also provides:

- Current year and date in UTC format.
- Predefined environment configurations for "private-sector" and "federal" environments.

### Dependencies

The module requires the following Python standard libraries:

- `os`
- `datetime`

### Class Description

#### EnvironmentConfig

#### `__init__(self, access_key, secret_key, region)`

The constructor initializes the `EnvironmentConfig` object with the provided AWS credentials and region.

- `access_key` (str): AWS access key.
- `secret_key` (str): AWS secret key.
- `region` (str): AWS region.

#### `set_aws_credentials(self)`

This method sets the AWS credentials as environment variables.

- Sets `AWS_ACCESS_KEY_ID` to `self.access_key`.
- Sets `AWS_SECRET_ACCESS_KEY` to `self.secret_key`.
- Sets `AWS_DEFAULT_REGION` to `self.region`.

### Additional Variables

- `current_year` (str): The current year in UTC format (`%Y`).
- `current_date` (str): The current date in UTC format (`%Y-%m-%d`).

### Predefined Environments

The module defines configurations for two environments:

- `private-sector`
- `federal`

#### Environment Details

- **private-sector**
  - Access Key: Retrieved from `DEVOPS_CORP_AWS_ACCESS_KEY_ID` environment variable.
  - Secret Key: Retrieved from `DEVOPS_CORP_AWS_SECRET_ACCESS_KEY` environment variable.
  - Region: `us-east-1`
- **federal**
  - Access Key: Retrieved from `DEVOPS_FEDERAL_AWS_ACCESS_KEY_ID` environment variable.
  - Secret Key: Retrieved from `DEVOPS_FEDERAL_AWS_SECRET_ACCESS_KEY` environment variable.
  - Region: `us-east-1`


