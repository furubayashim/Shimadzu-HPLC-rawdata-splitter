#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2018/12/13

import re
import os
import sys
import glob
import numpy as np
import shutil

def split_lc(rawfile_path,rawfile_name,opfolder):
    """Split the LC file and save into .txt, return the splitted filename list
    LC raw ファイルを開いて、splitして、別々のtxtファイルに保存
    """
    print("Splitting txt file...")

    splitted_files = []    # empty list to record the new file names
    for fpath,fname in zip(rawfile_path,rawfile_name):    # open the file, store in "content"
        try:
            with open(fpath, 'r',encoding='mac_roman') as f:
                state = 'stop'   # もう write/stop 使ってないので、state いらないかも
                i = 0
                content = f.readlines() # ここにいれなくても、for line in f でいいのでは
                for line in content:
                    if re.match(r'^\[(.+)',line):
                        state = 'write'
                        i+=1
                        newsplitfname = opfolder+"/files/{}/{}-{}-{}.txt".format(fname,fname,i,line[1:-2])
                        splitted_files.append(newsplitfname)
                        f2 = open(newsplitfname,'w')
                        f2.write(line)
                    elif state == 'write':
                        f2.write(line)
                    #else:
        except:
            with open(fpath, 'r',encoding='UTF-8') as f:
                state = 'stop'
                i = 0
                content = f.readlines()
                for line in content:
                    if re.match(r'^\[(.+)',line):
                        state = 'write'
                        i+=1
                        newsplitfname = opfolder+"/files/{}/{}-{}-{}.txt".format(fname,fname,i,line[1:-2])
                        splitted_files.append(newsplitfname)
                        f2 = open(newsplitfname,'w')
                        f2.write(line)
                    elif state == 'write':
                        f2.write(line)
                    #else:
        #f2.close()
        f.closed    # maybe I should write f.closed since I'm using the with statement?
    print("Done")
    return splitted_files # but I don't use this anywhere

def rewrite_MS_filename(rawfile_name):
    """Rename the MS file name from "MS Chromatogram.txt" into "(m/z).txt" and put it into mz folder
    """
    print("Rewriting mz filename...")

    # rename MS filename by its m/z.
    # open file, read the 2nd row (where m/z is written) and make that into the filename
    newfname = []
    replacename = ''
    for folder in rawfile_name:
        msfiles = [os.path.basename(path) for path in sorted(glob.glob(opfolder+"/files/"+folder+"/*-MS Chromatogram.txt"))]
        for fname in msfiles:    # MS chromatogram files のファイル名を mzに書き換える。そのファイル名リストをnewfnameに入れる
            filepath = opfolder+"/files/{}/{}".format(folder,fname)
            with open(filepath, 'r') as f:
                for i, line in enumerate(f):
                    if i == 2: break
                    if i == 1:    # read 2nd row, where the m/z are written
                        if isfloat(line[-8:-2].strip()):
                            replacename = '{}-{}'.format(folder,line[-8:-2].strip())
                            newfname.append("{}/{}.txt".format(folder,replacename))
                        elif re.search(r'1-1MS',line) :
                            replacename = '{}-{}-1'.format(folder,line[-5:].strip())
                            newfname.append("{}/{}.txt".format(folder,replacename))
                        elif re.search(r'1-2MS',line) :
                            replacename = '{}-{}-2'.format(folder,line[-5:].strip())
                            newfname.append("{}/{}.txt".format(folder,replacename))
            f.close()
            os.rename(filepath,opfolder+"/mz/{}/{}.txt".format(folder,replacename))
    print("Done")
    return newfname

def get_abs_rel_intensity(mz_files):
    """Absolute intensity & Relative intensity わける
    """
    print("Separating abs/rel itensity...")
    for fname in set(mz_files):
        data = np.loadtxt(opfolder+'/mz/'+fname,skiprows=7)
        data = data.astype(float)
        data_abs = np.delete(data,2,1)
        data_rel = np.delete(data,1,1)

        with open(opfolder+'/mz_abs/'+fname,'w') as f_abs:
            for lines in data_abs:
                lines = np.array_str(lines)
                f_abs.write(lines[1:-1]+'\n')
        f_abs.close()
        with open(opfolder+'/mz_rel/'+fname,'w') as f_rel:
            for lines in data_rel:
                lines = np.array_str(lines)
                f_rel.write(lines[1:-1]+'\n')
        f_rel.close()
    #    try:
    #    except IndexError:
    #        pass
    print("Done")

def cut_MS_data(mz_files,num):
    """ms data point が多すぎるので、与えた数字でカット。
    """
    print("Cutting mz data by {}...".format(num))

    for type in ('abs','rel'):
        for fname in mz_files:
            filepath = opfolder+"/mz_{}/{}".format(type,fname)
            data = np.loadtxt(filepath,skiprows=0)

            f2 = open(filepath,"w")
            count = 0
            for lines in data:
                if count % num == 0:
                    # print(lines)
                    f2.write(np.array_str(lines)[1:-1]+'\n')
                count+=1
            f2.close()
    print("Done")


def delete_mz_folder():
    """mzフォルダごと消す。
    """
    try:
        shutil.rmtree(opfolder+"/mz")
        #print("Deleted mz folder...")
    except OSError as e:
        print ("Error: {} - {}.".format(e.filename, e.strerror))

def create_folder(folders_to_create=[]):
    """Make new folders if they don't exist
    """
    for f in folders_to_create:
        if not os.path.exists(f):
            os.makedirs(f)

def obtain_filename(folder):
    """Obtain the filename in the given folder and return in list
    """
    fname_list = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if '.DS_Store' in fname_list: fname_list.remove('.DS_Store')
    fname_list.sort()
    return fname_list

def obtain_dirname(folder):
    """Obtain the folder name in the given folder and return in list
    """
    dirname_list = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    fname_list.sort()
    return dirname_list

def isfloat(string):
    try:
        float(string)
        return True
    except:
        return False

### Ongoing
# Want to make "selected-mz folder". pick the selected mz files.


if __name__ == "__main__":

    # obtain filename in the ipfolder
    ipfolder = sys.argv[1]
    rawfile_path = sorted(glob.glob(ipfolder+"/*.txt"))
    rawfile_name = [os.path.basename(path)[:-4] for path in rawfile_path]

    # create empty folders to store files (mz, pda, etc...)
    opfolder = ipfolder + '-output'
    folders1 = [opfolder,opfolder+'/files',opfolder+'/mz']
    folders2 = [opfolder+"/files/"+fname for fname in rawfile_name]
    folders3 = [opfolder+"/mz/"+fname for fname in rawfile_name]
    folders4 = [opfolder+'/mz_abs',opfolder+'/mz_rel'] + [opfolder+'/mz_abs/'+ f for f in rawfile_name] + [opfolder+'/mz_rel/'+ f for f in rawfile_name]
    create_folder(folders1+folders2+folders3+folders4)

    # Split HPLC file and store in ./split folder
    split_lc(rawfile_path,rawfile_name,opfolder)

    # Organize MS Chromatogram file
    mz_files = rewrite_MS_filename(rawfile_name)    # rename the MS Chromatogram filename to m/z, store in ./mz/ folder and return the filename
    get_abs_rel_intensity(mz_files)    # get only abs intensity
    cut_MS_data(mz_files,3)    # cut down MS Chromatogram data
    delete_mz_folder()    # delete mz folder

    print("Finished")
