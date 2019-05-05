from symbol_vgg_text import *
import mxnet as mx


mod = mx.mod.Module(symbol=net,
                   context=mx.gpu(),
                   data_names=['data'],
                   label_names=['softmax_label'])

