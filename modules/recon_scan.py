import subprocess

def run_scan(targets):

    try:
        process = subprocess.run(
            [
                "nuclei",
                "-severity", "critical,high",
                "-silent"
            ],
            input="\n".join(targets),
            text=True,
            capture_output=True
        )

        return process.stdout.splitlines()

    except:
        return []
