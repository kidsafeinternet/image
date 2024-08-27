# image
NSFW/SFW Image classification.

## Table of Contents
- [Confusion](#confusion)
- [Models](#models)
- [Datasets](#datasets)

## Confusion
All of the datasets were run on 5 epochs and 20% of the data was used for validation. For all of the datasets above the large dataset, 5% of the data was used for validation. 

### Small Dataset
5 images of each class. 10 images total.

![Small Dataset Confusion Matrix](matrixes/small_set_confusion_matrix.png)

### Medium Dataset
100 images of each class. 200 images total.

![Medium Dataset Confusion Matrix](matrixes/medium_set_confusion_matrix.png)

### Large Dataset
500 images of each class. 1000 images total.

![Large Dataset Confusion Matrix](matrixes/large_set_confusion_matrix.png)

### XL Dataset
10,000 images of each class. 20,000 images total.

![XL Dataset Confusion Matrix](matrixes/xl_set_confusion_matrix.png)

## Models

### Small
NONE

### Medium
[zanderlewis/nsfw_medium](https://huggingface.co/zanderlewis/nsfw_medium)

### Large
NONE YET

### XL
[zanderlewis/nsfw_xl](https://huggingface.co/zanderlewis/nsfw_xl)

## Datasets

### Small
NONE

### Medium
[zanderlewis/nsfw_detection_medium](https://huggingface.co/datasets/zanderlewis/nsfw_detection_medium)

### Large
[zanderlewis/nsfw_detection_large](https://huggingface.co/datasets/zanderlewis/nsfw_detection_large)

### XL
[zanderlewis/nsfw_detection_xl](https://huggingface.co/datasets/zanderlewis/nsfw_detection_xl)
