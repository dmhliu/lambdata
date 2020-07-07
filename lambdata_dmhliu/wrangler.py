#!/usr/bin/env python

# lambdata module containing wrangler class

import pandas as pd
import numpy as np


class Wrangler:
    """the intent is for each instance of wrangler to contain lists of
    specific transformations to be performed on an dataframe
    by the class methods. """

    def calc_lt_005_cat(self, df):
        """ return a list of the bottom .5% category names for binning"""
        return df.Category.value_counts(
        )[df.Category.value_counts(normalize=True).values < .005]

    def __init__(self, data=None):
        if data is None:
            data = pd.DataFrame()
        self.dropcols = list()  # list to store columns to drop
        self.droprows = dict()  # row boolean filters
        self.encoders = dict()    # colname, function to be applied to elements
        self.dropcols_post = list()  # list to drop after enconding

        self.raw_df = data.copy()  # preserve the original dataframe
        # this will be passed around or be used as default by class methods
        self.working = self.raw_df.copy()

    # methods

    def set_data(self, newdf):
        """reset dataframe to new df, leaving configuration intact"""
        self.raw_df = newdf.copy()
        self.working = self.raw_df.copy()
        return self.working

    def add_to_dropcols(self, labels):
        for l in labels:
            if l in self.dropcols:
                print('error column already in dropcols list')
                break
                return self.dropcols
        self.dropcols.extend(labels)
        return self.dropcols

    def get_dropcols(self):  # why use accessor methods in python?

        if not self.dropcols:
            print('no columns to drop')
        return self.dropcols

    def clear_dropcols(self):
        self.dropcols = list()
        return True

    def get_nancols(self, df=None, store=False):
        if df is None:
            df = self.working
        cols = df.columns
        nc = df[cols].isnull().sum().index.tolist()
        if store:
            self.nancols = nc
        return nc

    def add_to_droprows(self, name, expr):
        self.droprows[name] = expr
        return self.droprows.keys()

    def add_encoding(self, label, mapper):
        try:
            label in self.working.columns
        except:
            print(label, 'not found in working copy, may have been dropped')
            assert label in self.raw_df.columns
        self.encoders[label] = mapper

# "internal"
    def drop_rows_by_mask(self, df=None, rowmask=None):
        """takes a dataframe, a boolean row rowmask to drop INPLACE,
        or drop all the rows in self.droprows,
        returns the modified dataframe"""
        if df is None:
            df = self.working
        if rowmask is None:
            print('dropping all in droprows..')
            if self.droprows:
                dropdict = list(self.droprows.keys())
            rowmask = self.homedroprows[dropdict[0]]  # get first boolean mask
            for l in dropdict:
                print('\napplying mask: ', l)
                rowmask = rowmask | self.droprows[l]  # or them all together
        df.drop(index=df[rowmask].index, inplace=True)
        return df

    def drop_dupes(self, df=None):
        """INPLACE: drop duplicate rows in df,
        return modified copy"""
        if df is None:
            df = self.working
        todropindex = df[df.duplicated()].index
        print('\n dropping', todropindex.shape, 'rows')
        df.drop(todropindex, axis=0, inplace=True)
        return df

    def drop_columns(self, df=None, list=None):
        """INPLACE if df provided, use working
        if no list is provided, drop all columns in list
        if list is provided, drop only the columns in argument list
        and add them to the dropcols list
        return modified dataframe"""

        if df is None:
            df = self.working
        # list of droplabels is passed, added to self.dropcols,then dropped.
        if list:
            for l in list:
                if l in self.dropcols:
                    print('error column already in dropcols list')
                    break
                    return self.dropcols
            self.dropcols.extend(list)
        else:
            list = self.dropcols
            # TODO: check dropcols present in df.columns
        return df.drop(labels=list, axis=1, inplace=True)

    def drop_columns_post(self):
        """INPLACE drop any columns in list dropcols_post 
        dont return anything"""
        drop_columns(list=dropcols_post)

    def bin_othercats(self):
        """to help reduce cardinality bin the lower .5pct of categories as other
            CAUTION need to do this after dropping bad data rows, it will change every time
            the df is resampled.... """
        df = self.working
        othercats = self.calc_lt_005_cat(df).index.tolist()
        df['Category'] = df.Category.map(
            lambda cat: 'other' if cat in othercats else cat)

    def bin_lwr_pt_5(self, labels):  # generalized
        df = self.working
        for col in labels:
            other = df[col].value_counts()[df[col].value_counts(
                normalize=True).values < .005].index.tolist()
            df[col] = df[col].map(
                lambda value: 'other' if value in other else value)

    def encode(self, df=None, label=None, fun=None):
        """label is key for dict AND is column label 
        fun is a function for pd.Series.map()
        """
        if df is None:
            df = self.working
            print('\n Encoding, changing working copy..')
        if fun is None:
            fun = list(self.encoders.keys())
            for k in fun:
                print('  ... encoding column: ', k)
                df[k] = df[k].map(self.encoders[k])
        else:
            df[label] = df[label].map(fun)
        return df

    def to_datetime(self, cols=None, df=None):
        if df is None:
            df = self.working
            print('\nworking df is being changed..')
        if cols is None:
            cols = self.dt_cols
        for c in cols:
            print('converting', c, 'to datetime')
            try:
                df[c] = pd.to_datetime(
                    df[c], infer_datetime_format=True)  # inplace
            except:
                print('error - possible this column needs cleaning')
        return df

    def make_feature(self, newlabel, input, fun):
        """ make or overwrite column newlabel
        input=label or list of labels that form series to apply fun"""

        df = self.working
        try:
            df[newlabel] = df[input].apply(fun, axis=1)  # or map or tranform?
            print('\nadded feature:', newlabel)
        except:
            print('there was a problem, not added!!')
            return False
        return True

    def calc_open_cases(self, sometime):  # input time
        df = self.working[['CaseID', 'Opened', 'Closed']]
        opened_prior = df['Opened'] < sometime        # cases opened before it,
        not_closed_prior = ~(df['Closed'] < sometime)  # not closed,
        open_at_thattime = opened_prior & not_closed_prior  # and
        return open_at_thattime.sum()

    order_default = [drop_rows_by_mask,
                     drop_columns,
                     drop_dupes,
                     encode,
                     drop_columns_post]  # methods in order of application

    def wrangle(self, df=None):

        if df is None:
            df = self.raw_df.copy()  # start from the beginning
            result = df
            print('will apply :', self.order_default)
            for f in self.order_default:
                print('level')
                result = f(result)
        return result
