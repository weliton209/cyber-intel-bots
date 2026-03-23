import subprocess

def run_scan(targets):

    try:
        process = subprocess.run(
            ["nuclei", "-severity", "critical,high,medium", "-silent"],
            input="\n".join(targets),
            text=True,
            capture_output=True
        )

        findings = process.stdout.splitlines()

        return findings

    except:
        return []
