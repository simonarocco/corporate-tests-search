from datetime import datetime
import os

import pandas as pd

from google_services_manager import GoogleServicesManager
from google_custom_search_manager import create_search_engine, run_search_across_companies


def main():
    # Read CSV file with list of companies from drive
    google = GoogleServicesManager()
    file_id = os.getenv('SEARCH_GROUP')
    file_name = google.download_file_from_drive(file_id)
    df = pd.read_csv('{}.csv'.format(file_name))
    print(df)
    exit()

    # Get custom search engine instance
    custom_search = create_search_engine()

    # Run search on all companies and get one df of all search results
    input_df = pd.read_csv('Dummy test.csv')
    companies = input_df['COMPANY_NAME'].tolist()
    results_df = run_search_across_companies(companies, custom_search)

    # Set date retrieved column to be current datetime
    date_retrieved = datetime.now()
    date_retrieved_day = date_retrieved.day
    date_retrieved_month = date_retrieved.month
    date_retrieved_year = date_retrieved.year
    results_df['DATE_RETRIVED'] = date_retrieved

    # Create csv name based on date
    csv_name = '{}-{}-{} corporate search results.csv'.format(date_retrieved_year,
                                                              date_retrieved_month,
                                                              date_retrieved_day)
    results_df.to_csv(csv_name, index=False)

    # Create google services manager obj to control uploading csvs to Google Drive
    google = GoogleServicesManager()
    google.upload_file_to_drive(csv_name)

    # Delete local csv file of results
    os.remove(csv_name)
    return


if __name__ == "__main__":
    main()
