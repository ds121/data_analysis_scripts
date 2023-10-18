import subprocess


with open('/home/bioinfo03/Desktop/fq-gz/16Aug23/fastq_pass_NA01536/filtered_barcode3_01536.TXT', 'r')as fh:

    for rows in fh:
        out = open('igv_script.txt', 'w')
        row = rows.strip().split('\t')
        info = row[7].strip().split(';')
        for i in info:
            if 'CHR2' in i:
                i = i.split('=')
                confName = '{}_{}_{}_transloc_cordinate.png'.format(row[0], i[1], str(row[1]))
                a = '''
                new
                genome hg38
                load /home/bioinfo03/Desktop/fq-gz/16Aug23/fastq_pass_NA01536/barcode3_sort.bam
                track name=Sample colorByStrand="true"
                goto {}:{}
                snapshot {}
                exit
                '''.format(row[0], row[1], confName)
                print(confName)
                print(a, file=out)
        out.close()

        # Specify the IGV batch script file
        igv_script_file = 'igv_script.txt'
        # Specify the path to the IGV executable
        igv_executable = 'igv'  # On Windows, this might be igv.bat# Specify the path to the IGV executable
        # Run IGV with the batch script
        try:
            # subprocess.run(['java', '-Xmx2g', '-Djava.awt.headless=true', '-jar', igv_executable, '-b', igv_script_file], check=True)
            subprocess.run([igv_executable, '-b', igv_script_file], check=True)
        except subprocess.CalledProcessError:
            print("Error running IGV.")
