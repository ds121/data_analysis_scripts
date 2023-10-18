import pandas as pd

with open('/home/bioinfo03/Desktop/fq-gz/16Aug23/wetransfer_nanopore-p2-worksheet-20230811-hk-xlsx_2023-08-14_2050/fastq_pass_NA05654/barcode3.vcf')as fh:
    header = ""
    data = []
    for rows in fh:
        if rows.startswith("##"):
            continue
        elif rows.startswith("#"):
            header   = rows.strip().split("\t")
        else:
            row = rows.strip().split("\t")
            pre = row[7].strip().split(";")
            if "chrUn" not in row[0] and "alt" not in row[0] and "random" not in row[0]:
                if "INS" in row[2] or "DEL" in row[2]:
                    if pre[0] == "PRECISE":
                        data.append(row)

    print(header)

    appended_data = pd.DataFrame(data, columns=header)
    appended_data.to_csv('barcodeaaaaaaaaaaaaa.txt', sep="\t", index=False)
