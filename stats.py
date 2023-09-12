# Retrives the all the information related to the github repositories

import json
import subprocess
# access the numfocus.jason file aand take the repository name and owner name
json_file_path = 'data/numfocus.jsonl'
repo_names = []

# Open the file and read it line by line
with open(json_file_path, 'r') as json_file:
    for line in json_file:
        # Load each JSON object separately
        data = json.loads(line)
        repo_names.append(dat
                          a['github_name'])

# Initialize a list to store the stdout for each command
stdout_list = []

# runing the 'python get_funders.py' command for each repo name
for repo_name in repo_names:
    # Constructing  the command
    command = ['python', 'get_funders.py', repo_name]
    
    # Run the command as a subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    
    stdout, stderr = process.communicate()
    
    # Checking for errors 
    if process.returncode != 0:
        print(f"Error running 'get_funders.py' for repo '{repo_name}':")
        print(stderr)
    else:
        print(f"Successfully ran 'get_funders.py' for repo '{repo_name}'")
        # Append stdout to the list
        print(stdout)
        stdout_list.append(stdout)


print("All commands have been executed.")


