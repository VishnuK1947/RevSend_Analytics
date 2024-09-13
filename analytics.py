import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class RevSendAnalysis:
    def __init__(self):
        self.data = None
    
    def load_data(self, file_path):
        """Load customer data from a CSV file."""
        self.data = pd.read_csv(file_path)
        print(f"Loaded data with {len(self.data)} rows and {len(self.data.columns)} columns.")
        print("Columns in the dataset:", self.data.columns.tolist())
    
    def analyze_company_spending(self):
        """Analyze spending patterns by company type."""
        industry_spending = self.data.groupby('industry')['total_spend'].agg(['mean', 'sum']).sort_values('sum', ascending=False)
        print("Industry Spending Analysis:")
        print(industry_spending)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=industry_spending.index, y=industry_spending['sum'])
        plt.title('Total Spending by Industry')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Total Spend')
        plt.tight_layout()
        plt.show()

        # Additional analysis: Average spend by company size
        size_spending = self.data.groupby('company_size')['total_spend'].mean().sort_values(ascending=False)
        plt.figure(figsize=(10, 5))
        sns.barplot(x=size_spending.index, y=size_spending.values)
        plt.title('Average Spending by Company Size')
        plt.ylabel('Average Spend')
        plt.tight_layout()
        plt.show()
    
    def analyze_gift_preferences(self):
        """Analyze gift preferences overall and by industry."""
        gift_preferences = self.data['preferred_gift_type'].str.get_dummies(sep=', ').sum().sort_values(ascending=False)
        print("Overall Gift Preferences:")
        print(gift_preferences)

        plt.figure(figsize=(10, 5))
        gift_preferences.plot(kind='bar')
        plt.title('Overall Gift Type Preferences')
        plt.ylabel('Number of Preferences')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # Gift preferences by top 3 industries
        top_industries = self.data['industry'].value_counts().nlargest(3).index
        for industry in top_industries:
            industry_prefs = self.data[self.data['industry'] == industry]['preferred_gift_type'].str.get_dummies(sep=', ').sum().sort_values(ascending=False)
            print(f"\nGift preferences for {industry}:")
            print(industry_prefs)
    
    def analyze_customer_satisfaction(self):
        """Analyze factors influencing customer satisfaction."""
        correlation_matrix = self.data[['customer_satisfaction', 'total_spend', 'gift_frequency', 'average_gift_value']].corr()
        print("Correlation with customer satisfaction:")
        print(correlation_matrix['customer_satisfaction'].sort_values(ascending=False))
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
        plt.title('Correlation Heatmap: Factors Influencing Customer Satisfaction')
        plt.tight_layout()
        plt.show()

        # Satisfaction distribution
        plt.figure(figsize=(10, 5))
        sns.histplot(data=self.data, x='customer_satisfaction', kde=True)
        plt.title('Distribution of Customer Satisfaction Scores')
        plt.xlabel('Satisfaction Score')
        plt.tight_layout()
        plt.show()
    
    def identify_growth_opportunities(self):
        "HYBRID"
        """Identify potential growth opportunities."""
        # Identify underrepresented industries with high average spend
        industry_metrics = self.data.groupby('industry').agg({
            'customer_id': 'count',
            'total_spend': 'mean',
            'customer_satisfaction': 'mean'
        }).sort_values('total_spend', ascending=False)
        
        print("Industry Metrics:")
        print(industry_metrics)
        
        # Identify industries with low representation but high average spend
        median_customers = industry_metrics['customer_id'].median()
        median_spend = industry_metrics['total_spend'].median()
        growth_targets = industry_metrics[
            (industry_metrics['customer_id'] < median_customers) &
            (industry_metrics['total_spend'] > median_spend)
        ]
        
        print("\nTop Growth Target Industries:")
        print(growth_targets)

        # Visualize growth opportunities
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=industry_metrics.reset_index(), x='customer_id', y='total_spend', size='customer_satisfaction', hue='industry', sizes=(50, 500))
        plt.axvline(x=median_customers, color='r', linestyle='--', label='Median Customers')
        plt.axhline(y=median_spend, color='r', linestyle='--', label='Median Spend')
        plt.title('Industry Growth Opportunities')
        plt.xlabel('Number of Customers')
        plt.ylabel('Average Total Spend')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

# Usage example
analyzer = RevSendAnalysis()
analyzer.load_data('revsend_synthetic_data.csv')
analyzer.analyze_company_spending()
analyzer.analyze_gift_preferences()
analyzer.analyze_customer_satisfaction()
analyzer.identify_growth_opportunities()