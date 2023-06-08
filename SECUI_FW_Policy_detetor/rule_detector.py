import pandas as pd
import re
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", help="Name of File")
    options = parser.parse_args()
    if not options.name:
        parser.error("[-] Please specify name of the file")
    return options

# regex
def decompose_ip_address_type(ip_address):
    # Regex pattern for IPv4 address
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}'

    if re.match(ipv4_pattern, ip_address):
        # Extract the first three octets of IPv4 address
        octets = ip_address.split('.')
        first_three_octets = '.'.join(octets[:3])
        return first_three_octets
    else:
        return 'Unknown'

# Global variable
UNUSED_NET = [
    # IP should be confidential
    1.1.1.1
]


if __name__ == '__main__' :

    options = get_arguments()
    nof = options.name
    nof_FINAL = "FINAL_"+nof
    print(f"[+] Name of File is {nof}")

    df = pd.read_csv(f"./{nof}", encoding='utf-8', index_col=0)
    df['Unused'] = False
    df['Reason'] = "None"

    for i, row in enumerate(df['From']):
        row = str(row)
        for element in row.split(', '):
            for net in UNUSED_NET:
                # element decomposition
                three_octets = decompose_ip_address_type(element) 
                #print(three_octets)
                if three_octets == net:
                    print(f"Match : {df.iloc[i, 0]}") 
                    df.iloc[i, 4] = True
                    if df.iloc[i, 5] != "None":
                        arr = df.iloc[i, 5]
                        narr = arr.split(',')
                        narr.append(net)
                        print(list(set(narr)))
                        df.iloc[i, 5] = ",".join(list(set(narr)))
                    else : df.iloc[i, 5] = net
    
    # Trim for False
    df = df.drop(index=df[df['Unused']==False].index.tolist(), axis=0)
    df = df.drop(["Unused"], axis = 1).reset_index(drop=True)

    df.to_csv(f"./{nof_FINAL}", encoding='utf-8')