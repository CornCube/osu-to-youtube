# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 12:50:07 2022

@author: Corn Cube
"""

import os
import urllib.request
import re
import webbrowser
from tqdm import tqdm                                               # progress bar

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

outputfile = "osusongs.txt"                                         # file to save the results to
folder = input("Enter the full path to your osu! song folder: ")    # the folder to inventory (replace with your "Songs path")
exclude	= ['.osu','.tmp', '.jpg', '.mp3', '.wav', '.png', '.osb']	# exclude files containing these strings
pathsep	= "\\"                                             		 	# path seperator ('/' for linux, '\' for Windows)

with open(outputfile, "w") as txtfile:
    for path,dirs,files in walklevel(folder, 1):
        split = path.split(pathsep)
        sep = split[len(path.split(pathsep))-1]
        sep = sep[7:]                                               # remove "Songs/"
        sep = sep.lstrip("0123456789 ")                             # remove number id
        print(sep)
        txtfile.write("%s\n" % sep)

txtfile.close()

playlistids = ""
count = 0
with open(outputfile, "r") as file:
    next(file)                                                      # skip first line
    for line in tqdm(file):
        line = line.replace('[no video]', '')
        line = line.replace('(TV Size)', '')
        line = line.replace(' ', '')                                # strip spaces from query
        line = re.sub('[^A-Za-z0-9-&]+', '', line)                  # strip special chars
        line = line.lstrip("-")
        search_keyword = line
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        playlistids = playlistids + video_ids[0] + ","
        count += 1
        print("https://www.youtube.com/watch?v=" + video_ids[0])    # individual links
        if (count % 50 == 0):
            webbrowser.open("https://www.youtube.com/watch_videos?video_ids=" + playlistids)
            playlistids = ""

playlistids = playlistids.rstrip(",")
webbrowser.open("https://www.youtube.com/watch_videos?video_ids=" + playlistids)