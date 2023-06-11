import datetime
import json
import os
import time
import logging

import boto3
import pandas as pd


currency_mappings = {
    'Argentine Peso': 'ARS',
    'Australian Dollar': 'AUD',
    'Bahraini Dinar': 'BHD',
    'Botswana Pula': 'BWP',
    'Brazilian Real': 'BRL',
    'British Pound': 'GBP',
    'Bruneian Dollar': 'BND',
    'Bulgarian Lev': 'BGN',
    'Canadian Dollar': 'CAD',
    'Chilean Peso': 'CLP',
    'Chinese Yuan Renminbi': 'CNY',
    'Colombian Peso': 'COP',
    'Czech Koruna': 'CZK',
    'Croatian Kuna': 'HRK',
    'Danish Krone': 'DKK',
    'Emirati Dirham': 'AED',
    'Hong Kong Dollar': 'HKD',
    'Hungarian Forint': 'HUF',
    'Icelandic Krona': 'ISK',
    'Indian Rupee': 'INR',
    'Indonesian Rupiah': 'IDR',
    'Iranian Rial': 'IRR',
    'Israeli Shekel': 'ILS',
    'Japanese Yen': 'JPY',
    'Kazakhstani Tenge': 'KZT',
    'Kuwaiti Dinar': 'KWD',
    'Libyan Dinar': 'LYD',
    'Malaysian Ringgit': 'MYR',
    'Mauritian Rupee': 'MUR',
    'Mexican Peso': 'MXN',
    'Nepalese Rupee': 'NPR',
    'New Zealand Dollar': 'NZD',
    'Norwegian Krone': 'NOK',
    'Omani Rial': 'OMR',
    'Pakistani Rupee': 'PKR',
    'Philippine Peso': 'PHP',
    'Polish Zloty': 'PLN',
    'Qatari Riyal': 'QAR',
    'Romanian New Leu': 'RON',
    'Russian Ruble': 'RUB',
    'Saudi Arabian Riyal': 'SAR',
    'Singapore Dollar': 'SGD',
    'South African Rand': 'ZAR',
    'South Korean Won': 'KRW',
    'Sri Lankan Rupee': 'LKR',
    'Swedish Krona': 'SEK',
    'Swiss Franc': 'CHF',
    'Taiwan New Dollar': 'TWD',
    'Thai Baht': 'THB',
    'Trinidadian Dollar': 'TTD',
    'Turkish Lira': 'TRY',
    'US Dollar': 'USD',
    'Venezuelan Bolivar': 'VES'
}


def lambda_handler(event, context):
    """
    Process lambda event
    :param event: aws lambda event
    :param context: aws lambda context
    :return:
    """

    s3_client = boto3.client('s3')

    S3_URI = os.getenv('S3_URI') # s3://{bucket}/../exchanges.csv
    bucket_name = S3_URI.split('s3://')[1].split('/')[0]
    key = S3_URI.split('s3://')[1].split('/', 1)[1]

    lambda_exchange_path = '/tmp/exchanges.csv'

    # Download the file from S3
    s3_client.download_file(bucket_name, key, lambda_exchange_path)

    # Read the file
    exchanges = pd.read_csv(lambda_exchange_path)


    # Get the latest date and convert it to datetime
    latest_date = exchanges['date'].max()

    # Convert to datetime
    latest_date = datetime.datetime.strptime(latest_date, '%Y-%m-%d')


    # Find days if any that are missing
    today = datetime.datetime.now()
    missing_days = [date for date in pd.date_range(latest_date, today) if date not in exchanges['date'].values]


    # Crawl for missing days
    if not missing_days:
        print(f"Missing days: {missing_days}")
        return None

    for missing_day in missing_days:
        base_currency = 'EUR'
        date_ = missing_day.strftime('%Y-%m-%d')
        print(f"Getting exchange rates for {date_}")

        url = f"https://www.x-rates.com/historical/?from={base_currency}&amount=1&date={date_}"
        df = pd.read_html(url)[1]
        df = df.rename(columns={'Euro': 'currency_raw', '1.00 EUR': 'rates'})
        df['currency'] = df['currency_raw'].apply(lambda x: currency_mappings.get(x))
        df = df[['currency', 'rates']]
        df = df.set_index('currency')

        if df.empty:
            print(f"Empty dataframe for {date_}")
            continue

        # change currency, rates to -> date, ARS, ...
        df = df.T
        df = df.reset_index()
        df.drop(columns=['index'], inplace=True)
        df['date'] = missing_day.strftime('%Y-%m-%d')


        # Append to existing dataframe
        exchanges = pd.concat([exchanges, df], ignore_index=True)

    # Order by date
    exchanges = exchanges.sort_values(by=['date'], ascending=False)

    # Upload to S3
    exchanges.to_csv(lambda_exchange_path, index=False)
    s3_client.upload_file(lambda_exchange_path, bucket_name, key)

    return {"message": "success"}
