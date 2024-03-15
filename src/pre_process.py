
#^ Imports =========================================================================================>
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

#^ Functions =======================================================================================>
def Create_IN_OUT_Dataset():
    """ Function used to create IN and OUT degree datasets of accounts;
    """
    
    acc_21 = pd.DataFrame()
    acc_22 = pd.DataFrame()

    for i in range(26):
        aux = pd.read_csv('../../data/transactions/processed/flashbots_21_' + str(i) + '.csv')
        aux = pd.DataFrame(aux)

        acc_21 = pd.concat([acc_21, aux])

    for i in range(4):
        aux = pd.read_csv('../../data/transactions/processed/flashbots_22_' + str(i+1) + '.csv')
        aux = pd.DataFrame(aux)

        acc_22 = pd.concat([acc_22, aux])
        
    acc_21_to = acc_21[['to_address', 'value', 'date']].rename(columns={'to_address': 'address'})
    acc_21_from = acc_21[['from_address', 'value', 'date']].rename(columns={'from_address': 'address'})

    acc_22_to = acc_22[['to_address', 'coinbase_transfer', 'date']].rename(columns={'to_address': 'address'})
    acc_22_from = acc_22[['eoa_address', 'coinbase_transfer', 'date']].rename(columns={'eoa_address': 'address'})

    acc_21 = pd.concat([acc_21_to, acc_21_from])
    acc_22 = pd.concat([acc_22_to, acc_22_from])
    
    acc_21_to['date'] = acc_21_to['date'].str[:2]
    acc_21_from['date'] = acc_21_from['date'].str[:2]

    acc_22_to['date'] = acc_22_to['date'].str[:2]
    acc_22_from['date'] = acc_22_from['date'].str[:2]

    acc_21['date'] = acc_21['date'].str[:2]
    acc_22['date'] = acc_22['date'].str[:2]
    
    acc_21_to_formated = acc_21_to.groupby(['address', 'date']).size().reset_index(name = 'count')
    acc_21_from_formated = acc_21_from.groupby(['address', 'date']).size().reset_index(name = 'count')

    acc_22_to_formated = acc_22_to.groupby(['address', 'date']).size().reset_index(name = 'count')
    acc_22_from_formated = acc_22_from.groupby(['address', 'date']).size().reset_index(name = 'count')

    acc_21_formated = acc_21.groupby(['address', 'date']).size().reset_index(name = 'count')
    acc_22_formated = acc_22.groupby(['address', 'date']).size().reset_index(name = 'count')
    
    acc_21_to_formated.to_csv('../../data/accounts/acc_21_to_new.csv', index = False)
    acc_21_from_formated.to_csv('../../data/accounts/acc_21_from_new.csv', index = False)

    acc_22_to_formated.to_csv('../../data/accounts/acc_22_to_new.csv', index = False)
    acc_22_from_formated.to_csv('../../data/accounts/acc_22_from_new.csv', index = False)

    acc_21_formated.to_csv('../../data/accounts/acc_21_new.csv', index=False)
    acc_22_formated.to_csv('../../data/accounts/acc_22_new.csv', index=False)
    
def Column_Format():
    """ Function used to format accounts datasets in columns of months;
    """
    
    acc_21_to = pd.DataFrame()
    acc_21_from = pd.DataFrame()
    acc_22_to = pd.DataFrame()
    acc_22_from = pd.DataFrame()
    acc_21 = pd.DataFrame()
    acc_22 = pd.DataFrame()
    
    aux_to = pd.DataFrame()
    aux_from = pd.DataFrame()
    aux = pd.DataFrame()

    acc_21_to_formated = pd.read_csv('../../data/accounts/acc_21_to_new.csv')
    acc_21_from_formated = pd.read_csv('../../data/accounts/acc_21_from_new.csv')

    acc_21_to_formated = pd.DataFrame(acc_21_to_formated)
    acc_21_from_formated = pd.DataFrame(acc_21_from_formated)

    acc_22_to_formated = pd.read_csv('../../data/accounts/acc_22_to_new.csv')
    acc_22_from_formated = pd.read_csv('../../data/accounts/acc_22_from_new.csv')

    acc_22_to_formated = pd.DataFrame(acc_22_to_formated)
    acc_22_from_formated = pd.DataFrame(acc_22_from_formated)
    
    acc_21_formated = pd.read_csv('../../data/accounts/acc_21_new.csv')
    acc_22_formated = pd.read_csv('../../data/accounts/acc_22_new.csv')
    
    acc_21_formated = pd.DataFrame(acc_21_formated)
    acc_22_formated = pd.DataFrame(acc_22_formated)
    
    for i in range(12):
        aux_to = acc_21_to_formated.loc[acc_21_to_formated['date'] == (i+1)]
        aux_from = acc_21_from_formated.loc[acc_21_from_formated['date'] == (i+1)]
        aux = acc_21_formated.loc[acc_21_formated['date'] == str(i+1)]

        if i == 0:
            acc_21_to = aux_to
            acc_21_from = aux_from
            acc_21 = aux
        else:
            acc_21_to = acc_21_to.merge(aux_to, on='address', how='outer')
            acc_21_from = acc_21_from.merge(aux_from, on='address', how='outer')
            acc_21 = acc_21.merge(aux, on='address', how='outer')

            if i == 1:
                acc_21_to = acc_21_to.rename(columns = {'count_x': 'count_month_' + str(i), 'count_y': 'count_month_' + str(i+1)})
                acc_21_to = acc_21_to.drop(columns=['date_x', 'date_y'])

                acc_21_from = acc_21_from.rename(columns = {'count_x': 'count_month_' + str(i), 'count_y': 'count_month_' + str(i+1)})
                acc_21_from = acc_21_from.drop(columns=['date_x', 'date_y'])

                acc_21 = acc_21.rename(columns = {'count_x': 'count_month_' + str(i), 'count_y': 'count_month_' + str(i+1)})
                acc_21 = acc_21.drop(columns=['date_x', 'date_y'])
            else:
                acc_21_to = acc_21_to.rename(columns = {'count': 'count_month_' + str(i+1)})
                acc_21_to = acc_21_to.drop(columns=['date'])

                acc_21_from = acc_21_from.rename(columns = {'count': 'count_month_' + str(i+1)})
                acc_21_from = acc_21_from.drop(columns=['date'])

                acc_21 = acc_21.rename(columns = {'count': 'count_month_' + str(i+1)})
                acc_21 = acc_21.drop(columns=['date'])

    for j in range(12):
        acc_21_to['count_month_' + str(j+1)] = acc_21_to['count_month_' + str(j+1)].fillna(0)
        acc_21_from['count_month_' + str(j+1)] = acc_21_from['count_month_' + str(j+1)].fillna(0)
        acc_21['count_month_' + str(j+1)] = acc_21['count_month_' + str(j+1)].fillna(0)
        
    acc_21_to.to_csv('../../data/accounts/acc_21_to_culumn.csv', index = False)
    acc_21_from.to_csv('../../data/accounts/acc_21_from_culumn.csv', index = False)
    acc_21.to_csv('../../data/accounts/acc_21_column.csv', index=False)
    
def Quarter_Format():
    """ Function used to format datasets in columns of mean degree in quarters;
    """
    acc_21_to = pd.read_csv('../../data/accounts/acc_21_to_culumn.csv')
    acc_21_from = pd.read_csv('../../data/accounts/acc_21_from_culumn.csv')

    acc_21_to = pd.DataFrame(acc_21_to)
    acc_21_from = pd.DataFrame(acc_21_from)

    acc_22_to = pd.read_csv('../../data/accounts/acc_22_to_new.csv')
    acc_22_from = pd.read_csv('../../data/accounts/acc_22_from_new.csv')

    acc_22_to = pd.DataFrame(acc_22_to)
    acc_22_from = pd.DataFrame(acc_22_from)

    acc_22_to = acc_22_to.rename(columns={'to_address': 'address', 'count': 'count_month_13'})
    acc_22_from = acc_22_from.rename(columns={'eoa_address': 'address', 'count': 'count_month_13'})
    
    acc_to = acc_21_to.merge(acc_22_to, on='address', how='left')
    acc_from = acc_21_from.merge(acc_22_from, on='address', how='left')
    
    acc_to = acc_to.drop(columns={'date'})
    acc_from = acc_from.drop(columns={'date'})

    acc_to['count_month_13'] = acc_to['count_month_13'].fillna(0)
    acc_from['count_month_13'] = acc_from['count_month_13'].fillna(0)
    
    scaler = MinMaxScaler()
    df_std = pd.DataFrame()

    df_scaled = scaler.fit_transform(acc_to[['count_month_1', 'count_month_2', 'count_month_3',
                                        'count_month_4', 'count_month_5', 'count_month_6',
                                        'count_month_7', 'count_month_8', 'count_month_9','count_month_10','count_month_11','count_month_12','count_month_13','count_month_14']])
    df_scaled = pd.DataFrame(df_scaled, columns = [['count_month_1', 'count_month_2', 'count_month_3',
                                                    'count_month_4', 'count_month_5', 'count_month_6',
                                                    'count_month_7', 'count_month_8', 'count_month_9','count_month_10','count_month_11','count_month_12','count_month_13','count_month_14']])
    df_scaled['address'] = acc_to['to_address']

    df_std['std_quarter_1'] = df_scaled[['count_month_1', 'count_month_2', 'count_month_3']].std(axis = 1)
    df_std['std_quarter_2'] = df_scaled[['count_month_1', 'count_month_2', 'count_month_3',
                                        'count_month_4', 'count_month_5', 'count_month_6']].std(axis = 1)
    df_std['std_quarter_3'] = df_scaled[['count_month_1', 'count_month_2', 'count_month_3',
                                        'count_month_4', 'count_month_5', 'count_month_6',
                                        'count_month_8', 'count_month_7', 'count_month_9']].std(axis = 1)
    df_std['std_quarter_4'] = df_scaled[['count_month_1', 'count_month_2', 'count_month_3',
                                        'count_month_4', 'count_month_5', 'count_month_6',
                                        'count_month_8', 'count_month_7', 'count_month_9',
                                        'count_month_10','count_month_11','count_month_12','count_month_13','count_month_14']].std(axis = 1)

    df_std['address'] = df_scaled['address']
    df_std.to_csv('../../data/accounts/acc_21_22_std_quarter_to_value_new.csv', index=False) 
        