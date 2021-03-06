"""
    Hamming Weight DPA - May 2017
    Vernam Lab - WPI
    Abraham Fernandez-Rubio
    Kewal Vora
""" 


# Sbox look up table
Sbox = ['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', \
'2b', 'fe', 'd7', 'ab', '76', 'ca', '82', 'c9', '7d', 'fa', '59', '47', \
'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0', 'b7', 'fd', '93', \
'26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', \
'15', '04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', \
'e2', 'eb', '27', 'b2', '75', '09', '83', '2c', '1a', '1b', '6e', '5a', \
'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84', '53', 'd1', '00', \
'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', \
'cf', 'd0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', \
'7f', '50', '3c', '9f', 'a8', '51', 'a3', '40', '8f', '92', '9d', '38', \
'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2', 'cd', '0c', '13', \
'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', \
'73', '60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', \
'14', 'de', '5e', '0b', 'db', 'e0', '32', '3a', '0a', '49', '06', '24', \
'5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79', 'e7', 'c8', '37', \
'6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', \
'08', 'ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', \
'1f', '4b', 'bd', '8b', '8a', '70', '3e', 'b5', '66', '48', '03', 'f6', \
'0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e', 'e1', 'f8', '98', \
'11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', \
'df', '8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', \
'0f', 'b0', '54', 'bb', '16' ]


secretkey = (); 

## Read the data from sample files

traceNum = 5000;
traceLen = 7200;
keyNum = 256;

# traceFile = sprintf('C:\\Users\\afernandezrubio\\Desktop\\abraham\\python\\DPA\\power_traces.csv');
# trc_matrix = csvread(traceFile);
# trc_matrix = trc_matrix' ; 

# ptxtFile = sprintf('C:\\Users\\afernandezrubio\\Desktop\\abraham\\python\\DPA\\plaintext_list.csv');
# ptxt_matrix = csvread(ptxtFile);
# ptxt_matrix = ptxt_matrix' ; 

f2=open("power_traces.csv","rb")
f1=open("plaintext_list.csv","rb")

trc_matrix = csv.reader(f2)
ptxt_matrix = csv.reader(f1)

pt = list()
Y = list()
H = list()

## Run for bytes of the key (up to 16)
for selByte in range(1):
    
    # Get the first byte of every plaintext
    #pt = ptxt_matrix(selByte,1:traceNum);
    for trace in range(traceNum):
        pt.append( ptxt_matrix.next()[0] )
    
    # Cheap repmat
    #Y = repmat(pt',1,keyNum);
    for p in range(keyNum):
        Y.append(pt)
    
    
    #H = zeros(traceNum,keyNum);
    # for key = 1:keyNum
        # for pt_row = 1:traceNum
            # % S-box lookup:  %Y = S(y xor k)
            # Y(pt_row,key) = hex2dec(Sbox( bitxor( Y(pt_row,key), key-1)+1));
            # % we use the Hamming weight model:
            # H(pt_row,key) = sum(dec2bin(Y(pt_row,key))=='1'); % Hamming weight
        # end
    # end
    
    ## (b) Generates the S-Box output
    for key in range(keyNum):
        for pt_row in range(traceNum):
            # S-box lookup:  Y = S(y xor k)
            Y[pt_row][key] = Sbox[ int(Y[pt_row][key]) ^ key ]
            # Get the Hamming weight
            H[pt_row][key] = bin.(int(Y[pt_row][key])).count("1")
            



    ## (c) DPA correlation
    
    R = zeros(keyNum,traceLen);
    for key = 1:keyNum
        progress = sprintf('%d: %d',selByte,key);
        disp(progress);
        for time=1:traceLen
            R(key,time) = corr(H(:,key),trc_matrix(time,:)'); 	% correlation
        end
    end
    

    %% Find the highest correlation 
    highest_corr = zeros(1,256) ;
    for i=1:256
        highest_corr(i) = max(abs(R(i,:)));
    end

    [val, idx] = max(highest_corr);
    secretkey(selByte) = idx-1 ;
    disp(dec2hex(idx-1));
end


result = sprintf('Recovered key: %s\n',num2str(secretkey));
disp(result)
dec2hex(secretkey)
