import getopt,sys
import subprocess
import cleaningtools as ct 
import pandas as pd
import os
import assay_config as config
import file_config as fconfig
import datetime

def main(argv):
    assay_file=[]
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('assay_curate.py -i <input_file> -a <output_file>')
                print('using defaults in config, no file specified')
                
            elif opt in ("-i", "--input_file"):
                assay_file = arg
                print (f'Input file is ', assay_file)
                data=pd.read_csv(assay_file)
                output_file=assay_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR read from CONFIG')
    if len(assay_file)==0:
        assay_file=fconfig.assay_file
        data=pd.read_csv(assay_file,low_memory=False)
        output_file=assay_file
        

    print ('Input file is ', assay_file)
    print ('Output file is ', output_file)
    print('------------------------------------------------------------------------------')
    print('################ ASSAYS #############')
    msg = "Begin Cleaning"
    print(msg)
    #pull sample ids
    data=ct.pull_sample_ids(data,config.sample_id_formats)
    #### clean and fill spec data
    data=ct.carrot_cleanup(data)
    for map in config.mappings:
        data=ct.column_cleanup(data,mapping=map)
    data=ct.clean_column_names(data)
    data=ct.drop_no_data(data)
    data=data.reset_index()
    
    print('------------------------------------------------------------------------------')
    print('################ MERGE ASSAYS WITH ASSAY SAMPLES #############')
    assay_fname= fconfig.assay_fname
    base_path=ct.get_base_path(assay_file,start_point='_AZ_Kay')
    samples=pd.read_csv(base_path+config.samples)
    
    data_merged=pd.merge(samples,data,left_on='sample_id',right_on='sample_id',how='inner')



    print('------------------------------------------------------------------------------')
    print('################ Assay Soils #############')
    directory=base_path+config.soils
    soil=pd.DataFrame()
    for file in os.listdir(directory):
        print(file)
        skip=0

        broken = True
        while (broken==True) and (skip<=20):
            skip+=1
            try: 
                data=pd.read_csv(directory+file,skiprows=skip,header=0)
                cols = [c.lower().replace(' ','') for c in data.columns]
                #print(cols)
                if 'sample' in cols:
                    #print('data on line',skip)
                    data=data.drop(0)
                    broken=False
            except Exception as e:
                pass

        soil=pd.concat([soil,data])
    soil.to_csv(base_path+config.soil_export)

    
    print(f'output {assay_fname}')
    data_merged.to_csv(output_file)
    print('------------------------------------------------------------------------------')
    return data

if __name__ == "__main__":
    main(sys.argv[1:])