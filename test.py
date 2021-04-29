import math
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import xlsxwriter

#  "ml.xlsx", "mloutput.xlsx" are training set.
print("10%")
workbook1 = xlrd.open_workbook(r'I:\ml.xlsx')
sheet1 = workbook1.sheet_by_index(0)
x_data = np.zeros(shape=(25876,17))
for i in range(0,25876):
    x_data[i] =  sheet1.row_values(i+1)
    
workbook2 = xlrd.open_workbook(r'I:\mloutput.xlsx')
sheet2 = workbook2.sheet_by_index(0)
y_data = np.zeros(shape=(25876,1))
for m in range(0,25876):
    y_data[m] = sheet2.row_values(m+1)

#  "t1_1", "t1_2" are test set.

workbook3 = xlrd.open_workbook(r'I:\t1_1.xlsx')
sheet3 = workbook3.sheet_by_index(0)
x_t = np.zeros(shape=(663,17))
for a in range(0,662):
    x_t[a] =  sheet3.row_values(a)
    
workbook4 = xlrd.open_workbook(r'I:\t1_2.xlsx')
sheet4 = workbook4.sheet_by_index(0)
y_t = np.zeros(shape=(663,1))
for b in range(0,662):
    y_t[b] = sheet4.row_values(b)

time1 = np.linspace(1,25876,25876)
time2 = np.linspace(1,663,663)

# Tensorflow visualization

def variable_summaries(var):
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean',mean) # average value
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar('stddev',stddev) # standard deviation
        tf.summary.scalar('max', tf.reduce_max(var)) # max
        tf.summary.scalar('min', tf.reduce_min(var)) # min
        tf.summary.histogram('histogram',var) # histogram

batch_size = 100   
n_batch = 25876 // batch_size

# 17 input parameters, 1 output parameter

x = tf.placeholder(tf.float32, [None,17])
y = tf.placeholder(tf.float32, [None,1])

with tf.name_scope('W1'):
    W1 = tf.Variable(tf.truncated_normal([17,90],stddev=0.1))
    variable_summaries(W1)
with tf.name_scope('b1'):
    b1 = tf.Variable(tf.zeros([90])+0.1)
    variable_summaries(b1)
L1 = tf.nn.relu(tf.matmul(x,W1)+b1)


with tf.name_scope('W2'):
    W2 = tf.Variable(tf.truncated_normal([90,1],stddev=0.1))
    variable_summaries(W2)
with tf.name_scope('b2'):
    b2 = tf.Variable(tf.zeros([1])+0.1)
    variable_summaries(b2)

prediction = tf.nn.relu(tf.matmul(L1,W2)+b2)

with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.square(y-prediction))
    tf.summary.scalar('loss', loss)
    variable_summaries(loss)
#loss = tf.reduce_mean(tf.square(y-prediction))
with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

# training

saver = tf.train.Saver()
merged = tf.summary.merge_all()
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter('logs/',sess.graph)
    for epoch in range(1000):
        for batch in range(n_batch):
            sess.run(train_step,feed_dict={x:x_data, y:y_data})
            summary,_ = sess.run([merged, train_step], feed_dict={x:x_data, y:y_data})
        writer.add_summary(summary,epoch)
        prediction_value = sess.run(prediction,feed_dict={x:x_t})
    saver.save(sess,'project.ckpt')
    writer.close()
    
# output result visualization

    plt.figure()
    plt.plot(time2,prediction_value)
    plt.plot(time2,y_t,'r-')
    plt.ylim((0.8, 0.9))
    #plt.plot(x_data,prediction_value,'r-',lw=5)
    plt.xlabel('Time(s)')
    plt.ylabel('P(MPa)')
    plt.savefig("E:/fig.png")
    plt.show()
    print(y_t)
    print(prediction_value)
    
# write results to excel
    
    workbookout = xlsxwriter.Workbook('D:\out.xlsx')
    worksheet = workbookout.add_worksheet()
    for row in range(662):
        worksheet.write(row , 0 ,prediction_value[row])
    workbookout.close()
    error = xlsxwriter.Workbook('D:\error.xlsx')
    error_worksheet = error.add_worksheet()
    for error_row in range(642):
        error_worksheet.write(error_row , 0 ,prediction_value[error_row] - y_t[error_row+20])
    error.close()
