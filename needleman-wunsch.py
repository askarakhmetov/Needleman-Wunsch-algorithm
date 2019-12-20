from __future__ import print_function, division
import numpy as np
import random
import time

pt = {'match': 1, 'mismatch': -1, 'gap': -1}

def rp(x):
    return {
        1: 'A',
        2: 'C',
        3: 'G',
    }.get(x, 'T') 

def nw_generator(a,b,n,m):
    p=1
    o=1
    while p!=n:
        a.append(rp(random.randint(0, 3)))
        p=p+1
    while o!=m:
        b.append(rp(random.randint(0, 3)))
        o=o+1

def mch(alpha, beta):
    if alpha == beta:
        return pt['match']
    elif alpha == '-' or beta == '-':
        return pt['gap']
    else:
        return pt['mismatch']

def needle(s1, s2):
    m, n = len(s1), len(s2)
    score = np.zeros((m+1, n+1))
    
    #Initialization
    for i in range(m+1):
        score[i][0] = pt['gap'] * i
    for j in range(n+1):
        score[0][j] = pt['gap'] * j
    
    #Fill
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diag = score[i-1][j-1] + mch(s1[i-1], s2[j-1])
            delete = score[i-1][j] + pt['gap']
            insert = score[i][j-1] + pt['gap']
            score[i][j] = max(diag, delete, insert)

    #print('score matrix = \n%s\n' % score)
    align1, align2 = '', ''
    i,j = m,n
    
    #Traceback
    while i > 0 and j > 0:
        score_current = score[i][j]
        score_diag = score[i-1][j-1]
        score_left = score[i][j-1]
        score_up = score[i-1][j]
        
        #print('score_current: ',score_current)
        #print('score_diag: ',score_diag)
        #print('score_left: ',score_left)
        #print('score_up: ',score_up)

        if score_current == score_diag + mch(s1[i-1], s2[j-1]):
        #    print('diag')
            a1,a2 = s1[i-1],s2[j-1]
            i,j = i-1,j-1
        elif score_current == score_up + pt['gap']:
        #    print('up')
            a1,a2 = s1[i-1],'-'
            i -= 1
        elif score_current == score_left + pt['gap']:
        #    print('left')
            a1,a2 = '-',s2[j-1]
            j -= 1
        #print('%s ---> a1 = %s\t a2 = %s\n' % ('Add',a1,a2))
        align1 += a1
        align2 += a2
            

    while i > 0:
        a1,a2 = s1[i-1],'-'
        #print('%s ---> a1 = %s\t a2 = %s\n' % ('Add',a1,a2))
        align1 += a1
        align2 += a2
        i -= 1
        
    while j > 0:
        a1,a2 = '-',s2[j-1]
       # print('%s --> a1 = %s\t a2 = %s\n' % ('Add',a1,a2))
        align1 += a1
        align2 += a2
        j -= 1
    
    align1 = align1[::-1]
    align2 = align2[::-1]
    seqN = len(align1)
    sym = ''
    seq_score = 0
    ident = 0
    for i in range(seqN):
        a1 = align1[i]
        a2 = align2[i]
        if a1 == a2:
            sym += a1
            ident += 1
            seq_score += mch(a1, a2)
    
        else: 
            seq_score += mch(a1, a2)
            sym += ' '
        
    ident = ident/seqN * 100
    
    #print('Identity = %2.1f percent' % ident)
    #print('Score = %d\n'% seq_score) 
    #print(align1)
    #print(sym)
    #print(align2)

a = []
b = []

n = [10, 100, 1000, 10000]
m = [10, 100, 1000, 10000]

for i in range(0,4):
    for j in range(0,4):
        a = []
        b = []
        print("n = "+str(n[i])+" and m = "+str(m[j]))
        nw_generator(a,b,n[i],m[j])
        #time measurement
        time_cnt=0
        cnt = 0
        while cnt<10:
            stt = time.time()
            needle(a, b)
            time_cnt = time_cnt + (time.time() - stt)
            cnt=cnt+1
        print(" ",str(time_cnt/10),"seconds ")
