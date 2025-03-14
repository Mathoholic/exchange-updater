import datetime
import pandas as pd
import time
from tqdm import tqdm
import logging

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

def download_exchange_rates(year):
    """Download exchange rates for a specific year"""
    start_date = datetime.datetime(year, 1, 1)
    end_date = datetime.datetime(year, 3, 14)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    year_dfs = []
    for date in tqdm(dates, desc=f"Downloading {year}"):
        try:
            base_currency = 'USD'
            date_ = date.strftime('%Y-%m-%d')
            
            url = f"https://www.x-rates.com/historical/?from={base_currency}&amount=1&date={date_}"
            df = pd.read_html(url)[1]
            df = df.rename(columns={'US Dollar': 'currency_raw', '1.00 USD': 'rates'})
            df['currency'] = df['currency_raw'].apply(lambda x: currency_mappings.get(x))
            df = df[['currency', 'rates']]
            df = df.set_index('currency')

            if not df.empty:
                df = df.T
                df = df.reset_index()
                df.drop(columns=['index'], inplace=True)
                df['date'] = date_
                year_dfs.append(df)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error getting data for {date_}: {str(e)}")
            continue
            
    if year_dfs:
        year_df = pd.concat(year_dfs, ignore_index=True)
        year_df.to_csv(f"exchange_rates_{year}.csv", index=False)
        print(f"Saved data for {year}")
        return year_df
    return None

# Download data year by year
all_dfs = []
for year in range(2025, datetime.datetime.now().year + 1):
    print(f"\nProcessing year {year}")
    year_df = download_exchange_rates(year)
    if year_df is not None:
        all_dfs.append(year_df)

# Combine all years
if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.to_csv("exchange_rates_all.csv", index=False)
    print("\nCompleted downloading all exchange rates")