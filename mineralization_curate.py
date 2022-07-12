import getopt,sys
import subprocess
try:
    print('check for pandas')
    import pandas as pd
    
except:
    try:
        print('install pandas')
        subprocess.check_call([sys.executable,'-m','pip','install','pandas'])
    except:
        print('upgrade pip then try again')
        subprocess.check_call([sys.executable,'-m','pip','install','--upgrade','pip'])
        subprocess.check_call([sys.executable,'-m','pip','install','pandas'])
        import pandas as pd

import cleaningtools as ct
import file_config as config
import datetime

def main(argv):
    mineral_file=config.mineral_file
    mineral=pd.read_csv(mineral_file,low_memory=False)
    output_file=mineral_file
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('mineralogy_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                mineral_file = arg
                print ('Input file is ',)
                mineral=pd.read_csv(mineral_file)
                output_file=mineral_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError:
        print ('file error read grom google drive')
    print ('Input file is ', config.mineral_file)
    print ('Output file is ', output_file)
    #### clean and fill mineral data
    mineral=ct.depth_cleanup(mineral)

    
    print(f'output {output_file}')
    mineral.to_csv(config.mineral_file)
    return mineral

if __name__ == "__main__":
    main(sys.argv[1:])