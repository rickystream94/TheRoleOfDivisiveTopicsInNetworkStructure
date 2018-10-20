# Part 2: extend search to accounts that match the below patterns
egrep ".*care,|.*support,|.*help," "$2" | tee -a ../data/found_companies.csv
sort -u ../data/found_companies.csv > ../data/found_companies_nodup.csv # Remove duplicates
rm ../data/found_companies.csv # Delete original file