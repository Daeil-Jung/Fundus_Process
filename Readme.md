# Environmnets
`OS : Windows 10 `
`Python version: 3.7`

# requirements
```shell script
pip install -r requirements.txt
```
Fundus image folder or .zip file.

`DBdata.csv` for labels.


# Usage
### pre_train.py

```shell script
python pre_train.py [-h] [-z] [-s] [-r] [-he] foldername
```

````
positional arguments:
  foldername            Target folder name or .zip file's filename(without
                        '.zip')

optional arguments:
  -h, --help            show this help message and exit
  -z, --unzip           Unzip file
  -s, --sharpening      Use when you want to do sharpening filter process
  -r, --reduction_red   make red channel zeros
  -he, --hist_equalize  make histogram equalization
````