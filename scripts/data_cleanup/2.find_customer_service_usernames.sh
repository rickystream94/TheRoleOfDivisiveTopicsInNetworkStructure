# Part 2: extend search to accounts that match the patterns secified in the customer_service_patterns.txt
egrep -f ../../data/data_cleanup/customer_service_patterns.txt ../../data/usernames.csv | tee -a ../../data/data_cleanup/found_companies.csv
sort -u ../../data/data_cleanup/found_companies.csv > ../../data/data_cleanup/found_companies_nodup.csv # Remove duplicates
mv ../../data/data_cleanup/found_companies_nodup.csv ../../data/data_cleanup/found_companies.csv