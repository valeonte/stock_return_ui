# Stock Return UI

Run instructions:
1) Make sure you are in the project's folder
2) Create a virtual environment with the provided `requirements.txt`
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3) Make sure `.venv` environment is activated, then run `python -m flask run`
4) You should be able to visit `http://localhost:5000` to see the app running.

## Documentation

The app displays the performance of 10 US stocks and a portfolio of those stocks over a period. The price data were pulled from [Yahoo Finance](https://finance.yahoo.com/) and the standing data for the stocks were pulled from the [Wikipedia S&P 500 page](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).

### Layout
The period and the weighting used to build the portfolio, can be controlled from the sidebar.
To the right, there are 7 tabs with information and charts on the stocks and the portfolio.

![image](https://github.com/valeonte/stock_return_ui/assets/12778706/38a027d9-2887-456c-a59a-82fe7a82438f)


### Stock Returns
A chart with the cumulative performance of the 10 stocks over the selected period is displayed in the Stock Returns tab.
![image](https://github.com/valeonte/stock_return_ui/assets/12778706/8567d9d1-a273-4194-8e09-e68cb5bd080a)

### Portfolio Performance
The cumulative performance chart of our portfolio over the period is displayed in the Portfolio Performance tab. Below the chart, there is a table with the return, the volatility and the sharpe ratio of our portfolio.
![image](https://github.com/valeonte/stock_return_ui/assets/12778706/72d2189c-2c5f-44c4-bbf0-2be552248758)

### Stock Details
A table with standing data of the stocks is displayed in the Stock Details tab.
![image](https://github.com/valeonte/stock_return_ui/assets/12778706/1694a918-e08c-46cf-b24e-05af98047bf4)

### Stock Weights
The stock weights of the stocks over time are displayed in this tab.
![image](https://github.com/valeonte/stock_return_ui/assets/12778706/6067cafb-8c2d-46c5-bcf4-9d4fee528f72)

### Stock Contributions
The contribution of each stock to the portfolio return is displayed in the Stock Contributions tab.
![image](https://github.com/valeonte/stock_return_ui/assets/12778706/025080dc-8005-4c24-b092-d50b68e9489a)

### Sector Weights
The exposures to the sectors of the stocks over time, are displayed in the Sector Weights tab.
![image](https://github.com/valeonte/stock_return_ui/assets/12778706/7ccb0da9-47cb-466d-bd29-d04625d49d7a)

### Sector Contributions
The contribution to the portfolio's return from the sectors of the stocks are displayed in the Sector Contributions tab.
![image](https://github.com/valeonte/stock_return_ui/assets/12778706/7d67d497-86c1-427e-ac66-3302ff3b1173)



