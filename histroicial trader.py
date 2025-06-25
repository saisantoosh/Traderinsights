#!/usr/bin/env python
# coding: utf-8

# In[42]:


import pandas as pd

# Load the trader data
trader_df = pd.read_csv("historical_data.csv")
sentiment_df = pd.read_csv("fear_greed_index.csv")
print(trader_df)


# In[7]:


trader_df.info()


# In[23]:


trader_df.describe()


# In[9]:


trader_df.shape


# In[11]:


trader_df.size


# In[12]:


trader_df.columns


# In[14]:


trader_df.index


# In[17]:


df=trader_df


# In[20]:


df.loc[[0,100],['Timestamp']]


# In[33]:


trader_df.columns = [col.strip().replace(" ", "_") for col in trader_df.columns]


# In[34]:


trader_df['Timestamp'] = pd.to_datetime(trader_df['Timestamp'], unit='ms', errors='coerce')


# In[35]:


trader_df = trader_df.dropna(subset=['Timestamp'])


# In[36]:


numeric_cols = ['Execution_Price', 'Size_Tokens', 'Size_USD', 'Start_Position', 'Closed_PnL', 'Fee']
for col in numeric_cols:
    trader_df[col] = pd.to_numeric(trader_df[col], errors='coerce')


# In[37]:


trader_df = trader_df.dropna(subset=numeric_cols)


# In[38]:


q_low = trader_df["Execution_Price"].quantile(0.01)
q_high = trader_df["Execution_Price"].quantile(0.99)
trader_df = trader_df[(trader_df["Execution_Price"] >= q_low) & (trader_df["Execution_Price"] <= q_high)]


# In[39]:


trader_df = trader_df[(trader_df["Fee"] >= -10) & (trader_df["Fee"] <= 100)]


# In[40]:


#sentimenyt


# In[44]:


import pandas as pd

# Load the sentiment data
sentiment_df = pd.read_csv("Fear_Greed_Index.csv")

# See what it looks like
print(sentiment_df.head())


# In[45]:


# Convert UNIX timestamp to readable datetime
sentiment_df['timestamp'] = pd.to_datetime(sentiment_df['timestamp'], unit='s', errors='coerce')


# In[46]:


# Clean up classification column
sentiment_df['classification'] = sentiment_df['classification'].str.strip().str.title()


# In[47]:


# Filter out rows that are not exactly "Fear" or "Greed"
sentiment_df = sentiment_df[sentiment_df['classification'].isin(['Fear', 'Greed'])]


# In[48]:


# Extract only the date (no time) from the timestamp
sentiment_df['date'] = sentiment_df['timestamp'].dt.date


# In[49]:


sentiment_df


# In[51]:


# Merge on the 'date' column
merged_df = pd.merge(trader_df, sentiment_df[['date', 'classification']], on='date', how='left')


# In[52]:


# Convert Timestamp to datetime (if not already done)
trader_df['Timestamp'] = pd.to_datetime(trader_df['Timestamp'], unit='ms', errors='coerce')

# Extract just the date
trader_df['date'] = trader_df['Timestamp'].dt.date


# In[53]:


# Convert UNIX timestamp to datetime (if not already done)
sentiment_df['timestamp'] = pd.to_datetime(sentiment_df['timestamp'], unit='s', errors='coerce')

# Extract just the date
sentiment_df['date'] = sentiment_df['timestamp'].dt.date


# In[50]:


trader_df


# In[54]:


merged_df = pd.merge(
    trader_df,
    sentiment_df[['date', 'classification']],
    on='date',
    how='left'
)


# In[57]:


print(merged_df)


# #conversion of time stamp into new format
# df4['total_sqft']=df4['total_sqft'].apply(convert_sqftto_num)

# In[59]:


merged_df.describe()


# In[62]:


merged_df.info()


# In[61]:


merged_df = merged_df.dropna(subset=['classification'])


# In[65]:


avg_pnl = merged_df.groupby('classification')['Closed PnL'].mean()
print("🔹 Average Closed PnL by Sentiment:\n", avg_pnl)


# In[66]:


total_pnl = merged_df.groupby('classification')['Closed PnL'].sum()
print("🔹 Total Closed PnL by Sentiment:\n", total_pnl)


# In[67]:


avg_trade_size = merged_df.groupby('classification')['Size USD'].mean()
print("🔹 Average Trade Size (USD) by Sentiment:\n", avg_trade_size)


# In[68]:


side_pnl = merged_df.groupby(['classification', 'Side'])['Closed PnL'].mean()
print("🔹 Average PnL by Sentiment and Side:\n", side_pnl)


# In[69]:


import seaborn as sns
import matplotlib.pyplot as plt

# Make plot size bigger
plt.figure(figsize=(8, 5))

# Create boxplot
sns.boxplot(x='classification', y='Closed PnL', data=merged_df)
plt.title('Closed PnL Distribution: Fear vs Greed')
plt.xlabel('Market Sentiment')
plt.ylabel('Closed Profit & Loss')
plt.grid(True)
plt.show()


# 📊 Graphs Available for Download:
# Closed PnL Distribution by Sentiment
# 
# Average Trade Size by Sentiment
# 
# Average PnL by Sentiment and Side
# 
# ✅ Strategy Suggestion Based on Analysis:
# 🎯 Strategy Name: Sentiment-Aware Trade Tuning
# 💡 Key Observations:
# Greed Days:
# 
# Traders are more profitable on average ($87.89).
# 
# SELL trades perform exceptionally well (+$143.62).
# 
# Trade sizes are smaller, indicating cautious leverage or scalping behavior.
# 
# Fear Days:
# 
# Traders use larger trade sizes (~$5,260).
# 
# BUY trades perform better than SELL (+$58 vs +$42).
# 
# Total PnL is higher, possibly due to more trade activity.
# 
# 🧠 Strategy Breakdown:
# 1. 📈 On Greed Days:
# Focus on short (SELL) trades.
# 
# Use moderate leverage with tight stop-losses — capitalize on potential price reversals or overextensions.
# 
# Avoid high capital allocation; smaller trades work better.
# 
# 2. 📉 On Fear Days:
# Focus on long (BUY) positions.
# 
# Use larger positions if volatility and volume are high.
# 
# Look for rebound opportunities (buy the dip strategy).

# In[ ]:




