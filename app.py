import requests
import subprocess

# Load the list of subdomains from httpx_200.txt and httpx_301_302.txt
input_files = ["httpx_200.txt", "httpx_301_302.txt"]
subdomains = []

for file in input_files:
    try:
        with open(file, "r") as f:
            subdomains.extend([line.strip() for line in f.readlines()])
    except FileNotFoundError:
        print(f"[!] File not found: {file}")

# Fetch robots.txt for each subdomain
robots_disallowed = []
print("[*] Fetching robots.txt...")

for subdomain in subdomains:
    url = f"https://{subdomain}/robots.txt"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            for line in response.text.split("\n"):
                if "Disallow:" in line:
                    path = line.split(":")[1].strip()
                    if path and path != "/":
                        robots_disallowed.append((subdomain, path))
                        print(f"[+] Found Disallow: {subdomain}{path}")
    except requests.exceptions.RequestException:
        print(f"[-] Failed to fetch: {url}")

# Save disallowed directories
with open("robots_disallowed.txt", "w") as f:
    for subdomain, path in robots_disallowed:
        f.write(f"{subdomain} {path}\n")

# Run ffuf inside disallowed directories
print("[*] Running ffuf to brute-force inside disallowed directories...")
for subdomain, path in robots_disallowed:
    cmd = f"ffuf -u https://{subdomain}{path}/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302"
    subprocess.run(cmd, shell=True)

# Run dirsearch inside disallowed directories
print("[*] Running dirsearch to find files inside restricted directories...")
for subdomain, path in robots_disallowed:
    cmd = f"dirsearch -u https://{subdomain}{path} -w /usr/share/seclists/Discovery/Web-Content/common.txt -e php,html,txt,json,log,zip,bak,conf"
    subprocess.run(cmd, shell=True)

print("[*] Done!")
