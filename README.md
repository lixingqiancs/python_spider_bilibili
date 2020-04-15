# python_spider_bilibili

## usage

### example for request data

```bash
cd Bilibili 

python bilibiliComments.py -h

python bilibiliComments.py

** or **

python bilibiliComments.py -i "the oid of your want to request" -o "your result file name"
```

usage: bilibiliComments.py [-h] [-i OID] [-o CSV_OUT]

Bilibili comments spider

optional arguments:
  -h, --help  show this help message and exit
  -i OID      Bilibili oid
  -o CSV_OUT  csv format file out name
