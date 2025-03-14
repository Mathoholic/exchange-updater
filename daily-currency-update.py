import os
import datetime
import pandas as pd
import time
from tqdm import tqdm

currency_mappings = {
    'Argentine Peso': 'ARS', 'Australian Dollar': 'AUD', 'Bahraini Dinar': 'BHD',
    'Botswana Pula': 'BWP', 'Brazilian Real': 'BRL', 'British Pound': 'GBP',
    'Bruneian Dollar': 'BND', 'Bulgarian Lev': 'BGN', 'Canadian Dollar': 'CAD',
    'Chilean Peso': 'CLP', 'Chinese Yuan Renminbi': 'CNY', 'Colombian Peso': 'COP',
    'Czech Koruna': 'CZK', 'Croatian Kuna': 'HRK', 'Danish Krone': 'DKK',
    'Emirati Dirham': 'AED', 'Hong Kong Dollar': 'HKD', 'Hungarian Forint': 'HUF',
    'Icelandic Krona': 'ISK', 'Indian Rupee': 'INR', 'Indonesian Rupiah': 'IDR',
    'Iranian Rial': 'IRR', 'Israeli Shekel': 'ILS', 'Japanese Yen': 'JPY',
    'Kazakhstani Tenge': 'KZT', 'Kuwaiti Dinar': 'KWD', 'Libyan Dinar': 'LYD',
    'Malaysian Ringgit': 'MYR', 'Mauritian Rupee': 'MUR', 'Mexican Peso': 'MXN',
    'Nepalese Rupee': 'NPR', 'New Zealand Dollar': 'NZD', 'Norwegian Krone': 'NOK',
    'Omani Rial': 'OMR', 'Pakistani Rupee': 'PKR', 'Philippine Peso': 'PHP',
    'Polish Zloty': 'PLN', 'Qatari Riyal': 'QAR', 'Romanian New Leu': 'RON',
    'Russian Ruble': 'RUB', 'Saudi Arabian Riyal': 'SAR', 'Singapore Dollar': 'SGD',
    'South African Rand': 'ZAR', 'South Korean Won': 'KRW', 'Sri Lankan Rupee': 'LKR',
    'Swedish Krona': 'SEK', 'Swiss Franc': 'CHF', 'Taiwan New Dollar': 'TWD',
    'Thai Baht': 'THB', 'Trinidadian Dollar': 'TTD', 'Turkish Lira': 'TRY',
    'US Dollar': 'USD', 'Venezuelan Bolivar': 'VES'
}

DATA_FILE = "exchange-rates.csv"

def get_last_date():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        last_date = pd.to_datetime(df['date']).max()
        return last_date
    return None

def download_exchange_rates(start_date, end_date):
    """Download exchange rates for a date range"""
    dates = pd.date_range(start_date, end_date, freq='D')
    
    all_data = []
    for date in tqdm(dates, desc="Downloading exchange rates"):
        try:
            base_currency = 'USD'
            date_ = date.strftime('%Y-%m-%d')

            url = f"https://www.x-rates.com/historical/?from={base_currency}&amount=1&date={date_}"
            df = pd.read_html(url)[1]
            df = df.rename(columns={'US Dollar': 'currency_raw', '1.00 USD': 'rates'})
            df['currency'] = df['currency_raw'].map(currency_mappings)
            df = df[['currency', 'rates']]
            df = df.dropna().set_index('currency').T.reset_index(drop=True)
            df['date'] = date_
            all_data.append(df)

            time.sleep(1)  # To avoid being blocked

        except Exception as e:
            print(f"Error getting data for {date_}: {str(e)}")
            continue
    
    if all_data:
        new_data = pd.concat(all_data, ignore_index=True)
        new_data.rename({"Unnamed: 14":"Euro"},axis=1,inplace=True)
        return new_data
    return None

def update_data():
    last_date = get_last_date()
    if last_date is not None:
        start_date = last_date + pd.Timedelta(days=1)
    else:
        start_date = datetime.datetime(2015, 1, 1)

    end_date = datetime.datetime.today()
    if start_date <= end_date:
        new_data = download_exchange_rates(start_date, end_date)
        if new_data is not None:
            if os.path.exists(DATA_FILE):
                existing_data = pd.read_csv(DATA_FILE)
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            else:
                updated_data = new_data

            updated_data.to_csv(DATA_FILE, index=False)
            print(f"✅ Updated data till {end_date.date()}")

if __name__ == "__main__":
    update_data()
