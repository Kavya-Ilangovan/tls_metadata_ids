import pandas as pd

def load_zeek_log(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    headers = []
    for line in lines:
        if line.startswith('#fields'):
            headers = line.strip().split('\t')[1:]
            break

    data_lines = [line for line in lines if not line.startswith('#')]
    df = pd.DataFrame([line.strip().split('\t') for line in data_lines], columns=headers)
    return df

# Load logs
ssl_df = load_zeek_log('ssl.log')
conn_df = load_zeek_log('conn.log')

# Filter relevant fields (no ja3s)
ssl_df = ssl_df[['uid', 'id.orig_h', 'id.resp_h', 'version', 'cipher', 'server_name', 'ja3']]
conn_df = conn_df[['uid', 'duration', 'orig_bytes', 'resp_bytes']]

# Merge
merged_df = pd.merge(ssl_df, conn_df, on='uid', how='left')

# Save
merged_df.to_csv('tls_sessions.csv', index=False)
print(f"✅ Saved tls_sessions.csv with {len(merged_df)} records.")
