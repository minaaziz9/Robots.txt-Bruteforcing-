# 1️⃣ Get robots.txt from live subdomains
for url in $(cat httpx_200.txt httpx_301_302.txt); do 
    curl -s -L "$url/robots.txt" | tee -a robots_results.txt
done

# 2️⃣ Extract Disallow paths from robots.txt
cat robots_results.txt | grep "Disallow" | awk '{print $2}' | sed 's/^/\//' > robots_disallowed.txt

# 3️⃣ Brute-force directories found in robots.txt using ffuf
for dir in $(cat robots_disallowed.txt); do 
    ffuf -u https://target.com$dir/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302
done

# 4️⃣ Use dirsearch to find files inside restricted directories
for dir in $(cat robots_disallowed.txt); do 
    dirsearch -u https://target.com$dir -w /usr/share/seclists/Discovery/Web-Content/common.txt -e php,html,txt,json,log,zip,bak,conf
done
