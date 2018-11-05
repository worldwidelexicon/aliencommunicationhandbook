from PIL import Image, ImageDraw
import json
import math
import os
import random
from shutil import copyfile
import string

words = ['moon', 'planet', 'ring', 'crater', 'water', 'ocean', 'ice']
codes = list()

def load_metadata():
    f = open('metadata.json','r')
    text = f.read()
    metadata = json.loads(text)
    return metadata
    
def generate_metadata():
    md = dict()
    for w in words:
        code = ''
        pos = 0
        while pos < 16:
            code += str(random.randint(0,1))
            pos += 1
        if code not in codes:
            codes.append(code)
            md[w] = code
    text = json.dumps(md)
    f = open('metadata.json', 'wc')
    f.write(text)
    f.close()
            
def apply_metadata(filename, words, tile_size=5, offset=49):
    metadata = load_metadata()
    
    f = Image.open(filename)
    im = f.copy()
    im.convert('L')
    width = im.size[0]
    height = im.size[1]
    
    out = Image.new('L', (width, height))
    out.paste(im)
    x = 0
    y = 0
    
    draw = ImageDraw.Draw(out)
    
    for w in words:
        x = 0
        code = '1010' + metadata.get(w, None) + '0101'
        if code is not None:
            for c in code:
                if c == '0':
                    v = 0
                else:
                    v = 255
                draw.rectangle([((x * tile_size) + offset, (y * tile_size) + offset),((x * tile_size) + tile_size + offset, (y * tile_size) + tile_size + offset)], v)
                print 'Writing to pixel ' +str(x) + ' ' + str(y) + ' ' + str(v)
                x += 1
        y += 1
    out.save('metapix/' + filename)
    
def process_photos():
    cwd = os.getcwd()
    print cwd
    fileList = os.listdir(cwd)
    for f in fileList:
        if string.count(f, '.jpg') > 0 or string.count(f, 'png') > 0:
            print f
            to_bitstream(f, outfile = 'bitstreams/' + f)
        
def to_bin(v, length=8):
    v = v + int(math.pow(2,length))
    return string.replace(bin(v),'0b1','')

def to_bitstream(filename, outfile = None, threshold=10, lines_before=0, lines_after=0):
    im = Image.open(filename)
    im = im.convert('L')
    width = im.size[0]
    height = im.size[1]
    out = Image.new('1',(width*8,height+lines_before+lines_after))
    y = 0
    while y < height:
        x = 0
        while x < width:
            v = im.getpixel((x,y))
            if v < threshold:
                v = 0
            b = to_bin(v)
            p = 0
            while p < 8:
                out.putpixel(((x*8)+p,y+lines_before),int(b[p]))
                p = p + 1
            x = x + 1
        y = y + 1
    y = 0
    while y < lines_before:
        x = 0
        while x < width * 8:
            out.putpixel((x,y),random.randint(0,1))
            out.putpixel((x,y+lines_before+height),random.randint(0,1))
            x = x + 1
        y = y + 1
    if outfile is None:
        out.save(filename + 'bits.png')
    else:
        outfile = string.replace(outfile, '.jpg', '.png')
        out.save(outfile)