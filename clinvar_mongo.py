from pymongo import MongoClient
import pandas as pd
import vcf


def substitution(alt):
    """

    :rtype: alleles string
    """
    s = []
    for allele in alt:
        s.append(str(allele))
    return ",".join(s)


class ClinvarMongo:

    # used a hg19 dbSNP vcf file and same for the refGene GTF file to extract the gene
    def __init__(self, db_path="../../databases/clinvar.vcf"):
        self.cln_path = db_path
        self.client = MongoClient()
        self.db = self.client.clinical_databases
        self.col = self.db.clinvar_hg38

    def cln_database(self):
        total_import = 0
        cln_window = []
        vcf_reader = vcf.Reader(open(self.cln_path, 'r'))
        for record in vcf_reader:
            alt = substitution(record.ALT)
            records = {"CHROM": "chr" + record.CHROM, "ID": record.ID, "POS": record.POS, "REF": record.REF,
                       "ALT": alt, "FILTER": record.FILTER, "QUAL": record.QUAL}
            full_record = {**records, **record.INFO}
            if "RS" in full_record.keys():
                full_record['RS'] = "rs"+full_record['RS'][0]
            if "GENEINFO" in full_record.keys():
                gene = full_record["GENEINFO"].strip().split("|")
                gene_list = []
                for g in gene:
                    genes = {"gene": g.split(":")[0]}
                    gene_list.append(genes)
                full_record["genes"] = gene_list
            else:
                full_record["genes"] = ["-"]
                # self.col.insert_one(full_record)
                # total_import += 1

            if len(cln_window) == 1000000:
                self.col.insert_many(cln_window)
                total_import += 1000000
                print(f"Total {total_import} number of records has been imported into clinvar database...")
                cln_window = []
            else:
                cln_window.append(full_record)
        self.col.insert_many(cln_window)
        print(f"Total {total_import} number of records has been imported into clinvar database...")

    def cln_data_extract(self):
        # Extract the records that belongs to autism disorders only...
        all_records_a = self.col.find({"CLNDN": {'$regex': 'autism'}})
        all_records_A = self.col.find({"CLNDN": {'$regex': 'Autism'}})

        autism_records = []
        for aut, Aut in zip(all_records_a, all_records_A):
            # print(aut)
            autism_records.append(aut)
            autism_records.append(Aut)

        df = pd.DataFrame(autism_records)
        final_df = df.sort_values(by=["CHROM", "POS"]).drop_duplicates(subset=["POS", "REF", "ALT"])
        final_df.to_csv("Autism_data_extracted_from_clinvar.tsv", index=False, sep="\t")
        print(final_df)


if __name__ == "__main__":
    a = ClinvarMongo()
    a.cln_database()
