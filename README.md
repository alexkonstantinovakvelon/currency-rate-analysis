# currency-rate-analysis

# Scripts
1. init_database.py - creates clean database in redshift
2. fetch_new_currencies_data.py - fetches currency rates data and stores in intermediate S3 repository
3. currencies_data.py - persists data in red shift database
4. print_stored_data.py - prints data stored in red shift
5. restore_currencies_data.py - allows to restore currency rate data from specified time for specified currency