import matplotlib.pyplot as plt
import pandas as pd
import os

df = pd.read_csv('portfolios/portfolio_metrics.csv')

if not os.path.exists("analysis_plots"):
    os.mkdir("analysis_plots")

plt.figure(figsize=(16, 8))

# Return line chart
plt.title('Returns')
plt.axhline(y=0, color='r', linestyle='-')
plt.plot(df.index, df.RETURN)
plt.ylabel("Return")
plt.xlabel("Portfolios")
plt.savefig('analysis_plots/return_line-chart.png', pad_inches=0, transparent=True)
plt.close()

# Positive vs Negative Return plot
positive_return = df['RETURN'].where(df.RETURN >= 0).count()
negative_return = df['RETURN'].where(df.RETURN < 0).count()
plt.title('Returns')
plt.rcParams.update({'font.size': 18})
plt.pie([positive_return, negative_return], labels=['Positive', 'Negative'], autopct='%1.1f%%')
plt.savefig('analysis_plots/return_pie.png', pad_inches=0, transparent=True)
plt.close()

# Return plot
plt.ylabel("Portfolio Mix")
plt.xlabel("Return")
plt.title('Return on different Portfolios')
sorted_df = df.sort_values(by='RETURN', ascending=True)
plt.plot([], [], color='blue', label='Stocks')
plt.plot([], [], color='red', label='Corporate Bonds')
plt.plot([], [], color='purple', label='Public Bonds')
plt.plot([], [], color='orange', label='Gold')
plt.plot([], [], color='green', label='Cash')

plt.stackplot(sorted_df.RETURN, sorted_df.ST, sorted_df.CB, sorted_df.PB, sorted_df.GO, sorted_df.CA,
              colors=['blue', 'red', 'purple', 'orange', 'green'])
plt.legend(loc=(1.04, 0.5))
plt.savefig('analysis_plots/return_on_portfolios.png', pad_inches=0, transparent=True, bbox_inches="tight")
plt.close()


# Return vs Risk plot
plt.title("Return vs Risk")
plt.ylabel("Return")
plt.xlabel("Volatility")
plt.scatter(df.VOLAT, df.RETURN)
plt.savefig('analysis_plots/return_vs_risk.png', pad_inches=0, transparent=True)
plt.close()
