import tensorflow as tf
import numpy as np
import Vecterize as vec
from music21 import *

summer = converter.parse("Summer_Joe_Hisaishi.mxl")
part0 = summer.getElementsByClass('Part')[0]
vector0 = vec.vectorize(part0)

# part1 = summer.getElementsByClass('Part')[1]
# vector1 = vec.vectorize(part1)

learning_rate = 0.001
training_iters = 1000
batch_size = 1
display_step = 10

n_input = 1
n_steps, n_class = np.shape(vector0)
n_hidden = 128


x = tf.placeholder(tf.float32, [n_steps, n_classes])
y = tf.placeholder(tf.float32, [1, n_classes])

weights = tf.Variable(tf.random_normal([n_hidden, n_classes]))
biases = tf.Variable(tf.random_normal([n_classes]))

# x_trans = tf.transpose(x, [1, 0, 2])
# x_reshape = tf.reshape(x_trans, [-1, n_input])
# x_input = tf.split(0, n_steps, x_reshape)

lstm_cell = tf.nn.rnn_cell.BasicLSTMCell( n_hidden, forget_bias=1.0)
outputs, states = tf.nn.rnn(lstm_cell, vector0, dtype=tf.float32)
pred = tf.matmul(outputs[-1], weights) + biases

cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))


with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())

    step = 1
    while step * batch_size < training_iters:


        batch_x, batch_y = mnist.train.next_batch(batch_size)
        batch_x = batch_x.reshape((batch_size, n_steps, n_input))
        feed_dict = {x: batch_x, y: batch_y}
        sess.run(optimizer, feed_dict)
        if step & display_step == 0:
            acc = sess.run(accuracy, feed_dict)
            loss = sess.run(cost, feed_dict)
            print "Iter " + str(step*batch_size) + ", Minibatch Loss= " + "{:.6f}".format(loss) + ", Training Accuracy= " + "{:.5f}".format(acc)
        step += 1
    print "Optimization Finished!"

    test_len = 128
    test_data = mnist.test.images[:test_len].reshape((-1, n_steps, n_input))
    test_label = mnist.test.labels[:test_len]

    print "Testing Accuracy:", sess.run(accuracy, feed_dict)