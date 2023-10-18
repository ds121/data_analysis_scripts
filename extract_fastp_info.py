import json
import os

import pandas as pd


class FastP:

    def __init__(self, dir_path="/home/bioinfo3/Desktop/bam_files"):
        self.dir_path = dir_path

    def retrieve_value(self):
        get_dir = os.listdir(self.dir_path)
        records = []
        for file in get_dir:
            if file.endswith(".json"):
                sample_name = file.strip().split(".")[0]
                f = open(self.dir_path + "/" + file)
                data = json.load(f)
                before_filtering = data["summary"]["before_filtering"]
                after_filtering = data["summary"]["after_filtering"]
                fields = {
                    "sample_name": sample_name,
                    "mean_length_before_filtering": str(before_filtering["read1_mean_length"]) + " bp",
                    "mean_length_after_filtering": str(after_filtering["read1_mean_length"]) + " bp",
                    "total_read_before_filtering": str(round(before_filtering["total_reads"] / 1000000, 4)) + " M",
                    "total_read_after_filtering": str(round(after_filtering["total_reads"] / 1000000, 4)) + " M",
                    "total_based_before_filtering": str(round(before_filtering["total_bases"] / 1000000, 4)) + " M",
                    "total_based_after_filtering": str(round(after_filtering["total_bases"] / 1000000, 4)) + " M",
                    "duplication_rate": str(round(data["duplication"]["rate"] * 100, 2)) + "%",
                    "Q20_rate_before_filtering": str(before_filtering["q20_rate"] / 1000000) + " M (" + (
                        str(round(before_filtering["q20_rate"] * 100, 3))) + "%)",
                    "Q20_rate_after_filtering": str(after_filtering["q20_rate"] / 1000000) + " M (" + str(
                        round(after_filtering["q20_rate"] * 100, 3)) + "%)",
                    "Q30_rate_before_filtering": str(before_filtering["q30_rate"] / 1000000) + " M (" + str(
                        round(before_filtering["q30_rate"] * 100, 3)) + "%)",
                    "Q30_rate_after_filtering": str(before_filtering["q30_rate"] / 1000000) + " M (" + str(
                        round(after_filtering["q30_rate"] * 100, 3)) + "%)",
                    "GC-content_before_filtering": str(round(before_filtering["gc_content"] * 100, 2)) + "%",
                    "GC-content_after_filtering": str(round(after_filtering["gc_content"] * 100, 2)) + "%"

                }
                # print(fields)
                records.append(fields)

        df = pd.DataFrame(records)
        df.to_csv(self.dir_path+"/fastp_results_for_multiple_samples.tsv", index=False, sep="\t")


if __name__ == '__main__':
    a = FastP(dir_path="/home/bioinfo3/Desktop/fq-gz/run0627/Nanodrop")
    a.retrieve_value()
