# Part 4: extend search to hardcoded accounts
egrep -f hardcoded_companies.txt ../../data/usernames.csv | tee -a ../../data/found_companies.csv
sort -u ../../data/found_companies.csv > ../../data/found_companies_nodup.csv # Remove duplicates
mv ../../data/found_companies_nodup.csv ../../data/found_companies.csv