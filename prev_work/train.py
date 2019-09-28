import tensorflow as tf
import numpy as np
import Vecterize as vec
from keras.models import load_model, Model
from keras.layers import Dense, Activation, Dropout, Input, LSTM, Reshape, Lambda, RepeatVector
from keras.initializers import glorot_uniform
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras import backend as K


n_a = 64
n_values = vec.vector_size # need to be change
reshapor = Reshape((1, vec.vector_size))                        # Used in Step 2.B of djmodel(), below
LSTM_cell = LSTM(n_a, return_state = True)         # Used in Step 2.C
densor = Dense(n_values, activation='softmax')     # Used in Step 2.D
Y = np.random.rand(len(vec.allNotes1), 1, n_values)

def djmodel(Tx, n_a, n_values):
    """
    Implement the model

    Arguments:
    Tx -- length of the sequence in a corpus
    n_a -- the number of activations used in our model
    n_values -- number of unique values in the music data 

    Returns:
    model -- a keras model with the 
    """

    # Define the input of your model with a shape 
    X = Input(shape=(Tx, n_values))

    # Define s0, initial hidden state for the decoder LSTM
    a0 = Input(shape=(n_a,), name='a0')
    c0 = Input(shape=(n_a,), name='c0')
    a = a0
    c = c0

    ### START CODE HERE ### 
    # Step 1: Create empty list to append the outputs while you iterate (≈1 line)
    outputs = []

    # Step 2: Loop
    for t in range(Tx):

        # Step 2.A: select the "t"th time step vector from X. 
        x =  Lambda(lambda x: X[:,t,:])(X)
        # Step 2.B: Use reshapor to reshape x to be (1, n_values) (≈1 line)
        x = reshapor(x)

        # Step 2.C: Perform one step of the LSTM_cell
        a, _, c = LSTM_cell(x, initial_state=[a, c])
        # Step 2.D: Apply densor to the hidden state output of LSTM_Cell
        out = densor(a)
        # Step 2.E: add the output to "outputs"
        outputs.append(out)

    # Step 3: Create model instance
    model = Model(inputs=[X,a0,c0],outputs=outputs)

    ### END CODE HERE ###

    return model

Tx = len(vec.allNotes1)

model = djmodel(Tx=Tx, n_a=64, n_values=n_values)
opt = Adam(lr=0.01, beta_1=0.9, beta_2=0.999, decay=0.01)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

m = 1
a0 = np.zeros((m, n_a))
c0 = np.zeros((m, n_a))
model.fit([vec.vector1, a0, c0], list(Y), epochs=100)




def one_hot(x):
    x = K.argmax(x)
    x = tf.one_hot(x, len(vec.allNotes1)) 
    x = RepeatVector(1)(x)
    return x







# GRADED FUNCTION: music_inference_model

def music_inference_model(LSTM_cell, densor, one_hot, n_values = n_values, n_a = 64, Ty = 100):
    x0 = Input(shape=(1, n_values))
    a0 = Input(shape=(n_a,), name='a0')
    c0 = Input(shape=(n_a,), name='c0')
    a = a0
    c = c0
    x = x0
    outputs = []
    for t in range(Ty):
        a, _, c = LSTM_cell(x, initial_state=[a, c])
        out = densor(a)
        outputs.append(out)
        x =  Lambda(one_hot)(out)
    inference_model = Model(inputs=[x0,a0,c0],outputs=outputs)
    return inference_model



inference_model = music_inference_model(LSTM_cell, densor, one_hot, n_values = vec.vector_size, n_a = 64, Ty = len(vec.allNotes1))