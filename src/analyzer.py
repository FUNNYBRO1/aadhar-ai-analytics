import pandas as pd
import numpy as np

def age_wise_coverage(df, level="state"):
    group_cols = [level]

    grouped = df.groupby(group_cols)[
        ['demo_age_5_17', 'demo_age_17_']
    ].sum().reset_index()

    grouped['total'] = grouped['demo_age_5_17'] + grouped['demo_age_17_']

    grouped['youth_percent'] = (grouped['demo_age_5_17'] / grouped['total']) * 100
    grouped['adult_percent'] = (grouped['demo_age_17_'] / grouped['total']) * 100

    return grouped.sort_values(by='youth_percent', ascending=False)


def youth_pressure(df, level="district"):
    grouped = df.groupby(['state', level])['demo_age_5_17'].sum().reset_index()
    return grouped.sort_values(by='demo_age_5_17', ascending=False)


def adult_saturation(df, level="district"):
    grouped = df.groupby(['state', level])['demo_age_17_'].sum().reset_index()
    return grouped.sort_values(by='demo_age_17_', ascending=False)


def temporal_growth(df):
    df['month'] = df['date'].dt.to_period('M')

    grouped = df.groupby('month')[
        ['demo_age_5_17', 'demo_age_17_']
    ].sum().reset_index()

    return grouped


def district_disparity(df):
    grouped = df.groupby(['state', 'district'])[
        ['demo_age_5_17', 'demo_age_17_']
    ].sum().reset_index()
    
    # Division by zero handle karne ke liye
    grouped['ratio'] = grouped['demo_age_5_17'] / grouped['demo_age_17_'].replace(0, np.nan)
    return grouped.sort_values(by='ratio', ascending=False)


def pincode_coverage(df):
    grouped = df.groupby('pincode')[
        ['demo_age_5_17', 'demo_age_17_']
    ].sum().reset_index()

    grouped['total'] = grouped['demo_age_5_17'] + grouped['demo_age_17_']
    return grouped.sort_values(by='total')


def youth_adult_ratio(df, threshold=0.6):
    grouped = df.groupby(['state', 'district'])[
        ['demo_age_5_17', 'demo_age_17_']
    ].sum().reset_index()

    grouped['ratio'] = grouped['demo_age_5_17'] / grouped['demo_age_17_']
    return grouped[grouped['ratio'] > threshold]


def state_concentration(df):
    grouped = df.groupby('state')[
        ['demo_age_5_17', 'demo_age_17_']
    ].sum().reset_index()

    grouped['total'] = grouped['demo_age_5_17'] + grouped['demo_age_17_']
    return grouped.sort_values(by='total', ascending=False)


def longitudinal_stability(df):
    df['year'] = df['date'].dt.year

    grouped = df.groupby(['year', 'state'])[
        ['demo_age_5_17', 'demo_age_17_']
    ].sum().reset_index()

    return grouped


def resource_allocation(df):
    grouped = df.groupby(['state', 'district'])[
        ['demo_age_5_17', 'demo_age_17_']
    ].sum().reset_index()


def adult_enrollment_mapping(df, level="district"):
    # Dummy example for testing
    print("Adult Enrollment Mapping function called.")
    return df.head(10)  # return top 10 rows just for testing
