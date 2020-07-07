# python utility functions for data processsing
# goal refactor as custom tranformers to use with pipeline

def to_datetime(self, cols=None, df=None):
    if df is None:
        df=self.working
        print('\nworking df is being changed..')
    if cols is None:
        cols=self.dt_cols
    for c in cols:
        print('converting',c,'to datetime')
        try:
            df[c] = pd.to_datetime(df[c],infer_datetime_format=True)  #inplace
        except:
            print('error - possible this column needs cleaning')
    return df
    
def bin_lwr_pt_5(self, labels):  ##generalized 
    """list of labels to do binning on"""
    
    df=self.working
    for col in labels:
        other = df[col].value_counts()[df[col].value_counts(normalize=True).values < .005].index.tolist()
        df[col] = df[col].map(lambda value : 'other' if value in other else value)