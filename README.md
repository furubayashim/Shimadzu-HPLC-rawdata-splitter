# Shimadzu-HPLC-raw-data-splitter
This script allows you to split and organize the raw data file (.txt) exported by Shimadzu LC Solution software. 日本語は下記

## How to use
Prepare a folder containing the raw files (.txt) and run the script:
```bash
$ python hplc_split.py foldername
```
Then you will get your split files (.txt) inside the `foldername-output` folder.

You can also make `split_hplc.py` executable by simlinking it to `split_hplc` and putting it in your PATH:
```bash
$ chmod +x split_hplc.py
$ ln -s ./split_hplc.py ~/bin/split_hplc
```
Then you can call it as
```bash
$ split_hplc foldername
```
### Notes
* Using a short name for the raw file txt is recommended because will become the prefix of all split files
* This script also cuts down the MS chromatogram data into 1/3 because it was too big

---

### 用途
島津ソリューションから吐き出された HPLC-PDA-MS の raw ファイルを解体して、MS、PDAのそれぞれのクロマトグラムファイルを txt 形式で保存

### 使い方
raw file (.txt) をいれたフォルダを用意して、ターミナルで以下を入力
```bash
$ python hplc_split.py foldername
```
`foldername-output` フォルダの中に解体された txt ファイルが保存される

### 注意など
* raw ファイル名は短めな方が良い。全ての split txt の prefix になる
* ms クロマトグラムデータポイントが多すぎるので1/3にポイントをカットするようにした
