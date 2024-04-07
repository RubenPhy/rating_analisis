columns_to_check = ["Current Assets", "Cash and equivalents", "Receivables", "Total Assets", "Current Liabilities", "Long Term Debt", "Total Debt", "Total Equity", "Gastos financieros netos", "EBITDA"]
var_x_num = ["Net Debt to EBITDA", "Debt to Assets", "Current Ratio", "Quick Ratio", "Cash ratio", "Long Term Debt to Equity","Debt to Equity", "Debt ratio", "Financial Leverage"]
All_rating_order = ['AAA','AA+','AA','AA-','A+','A','A-','BBB+','BBB','BBB-','BB+','BB','BB-','B+','B','B-','CCC+','CCC','CCC-','CC','D','SD']
rating_order_group = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC','CC', 'D']
All_rating_order_group = {'AAA':'AAA',
                          'AA+':'AA',
                          'AA':'AA',
                          'AA-':'AA',
                          'A+':'A',
                          'A':'A',
                          'A-':'A',
                          'BBB+':'BBB',
                          'BBB':'BBB',
                          'BBB-':'BBB',
                          'BB+':'BB',
                          'BB':'BB',
                          'BB-':'BB',
                          'B+':'B',
                          'B':'B',
                          'B-':'B',
                          'CCC+':'CCC',
                          'CCC':'CCC',
                          'CCC-':'CC',
                          'CC':'CC',
                          'D':'D',
                          'SD':'D'}
sectores_dic = {'Energy':1, 'Materials':2, 'Industrials':3, 'Consumer Discretionary':4, 'Consumer Staples':5, 'Health Care':6, 'Financials':7, 'Information Technology':8, 'Communication Services':9, 'Utilities':10, 'Real Estate':11}

def compute_main_ratios(df_all):
    df_all = df_all.copy()
    
    df_all.loc[:,"Net Debt to EBITDA"] = (df_all["Total Debt"] - df_all["Cash and equivalents"]) / df_all["EBITDA"]
    df_all.loc[:,"Debt to Assets"] = df_all["Total Debt"] / (df_all["Total Equity"]+df_all["Total Debt"])
    df_all.loc[:,"Long Term Debt to Equity"] = df_all["Long Term Debt"] / df_all["Total Equity"]
    df_all.loc[:,"Financial Leverage"] = df_all["Total Assets"] / df_all["Total Equity"]

    df_all.loc[:,"Current Ratio"] = df_all["Current Assets"] / df_all["Current Liabilities"]
    df_all.loc[:,"Quick Ratio"] = (df_all["Cash and equivalents"] + df_all["Receivables"]) / df_all["Current Liabilities"]
    df_all.loc[:,"Cash ratio"] = df_all["Cash and equivalents"] / df_all["Current Liabilities"]
    df_all.loc[:,"Debt to Equity"] = df_all["Total Debt"] / df_all["Total Equity"]
    df_all.loc[:,"Debt ratio"] = df_all["Total Assets"] / df_all["Total Debt"]
    return df_all
