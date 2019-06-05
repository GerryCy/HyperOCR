## HyperOCR

A Simple light-weight text detection implementation based on CTPN with mobilenet1.0 backbone. 

### Startup

`python demo_ctpn.py --image textx.jpg --prefix model/rpn1 --epoch 80 --gpu 0 --vis`

### Demo Image

![test_output](images/test_output.jpg)

### Tips

- This is an experimental , maybe cannot achieve good effect.
- The code based on <https://github.com/chinakook/CTPN.mxnet>

### TODO

- new implementation based on PSENET

- Text region feature extractor for  template based ocr.
- OCR model.

