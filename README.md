# Shimadzu-HPLC-raw-data-splitter
This script allows you to split and organize the raw data file (.txt) exported by Shimadzu LC Solution software. Scroll below for English

---

### 用途
島津ソリューションから吐き出された HPLC-PDA-MS の raw ファイルを解体して、MS、PDAのそれぞれのクロマトグラムファイルを txt 形式で保存

### 使い方
1. スクリプトたちを丸ごとダウンロード
2. input フォルダの中に、島津ソリューションから吐き出した raw ファイル (.txt) を入れる。
3. フォルダをターミナルで開き、以下を入力
```python
$ python hplc_split.py
```
4. output フォルダに解体された txt ファイルがある

### ファイルたち

|- readme.md  
|- hplc_split.py -- 実行ファイル  
|- input / -- raw file をいれる場所  
|- output / -- split されたファイルが保存される場所（なければ自動的に作成される）  
|  |- files /  
|  |- mz_abs /  
|  |- mz_rel /  


### 注意など
* raw ファイル名は短めな方が良い。全ての split txt の prefix になる
* ms クロマトグラムデータポイントが多すぎるので1/3くらいにポイントをカットするようにした

---

## How to use
1. Download all the files and put your raw data file (txt) in the "raw" folder. You can put more than 1 files.
2. Go to your parent folder (hplc_split) in the Terminal. Run the script:
```python
$ python hplc_split.py
```
3. You will get your split files (.txt) inside the "output" folder

### Notes
* Using a short name for the raw file txt is recommended because will become the prefix of all split files
* This script also cuts down the MS chromatogram data into 1/3 because it was too big
