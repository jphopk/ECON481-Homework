import numpy as np
import pandas as pd

def github() -> str:
    
    return "https://github.com/jphopk/ECON481-Homework/blob/main/ECON481-HW3-JustinHopkins.py"

def import_yearly_data(years: list) -> pd.DataFrame:
    url_mapping = {
        2022: 'https://lukashager.netlify.app/econ-481/data/ghgp_data_2022.xlsx',
        2021: 'https://lukashager.netlify.app/econ-481/data/ghgp_data_2021.xlsx',
        2020: 'https://lukashager.netlify.app/econ-481/data/ghgp_data_2020.xlsx',
        2019: 'https://lukashager.netlify.app/econ-481/data/ghgp_data_2019.xlsx'
    }

    df = pd.DataFrame()
    for year in years:
        url = url_mapping.get(year)
        newDf = pd.read_excel(url, sheet_name = 'Direct Emitters', skiprows = 3)
        newDf.insert(0, 'year', year)
        df = pd.concat([df, newDf])
    
    return df

def import_parent_companies(years: list) -> pd.DataFrame:
    parentSite = 'https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb'
    parentDf = pd.DataFrame()
    for year in years:
        newParentDf = pd.read_excel(parentSite, sheet_name = str(year))
        for index, row in newParentDf.iterrows():
            is_null_row = row.isnull().all()
            if is_null_row:
                newParentDf = newParentDf.drop(index)
        newParentDf.insert(0, 'year', year)
        parentDf = pd.concat([parentDf, newParentDf])
    return parentDf

def n_null(df: pd.DataFrame, col: str) -> int:
    null_count = df[col].isnull().sum()
    return null_count

def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    url_mapping = {
        2022: 'https://lukashager.netlify.app/econ-481/data/ghgp_data_2022.xlsx',
        2021: 'https://lukashager.netlify.app/econ-481/data/ghgp_data_2021.xlsx',
        2020: 'https://lukashager.netlify.app/econ-481/data/ghgp_data_2020.xlsx',
        2019: 'https://lukashager.netlify.app/econ-481/data/ghgp_data_2019.xlsx'
    }
    parentSite = 'https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb'
    cleanDf = pd.DataFrame()
    cleanDf = pd.merge(emissions_data, parent_data, left_on=['year', 'Facility Id'], right_on=['year', 'GHGRP FACILITY ID'], how = 'left')
    

    cleaner_df = cleanDf[['Facility Id', 'year', 'State', 'Industry Type (sectors)', 
                            'Total reported direct emissions', 'PARENT CO. STATE', 
                            'PARENT CO. PERCENT OWNERSHIP']]
    
    cleaner_df.columns = cleaner_df.columns.str.lower()

    return cleaner_df

def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    aggVars = ['total reported direct emissions', 'parent co. percent ownership']
    aggDf = df.groupby(group_vars)[aggVars].agg(['min', 'median', 'mean', 'max'])
    aggDf = aggDf.sort_values(by=('total reported direct emissions', 'mean'), ascending=False)
    
    return aggDf
