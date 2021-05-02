import keras
import h5py
import xlrd
import pandas as pd
import matplotlib.pyplot as plt


#f = h5py.File('D:\Games\BPNN_BORC_numcombined.h5','r+')
#data_p = f.attrs['training_config']
#data_p = data_p.decode().replace("learning_rate","lr").encode()
#f.attrs['training_config'] = data_p
#f.close()
model = keras.models.load_model('D:\Games\BPNN_BORC_numcombined.h5')

dataset = pd.read_excel('D:\Games\BORC_numconbined_data_resaved.xls', sheet_name='Sheet1')
dataset_1 = dataset[["fluid number","T_h / K","T_eva / kPa","T_pp / k","T_sh / k","T_sc / k","T_con / K"]]
dataset_1 = dataset_1[0:56000]
#print(dataset_1.shape)

result = model.predict(dataset_1)
print(result)


plt.plot(result)
plt.show()