import subprocess
import os

def ping_website_from_env_variable():
    website = os.getenv('WEBSITE')
    if website:
        try:
            result = subprocess.run(['ping', '-c', '4', website], capture_output=True, text=True, timeout=10)
            print(result.stdout)
        except subprocess.TimeoutExpired:
            print(f"Timeout expired while pinging {website}")
        except subprocess.CalledProcessError as e:
            print(f"Error while pinging {website}: {e}")
    else:
        try:
            result = subprocess.run(['ping', '-c', '4', 'google.com'], capture_output=True, text=True, timeout=10)
            print(result.stdout)
        except subprocess.TimeoutExpired:
            print(f"Timeout expired while pinging {website}")
        except subprocess.CalledProcessError as e:
            print(f"Error while pinging {website}: {e}")
        print("Environment variable WEBSITE_TO_PING is not set.")

if __name__ == "__main__":
    while True:
        ping_website_from_env_variable()
