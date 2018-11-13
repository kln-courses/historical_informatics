"""
store slices of clean Saxo in data frame an add class information and early/late
"""

import glob, os, re
from natsort import natsorted
import pandas as pd

def clearstr(text):
    nachars = [r"\。",r"\@",r"\#",r'\d']
    for nachar in nachars:
        text = re.sub(nachar,"",text)
    return text

fnames = natsorted(glob.glob("*.txt"))
titles = [os.path.basename(fname).split(".")[0] for fname in fnames]

n = 250
eta = 1
pat = re.compile(r"\W+")
db = list()
for i, fname in enumerate(fnames):# threshold for speed
    with open(fname,"r") as f:
        text = f.read()
        text = clearstr(text.lower())
        tokens = pat.split(text)
        tokens = [token for token in tokens if len(token) > eta]
        slices = list()
        flag = 0
        for ii in range(0,len(tokens),n):
            slice = tokens[ii:(ii+n)]
            slices.append(slice)
            flag += 1
        db.append([" ".join(slice) for slice in slices])

class_book, class_slice, data = list(), list(), list()
book_flag = 1
for i, book in enumerate(db):
    for ii, slice in enumerate(book):
        data.append(slice)
        class_book.append(i + 1)
        class_slice.append(ii)

class_data = list()
for i in class_book:
    if i <= 8:
        class_data.append("early")
    elif i == 9:
        class_data.append("uncertain")
    elif i > 9:
        class_data.append("late")

df = pd.DataFrame()
df["book"] = class_book
df["book_class"] = class_data
df["slice_id"] = class_slice
df["content"] = data

df.to_csv("saxo_class.csv",index=False)
