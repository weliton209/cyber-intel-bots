import subprocess

def check_alive(subdomains):

    try:
        process = subprocess.run(
            ["httpx", "-silent"],
            input="\n".join(subdomains),
            text=True,
            capture_output=True
        )

        alive = process.stdout.splitlines()

        return alive

    except:
        return []
