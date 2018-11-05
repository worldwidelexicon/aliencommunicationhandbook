import math
import os
import random
import string

def fec_graph():
    # calculate error rate for 3, 5 and 7 NMR codes with range of bit error rates
    # generates a csv file with this data
    
    #
    # First let's generate some test data
    #
    
    nmr_codes = [3, 5, 7]
    test_data = dict()
    corrupted_data = dict()
    reliability = dict()
    for n in nmr_codes:
        data = ''
        pos = 0
        while pos < 100000:
            b = random.randint(0,1)
            ctr = 0
            while ctr < n:
                data += str(b)
                ctr += 1    
            pos += 1
        test_data[n] = data
    
    #
    # Next, let's cycle through a range of bit error rates from 1 to 30%
    #
    
    for n in nmr_codes:
        ber = 0
        while ber <= 30:
            data = test_data[n]
            pos = 0
            bits = 0
            errors = 0
            while (pos * n) < len(data):
                fecbit = data[pos: pos+n]
                errbit = ''
                
                for f in fecbit:
                    if random.randint(0, 100) <= ber:
                        if f == '0':
                            errbit += '1'
                        else:
                            errbit += '0'
                    else:
                        errbit += f
                        
                if string.count(fecbit, '0') > string.count(fecbit, '1'):
                    fec_value = 0
                else:
                    fec_value = 1
                    
                if string.count(errbit, '0') > string.count(errbit, '1'):
                    err_value = 0
                else:
                    err_value = 1
                    
                if fec_value != err_value:
                    conserved = False
                else:
                    conserved = True
                    
                bits += 1
                if conserved == False:
                    errors += 1
                pos += n
                
            cols = reliability.get(n, dict())
            cols[ber] = 1.0 - float(float(errors)/ bits)
            reliability[n] = cols
            ber += 1
    print reliability
    
    fh = open('ber.csv', 'wc')
    fh.write('NMR, 0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.30\n')
    for n in nmr_codes:
        row = str(n) + ','
        cols = reliability.get(n, None)
        if cols is not None:
            ber = 0
            while ber <= 30:
                err_rate = cols.get(ber, 0)
                if ber < 30:
                    row += str(err_rate) + ','
                else:
                    row += str(err_rate)
                print n, ber, 1-err_rate
                ber += 1
        row += '\n'
        fh.write(row)
    fh.close()
