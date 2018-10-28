# Part 3: extend search to hardcoded accounts
egrep -f ../../data/data_cleanup/hardcoded_companies.txt ../../data/usernames.csv | tee -a ../../data/data_cleanup/found_companies.csv
sort -u ../../data/data_cleanup/found_companies.csv > ../../data/data_cleanup/found_companies_nodup.csv # Remove duplicates
mv ../../data/data_cleanup/found_companies_nodup.csv ../../data/data_cleanup/found_companies.csv