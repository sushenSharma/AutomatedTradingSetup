import pandas as pd

data = pd.read_csv("Actual_result_daily.csv")
cash_full_data = pd.read_csv("cash.csv")

print(cash_full_data.columns)
stock_names = list(data["StockName"])

cash_full_data = cash_full_data.groupby(" DATE1")



hit =   0
miss =  0
for stock_counter in range(0,len(stock_names)):
    Stock_split_dataFrame = cash_full_data.get_group(stock_names[stock_counter])

    number_of_rows = len(Stock_split_dataFrame.index)
    n = 0

    while (n < (number_of_rows-1)):
        Sliced_DataFrame = Stock_split_dataFrame.iloc[0:(n+1)]
        delivery_factor_MAX = float(Sliced_DataFrame["delivery_Factor"].max())
        delivery_factor_Mean = float(Sliced_DataFrame["delivery_Factor"].mean())
        # print(Sliced_DataFrame)
        # print(delivery_factor_MAX)
        recent_row = (Sliced_DataFrame.iloc[-1])
        recent_delivery_Factor = (float)(recent_row["delivery_Factor"])
        if  (recent_delivery_Factor == delivery_factor_MAX):
                recent_Close_price = (float)(recent_row[" CLOSE_PRICE"])
                Next_Immidieate_Close_Price = (float)(Stock_split_dataFrame.iloc[n+1][" CLOSE_PRICE"])
                difference_between_close_Price = Next_Immidieate_Close_Price - recent_Close_price
                Percentage_Change_Close_price = ((difference_between_close_Price/Next_Immidieate_Close_Price) * 100)

                if ( (Percentage_Change_Close_price > 5) or (Percentage_Change_Close_price < -5)):
                    hit = hit + 1
                    print(f"Delivery_factor_MAX : {stock_names[stock_counter]}  ,Date : {recent_row['SYMBOL']}, Next Day Percentage_Change : {Percentage_Change_Close_price} %")
                else:
                    miss = miss + 1

        n = n +1

Accuracy = (hit/(hit+miss))* 100
print(f"Total hits {hit}")
print(f"Total miss {miss}")
print(Accuracy)

# for stock in stock_names:
#     data_slash = cash_full_data[cash_full_data[" DATE1"] == stock]
#     close_price_mean = data_slash[" CLOSE_PRICE"].mean()
#     hilo_mean = float(data_slash["HiLo_Percentage"].mean())
#
#     delivery_factor_MAX = float(data_slash["delivery_Factor"].max())
#
#     recent_row = (data_slash.iloc[-1])
#     recent_hilo = float(recent_row["HiLo_Percentage"])
#
#     recent_delivery_Factor = (float)(recent_row["delivery_Factor"])
#
#
#
#
#     if (recent_delivery_Factor == delivery_factor_MAX):
#         print(f"Delivery_factor_MAX : {stock}")
#
#     elif ((recent_hilo > hilo_mean) and (recent_delivery_Factor > 300)):
#         print(f"Recent_Hilo {stock}")

