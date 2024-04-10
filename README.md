# ImageNetToCOCO
You can convert ImageNet to COCO by this repository(But only support Image classification and Object Detection).
# 中文
本项目以ImageNet2012为例，来生成COCO中的`instances_train.json`和`instances_val.json`文件，用于图片分类和目标检测任务（segmentation目前尚未支持）。
我们项目的文件布局如下所示。
```
|—— resources
    |—— meta.mat
    |—— xmls
        |—— train
            |—— n01440764
            |—— n07579787
        |—— val
|—— example
    |—— resources
        |—— meta.mat
        |—— wnid_2_id_name_path.json
        |—— xmls
            |—— train
                |—— n01440764
                |—— n07579787
            |—— val
        |—— annotations
            |—— instances_ImageNet_val2012.json
            |—— instances_ImageNet_train2012.json
|—— convert2COCO.py
|—— preprocess.py
|—— run.sh
```
## 快速开始
```bash
./run.sh
```
运行完毕后，`resources`目录将会变成`examples/resources`目录的样子，新生成了`wnid_2_id_name_path.json`、`annotations/instances_ImageNet_val2012.json`和`annotations/instances_ImageNet_train2012.json`三个文件。

其中`wnid_2_id_name_path.json`文件是由`preprocess.py`生成的中间文件，记录了从WNID到ILSVRC2012_ID和类名的映射。

```python
import json
with open('wnid_2_id_name_path.json','r') as f:
    data = json.load(f)
print(data.keys()) # set of WNID
print(data['n01440764']) # a list containing ILSVRC2012_ID and class_name
print(data['n01440764'][0]) # ILSVRC2012_ID
print(data['n01440764'][1]) # class_name
```
其中`instances_ImageNet_val2012.json`和`annotations/instances_ImageNet_train2012.json`是COCO所需要的json文件。
```python
from pycocotools.coco import COCO
coco = COCO('instances_ImageNet_val2012.json')
```
接下来，如果你想读取图片，你应该使你的图片文件结构如下所示：
```
|—— your_images_path
    |—— train
        |—— n01440764
            |—— n01440764_10040.JPEG
            |—— n01440764_xxxxx.JPEG
        |—— nyyyyyyy
            |—— nyyyyyyyy_xxxxx.JPEG
            |—— ...
        |—— ...
    |—— val
        |—— ILSVRC2012_val_00000001.xml
        |—— ILSVRC2012_val_00000002.xml
        |—— ILSVRC2012_val_xxxxxxxx.xml
```
然后你可以这样子读取图片:
```python
from pycocotools.coco import COCO
import os
from PIL import Image
coco = COCO('instances_ImageNet_val2012.json')
img_id = 1
path = coco.loadImgs(img_id)[0]['file_name']
root = 'your_images_path/val' # or 'your_images_path/train'
img = Image.open(os.path.join(self.root, path)).convert('RGB')
```

因此，对于你的完整的ImageNet2012来说，你所需要准备的数据格式如下所示，（如`resource`所示）：

```
|—— your_path/resources
    |—— meta.mat  # Get it by unzipping the Development Kit(Task 1 & 2).
    |—— xmls 
        |—— train # Get it by unzipping the Training bounding box annotations(Task 1 & 2 only)
            |—— n01440764
                |—— n01440764_10040.xml
                |—— n01440764_xxxxx.xml
            |—— nyyyyyyy
                |—— nyyyyyyyy_xxxxx.xml
                |—— ...
            |—— ...
        |—— val # Get it by unzipping the Validation bounding box annotations
            |—— ILSVRC2012_val_00000001.xml
            |—— ILSVRC2012_val_00000002.xml
            |—— ILSVRC2012_val_xxxxxxxx.xml
```

然后，通过在将三个文件`convert2COCO.py`、`preprocess.py`和`run.sh`拷贝到目录`your_path`下，

```
|—— your_path
    |—— resources
        |—— ...
    |—— convert2COCO.py
    |—— prprocess.py
    |—— run.sh
```

接着在`run.sh`中把`path`变量修改成`your_path`即可，最后运行`./run.sh`，便可得到`your_path/resources/annoations/instances_ImageNet_train2012.json`、`your_path/resources/annoations/instances_ImageNet_val2012.json`和`your_path/resources/wnid_2_id_name_path.json`三个文件。

若想读取图片，则如上述示例使你的图片数据格式如下所示：

```
|—— your_images_path
    |—— train  # Get it by unzipping the Training images(Task1 & 2), You need to unzip the files in this directory to get the JPEG 
        |—— n01440764
            |—— n01440764_10040.JPEG
            |—— n01440764_xxxxx.JPEG
        |—— nyyyyyyy
            |—— nyyyyyyyy_xxxxx.JPEG
            |—— ...
        |—— ...
    |—— val  # Get it by unzipping the Validation images
        |—— ILSVRC2012_val_00000001.xml
        |—— ILSVRC2012_val_00000002.xml
        |—— ILSVRC2012_val_xxxxxxxx.xml
```

然后根据如下示例读取文件：

```python
from pycocotools.coco import COCO
import os
from PIL import Image
coco = COCO('instances_ImageNet_val2012.json')
img_id = 1
path = coco.loadImgs(img_id)[0]['file_name']
root = 'your_images_path/val' # or 'your_images_path/train'
img = Image.open(os.path.join(self.root, path)).convert('RGB')
```
