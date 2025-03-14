# Exchange Rates Updater

An automated system to collect and maintain daily currency exchange rates against USD. The data is automatically updated daily and published to Kaggle.

## Overview

This project scrapes daily exchange rates for 56 major global currencies against USD from 2015 to present. The data is automatically updated daily using GitHub Actions and published to a Kaggle dataset.

## Features

- Daily exchange rate updates
- Automated data collection via GitHub Actions
- Historical data from 2015
- 56 major global currencies
- Direct Kaggle dataset integration
- Data quality checks and validation

## Data Source

- Source: X-Rates.com
- Base Currency: USD
- Update Frequency: Daily
- Historical Coverage: 2015-present
- Number of Currencies: 56

## Data Format

The exchange rates are stored in CSV format with the following structure:

```csv
date,EUR,GBP,JPY,...
2024-03-14,0.9134,0.7845,147.235,...
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/exchange-updater.git
cd exchange-updater
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure GitHub Secrets:
   - `KAGGLE_USERNAME`: Your Kaggle username
   - `KAGGLE_KEY`: Your Kaggle API key
   - `KAGGLE_DATASET`: Your dataset path (username/dataset-slug)

## Usage

### Manual Update

```bash
python daily-currency-update.py
```

### Automated Updates

The repository uses GitHub Actions to automatically:
- Update exchange rates daily
- Commit changes to the repository
- Upload updated data to Kaggle

## Project Structure

```
exchange-updater/
├── .github/
│   └── workflows/
│       └── update-exchange-rates.yml
├── daily-currency-update.py
├── requirements.txt
├── exchange-rates.csv
├── dataset-metadata.json
└── README.md
```

## Dependencies

- Python 3.10+
- pandas
- kaggle
- beautifulsoup4
- lxml

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the CC0-1.0 License - see the LICENSE file for details.

## Acknowledgments

- Data sourced from X-Rates.com
- Kaggle for dataset hosting
- GitHub Actions for automation
- Forked from [Repo](https://github.com/tasozgurcem11/exchange-updater) by [tasozgurc](https://github.com/tasozgurcem11)

## Dataset

The complete dataset is available on Kaggle:
[Daily Updated Exchange Rates (2015-now) (USD)](https://www.kaggle.com/datasets/mathoholic/daily-updated-exchange-rates-2015-now-usd)

## Contact

Name - [@mathoholic](https://github.com/mathoholic)
Project Link: [https://github.com/mathoholic/exchange-updater](https://github.com/mathoholic/exchange-updater)
