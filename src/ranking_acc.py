
#^ Imports =========================================================================================>
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')
sns.set_theme()

#^ Functions =======================================================================================>
def separate_degree_in_months(df: pd.DataFrame, hash: str) -> pd.DataFrame:
    """  Function used to separate degrees in months;
    """
    
    df.rename(inplace = True, 
                    columns = {'avgValue1': '02/21 to 04/21', 'avgValue2': '05/21 to 07/21',
                                'avgValue3': '08/21 to 10/21', 'avgValue4': '11/21 to 01/22',
                                'degree': 'Russian Invasion'}
    )
    df = pd.melt(df, ignore_index = False, value_vars= ['02/21 to 04/21', '05/21 to 07/21', 
                                                                    '08/21 to 10/21', '11/21 to 01/22', 'Russian Invasion'],
                       value_name='Degree', var_name = ['Time Period']
    )
    try: 
        result = df.loc[hash].sort_values(by = ['Time Period'])
    except KeyError:
        df = pd.DataFrame(index = [hash, hash, hash, hash, hash],
                            data = {
                                'Degree': [0,0,0,0,0], 
                                'Time Period': ['02/21 to 04/21', '05/21 to 07/21', '08/21 to 10/21', '11/21 to 01/22', 'Russian Invasion']
                            }
        )
        return df
    return result        

def plot_account(df, lookup_in, lookup_out, hash_acc):
    """ Function used to plot matrix of graphs;
    """
    
    color_list = ['red', 'blue', 'green']
    copy_lookup_in = lookup_in.copy()
    copy_lookup_in['avgValue1'] = copy_lookup_in['avgValue1']
    copy_lookup_in['avgValue2'] = copy_lookup_in['avgValue2']
    copy_lookup_in['avgValue3'] = copy_lookup_in['avgValue3']
    copy_lookup_in['avgValue4'] = copy_lookup_in['avgValue4']

    copy_lookup_out = lookup_out.copy()
    copy_lookup_out['avgValue1'] = copy_lookup_out['avgValue1']
    copy_lookup_out['avgValue2'] = copy_lookup_out['avgValue2']
    copy_lookup_out['avgValue3'] = copy_lookup_out['avgValue3']
    copy_lookup_out['avgValue4'] = copy_lookup_out['avgValue4']

    df_degree = separate_degree_in_months(copy_lookup_in.add(copy_lookup_out, fill_value = 0), hash_acc)
    df_in = separate_degree_in_months(copy_lookup_in, hash_acc)
    df_out = separate_degree_in_months(copy_lookup_out, hash_acc)

    plt.figure(figsize=(7.7,7.5))
    sns.lineplot(data = df_degree, x = 'Time Period', y = 'Degree', color = color_list[0], label = 'Degree')
    sns.scatterplot(data = df_degree, x = 'Time Period', y = 'Degree', color = color_list[0])
    sns.lineplot(data = df_in, x = 'Time Period', y = 'Degree', color = color_list[1], label = 'In-degree')
    sns.scatterplot(data = df_in, x = 'Time Period', y = 'Degree', color = color_list[1])
    sns.lineplot(data = df_out, x = 'Time Period', y = 'Degree', color = color_list[2], label = 'Out-degree')
    sns.scatterplot(data = df_out, x = 'Time Period', y = 'Degree', color = color_list[2])
    sns.set(font_scale=3)
    plt.xticks(rotation=15, fontsize=19)
    plt.yticks(fontsize=20)
    plt.xlabel('Time Period', fontsize=16)
    plt.ylabel('Degree', fontsize=20)
    plt.legend(fontsize = '25')
    plt.savefig('../figs/'+hash_acc+'.pdf')

def get_desc_acc (df, max_std, min_total_val, min_degree = -1):
    """ Function used to get ascendent accounts;
    """
    
    aux = df.loc[(df['stdVal'] > 0) & (df['stdVal'] <= max_std) & (df['totalVal'] > min_total_val)]
    aux = aux.sort_values(by='avgValue1', ascending=False)
    aux = aux.loc[aux['avgValue1'] > 0]

    return aux

def get_asc_acc (df, max_std, max_total_val, min_degree = -1):
    """ Function used to get descendent accounts;
    """
    
    aux = df.loc[(df['stdVal'] > 0) & (df['stdVal'] <= max_std) & (df['totalVal'] <= max_total_val)]
    aux = aux.sort_values(by=['degree'], ascending=False)
    aux = aux.loc[aux['degree'] > 0]

    return aux

def plot_ascdef_bars(asc_df, desc_df):
    """ Function used to plot bar graph of ascendent and descendent accounts;
    """
    
    plt.figure(figsize=(6,5))
    plt.bar(x = ['Ascending', 'Descending'], height = [len(asc_df), len(desc_df)])

    plt.xlabel('Type of Account')
    plt.ylabel('Number of accounts')
    plt.savefig('../data/flashbots/graphs/bar/flashbots_asc_desc_bar_size.pdf')
    plt.show()

def plot_liers_ascdef(asc_df, desc_df):
    """ Function used to plot bar graph of outliers in ascendent and descendent accounts;
    """
    
    asc_iqr = asc_df['degree'].quantile(.75) - asc_df['degree'].quantile(.25)
    asc_median = asc_df['degree'].quantile(.5)
    dec_iqr = desc_df['degree'].quantile(.75) - desc_df['degree'].quantile(.25)
    dec_median = desc_df['degree'].quantile(.5)
    count_asc_liers = len(asc_df[asc_df['degree'] > asc_median + 1.5 * asc_iqr])
    count_dec_liers = len(desc_df[desc_df['degree'] > dec_median + 1.5 * dec_iqr])
    plt.figure(figsize=(6,5))
    plt.bar(x = ['Ascending outliers', 'Descending outliers'], height = [count_asc_liers, count_dec_liers])
    plt.xlabel('Type of Account')
    plt.ylabel('Number of outliers')
    plt.savefig('../data/flashbots/graphs/bar/flashbots_asc_desc_liers_size.pdf')
    plt.show()