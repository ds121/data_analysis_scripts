import argparse


if __name__ == "__main__":
    def get_sequence(ref_path, position, output):
        output_file = open(output, 'w')
        # print('''
        # The retrieved sequences are from given chromosome with flanking region of 500 base...
        # ''', sep="\t", file=output_file)
        input_file = open(ref_path, "r")
        seq = ""
        for s in input_file:
            if s.startswith(">"):
                print(s)
            else:
                seq += s.strip()

        sequence1 = seq[int(position)-499:int(position)-2]
        main = "[{}{}{}]".format(seq[(int(position)-2): int(position)], seq[int(position)], seq[int(position)+1 : int(position)+3])
        sequence2 = seq[(int(position)+3):((int(position)) + 500)]
        mainSeq = sequence1+main.lower()+sequence2

        # sequence = seq[(int(position) - 500):(int(position) + 500)]
        # output = open(self.out_path, "w")
        print('Retrieved base pairs from given chromosome is: \n')
        print(main)
        print(mainSeq, sep="\t", file=output_file)
        # print(seq[1500100 - 7 : 1500100 + 7])


    parser = argparse.ArgumentParser(description='''
    This tool is built to retrieve '+-' 500 bases as flanking region from the reference DNA sequences
    based on the given position as input ''')

    parser.add_argument('-p', '--position', dest='position',
                        help='specify the desired based position which you want to retrieve...')

    parser.add_argument('-cr', '--chr_ref', dest="chref",
                        help='chromosome wise reference fasta file...')

    parser.add_argument('-o', '--output', dest="output",
                        help="define the desired output file name")

    args = parser.parse_args()
    get_sequence(args.chref, args.position, args.output)
