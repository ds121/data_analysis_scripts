import vcf

import pandas as pd

vcf_reader = vcf.Reader(open('/home/bioinfo03/Desktop/fq-gz/16Aug23/wetransfer_nanopore-p2-worksheet-20230811-hk-xlsx_2023-08-14_2050/fastq_pass_NA05654/barcode3.vcf', 'r'))

intraTrans = []
interTrans = []
for index, record in enumerate(vcf_reader):
    record_dict = {
        'chrom': record.CHROM,
        'position': record.POS,
        'id': record.ID,
        'reference': record.REF,
        'alteration': str(record.ALT[0]),
        'quality': record.QUAL,
        'filter': record.FILTER
    }
    full_dict = {**record_dict, **record.INFO}
    # print(full_dict)
    if not full_dict['filter'] and 'IMPRECISE' not in full_dict.keys() and full_dict['SVTYPE'] == "BND":
        if 'chrUn' in full_dict['chrom'] or 'alt' in full_dict['chrom'] or 'random' in full_dict['chrom'] or 'chrUn' in full_dict['alteration'] or 'alt' in full_dict['alteration'] or 'random' in full_dict['alteration']:
            continue
        else:
            if record.CHROM in str(record.ALT[0]) and len(full_dict['ALT_READ_IDS']) >= 2:
                # print(index, full_dict)
                intraTrans.append(full_dict)
            else:
                if len(full_dict['ALT_READ_IDS']) >= 2:
                    full_dict['filter'] = "PASS"
                    interTrans.append(full_dict)
    #     # print(index, str(record.ALT[0]))

print(len(intraTrans))
print(len(interTrans))
df = pd.DataFrame(interTrans)
finalDF = df.drop_duplicates(subset=['chrom', 'alteration'])
sortedDF = finalDF.sort_values(by=['chrom'])
print(sortedDF)
sortedDF.to_csv('/home/bioinfo03/Desktop/fq-gz/16Aug23/wetransfer_nanopore-p2-worksheet-20230811-hk-xlsx_2023-08-14_2050/fastq_pass_NA05654/barcode3_filtered.tsv', index=False, sep="\t")


# with open('chrPattern.txt', 'r')as fh:
#     data = []
#     count = 0
#     for rows in fh:
#         row = rows.strip().split("\t")
#         for record in interTrans:
#             if row[0] == record['chrom'] and row[1] in record['alteration']:
#                 count += 1
#                 record['filter'] = "PASS"
#                 data.append(record)
#     df = pd.DataFrame(data)
#     final_df = df.drop_duplicates(subset=['chrom', 'alteration'])
#     print(final_df)
# # for record in interTrans:
# #     print(record)
