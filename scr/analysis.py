import pandas as pd
from db import read_sql 
from scipy.stats import linregress
import numpy as np

def get_last_n_years(max_year, n):
    return list(range(max_year - n + 1, max_year + 1))

def compare_rainfall_and_top_crops(state_code_x, state_code_y, years, top_m=5):
    """Compare average rainfall and top crops between two states."""

    year_list = ",".join(map(str, years))
    q = f"""
        SELECT state_code, year, annual_rainfall_mm, source_url
        FROM rainfall_annual_state
        WHERE state_code IN ('{state_code_x}', '{state_code_y}')
          AND year IN ({year_list})
    """
    df_rain = read_sql(q)
    
    if df_rain.empty:
        return {"error": "no data"}
    avg = df_rain.groupby('state_code')['annual_rainfall_mm'] \
                 .mean() \
                 .reset_index() \
                 .rename(columns={'annual_rainfall_mm': 'avg_annual_rainfall_mm'})
    
    yrs = ','.join(map(str, years))
    q2 = f"""
        SELECT state_code, crop_id, year, production_tonnes, source_url
        FROM crop_state_year
        WHERE state_code IN ('{state_code_x}', '{state_code_y}')
          AND year IN ({yrs})
    """
    df_crop = read_sql(q2)
    crop_agg = df_crop.groupby(['state_code', 'crop_id'])['production_tonnes'].sum().reset_index()

    top_x = (crop_agg[crop_agg['state_code'] == state_code_x] \
                .sort_values('production_tonnes', ascending=False) \
                .head(top_m)['crop_id'].tolist()
                .tolist())
    top_y = (crop_agg[crop_agg['state_code'] == state_code_y] \
                .sort_values('production_tonnes', ascending=False) \
                .head(top_m)['crop_id'].tolist()
                .tolist()
    )
    return {
        "rainfall_avg": avg,
        "top_crops_state_x": top_x,
        "top_crops_state_y": top_y,
        "rain_provenance": df_rain,
        "crop_provenance": df_crop
    }

def district_max_crop(state_code, crop_id):
    df = read_sql("SELECT * FROM raw_crop")
    sub_crop = df[(df['state'] == state_code) | (df['state'].str.lower() == state_code.lower())]
    
    if sub_crop.empty:
        return {"error": "no data"}
    
    max_year = int(sub_crop['year'].max())
    sub_recent = sub_crop[sub_crop['year'] == max_year]
    group = sub_recent.groupby('district')['production_tonnes'].sum().reset_index()
    
    highest = group.sort_values('production_tonnes', ascending=False).iloc[0].to_dict()
    lowest = group.sort_values('production_tonnes', ascending=True).iloc[0].to_dict()
    
    return {
        "max_year": max_year,
        "highest_producing_district": highest,
        "lowest_producing_district": lowest,
        "provenance": sub_recent
    }

def trend_and_correlation(state_code, crop_id, years):
    q = f"""
        SELECT year, production_tonnes
        FROM crop_state_year
        WHERE state_code = '{state_code}'
          AND crop_id = '{crop_id}'
          AND year <= {max(years)}
          AND year >= {min(years)}
    """
    prod = read_sql(q).set_index('year').reindex(years, fill_value=0).reset_index()
    
    q2 = f"""
        SELECT year, annual_rainfall_mm
        FROM rainfall_annual_state
        WHERE state_code = '{state_code}'
          AND year <= {max(years)}
          AND year >= {min(years)}
    """
    rain = read_sql(q2).set_index('year').reindex(years, fill_value=0).reset_index()
    prod = prod.sort_values('year').reindex(years,fill_value=0).reset_index(drop=True)
    year_arr = np.array(years)
    prod_arr = prod['production_tonnes'].values
    
    slope, intercept, r_value, p_value, std_err = linregress(year_arr, prod_arr)
    corr = np.corrcoef(prod_arr, rain['annual_rainfall_mm'].values)[0, 1] if prod_arr.size > 1 else None
    
    return {
        "years": years,
        "production": prod.reset_index().to_dict(orient='records'),
        "rainfall": rain.reset_index().to_dict(orient='records'),
        "trend": {
            "slope": slope,
            "r_squared": r_value**2,
            "p_value": p_value
        },
        "correlation": corr
    }
