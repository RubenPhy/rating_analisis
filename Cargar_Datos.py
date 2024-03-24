import pandas as pd


def read_all_sheets(file_path, sheets):
    """
    Lectura de todos los datos de cada pestaña
    :param sheets: Pestañas del excel para leer
    :return: Diccionario de df con key = años y value = df con los datos del año
    """

    dfs = {}
    for Sheet in sheets:
        df = read_sheet(file_path, Sheet)
        dfs.update({'20' + Sheet[-2:]: df})
    return dfs


def read_sheet(file_path, sheet_):
    """
    Lectura de cada pestaña
    :param file_path: Dirección del archivo
    :param sheet_: Pestaña a leer
    :return: df con los datos
    """

    df_raw = pd.read_excel(file_path, sheet_name=sheet_, skiprows=3, header=0, na_values=['NR', 'NR/NR'])

    for col in df_raw.columns:
        if 'Unnamed' in col:
            del df_raw[col]
    return df_raw


def nueva_columna(dfs):
    for ano, df in dfs.items():
        try:
            df['ID'] = ano + '-' + df['Excel Company ID']
        except:
            print('Columna ID ya creada')
            return dfs

    return dfs


def clean_df(df):

    columns_to_float = df.columns[5:]
    df[columns_to_float] = df[columns_to_float].apply(pd.to_numeric, errors='coerce')
    df.dropna(axis=0, how="any", inplace=True)
    for special in ['NR', 'NR/NR', 'SD', 0]:
        df = df[df.Rating != special]
    return df


if __name__ == '__main__':

    path = r"""G:\Shared drives\ES ES Valuations - Equipo\Methodology\WORKSTREAM 1 - Tasas de descuento\2-Internacional\Otros\Rating\Datos"""
    file = "Datos.xlsm"

    Sheets = ['Raw_data_' + str(i) for i in range(18, 13, -1)]
    file_path = path + r'\\' + file

    dict_dfs_raw = read_all_sheets(Sheets)

    print('Datos del excel: ', file, '\nPestañas con datos: ', [pestana for pestana in Sheets if 'Raw_data' in pestana],
          '\nTamaño de la muestras (filas x columnas): ',
          [ano + ' -> ' + str(len(df)) + ' x ' + str(len(df.columns)) for ano, df in dict_dfs_raw.items()])

    dfs = nueva_columna(dict_dfs_raw)
    list_df = [df for ano, df in dfs.items()]
    df_union = pd.concat(list_df)
    ordered_columns = df_union.columns[[0, -1, -2] + list(range(1, len(df_union.columns) - 2))]
    df_union = df_union[ordered_columns]

    df = clean_df(df_union)
    df.to_csv("Clean_Data_No_Normalizados.csv")
    print('Tamaño de la muestra limpia: ', len(df.columns), 'x', len(df), '\nRatings : ', set(df['Rating']),
          '\nSector : ', set(df['Sector']))

