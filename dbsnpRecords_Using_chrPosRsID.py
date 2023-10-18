# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pymongo import MongoClient
import pandas as pd


def clinvar_required_cols(rec, cln_rec):
    rec["Clinvar ALLELEID"] = cln_rec["ALLELEID"] if "ALLELEID" in cln_rec.keys() else "-"
    rec["Clinvar CLNDN (Disease_Name)"] = cln_rec["CLNDN"] if "CLNDN" in cln_rec.keys() else "-"
    rec["Clinvar CLNSIG"] = cln_rec["CLNSIG"] if "CLNSIG" in cln_rec.keys() else "-"
    rec["Clinvar CLNREVSTAT"] = cln_rec["CLNREVSTAT"] if "CLNREVSTAT" in cln_rec.keys() else "-"
    rec["Clinvar MC (sequence_ontology | molecular_consequences)"] = cln_rec[
        "MC"] if "MC" in cln_rec.keys() else "-"
    return rec


class Mongo:

    # used a hg19 dbSNP vcf file and same for the refGene GTF file to extract the gene
    def __init__(self, db_path="../../databases/00-All.vcf",
                 rs_input="../../databases/autism_records/input_autism-database_rsid.tsv",
                 f_input="/home/bioinfo3/Desktop/databases/autism_records/autism-Unannotated-records-based_rsid.tsv",
                 f2_input="/home/bioinfo3/Desktop/databases/autism_records/autism-database - autism_SNVchr_pos.tsv"):
        self.unannotated_record = f_input
        self.input_file1 = f2_input
        self.input_file = rs_input
        self.client = MongoClient("192.168.0.155",
                                  username='admin',
                                  password='bioinfo3')
        self.db = self.client.clinical_databases
        self.col = self.db.dbsnp
        self.cln_col = self.db.clinvar

    def fetch_records(self):
        with open(self.input_file, "r") as fh:
            dbsnp_data_hg19 = []
            dbsnp_data = []
            header = fh.readline()
            print(header)
            count = 0
            for rows in fh:
                row = rows.strip().split("\t")
                # fetch the records from the dbSNP and clinvar database based on the genes name...
                doc = self.col.find_one({"ID": row[0]})
                if doc is None:
                    if row[2] == "-":
                        pass
                    else:
                        doc = self.col.find_one({"$and": [{"CHROM": "chr" + row[1]}, {"POS": int(row[2])}]})
                    if doc is None:
                        dbsnp_data.append(row)
                    else:
                        del [doc["_id"], doc["QUAL"], doc["FILTER"]]
                        cln_rec = self.cln_col.find_one({"$and": [{"CHROM": doc["CHROM"]}, {"POS": doc["POS"]}]})
                        if cln_rec is None:
                            doc["Clinvar ALLELEID"] = "-"
                            doc["Clinvar CLNSIG"] = "-"
                            doc["Clinvar CLNDN (Disease_Name)"] = "-"
                            doc["Clinvar CLNREVSTAT"] = "-"
                            doc["Clinvar MC (sequence_ontology | molecular_consequences)"] = "-"
                        else:
                            clinvar_required_cols(doc, cln_rec)
                        dbsnp_data_hg19.append(doc)
                        count += 1

                else:
                    del [doc["_id"], doc["QUAL"], doc["FILTER"]]
                    cln_rec = self.cln_col.find_one({"$and": [{"CHROM": doc["CHROM"]}, {"POS": doc["POS"]}]})
                    if cln_rec is None:
                        doc["Clinvar ALLELEID"] = "-"
                        doc["Clinvar CLNSIG"] = "-"
                        doc["Clinvar CLNDN (Disease_Name)"] = "-"
                        doc["Clinvar CLNREVSTAT"] = "-"
                        doc["Clinvar MC (sequence_ontology | molecular_consequences)"] = "-"
                    else:
                        clinvar_required_cols(doc, cln_rec)
                    dbsnp_data_hg19.append(doc)
                    count += 1
            print(count)
            df = pd.DataFrame(dbsnp_data_hg19)
            df_dropDup = df.drop_duplicates(subset=["ID", "CHROM", "POS"])
            fd = pd.DataFrame(dbsnp_data)
            fd_dropDup = fd.drop_duplicates()
            df_dropDup.to_csv("/home/bioinfo3/Desktop/databases/autism_records/autism-annotated-records-based_rsid.tsv",
                              sep="\t", index=False)
            print(df, fd)
            fd_dropDup.to_csv(
                "/home/bioinfo3/Desktop/databases/autism_records/autism-Unannotated-records-based_rsid.tsv",
                sep="\t", index=False)

    def chr_pos(self):
        # fetch the dbsnp records using chromosomes and positions...
        with open(self.input_file1, "r") as fh:
            header = fh.readline().strip().split("\t")
            c = 0
            data_fetched = []
            data_ntFetch = []
            for rows in fh:
                row = rows.strip().split("\t")
                # doc = self.col.find_one({"$and": [{"CHROM": "chr"+row[1]}, {"POS": int(row[2])}]})
                # print(doc)
                if row[2] == "-":
                    pass
                else:
                    doc = self.col.find_one({"$and": [{"CHROM": "chr" + row[1]}, {"POS": int(row[2])}]})
                    if doc is None:
                        data_ntFetch.append(row)
                    else:
                        cln_rec = self.cln_col.find_one({"$and": [{"CHROM": doc["CHROM"]}, {"POS": doc["POS"]}]})
                        if cln_rec is None:
                            doc["Clinvar ALLELEID"] = "-"
                            doc["Clinvar CLNSIG"] = "-"
                            doc["Clinvar CLNDN (Disease_Name)"] = "-"
                            doc["Clinvar CLNREVSTAT"] = "-"
                            doc["Clinvar MC (sequence_ontology | molecular_consequences)"] = "-"
                        else:
                            clinvar_required_cols(doc, cln_rec)
                        del [doc["_id"], doc["QUAL"], doc["FILTER"]]
                        data_fetched.append(doc)
            df = pd.DataFrame(data_fetched)
            fd = pd.DataFrame(data_ntFetch)
            df.to_csv("/home/bioinfo3/Desktop/databases/autism_records/autism-database-SNVchr_pos_fetched.tsv",
                      sep="\t",
                      index=False)
            fd.to_csv("/home/bioinfo3/Desktop/databases/autism_records/autism-database-SNVchr_pos_ntfetch.tsv",
                      sep="\t",
                      index=False)


if __name__ == "__main__":
    cls = Mongo()
    cls.chr_pos()
