# Shimadzu-HPLC-raw-data-splitter
This script allows you to split and organize the raw data file (.txt) exported by Shimadzu LC Solution software. 日本語は下記
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
