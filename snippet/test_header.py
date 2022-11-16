import pandas as pd

csvfile = 'dcp_test_001_KT_202203111830_202203151830.zip'
df = pd.read_csv(csvfile)
for header in df.columns:
    print(header)