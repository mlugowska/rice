import pandas as pd


def styler(df, column_name, color, name):
    # Subset your original dataframe with condition
    df_ = df[df[column_name].gt(0.0)]

    # Pass the subset dataframe index and column to pd.IndexSlice
    slice_ = pd.IndexSlice[df_.index, df_.columns]

    style = df.style.set_properties(**{'background-color': color}, subset=slice_)
    style.to_excel(f'{name}.xlsx', engine='openpyxl')
    return style