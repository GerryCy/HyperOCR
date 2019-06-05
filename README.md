## HyperOCR

A Simple light-weight text detection implementation based on CTPN with mobilenet1.0 backbone. 

### Startup

`python demo_ctpn.py --image textx.jpg --prefix model/rpn1 --epoch 80 --gpu 0 --vis`

### Demo Image

![test_output](images/test_output.jpg)

### Training Tips
1. Execute script init.sh(init.bat on Windows) to initialize project.
2. Download pretrained model from [here]() into ```model``` folder.
3. Download dataset from [baidu yun](). This dataset is already prepared by **@eragonruan** to fit CTPN.
4. Unzip the dataset downloaded to ```'VOCdevkit'``` folder, and set both ```default.root_path``` and ```default.dataset_path``` in ```rcnn/config.py``` to ```'<somewhere>/VOCdevkit/VOC2007'```. You can also change other hyperparams in ```rcnn/config.py```.
5. Run ```python train_ctpn.py``` to train. Run ```python train_ctpn.py --gpus '0' --rpn_lr 0.01 --no_flip 0``` to train model on gpu 0 + with learning rate 0.01 and with flip data augmentation.


### Tips

- This is an experimental , maybe cannot achieve good effect.
- The code based on <https://github.com/chinakook/CTPN.mxnet>

### TODO

- new implementation based on PSENET

- Text region feature extractor for  template based ocr.
- OCR model.

