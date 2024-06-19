import os
import json

class AWSHandler:
    def __init__(self, env_name, config):
        self.env_name = env_name
        self.config = config

    def collect_evidence(self, command_runner, aws_command, output_file):
        # Initialize an empty list to store JSON output
        output = []

        # Run the command and capture the output
        try:
            command_output = command_runner.run_command(aws_command)
            for line in command_output:
                output.append(json.loads(line))
        except Exception as e:
            print(f"Error running command for {self.env_name}: {e}")
            return

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Write the JSON output to the specified file path
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=4)

        print(f"Evidence for {self.env_name} environment saved to {output_file}")
