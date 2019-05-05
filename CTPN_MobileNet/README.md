# Connectionist Text Proposal Network with MobileNet Backbone

## Introduction
CTPN is a nice scene text detection method.

## Training
1. Execute script init.sh(init.bat on Windows) to initialize project.
2. Download pretrained model from [here]() into ```model``` folder.
3. Download dataset from [baidu yun](). This dataset is already prepared by **@eragonruan** to fit CTPN.
4. Unzip the dataset downloaded to ```'VOCdevkit'``` folder, and set both ```default.root_path``` and ```default.dataset_path``` in ```rcnn/config.py``` to ```'<somewhere>/VOCdevkit/VOC2007'```. You can also change other hyperparams in ```rcnn/config.py```.
5. Run ```python train_ctpn.py``` to train. Run ```python train_ctpn.py --gpus '0' --rpn_lr 0.01 --no_flip 0``` to train model on gpu 0 with learning rate 0.01 and with flip data augmentation.

## Testing
Use ```python demo_ctpn.py --image "<your_image_path>" --prefix model/rpn1 --epoch 8``` to test.

## Our results
`NOTICE:` all the photos used below are collected from the internet. If it affects you, please contact me to delete them.
<img src="/results/demo.jpg" width=320 height=240 /><img src="/results/demo2.jpg" width=320 height=240 />
<img src="/results/demo3.jpg" width=320 height=240 /><img src="/results/demo4.jpg" width=320 height=240 />
<img src="/results/demo5.jpg" width=320 height=240 />
<img src="/results/demo6.jpg" width=320 height=480 />
<img src="/results/demo7.jpg" width=480 height=320/>
<img src="/results/demo8.jpg" width=320 height=480/><img src="/results/demo9.jpg" width=320 height=480/>
<img src="/results/demo10.jpg" />

## Requirements: Hardware
Any NVIDIA GPUs with at least **2GB** memory should be OK.

## References
1. https://github.com/chinakook/CTPN.mxnet
1. https://github.com/tianzhi0549/CTPN
2. https://github.com/eragonruan/text-detection-ctpn

