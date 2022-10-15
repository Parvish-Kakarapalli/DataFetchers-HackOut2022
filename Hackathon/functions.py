from enum import auto
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io

def do_plot(df, f1, f2, classes):


    f, ax = plt.subplots(figsize=(11, 9))

    sns.scatterplot(data = df, x=f1, y=f2, hue=classes, legend = auto)
    
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image


def process(df, label):
  labels = df[label]
  df = df._get_numeric_data()
  columns = df.columns
  means = [df[column].mean() for column in columns]
  for column, mean in zip(columns, means):
    df[column] = df[column].fillna(mean)
  df["labels"] = labels
  print(df)
  return df


def num_cols(df):
    df = df._get_numeric_data()
    columns = df.columns
    means = [df[column].mean() for column in columns]
    for column, mean in zip(columns, means):
        df[column] = df[column].fillna(mean)
    return list(df.columns)

def do_hist(df, feature, classes):


    f, ax = plt.subplots(figsize=(11, 9))

    sns.histplot(data = df, x=feature, hue=classes)
    
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image
