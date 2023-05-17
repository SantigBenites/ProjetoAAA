from tensorflow.keras import Sequential, layers
import tensorflow as tf

t_model = Sequential(
    [
        layers.Input(shape=(4,)),
        layers.Dense(3, activation="relu"),
        layers.Dense(4),
    ]
)

arr = [1] * 64

print()

con = tf.constant([1, 2, 3])

print('[shape]', tf.shape(con))

#print(tf.ones((64,)))
