## Scripts for making ko-wikitext

This directory is a modification of the one found in [Lovit's Ko-wikitext repository](https://github.com/lovit/kowikitext/).

First, download and decompress dump data from https://dumps.wikimedia.org/kowiki/20240501/

```bash
cd kowikitext_script
./download.sh 20240501
```

Check `dump_xml_file`, `text_root`, and `DEBUG` in `split_dump_to_wikitext_files.py` and run it.
This script extract plain text from xml-format dump file using [`wikitextparser`](https://pypi.org/project/wikitextparser/).

```
python split_dump_to_wikitext_files.py
```

Snapshot of `text_root`. Redirected pages are removed

```
├── 000
|    ├── ...
|    ├── 97000.txt
|    ├── 98000.txt
|    └── 99000.txt
├── ...
├── 998
└── 999
```

Corpus size
- after removing redirect page: 1147399

Run below script to make train, dev, test dataset. Check `n_train`, `n_dev`, and `n_test` in `to_csv.py`

```
python to_csv.py
```