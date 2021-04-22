import glob
from pprint import pprint

filelist = []
for name in glob.glob('FObhavCopy_Data//[0-9][0-9]_sec_bhavdata_full_*.csv'):
        filelist.append(name)

for name in glob.glob('FObhavCopy_Data//[0-9][0-9][0-9]_sec_bhavdata_full_*.csv'):
        filelist.append(name)

pprint(filelist)