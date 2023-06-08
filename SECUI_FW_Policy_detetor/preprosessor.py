import pandas as pd
import numpy as np
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", help="Name of File")
    parser.add_argument("-t", "--type", dest="type", help="Type of File, b for BLUEMAX, m for MF2")
    options = parser.parse_args()
    if not options.name:
        parser.error("[-] Please specify name of the file")
    return options

def parse_column(df):
    # set first row to column
    df = df.set_axis(df.iloc[0], axis=1)
    df = df.drop(labels=0, axis=0)

    #  make new column values
    first_col_name = df.columns
    second_col_name = df.iloc[0]

    # merge two different row for formulating column
    columns = []
    criterion = ""
    for e in zip(first_col_name, second_col_name):
        e_0 = str(e[0])
        e_1 = str(e[1])
        
        if (e_0 != "nan") and (e_1 != "nan"):
            criterion = e_0
            columns.append(f"{criterion}_{e_1}")
        elif e_1 == "nan":
            columns.append(e_0)
        elif e_0 == "nan":
            columns.append(f"{criterion}_{e_1}")

    # set columns again
    df = df.set_axis(columns, axis='columns').reset_index(drop=True).drop(labels=0, axis=0)

    needed_col = ["Rule Number", "Action", "From_IP,Domain", "To_IP,Domain", "Service_Protocol", "Service_Service Port"]
    renamed_needed_col = ["Rule", "Action", "From", "To", "Protocol", "Port"]

    map_dic = dict(zip(needed_col, renamed_needed_col))

    df = df[needed_col].reset_index(drop=True)
    df = df.rename(columns = map_dic)

    #print(df.sample(10))

    return df

def parse_column_mf(df):
    df = df.set_axis(df.iloc[1], axis=1)
    df = df.drop(index=[0, 1, 3, 4], axis=0)

    #  make new column values
    first_col_name = df.columns
    second_col_name = df.iloc[0]

    # merge two different row for formulating column
    columns = []
    criterion = ""
    for e in zip(first_col_name, second_col_name):
        e_0 = str(e[0])
        e_1 = str(e[1])
        
        if (e_0 != "nan") and (e_1 != "nan"):
            criterion = e_0
            columns.append(f"{criterion}_{e_1}")
        elif e_1 == "nan":
            columns.append(e_0)
        elif e_0 == "nan":
            columns.append(f"{criterion}_{e_1}")

    # set columns again
    df = df.set_axis(columns, axis='columns').reset_index(drop=True).drop(labels=0, axis=0)

    needed_col = ["Seq", "Action", "From_IP", "To_IP", "Service_Service OBJ Name"]
    renamed_needed_col = ["Rule", "Action", "From", "To", "PP"]

    map_dic = dict(zip(needed_col, renamed_needed_col))

    df = df[needed_col].reset_index(drop=True)
    df = df.rename(columns = map_dic)

    return df

def pad_rule(df):
    pad_num = 0
    for i, row in enumerate(df["Rule"]):
        row = str(row)
        if row != "nan":
            pad_num = row
        else :
            df.loc[i, "Rule"] = pad_num

    return df

def aggregate_column(df):
    # parse protocl - port mapping
    if 'PP' not in df.columns:
        df['PP'] = df['Protocol']+df['Port']
        df = df.drop(['Protocol', 'Port'], axis=1)

    # aggregate for rule id
    #print(df.groupby('Rule')['From'].apply(lambda x: x))
    gdf_from = df.groupby('Rule')['From'].apply(lambda x: ', '.join(map(str, x)))
    gdf_to = df.groupby('Rule')['To'].apply(lambda x: ', '.join(map(str, x)))
    gdf_pp = df.groupby('Rule')['PP'].apply(lambda x: ', '.join(map(str, x)))

    from_n_to = pd.merge(gdf_from, gdf_to, on='Rule', how='inner').reset_index()
    merged = pd.merge(from_n_to, gdf_pp, on='Rule', how='inner')

    merged['Rule'] = from_n_to['Rule'].astype(int)

    mdf = merged.sort_values('Rule').reset_index(drop=True)
    #print(mdf)

    return mdf

def clean_nan(df):
    
    target = ["From", "To", "PP"]

    for col in target:
        for idx, row in enumerate(df[col]):
            arr = row.split(', ')
            if "nan" in arr:
                arr = list(set(arr)) #dedup nan
                arr.remove("nan")
                converted_row = ", ".join(arr)
                df.loc[idx, col] = converted_row
    
    return df

if __name__ == '__main__' :

    options = get_arguments()
    nof = options.name
    nof_PREPROCESSED = "PREPROCESSED_"+nof
    t = options.type
    print(f"[+] Name of File is {nof}")

    df = pd.read_csv(f"./{nof}", encoding='utf-8')

    if t == "b": # bluemax
        # parse column
        df = parse_column(df)
        # aggregate column
        df = aggregate_column(df)
        # clean nan
        df = clean_nan(df)
    elif t == "m": # mf2
        df = parse_column_mf(df)
        df = pad_rule(df)
        df = aggregate_column(df)
        df = clean_nan(df)
    else:
        print("[!] Type error")
        exit()


    print(df)
    df.to_csv(f"./{nof_PREPROCESSED}", encoding='utf-8')
    print(f"[+] File is successfully preprocessed")