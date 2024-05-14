import numpy as np
import os
from glob import glob
from tqdm import tqdm
import pandas as pd

text_root = './texts/'
data_root = '../data/'
os.makedirs(data_root, exist_ok=True)

paths = sorted(glob(f'{text_root}/*/*.txt'))
print(f'Found {len(paths)} multiline texts')

n = len(paths)

outpath = f'{data_root}/kowikitext_20240501.csv'
inpaths = dict(zip(range(n), paths))

def to_csv(outpath, inpaths):
    _dict = {}
    for i, inpath in tqdm(inpaths.items(), desc='to_csv', total=len(inpaths)):
        with open(inpath, encoding='utf-8') as f:
            inputs = f.read()
            inputs = inputs.rstrip('\n')
        _dict[i] = {'text': inputs}
    pd.DataFrame.from_dict(_dict, orient='index').dropna().to_csv(outpath, index=False)

to_csv(outpath, inpaths)
print(f'saved at {outpath} ({len(inpaths)} files)')