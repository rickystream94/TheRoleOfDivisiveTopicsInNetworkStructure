# Part 3: extend search to accounts that match the below patterns
egrep ".*porn.*,|.*movistar.*,|.*xboxsupport.*,|^vodafone.*,|.*airways,|.*playstation.*," ../../data/usernames.csv | tee -a ../../data/found_companies.csv
sort -u ../../data/found_companies.csv > ../../data/found_companies_nodup.csv # Remove duplicates
mv ../../data/found_companies_nodup.csv ../../data/found_companies.csv