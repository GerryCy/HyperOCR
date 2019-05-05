# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import mxnet as mx
from mxnet import rnn
from rcnn.config import config
from . import proposal
from . import proposal_target

def Act(data, act_type, name):
    #ignore param act_type, set it in this function 
    body = mx.sym.LeakyReLU(data = data, act_type='prelu', name = name)
    #act = mx.sym.Activation(data=bn, act_type='relu', name='%s%s_relu' %(name, suffix))
    return body

def Conv(data, num_filter=1, kernel=(1, 1), stride=(1, 1), pad=(0, 0), num_group=1, name=None, suffix=''):
    conv = mx.sym.Convolution(data=data, num_filter=num_filter, kernel=kernel, num_group=num_group, stride=stride, pad=pad, no_bias=True, name='%s%s_conv2d' %(name, suffix))
    bn = mx.sym.BatchNorm(data=conv, name='%s%s_batchnorm' %(name, suffix), fix_gamma=True)
    act = Act(data=bn, act_type='relu', name='%s%s_relu' %(name, suffix))
    return act

def ConvOnly(data, num_filter=1, kernel=(1, 1), stride=(1, 1), pad=(0, 0), num_group=1, name=None, suffix=''):
    conv = mx.sym.Convolution(data=data, num_filter=num_filter, kernel=kernel, num_group=num_group, stride=stride, pad=pad, no_bias=True, name='%s%s_conv2d' %(name, suffix))
    return conv

def get_mobilenet_conv(data):
    """
    shared convolutional layers
    :param data: Symbol
    :return: Symbol
    """
    bf = 32
    conv_1 = Conv(data, num_filter=bf, kernel=(3, 3), pad=(1, 1), stride=(2, 2), name="conv_1") # 224/112
    conv_2_dw = Conv(conv_1, num_group=bf, num_filter=bf, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_2_dw") # 112/112
    conv_2 = Conv(conv_2_dw, num_filter=bf*2, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_2") # 112/112
    conv_3_dw = Conv(conv_2, num_group=bf*2, num_filter=bf*2, kernel=(3, 3), pad=(1, 1), stride=(2, 2), name="conv_3_dw") # 112/56
    conv_3 = Conv(conv_3_dw, num_filter=bf*4, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_3") # 56/56
    conv_4_dw = Conv(conv_3, num_group=bf*4, num_filter=bf*4, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_4_dw") # 56/56
    conv_4 = Conv(conv_4_dw, num_filter=bf*4, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_4") # 56/56
    conv_5_dw = Conv(conv_4, num_group=bf*4, num_filter=bf*4, kernel=(3, 3), pad=(1, 1), stride=(2, 2), name="conv_5_dw") # 56/28
    conv_5 = Conv(conv_5_dw, num_filter=bf*8, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_5") # 28/28
    conv_6_dw = Conv(conv_5, num_group=bf*8, num_filter=bf*8, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_6_dw") # 28/28
    conv_6 = Conv(conv_6_dw, num_filter=bf*8, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_6") # 28/28
    conv_7_dw = Conv(conv_6, num_group=bf*8, num_filter=bf*8, kernel=(3, 3), pad=(1, 1), stride=(2, 2), name="conv_7_dw") # 28/14
    conv_7 = Conv(conv_7_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_7") # 14/14

    conv_8_dw = Conv(conv_7, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_8_dw") # 14/14
    conv_8 = Conv(conv_8_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_8") # 14/14
    conv_9_dw = Conv(conv_8, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_9_dw") # 14/14
    conv_9 = Conv(conv_9_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_9") # 14/14
    conv_10_dw = Conv(conv_9, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_10_dw") # 14/14
    conv_10 = Conv(conv_10_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_10") # 14/14
    conv_11_dw = Conv(conv_10, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_11_dw") # 14/14
    conv_11 = Conv(conv_11_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_11") # 14/14
    conv_12_dw = Conv(conv_11, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_12_dw") # 14/14
    conv_12 = Conv(conv_12_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_12") # 14/14

    conv_13_dw = Conv(conv_12, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1,1), name="conv_13_dw") # 14/7
    conv_13 = Conv(conv_13_dw, num_filter=bf*32, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_13") # 7/7
    conv_14_dw = Conv(conv_13, num_group=bf*32, num_filter=bf*32, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_14_dw") # 7/7
    conv_14 = Conv(conv_14_dw, num_filter=bf*32, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_14") # 7/7
    return conv_14 

def get_mobilenet_text_conv(data):
    """
    shared convolutional layers
    :param data: Symbol
    :return: Symbol
    """
    bf = 32
    conv_1 = Conv(data, num_filter=bf, kernel=(3, 3), pad=(1, 1), stride=(2, 2), name="conv_1") # 224/112
    conv_2_dw = Conv(conv_1, num_group=bf, num_filter=bf, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_2_dw") # 112/112
    conv_2 = Conv(conv_2_dw, num_filter=bf*2, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_2") # 112/112
    conv_3_dw = Conv(conv_2, num_group=bf*2, num_filter=bf*2, kernel=(3, 3), pad=(1, 1), stride=(2, 2), name="conv_3_dw") # 112/56
    conv_3 = Conv(conv_3_dw, num_filter=bf*4, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_3") # 56/56
    conv_4_dw = Conv(conv_3, num_group=bf*4, num_filter=bf*4, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_4_dw") # 56/56
    conv_4 = Conv(conv_4_dw, num_filter=bf*4, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_4") # 56/56
    conv_5_dw = Conv(conv_4, num_group=bf*4, num_filter=bf*4, kernel=(3, 3), pad=(1, 1), stride=(2, 2), name="conv_5_dw") # 56/28
    conv_5 = Conv(conv_5_dw, num_filter=bf*8, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_5") # 28/28
    conv_6_dw = Conv(conv_5, num_group=bf*8, num_filter=bf*8, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_6_dw") # 28/28
    conv_6 = Conv(conv_6_dw, num_filter=bf*8, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_6") # 28/28
    conv_7_dw = Conv(conv_6, num_group=bf*8, num_filter=bf*8, kernel=(3, 3), pad=(1, 1), stride=(2, 2), name="conv_7_dw") # 28/14
    conv_7 = Conv(conv_7_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_7") # 14/14

    conv_8_dw = Conv(conv_7, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_8_dw") # 14/14
    conv_8 = Conv(conv_8_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_8") # 14/14
    conv_9_dw = Conv(conv_8, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_9_dw") # 14/14
    conv_9 = Conv(conv_9_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_9") # 14/14
    conv_10_dw = Conv(conv_9, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_10_dw") # 14/14
    conv_10 = Conv(conv_10_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_10") # 14/14
    conv_11_dw = Conv(conv_10, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_11_dw") # 14/14
    conv_11 = Conv(conv_11_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_11") # 14/14
    conv_12_dw = Conv(conv_11, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_12_dw") # 14/14
    conv_12 = Conv(conv_12_dw, num_filter=bf*16, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_12") # 14/14

    conv_13_dw = Conv(conv_12, num_group=bf*16, num_filter=bf*16, kernel=(3, 3), pad=(1, 1), stride=(1,1), name="conv_13_dw") # 14/7
    conv_13 = Conv(conv_13_dw, num_filter=bf*32, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_13") # 7/7
    conv_14_dw = Conv(conv_13, num_group=bf*32, num_filter=bf*32, kernel=(3, 3), pad=(1, 1), stride=(1, 1), name="conv_14_dw") # 7/7
    conv_14 = Conv(conv_14_dw, num_filter=bf*32, kernel=(1, 1), pad=(0, 0), stride=(1, 1), name="conv_14") # 7/7
    return conv_14 


def get_vgg_text_conv(data):
    """
    shared convolutional layers
    :param data: Symbol
    :return: Symbol
    """
    # group 1
    conv1_1 = mx.symbol.Convolution(
        data=data, kernel=(3, 3), pad=(1, 1), num_filter=64, workspace=2048, name="conv1_1")
    relu1_1 = mx.symbol.Activation(data=conv1_1, act_type="relu", name="relu1_1")
    conv1_2 = mx.symbol.Convolution(
        data=relu1_1, kernel=(3, 3), pad=(1, 1), num_filter=64, workspace=2048, name="conv1_2")
    relu1_2 = mx.symbol.Activation(data=conv1_2, act_type="relu", name="relu1_2")
    pool1 = mx.symbol.Pooling(
        data=relu1_2, pool_type="max", kernel=(2, 2), stride=(2, 2), name="pool1")

#112
    # group 2
    conv2_1 = mx.symbol.Convolution(
        data=pool1, kernel=(3, 3), pad=(1, 1), num_filter=128, workspace=2048, name="conv2_1")
    relu2_1 = mx.symbol.Activation(data=conv2_1, act_type="relu", name="relu2_1")
    conv2_2 = mx.symbol.Convolution(
        data=relu2_1, kernel=(3, 3), pad=(1, 1), num_filter=128, workspace=2048, name="conv2_2")
    relu2_2 = mx.symbol.Activation(data=conv2_2, act_type="relu", name="relu2_2")
    pool2 = mx.symbol.Pooling(
        data=relu2_2, pool_type="max", kernel=(2, 2), stride=(2, 2), name="pool2")
    # group 3
#56
    conv3_1 = mx.symbol.Convolution(
        data=pool2, kernel=(3, 3), pad=(1, 1), num_filter=256, workspace=2048, name="conv3_1")
    relu3_1 = mx.symbol.Activation(data=conv3_1, act_type="relu", name="relu3_1")
    conv3_2 = mx.symbol.Convolution(
        data=relu3_1, kernel=(3, 3), pad=(1, 1), num_filter=256, workspace=2048, name="conv3_2")
    relu3_2 = mx.symbol.Activation(data=conv3_2, act_type="relu", name="relu3_2")
    conv3_3 = mx.symbol.Convolution(
        data=relu3_2, kernel=(3, 3), pad=(1, 1), num_filter=256, workspace=2048, name="conv3_3")
    relu3_3 = mx.symbol.Activation(data=conv3_3, act_type="relu", name="relu3_3")
    pool3 = mx.symbol.Pooling(
        data=relu3_3, pool_type="max", kernel=(2, 2), stride=(2, 2), name="pool3")
#28
    # group 4
    conv4_1 = mx.symbol.Convolution(
        data=pool3, kernel=(3, 3), pad=(1, 1), num_filter=512, workspace=2048, name="conv4_1")
    relu4_1 = mx.symbol.Activation(data=conv4_1, act_type="relu", name="relu4_1")
    conv4_2 = mx.symbol.Convolution(
        data=relu4_1, kernel=(3, 3), pad=(1, 1), num_filter=512, workspace=2048, name="conv4_2")
    relu4_2 = mx.symbol.Activation(data=conv4_2, act_type="relu", name="relu4_2")
    conv4_3 = mx.symbol.Convolution(
        data=relu4_2, kernel=(3, 3), pad=(1, 1), num_filter=512, workspace=2048, name="conv4_3")
    relu4_3 = mx.symbol.Activation(data=conv4_3, act_type="relu", name="relu4_3")
    pool4 = mx.symbol.Pooling(
        data=relu4_3, pool_type="max", kernel=(2, 2), stride=(2, 2), name="pool4")
#14
    # group 5
    conv5_1 = mx.symbol.Convolution(
        data=pool4, kernel=(3, 3), pad=(1, 1), num_filter=512, workspace=2048, name="conv5_1")
    relu5_1 = mx.symbol.Activation(data=conv5_1, act_type="relu", name="relu5_1")
    conv5_2 = mx.symbol.Convolution(
        data=relu5_1, kernel=(3, 3), pad=(1, 1), num_filter=512, workspace=2048, name="conv5_2")
    relu5_2 = mx.symbol.Activation(data=conv5_2, act_type="relu", name="relu5_2")
    conv5_3 = mx.symbol.Convolution(
        data=relu5_2, kernel=(3, 3), pad=(1, 1), num_filter=512, workspace=2048, name="conv5_3")
    relu5_3 = mx.symbol.Activation(data=conv5_3, act_type="relu", name="relu5_3")
#14

    return relu5_3


def get_vgg_text_rpn(data, label, bbox_target, bbox_weight, num_anchors=10):
    """
    Region Proposal Network with VGG
    :param num_anchors: used to determine output size
    :return: Symbol
    """

    # shared convolutional layers
    relu5_3 = get_mobilenet_text_conv(data)
    _,relu_shape,_ = relu5_3.infer_shape_partial()
    shape = relu_shape[0]

    # RPN
    rpn_conv = mx.symbol.Convolution(
        data=relu5_3, kernel=(3, 3), pad=(1, 1), num_filter=512, name="rpn_conv_3x3")

    bilstm = rnn.BidirectionalCell(
        rnn.LSTMCell(128, prefix="l_"),
        rnn.LSTMCell(128, prefix='r_')
    )
    #mx.symbol.RNN
    rpn_conv_t = mx.symbol.transpose(rpn_conv, axes=(0, 2, 3, 1))
    rpn_conv_t = mx.symbol.reshape(rpn_conv_t, shape=(-3, -2))

    lstm_o, _ = bilstm.unroll(shape[0] * shape[3], rpn_conv_t, layout='NTC', merge_outputs=True)
    pred = mx.sym.FullyConnected(data=lstm_o, num_hidden=512, flatten=False, name='lstm_proj')
    pred = mx.sym.reshape(pred, shape=(shape[0], shape[2], shape[3], 512))
    pred = mx.symbol.transpose(pred, axes=(0, 3, 1, 2))

    rpn_relu = mx.symbol.Activation(data=pred, act_type="relu", name="rpn_relu")
    rpn_cls_score = mx.symbol.Convolution(
        data=rpn_relu, kernel=(1, 1), pad=(0, 0), num_filter=2 * num_anchors, name="rpn_cls_score")
    rpn_bbox_pred = mx.symbol.Convolution(
        data=rpn_relu, kernel=(1, 1), pad=(0, 0), num_filter=4 * num_anchors, name="rpn_bbox_pred")

    # prepare rpn data
    rpn_cls_score_reshape = mx.symbol.Reshape(
        data=rpn_cls_score, shape=(0, 2, -1, 0), name="rpn_cls_score_reshape")

    # classification
    cls_prob = mx.symbol.SoftmaxOutput(data=rpn_cls_score_reshape, label=label, multi_output=True,
                                       normalization='valid', use_ignore=True, ignore_label=-1, name="cls_prob")
    # bounding box regression
    bbox_loss_ = bbox_weight * mx.symbol.smooth_l1(name='bbox_loss_', scalar=3.0, data=(rpn_bbox_pred - bbox_target))
    bbox_loss = mx.sym.MakeLoss(name='bbox_loss', data=bbox_loss_, grad_scale=1.0 / config.TRAIN.RPN_BATCH_SIZE)
    # group output
    group = mx.symbol.Group([cls_prob, bbox_loss])
    return group


def get_vgg_text_rpn_test(data, im_info, num_anchors=10):
    """
    Region Proposal Network with VGG
    :param num_anchors: used to determine output size
    :return: Symbol
    """

    # shared convolutional layers
    relu5_3 = get_mobilenet_text_conv(data)
    _,relu_shape,_ = relu5_3.infer_shape_partial()
    shape = relu_shape[0]

    # RPN
    rpn_conv = mx.symbol.Convolution(
        data=relu5_3, kernel=(3, 3), pad=(1, 1), num_filter=512, name="rpn_conv_3x3")

    bilstm = rnn.BidirectionalCell(
        rnn.LSTMCell(128, prefix="l_"),
        rnn.LSTMCell(128, prefix='r_')
    )

    rpn_conv_t = mx.symbol.transpose(rpn_conv, axes=(0, 2, 3, 1))
    rpn_conv_t = mx.symbol.reshape(rpn_conv_t, shape=(-3, -2))

    lstm_o, _ = bilstm.unroll(shape[0] * shape[3], rpn_conv_t, layout='NTC', merge_outputs=True)
    pred = mx.sym.FullyConnected(data=lstm_o, num_hidden=512, flatten=False, name='lstm_proj')
    pred = mx.sym.reshape(pred, shape=(shape[0], shape[2], shape[3], 512))
    pred = mx.symbol.transpose(pred, axes=(0, 3, 1, 2))

    rpn_relu = mx.symbol.Activation(data=pred, act_type="relu", name="rpn_relu")
    rpn_cls_score = mx.symbol.Convolution(
        data=rpn_relu, kernel=(1, 1), pad=(0, 0), num_filter=2 * num_anchors, name="rpn_cls_score")
    rpn_bbox_pred = mx.symbol.Convolution(
        data=rpn_relu, kernel=(1, 1), pad=(0, 0), num_filter=4 * num_anchors, name="rpn_bbox_pred")

    # ROI Proposal
    rpn_cls_score_reshape = mx.symbol.Reshape(
        data=rpn_cls_score, shape=(0, 2, -1, 0), name="rpn_cls_score_reshape")
    rpn_cls_prob = mx.symbol.SoftmaxActivation(
        data=rpn_cls_score_reshape, mode="channel", name="rpn_cls_prob")
    rpn_cls_prob_reshape = mx.symbol.Reshape(
        data=rpn_cls_prob, shape=(0, 2 * num_anchors, -1, 0), name='rpn_cls_prob_reshape')
    if config.TEST.CXX_PROPOSAL:
        rois = mx.symbol.contrib.Proposal(
            cls_prob=rpn_cls_prob_reshape, bbox_pred=rpn_bbox_pred, im_info=im_info, name='rois', output_score=True,
            feature_stride=config.RPN_FEAT_STRIDE, scales=tuple(config.ANCHOR_SCALES), ratios=tuple(config.ANCHOR_RATIOS),
            rpn_pre_nms_top_n=config.TEST.PROPOSAL_PRE_NMS_TOP_N, rpn_post_nms_top_n=config.TEST.PROPOSAL_POST_NMS_TOP_N,
            threshold=config.TEST.PROPOSAL_NMS_THRESH, rpn_min_size=config.TEST.PROPOSAL_MIN_SIZE)
    else:
        rois = mx.symbol.Custom(
            cls_prob=rpn_cls_prob_reshape, bbox_pred=rpn_bbox_pred, im_info=im_info, name='rois', output_score=True,
            op_type='proposal', feat_stride=config.RPN_FEAT_STRIDE,
            scales=tuple(config.ANCHOR_SCALES), ratios=tuple(config.ANCHOR_RATIOS),
            rpn_pre_nms_top_n=config.TEST.PROPOSAL_PRE_NMS_TOP_N, rpn_post_nms_top_n=config.TEST.PROPOSAL_POST_NMS_TOP_N,
            threshold=config.TEST.PROPOSAL_NMS_THRESH, rpn_min_size=config.TEST.PROPOSAL_MIN_SIZE)
    # rois = group[0]
    # score = group[1]

    group = rois #mx.sym.Group([rois, rpn_cls_prob_reshape, rpn_bbox_pred])

    return group

