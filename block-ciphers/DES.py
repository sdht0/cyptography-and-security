def hex2bin(shex):
    sbin=""
    shex=shex.lower()
    for c in shex:
        sbin+="{0:04b}".format(ord(c)-ord('a')+10 if c in [chr(ord('a')+x) for x in range(6)] else ord(c)-ord('0'))
    return sbin

def bin2hex(sbin):
    atable=dict()
    for i in range(16):
        atable[i]=chr(ord('0')+i) if i<10 else chr(ord('a')+i-10)
    text=""
    for i in range(0,len(sbin),4):
        text+=atable[int(sbin[i:i+4],2)]
    return text.upper()

def ascii2bin(sascii):
    sbin=""
    for c in sascii:
        sbin+="{0:08b}".format(ord(c))
    return sbin

def bin2ascii(sbin):
    text=""
    for i in range(0,len(sbin),8):
        text+=chr(int(sbin[i:i+8],2))
    return text

def bin2base64(sbin):
    btable=dict()
    for i in range(26):
        btable[i]=chr(ord('A')+i)
        btable[i+26]=chr(ord('a')+i)
    for i in range(10):
        btable[i+52]=chr(ord('0')+i)
    btable[62]='+'
    btable[63]='/'
    text=""
    for i in range(0,len(sbin),6):
        st = sbin[i:i+6]
        if len(st)==2:
            st+="0000"
            text+=btable[int(st,2)]
            text+="=="
        elif len(st)==4:
            st+="00"
            text+=btable[int(st,2)]
            text+="="
        else:
            text+=btable[int(st,2)]
    return text

def xorsum(s1,s2):
    assert len(s1)==len(s2)
    return "".join([str(ord(a)^ord(b)) for a,b in zip(s1,s2)])

def printBinInBlocksOf4(binmsg, pre=""):
    for i in range(0,len(binmsg),4):
        print(binmsg[i:i+4], end=" ")
    if len(pre)!=0:
        print("("+pre+")",end="")
    print()

def applyPermutation(binstring, perTable):
    return "".join([binstring[i-1] for i in perTable])

def DES(M, Key, decrypt = 0):

    msgsize=64
    keysizeorig=64
    keysizeuse=56

    PC1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
    PC2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
    SLS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    IP = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
    IPI = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
    E = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
    S = {0:[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
        1:[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
        2:[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
        3:[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
        4:[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
        5:[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
        6:[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
        7:[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]}
    P = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]

    #printBinInBlocksOf4(Key, "Key")
    if len(Key)!=keysizeorig:
        raise Exception("Wrong key size")
    #printBinInBlocksOf4(M, "Msg")
    if len(M)!=msgsize:
        raise Exception("Wrong msg size")

    #calculate keys
    C={}
    D={}
    K=[]
    KPC1 = applyPermutation(Key, PC1)
    C[0]=KPC1[0:keysizeuse//2]
    D[0]=KPC1[keysizeuse//2:]
    for i in range(1,17):
        C[i]=C[i-1][SLS[i-1]:]+C[i-1][0:SLS[i-1]]
        D[i]=D[i-1][SLS[i-1]:]+D[i-1][0:SLS[i-1]]
        K.append(applyPermutation(C[i]+D[i], PC2))
    if decrypt == 1:
        K = K[::-1]
    #print(K)

    #main rounds
    L={}
    R={}
    MIP = applyPermutation(M,IP)
    #printBinInBlocksOf4(MIP, "MIP")
    L[0]=MIP[0:msgsize//2]
    R[0]=MIP[msgsize//2:]
    for i in range(1,17):
        L[i] = R[i-1]
        RE = applyPermutation(R[i-1], E)
        res = xorsum(RE, K[i-1])
        RS = ""
        for j in range(8):
            x = res[j*6:(j+1)*6]
            row = int(x[0]+x[-1],2)
            col = int(x[1:-1],2)
            RS += "{0:04b}".format(S[j][16*row+col])
        RP = applyPermutation(RS, P)
        R[i] = xorsum(L[i-1],RP)
    FR = R[16]+L[16]
    CIPHER = applyPermutation(FR, IPI)
    return CIPHER

def ecb(binmsg, binkey, decrypt = 0):
    binmsg += "0" * (64-len(binmsg)%64) if len(binmsg)%64!=0 else ""
    res = ""
    for i in range(0,len(binmsg),64):
        res += DES(binmsg[i:i+64],binkey[0:64], decrypt)
    return res

def main():
    #s="Your lips are smoother than vaseline"
    #print(bin2hex(ascii2bin(s)))

    msg = "Mangal is here!"
    key = "0E329232EA6D0D73"
    res = ecb(hex2bin(msg), hex2bin(key))
    cipher = bin2hex(res)
    print("%s * %s = %s" % (msg,key,cipher))

    msg = "85E813540F0AB405"
    key = "133457799BBCDFF1"
    res = DES(hex2bin(msg), hex2bin(key), 1)
    cipher = bin2hex(res)
    print("%s * %s = %s" % (msg,key,cipher))

    #msg = "Algorithms supported: Cast-128, Gost, Rijndael-128, Twofish, Arcfour, Cast-256, Loki97, Rijndael-192, Saferplus, Wake, Blowfish-compat, Des, Rijndael-256, Serpent, Xtea, Blowfish, Enigma, Rc2, Tripledes."
    #key = "heythereAreyoucool?"
    #res = ecb(ascii2bin(msg), ascii2bin(key))
    #cipher = bin2hex(res)
    ##print(cipher)
    #ans = "f4d2eac71a1bc48a4e8ee28d08e188855a4d7f3f1487a899e85d2f01a25794c261adb9346f149cc98a511908b9b1404aad0bc6011951ec5f670f0eeca2f49fc2f7e840c00803d53736d6c3c580dd81c5c613c2f5560f97949ba4cd24638b7998714ecab654beeb08a2bdd500109a45b318367230f6bf7228014e34c222fb79b377acde06a91a68ed24b90abd7294926be1364f8baaed2cff425d884901f9cb1fce79829912daa452ad5fc9e57edd989f076bc5c07a286a6f652c62442ba67aaf180d37abca5d71aaac01865b972edef3".upper()
    ##print(ans)
    #assert ans==cipher
    #res = ecb(hex2bin(ans), ascii2bin(key), 1)
    #resmsg = bin2ascii(res)
    #print(resmsg)
    #print(msg)
    #print(ord(resmsg[-1]))
    #assert resmsg == msg

    key = "133457799BBCDFF1"
    for i in range(16):
        msg = "f"*(i+1)
        print(msg, ascii2bin(msg))
        res = ecb(ascii2bin(msg), ascii2bin(key))
        cipher = bin2hex(res)
        res = bin2ascii(ecb(res, ascii2bin(key), 1)).strip(chr(0))
        print(res, ascii2bin(res))


if __name__ == "__main__":
    main()