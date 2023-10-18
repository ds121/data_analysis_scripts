import os
import sys


class CHROM:

    def __init__(self,
                 r_path=sys.path[1],
                 directory=sys.argv[2]
                 # r_path="/home/bioinfo3/Desktop/reference/hg19/hg19_v0_Homo_sapiens_assembly19.fasta",
                 # directory="/home/bioinfo3/Desktop/reference/hg19/hg19_chr/"
                 ):
        self.ref_path = r_path
        self.out_dir = directory

    def seg_chr(self):

        # create the directory named as hg38_dir
        if not os.path.isdir(self.out_dir):
            os.makedirs(self.out_dir)

        with open(self.ref_path, "r") as fh:
            output = open(self.out_dir + "/chr0.fasta", "w")
            for row in fh:
                if row.startswith(">"):
                    output.close()
                    # get the chromosome name only instead of taking entire chromosomes details for creating the file name
                    ch = row.strip().split("  ")[0].split(">")[1]
                    output = open(self.out_dir + "/{}.fasta".format(ch), "w")
                    print(row, file=output)
                else:
                    print(row, file=output)
            output.close()

        chr_list = os.listdir(self.out_dir)
        for files in chr_list:
            name = files.strip().split("_")
            ch_name = "{}_".format(name[0])
            print(ch_name)
            if files.startswith(ch_name) or files.startswith("chr0") or files.startswith("chrUn_") or files.startswith(
                    "chrEBV") or files.startswith("GL"):
                print(name)
                file_path = os.path.join(self.out_dir, files)
                os.remove(file_path)


if __name__ == "__main__":
    a = CHROM()
    a.seg_chr()
