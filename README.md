[![Build Status](https://travis-ci.org/PPACI/yast.svg?branch=master)](https://travis-ci.org/PPACI/yast)
# Yast
Yet Another Sequence Transcoder - transcode sequences to vector of vectors in python !

## Why Yast ?
Yast enable you to transcode **any** sequence which can be represented by **string**
to be encoded into a **list of word-vector** representation.

When searching over a tool to encode a sentence as a list of word-vector, it was clear that there was no
simple tool to use. And so, i decided to create Yast.

Note : If you only want to get the word-vector of a word, or average of word-vector in sentence,
you should probably better check [Spacy](https://github.com/explosion/spaCy).

## Requirements
Yast requirements are :
* [numpy](https://github.com/numpy/numpy)
* [tqdm](https://github.com/tqdm/tqdm)

## Mapping file
The mapping should be a columnar file like :
```
<token> <vector value>
token1 0.1 0.6 -1.2
token2 0.6 -2.3 3.4
```

All data should be separated by space, thus no space is allowed in token.
You should be able to directly use [Facebook Fast Text pretrained word vector](https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md) as mapping.

## Input file
Input file should be a list of text, with one sample per line.
```
hello world
Yast is awesome !
```
The default separator is a space " " but any regular expression can be provided.

**Note that Yast is case insensitive**

## How to use
1) Clone Yast
2) Install dependencies with `pip install -r requirements.txt`
3) Use Yast !

```
>> python main.py -h
usage: main.py [-h] --input input.txt --output output.txt --mapping
               mapping.vec --separator \ |\.|\,

Yet Another Sequence Translator

optional arguments:
  -h, --help            show this help message and exit
  --input input.txt     Path to file to transcode
  --output output.txt   Path to output file
  --mapping mapping.vec
                        Path to mapping file
  --separator \ |\.|\,  regular expression used to split the input sequence

```

If you wanted to use the english word vector for an input file like previously described :
```
python main.py --input "input.txt" --output "output.csv" --mapping "wiki.en.vec" 
```

## Output format
The idea behind yast is to be as easy as possible to integrate it in all data science processing.

Yast output it's your data as **CSV**.

The only problem with CSV is that it's difficult to integrate multi-dimensional array. So we had to find a compromise..

Yast encode the vector columns in JSON format, which is easily readable and is very similar to python array representation.

The output file will be similar to :

|inputs|vectors|
|:----:|:-----:|
|hello world|[[1,1,1],[2,2,2]]
|yast is awesome !|[[3,3,3],[4,4,4]]|

## How to load a yast output ?

As said previously, the choice made with Yast make it possible to use it as simply as :

```python
import pandas, json

csv = pandas.read_csv("output.csv")
csv.vectors = csv.vectors.apply(json.loads)

csv.head()
```

Note that [Pandas](https://github.com/pandas-dev/pandas) is not mandatory but very recommended for data science.

## TODO

* Optimize Mapping loading time
* Optional argument to output fixed size vectors for all input sequences
* Surely lot of thing !

## Can i contribute ?

Off course ! If you want to improve Yast, your idea / pull requests / issues are welcomed !