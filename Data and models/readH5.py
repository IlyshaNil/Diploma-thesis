#import h5py
#filename = 'D:\Games\BPNN_BORC_procombined.h5'

#with h5py.File(filename, "r") as f:
    # List all groups
 #   print("Keys: %s" % f.keys())
  #  a_group_key = list(f.keys())[0]

    # Get the data
   # data = list(f[a_group_key])
import pickle
from sklearn import svm


with open('D:\Games\SVR_BORC_R141b_exergy.pkl', 'rb') as f:
    data = pickle.load(f)