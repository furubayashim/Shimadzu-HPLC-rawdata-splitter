# -*- coding: utf-8 -*-
import re # regular expressions
import os
import numpy as np
import shutil

def split_lc(files):
    """Split the LC file and save into .txt, return the splitted filename list
    LC raw ファイルを開いて、splitして、別々のtxtファイルに保存
    """
    create_folder(["output/files/"+fname[:-4] for fname in files])

    splitted_files = []    # empty list to record the new file names
    for fname in files:    # open the file, store in "content"
        try:
            with open('input/'+fname, 'r',encoding='mac_roman') as f:
                state = 'stop'   # もう write/stop 使ってないので、state いらないかも
                i = 0
                content = f.readlines() # ここにいれなくても、for line in f でいいのでは
                for line in content:
                    if re.match(r'^\[(.+)',line):
                        state = 'write'
                        i+=1
                        newsplitfname =  "output/files/{}/{}-{}-{}.txt".format(fname[:-4],fname[:-4],i,line[1:-2])
                        splitted_files.append(newsplitfname)
                        f2 = open(newsplitfname,'w')
                        f2.write(line)
                    elif state == 'write':
                        f2.write(line)
                    #else:
        except:
            with open('input/'+fname, 'r',encoding='UTF-8') as f:
                state = 'stop'
                i = 0
                content = f.readlines()
                for line in content:
                    if re.match(r'^\[(.+)',line):
                        state = 'write'
                        i+=1
                        newsplitfname =  "output/files/{}/{}-{}-{}.txt".format(fname[:-4],fname[:-4],i,line[1:-2])
                        splitted_files.append(newsplitfname)
                        f2 = open(newsplitfname,'w')
                        f2.write(line)
                    elif state == 'write':
                        f2.write(line)
                    #else:
        #f2.close()
        f.closed    # maybe I should write f.closed since I'm using the with statement?
    print("Done splitting file...")
    return splitted_files # but I don't use this anywhere

def rewrite_MS_filename(files):
    """Rename the MS file name from "MS Chromatogram.txt" into "(m/z).txt" and put it into mz folder
    """

    # Make imaginary file name "n-MS Chromatogram.txt" and return
    msfilename_list = [str(n)+"-MS Chromatogram.txt" for n in range(6,133)] # 1-6 is

    # make folder name list
    foldername_list = [fname[:-4] for fname in files]

    #foldername_list.remove('.DS_Store')
    for fname in foldername_list:
        if not os.path.exists("output/mz/"+fname):
            os.makedirs("output/mz/"+fname)

    # rename MS filename by its m/z.
    # open file, read the 2nd row (where m/z is written) and make that into the filename
    newfname = []
    replacename = ''
    for folder in foldername_list:
        for fname in msfilename_list:    # MS chromatogram files のファイル名を mzに書き換える。そのファイル名リストをnewfnameに入れる
            filepath = "output/files/{}/{}-{}".format(folder,folder,fname)
            if os.path.exists(filepath):
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
                os.rename(filepath,"output/mz/{}/{}.txt".format(folder,replacename))
            else:
                pass
    print("Done rewriting mz filename...")
    return newfname

def get_abs_rel_intensity(raw_files,mzname_list):
    """Absolute intensity & Relative intensity わける
    """
    create_folder(['output/mz_abs','output/mz_rel'] + ['output/mz_abs/'+ f[:-4] for f in raw_files] + ['output/mz_rel/'+ f[:-4] for f in raw_files])

    for fname in set(mzname_list):
        data = np.loadtxt('output/mz/'+fname,skiprows=7)
        data = data.astype(float)
        data_abs = np.delete(data,2,1)
        data_rel = np.delete(data,1,1)

        with open('output/mz_abs/'+fname,'w') as f_abs:
            for lines in data_abs:
                lines = np.array_str(lines)
                f_abs.write(lines[1:-1]+'\n')
        f_abs.close()
        with open('output/mz_rel/'+fname,'w') as f_rel:
            for lines in data_rel:
                lines = np.array_str(lines)
                f_rel.write(lines[1:-1]+'\n')
        f_rel.close()
    print("Got abs/rel itensity...")
    #    try:
    #    except IndexError:
    #        pass


def cut_MS_data(mzname_list,num):
    """ms data point が多すぎるので、カット。
    """
    for type in ('abs','rel'):
        for fname in mzname_list:
            filepath = "output/mz_{}/{}".format(type,fname)
            data = np.loadtxt(filepath,skiprows=0)

            f2 = open(filepath,"w")
            count = 0
            for lines in data:
                if count % num == 0:
                    # print(lines)
                    f2.write(np.array_str(lines)[1:-1]+'\n')
                count+=1
            f2.close()
    print("Done cutting mz file...")


def delete_mz_folder():
    """mzフォルダごと消す。
    """
    try:
        shutil.rmtree("output/mz")
        print("Deleted mz folder...")
    except OSError as e:
        print ("Error: {} - {}.".format(e.filename, e.strerror))

def create_folder(additional_folders=[]):
    """Make new folders if they don't exist
    """
    basic_folders = []
    for f in basic_folders + additional_folders:
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
    # create empty folders to store files (mz, pda, etc...)
    create_folder(['output','output/files','output/mz'])

    # obtain filename in the ./raw folder
    raw_files = obtain_filename('./input')

    # Split HPLC file and store in ./split folder
    split_lc(raw_files)

    # Organize MS Chromatogram file
    mz_files = rewrite_MS_filename(raw_files)    # rename the MS Chromatogram filename to m/z, store in ./mz/ folder and return the filename
    get_abs_rel_intensity(raw_files,mz_files)    # get only abs intensity
    cut_MS_data(mz_files,3)    # cut down MS Chromatogram data
    delete_mz_folder()    # delete mz folder

    print("Finished")
