import pandas as pd
import numpy as np
import random

def generate_synthetic_data(num_records=1000):
    # Define possible values for categorical variables
    industries = ['Tech', 'Finance', 'Healthcare', 'Manufacturing', 'Retail', 'Education', 'Insurance', 'Real Estate', 'Energy', 'Hospitality']
    company_sizes = ['Small', 'Medium', 'Large', 'Enterprise']
    gift_types = ['Gift Cards', 'Physical Gifts', 'Experiences', 'Custom Gifts']

    # Generate synthetic data
    data = {
        'customer_id': range(1, num_records + 1),
        'industry': np.random.choice(industries, num_records),
        'company_size': np.random.choice(company_sizes, num_records),
        'total_spend': np.random.lognormal(mean=10, sigma=1, size=num_records),  # More realistic spending distribution
        'gift_frequency': np.random.randint(1, 52, num_records),  # Assuming weekly frequency at most
        'average_gift_value': np.random.lognormal(mean=4, sigma=0.5, size=num_records),  # More realistic gift value distribution
        'customer_satisfaction': np.random.normal(loc=4, scale=0.5, size=num_records).clip(1, 5)  # Normal distribution centered around 4
    }

    # Generate preferred gift types
    preferred_gift_types = []
    for _ in range(num_records):
        num_preferences = random.randint(1, 3)  # Each company might have 1-3 preferred gift types
        preferences = random.sample(gift_types, num_preferences)
        preferred_gift_types.append(', '.join(preferences))
    
    data['preferred_gift_type'] = preferred_gift_types

    # Create DataFrame
    df = pd.DataFrame(data)

    # Add some correlations and patterns
    df.loc[df['company_size'] == 'Enterprise', 'total_spend'] *= 1.5
    df.loc[df['industry'] == 'Tech', 'average_gift_value'] *= 1.2
    df.loc[df['gift_frequency'] > 26, 'customer_satisfaction'] += 0.5
    df['customer_satisfaction'] = df['customer_satisfaction'].clip(1, 5)

    # Round numerical values for better readability
    df['total_spend'] = df['total_spend'].round(2)
    df['average_gift_value'] = df['average_gift_value'].round(2)
    df['customer_satisfaction'] = df['customer_satisfaction'].round(2)

    # Save to CSV
    df.to_csv('revsend_synthetic_data.csv', index=False)
    print(f"Generated {num_records} records of synthetic data and saved to 'revsend_synthetic_data.csv'")

    # Display first few rows and data info
    print(df.head())
    print(df.info())

# Generate the synthetic data
generate_synthetic_data(1000)