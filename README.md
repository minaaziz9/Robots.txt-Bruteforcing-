🔹 What Happens at Each Step?
1️⃣ Gets robots.txt from all live subdomains → Saves results in robots_results.txt.
2️⃣ Extracts Disallow paths and saves them in robots_disallowed.txt.
3️⃣ Uses ffuf to test directories inside robots.txt paths using a good SecLists wordlist.
4️⃣ Uses dirsearch to look for real files in restricted directories.

🚀 After this, check results for sensitive files or admin panels and move to exploitation!
