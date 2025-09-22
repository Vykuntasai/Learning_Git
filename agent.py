# import sys
# import subprocess
# import yaml

# def load_yaml(yaml_file):
#     """Load YAML and return as a Python dict."""
#     try:
#         with open(yaml_file, "r") as f:
#             workflow = yaml.safe_load(f)
#         if not workflow:
#             print(" Error: YAML file is empty.")
#             sys.exit(1)
#         return workflow
#     except Exception as e:
#         print(f" Failed to load YAML file '{yaml_file}': {e}")
#         sys.exit(1)

# def run_job(yaml_file, job_name):
#     """Run the specified job from the YAML file."""
#     workflow = load_yaml(yaml_file)

#     if "jobs" not in workflow:
#         print("Error: No 'jobs' section found in the YAML file.")
#         sys.exit(1)

#     jobs = workflow["jobs"]

#     if job_name not in jobs:
#         print(f"Error: Job '{job_name}' not found. Available jobs: {list(jobs.keys())}")
#         sys.exit(1)

#     job = jobs[job_name]

#     if "steps" not in job:
#         print(f"Error: Job '{job_name}' has no 'steps' section.")
#         sys.exit(1)

#     print(f"Running job: {job_name}")

#     for step in job["steps"]:
#         name = step.get("name", "Unnamed Step")
#         command = step.get("run")

#         if not command:
#             print(f"Skipping step '{name}' (no 'run' command found)")
#             continue

#         print(f"Step: {name}")
#         try:
#             result = subprocess.run(command, shell=True, check=True)
#             # print(result.stdout)
#             if result.stderr:
#                 print("Warnings/Errors:\n", result.stderr)
#         except subprocess.CalledProcessError as e:
#             print(f"Step '{name}' failed with error:\n{e.stderr}")
#             sys.exit(1)

# def main():
#     if len(sys.argv) != 3:
#         print("Usage: python agent.py <yaml_file> <job_name>")
#         sys.exit(1)

#     yaml_file = sys.argv[1]
#     job_name = sys.argv[2]

#     run_job(yaml_file, job_name)

# if __name__ == "__main__":
#     main()

import yaml

def get_input(prompt, default=None):
    """Helper function to allow default values when Enter is pressed"""
    val = input(f"{prompt} [{default}]: ") if default else input(f"{prompt}: ")
    return val.strip() if val else default

def get_pipeline_inputs():
    print("=== Azure DevOps YAML Pipeline Generator ===\n")

    # Pipeline basics
    pipeline_name = get_input("Enter pipeline name", "SamplePipeline")
    agent_pool = get_input("Enter agent pool name", "Default")
    trigger_branch = get_input("Enter trigger branch (e.g., main)", "main")
    
    # Default jobs for quick generation
    default_jobs = [
        {
            "job_name": "Build",
            "steps": [
                {"script": "echo 'Building the project...'"},
                {"script": "echo 'Bash build step simulated'"},
                {"script": "echo 'PowerShell build step simulated'"}
            ]
        },
        {
            "job_name": "Test",
            "steps": [
                {"script": "echo 'Running unit tests...'"},
                {"script": "echo 'Bash test step simulated'"},
                {"script": "echo 'PowerShell test step simulated'"}
            ]
        },
        {
            "job_name": "Deploy",
            "steps": [
                {"script": "echo 'Starting deployment...'"},
                {"script": "docker run hello-world"},
                {"script": "echo 'Deployment completed'"}
            ]
        }
    ]

    # Ask user for number of jobs (default to 3)
    jobs_count = int(get_input("Enter number of jobs", str(len(default_jobs))))

    jobs = []
    for i in range(jobs_count):
        if i < len(default_jobs):
            job_name = get_input(f"Enter job {i+1} name", default_jobs[i]["job_name"])
            steps_list = default_jobs[i]["steps"]
        else:
            job_name = get_input(f"Enter job {i+1} name", f"Job{i+1}")
            steps_count = int(get_input(f"Enter number of steps in job {i+1}", "1"))
            steps_list = []
            for j in range(steps_count):
                step_script = get_input(f"Enter script for step {j+1} in job {i+1}", f"echo 'Step {j+1}'")
                steps_list.append({"script": step_script})

        jobs.append({
            "job": job_name,
            "pool": {"name": agent_pool},
            "steps": steps_list
        })

    pipeline = {
        "name": pipeline_name,
        "trigger": {"branches": {"include": [trigger_branch]}},
        "jobs": jobs
    }

    return pipeline

def main():
    pipeline = get_pipeline_inputs()
    
    # Save generated YAML dynamically
    with open("generated_pipeline.yml", "w") as f:
        yaml.dump(pipeline, f, sort_keys=False)

    print("\nPipeline YAML dynamically generated: generated_pipeline.yml")

if __name__ == "__main__":
    main()


