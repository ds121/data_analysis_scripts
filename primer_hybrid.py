import sys, os
import subprocess

file1 = open(sys.argv[1], 'r')
file2 = open(sys.argv[2], 'r')

seq1, seq2 = file1.readline(), file2.readline()
print(seq1,'\n', seq2)
index1_f, _index2_r = seq1.index('['), seq2.index(']')

seq1_f, seq2_r = seq1.strip()[:index1_f+4], seq2.strip()[_index2_r-3:]
hybrid1 = seq1_f+seq2_r
hybrid1 = hybrid1.replace('[','').replace(']','')
print('hybrid for {} and {}:'.format(sys.argv[1], sys.argv[2]))
print(hybrid1)


index1_r, _index2_f = seq1.index(']'), seq2.index('[')

seq2_f, seq1_r = seq2.strip()[:_index2_f+4], seq1.strip()[index1_r-3:]
hybrid2 = seq2_f+seq1_r
hybrid2 = hybrid2.replace('[','').replace(']','')
print('Hybrid for {} and {}:'.format(sys.argv[2], sys.argv[1]))
print(hybrid2)


primer3_param1 = '''SEQUENCE_ID=example
SEQUENCE_TEMPLATE={}
SEQUENCE_TARGET=500,6
PRIMER_TASK=generic
PRIMER_PICK_LEFT_PRIMER=1
PRIMER_PICK_INTERNAL_OLIGO=0
PRIMER_PICK_RIGHT_PRIMER=1
PRIMER_OPT_SIZE=20
PRIMER_MIN_SIZE=18
PRIMER_MAX_SIZE=22
PRIMER_PRODUCT_SIZE_RANGE=75-275
PRIMER_EXPLAIN_FLAG=1
='''.format(hybrid1)
out1 = open('primer3_param1', 'w')
print(primer3_param1, file=out1)
out1.close()

primer3_param2 = '''SEQUENCE_ID=example
SEQUENCE_TEMPLATE={}
SEQUENCE_TARGET=500,6
PRIMER_TASK=generic
PRIMER_PICK_LEFT_PRIMER=1
PRIMER_PICK_INTERNAL_OLIGO=0
PRIMER_PICK_RIGHT_PRIMER=1
PRIMER_OPT_SIZE=20
PRIMER_MIN_SIZE=18
PRIMER_MAX_SIZE=22
PRIMER_PRODUCT_SIZE_RANGE=75-275
PRIMER_EXPLAIN_FLAG=1
='''.format(hybrid2)
out2 = open('primer3_param2', 'w')
print(primer3_param2, file=out2)
out2.close()
# PRIMER_PRODUCT_SIZE_RANGE=75-150
# original_stdout = sys.stdout
# pri3_path = "/home/bioinfo03/tools/primer3/primer3/src/primer3_core"
# primer_param1 = "/home/bioinfo03/Desktop/Program/database/primer3_param1"
# try:
# subprocess.run([pri3_path, '-b', primer_param1], check=True)
# print()
# a = os.popen('/home/bioinfo03/tools/primer3/primer3/src/primer3_core < {}'.format( primer_param1))
# preprocessed = a.read()
# a.close()

# except:
#     print("Error...")
