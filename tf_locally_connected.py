import tensorflow as tf
import numpy as np
from tensorflow.contrib.slim import fully_connected as fc

def locally_connected_1d(input,scope,stride,filter_count,activation_function):
    connector_list = []
    starts = np.arange(0,input.shape[1]-scope,stride)
    for i in starts[:-1]:
        connector_list.append( fc(input[:,i:i+scope], filter_count,activation_fn=activation_function ) )
    connector_list.append(fc(input[:,starts[-1]:input.shape[1]],filter_count,activation_fn=activation_function))
    result = connector_list[0]
    for i in range(1,len(connector_list)):
        result = tf.concat(1,connector_list[i])
    return result

def reverse_locally_connected_1d(input,output_size,scope,stride,filter_count,activation_function):
    connector_list = []
    strides_per_scope = scope//stride
    last_stride = (output_size-scope)//stride

    for i in range(last_stride):
        connector_list.append( fc( input[:,max(0,i-strides_per_scope+1)*filter_count:(i+1)*filter_count] , stride,activation_fn=activation_function ) )
    for i in range(1,strides_per_scope):
        connector_list.append(  fc( input[:,(last_stride-strides_per_scope+i)*filter_count:(last_stride+1)*filter_count],stride,activation_fn=activation_function ) )
    connector_list.append( fc( input[:,last_stride*filter_count:(last_stride+1)*filter_count],stride+(output_size%stride), activation_fn=activation_function ))
    
    result = connector_list[0]
    for i in range(1,len(connector_list)):
        result = tf.concat(1,connector_list[i])
    return result


