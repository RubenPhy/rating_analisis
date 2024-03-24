import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.style.use('ggplot')


def bar_grafica(titulo, All_rating_order, df):
    #     Obtenemos un dict con la frecuencia absoluta de cada rating que existe en el df
    filas_df = sum(df['Rating'].value_counts())
    print('Número de datos: ', filas_df)
    X = dict(df['Rating'].value_counts() / filas_df)

    #     Los ordenamos por rating
    x_sorted = {}
    for rating in All_rating_order:
        if rating in X.keys():
            x_sorted.update({rating: X[rating]})

    # Set Gráfico
    size_plot = 5
    fig = plt.figure(1, (size_plot * 1.6180, size_plot))
    ax = fig.add_subplot(1, 1, 1)

    # Gráfico de barras
    ax.bar(list(x_sorted.keys()), list(x_sorted.values()))

    # Ordenamos por rating
    plt.xticks([index for index, x in enumerate(x_sorted.values())], list(x_sorted.keys()))

    # Porcentage en el eje y, y valores
    fmt = '%.2f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)
    plt.xticks(rotation=45)

    # Labels número de datos
    x_numero_rating = dict(df['Rating'].value_counts())
    labels = list(df.groupby('Rating').count()['Sector'])
    for i, k in enumerate(x_sorted.keys()):
        plt.text(x=i - 0.5, y=(x_numero_rating[k] / filas_df) + 0.0025, s=x_numero_rating[k], size=10)

    plt.title(titulo)
    plt.show()


def clean_df(df, columnas, percentile):
    #     Para empezar nos quedamos con las columnas que nos interesan
    df = df[columnas]
    #     Quitamos los NA
    df = df.dropna(axis=0, how="any")
    for columna in df.columns:
        df = df[df[columna] != 'n.a.']
    #     Quitamos las que no tiene rating
    df = df[df.Rating != 'NR']
    df = df[df.Rating != 'NR/NR']
    df = df[df.Rating != 'SD']
    #     Redondeamos los datos, ya que no necesitmos tanta precisión
    # df = df.round(2)
    #     Existen compañias que obtemos 0 como output de CIQ, esos tampoco los queremos
    df = df[df.Rating != 0]
    #     df = df[df['Total Assets'] != 0]

    #     Lo convertimos en float en lugar de object.
    for columna in df.columns[3:]:
        if len(set(df[columna])) > 5:
            df[columna] = [float(x) for x in df[columna]]
            #         Tiene demasiada dispersion por tanto normalizamos las datos
            df[columna] = (df[columna] - df[columna].min()) / (df[columna].max() - df[columna].min())
            #         Además podemos eleminiar algunos valores extremos
            mask1 = list(df[columna] > df[columna].quantile(percentile))
            mask2 = list(df[columna] < df[columna].quantile(1 - percentile))
            df = df[mask1 and mask2]
        else:
            pass
            # del df[columna]
    return df


if __name__=='__main__':
    All_rating_order = ['AAA+', 'AAA', 'AAA-', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+', 'BB',
                        'BB-', 'B+', 'B',
                        'B-', 'CCC+', 'CCC', 'CCC-', 'C+''C', 'C-', 'D']

    df = pd.read_csv("Clean_Data.csv", index_col=0)
    df.head()

    bar_grafica('Frecuencia y número de observaciones por rating sobre datos definitivos',
                All_rating_order,
                df)

    for per in [0, 0.001, 0.02, 0.09]:
        df_mod = clean_df(df, df.columns, per)
