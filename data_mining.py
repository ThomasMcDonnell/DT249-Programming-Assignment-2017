import datetime as dt
import pandas as pd
import pandas_datareader.data as web


"""
Global variables that will hold the selected data and be callable to print data to users terminal.

Normally global variables are considered a bad idea, but owing to the fact that in this use case they 
wont be used anywhere in the program other than to be callable by the user and thus no risk of being 
mutated and causing semantic errors.   
"""
six_worst_years = []
six_best_years = []
six_best_months = []
six_worst_months = []


def get_data_from_yahoo():
    """
    GOOGLE TICKER = GOOGL

    :return: requested data set saved as a csv file
    """
    try:
        ticker = input('Enter the ticker symbol: ').upper()
        start = dt.datetime(2004, 8, 19)
        end = dt.datetime.today()

        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv('stock_data.csv')
    except Exception as e:
        print(e)
        exit()


def weighted_monthly_average(csv):
    """
    :param csv: Takes in the csv file downloaded and maps a function weighted averages to data set grouped by month
            per year.
    :return: monthly weighted averages and appends best six and worst six to their respective global
            variables.
    """
    df = pd.read_csv('stock_data.csv', parse_dates=True, index_col=0)
    monthly = df.groupby(pd.Grouper(freq='M'))
    monthly_avg = monthly.apply(lambda wavg: (wavg['Adj Close'] * wavg['Volume']).sum() / wavg['Volume'].sum())

    six_worst_months.append(monthly_avg.nsmallest(6))
    six_best_months.append(monthly_avg.nlargest(6))


def weighted_yearly_average(csv):
    """
    :param csv: Takes in the csv file downloaded and maps a function weighted averages to data set grouped by year.
    :return: yearly weighted averages and appends best six and worst six to their respective global variables.
    """
    df = pd.read_csv('stock_data.csv', parse_dates=True, index_col=0)
    by_year = df.groupby(lambda x: x.year)
    yearly_avg = by_year.apply(lambda wavg: (wavg['Adj Close'] * wavg['Volume']).sum() / wavg['Volume'].sum())

    six_worst_years.append(yearly_avg.nsmallest(6))
    six_best_years.append(yearly_avg.nlargest(6))


def data_selection_choice():
    try:
        data_selection = input("would you like to see;\n"
                               "1 The best and worst six months\n"
                               "2 The best and worst six years\n"
                               "3 Both best and worst six months and years ")
        if data_selection == '1':
            print('The best six months are as follows: \n', six_best_months)
            print('The worst six months are as follows: \n', six_worst_months)
        elif data_selection == '2':
            print('The best six years are as follows: \n', six_best_years)
            print('The worst six years are as follows: \n', six_worst_years)
        else:
            print('The best six months are as follows: \n', six_best_months)
            print('The worst six months are as follows: \n', six_worst_months)
            print('The best six years are as follows: \n', six_best_years)
            print('The worst six years are as follows: \n', six_worst_years)
    except Exception as e:
        print(e)
        exit()


if __name__ == '__main__':
    get_data_from_yahoo()
    weighted_monthly_average('stock_data.csv')
    weighted_yearly_average('stock_data.csv')
    data_selection_choice()
