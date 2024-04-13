import json
import os
from tqdm import tqdm
import sys

# gen_info gen_licenses gen_categories the same as val
def gen_info(my_data):
    my_data['info'] = {}
    my_data['info']['description'] = 'ImageNet 2012 Dataset'
    my_data['info']['url'] = 'https://image-net.org/'
    my_data['info']['version'] = '1.0'
    my_data['info']['year'] = 2012
    my_data['info']['contributor'] = ''
    my_data['info']['date_created'] = '2012'

def gen_licenses(my_data):
    my_data['licenses'] = []
    fake_license = {}
    fake_license['url'] = 'http://fakeurl'
    fake_license['id'] = 1
    fake_license['name'] = 'Fake License'
    my_data['licenses'].append(fake_license)

def gen_categories(my_data,wnid_2_id_name_path):
    my_data['categories'] = []
    with open(wnid_2_id_name_path,'r') as f:
        wnid_2_id_name_path = json.load(f)
    i = 0
    for k,v in wnid_2_id_name_path.items(): # ImageNet 2012 just take the top 1000
        my_data['categories'].append(dict(supercategory=v[1],id=v[0],name=v[1]))
        i += 1
        if i == 1000:
            break

def gen_images_gen_annotations_train(my_data,train_images_xml_dir_path,wnid_2_id_name_path):
    """
    train_images_xml_dir_path: the path of the directory
    path/train_images_xml_dir_path/
        /n01440764
            /n01440764_10040.xml
            /n01440764_xxxxx.xml
        /nxxxxxxxx
            ...
        /...
    """
    my_data['images'] = []
    my_data['annotations'] = []
    with open(wnid_2_id_name_path,'r') as f:
        wnid_2_id_name = json.load(f)
    annotation_id = 1
    image_id = 1
    xml_parent_dirs = os.listdir(train_images_xml_dir_path)
    for parent_dir in tqdm(xml_parent_dirs):
        try:
            category_id = int(wnid_2_id_name[parent_dir][0])
        except KeyError as e:
            print(f'KeyError: {e} in xml directory {parent_dir}')
            sys.exit()
        xml_files = os.listdir(os.path.join(train_images_xml_dir_path,parent_dir))
        for file in xml_files:
            # -- for images --  
            license = 1
            file_name = parent_dir + '/' + file.replace('xml','JPEG')
            coco_url = 'http://fakeurl'
            height = 0
            width = 0
            date_captured = '2012'
            flickr_url = 'http://fakeurl'
            # -- for annotations --
            segmentation = [[]]
            area = 0
            iscrowd = 0
            bbox = [] # xywh
            xmin = 0
            ymin = 0
            xmax = 0
            ymax = 0
            with open(os.path.join(train_images_xml_dir_path,parent_dir,file),'r') as f:
                lines = f.readlines()
            i = 0
            # -- for images --
            while i < len(lines):
                line = lines[i].strip()
                if 'height' in line:
                    height = int(line.split('>')[1].split('<')[0])
                elif 'width' in line:
                    width = int(line.split('>')[1].split('<')[0])
                elif 'object' in line:
                    break
                i += 1
            my_data['images'].append(dict(license=license,file_name=file_name,coco_url=coco_url,height=height,width=width,date_captured=date_captured,flickr_url=flickr_url,id=image_id))
            flag = False
            while i < len(lines):
                line = lines[i].strip()
                # -- for annotations --
                if '<object>' == line:
                    flag = True
                elif 'xmin' in line and flag:
                    xmin = int(line.split('>')[1].split('<')[0])
                elif 'ymin' in line and flag:
                    ymin = int(line.split('>')[1].split('<')[0])
                elif 'xmax' in line and flag:
                    xmax = int(line.split('>')[1].split('<')[0])
                elif 'ymax' in line and flag:
                    ymax = int(line.split('>')[1].split('<')[0])
                elif '</object>' == line:
                    flag = False
                    h = ymax - ymin
                    w = xmax - xmin
                    area = h * w
                    bbox = [xmin,ymin,w,h]
                    my_data['annotations'].append(dict(segmentation=segmentation,area=area,iscrowd=iscrowd,image_id=image_id,bbox=bbox,category_id=category_id,id=annotation_id))
                    annotation_id += 1
                i += 1
            image_id += 1

def gen_images_gen_annotations_val(my_data,val_images_xml_dir_path,wnid_2_id_name_path):
    """
    val_images_xml_dir_path: the path of the directory which contains the whole xml files of images
    path/val_images_xml_dir_path/
        /ILSVRC2012_val_00000001.xml
        /ILSVRC2012_val_00000002.xml
        /ILSVRC2012_val_xxxxxxxx.xml
        /...
    """
    my_data['images'] = []
    my_data['annotations'] = []
    xml_files = os.listdir(val_images_xml_dir_path)
    with open(wnid_2_id_name_path,'r') as f:
        wnid_2_id_name = json.load(f)
    annotation_id = 1
    image_id = 1
    for file in tqdm(xml_files):
        # -- for images --  
        license = 1
        file_name = file.replace('xml','JPEG')
        coco_url = 'http://fakeurl'
        height = 0
        width = 0
        date_captured = '2012'
        flickr_url = 'http://fakeurl'
        # -- for annotations --
        segmentation = [[]]
        area = 0
        iscrowd = 0
        bbox = [] # xywh
        category_id = 0
        xmin = 0
        ymin = 0
        xmax = 0
        ymax = 0
        with open(os.path.join(val_images_xml_dir_path,file),'r') as f:
            lines = f.readlines()
        i = 0
        # -- for images --
        while i < len(lines):
            line = lines[i].strip()
            if 'height' in line:
                height = int(line.split('>')[1].split('<')[0])
            elif 'width' in line:
                width = int(line.split('>')[1].split('<')[0])
            elif 'object' in line:
                break
            i += 1
        my_data['images'].append(dict(license=license,file_name=file_name,coco_url=coco_url,height=height,width=width,date_captured=date_captured,flickr_url=flickr_url,id=image_id))
        flag = False
        while i < len(lines):
            line = lines[i].strip()
            # -- for annotations --
            if '<object>' == line:
                flag = True
            elif 'name' in line and flag:
                try:
                    category_id = int(wnid_2_id_name[line.split('>')[1].split('<')[0]][0])
                except KeyError as e:
                    print(f'KeyError: {e} in xml file {file}')
                    sys.exit()
            elif 'xmin' in line and flag:
                xmin = int(line.split('>')[1].split('<')[0])
            elif 'ymin' in line and flag:
                ymin = int(line.split('>')[1].split('<')[0])
            elif 'xmax' in line and flag:
                xmax = int(line.split('>')[1].split('<')[0])
            elif 'ymax' in line and flag:
                ymax = int(line.split('>')[1].split('<')[0])
            elif '</object>' == line:
                flag = False
                h = ymax - ymin
                w = xmax - xmin
                area = h * w
                bbox = [xmin,ymin,w,h]
                my_data['annotations'].append(dict(segmentation=segmentation,area=area,iscrowd=iscrowd,image_id=image_id,bbox=bbox,category_id=category_id,id=annotation_id))
                annotation_id += 1
            i += 1
        image_id += 1

def convert2coco(my_data,wnid_2_id_name_path,images_xml_dir_path,output_path,mode='val'):
    gen_info(my_data)
    gen_licenses(my_data)
    gen_categories(my_data,wnid_2_id_name_path)
    if mode == 'train':
        gen_images_gen_annotations_train(my_data,images_xml_dir_path,wnid_2_id_name_path)
    elif mode == 'val':
        gen_images_gen_annotations_val(my_data,images_xml_dir_path,wnid_2_id_name_path)
    else:
        raise ValueError('Mode Error!')
    with open(output_path,'w') as f:
        json.dump(my_data,f)

wnid_2_id_name_path = './resources/wnid_2_id_name_path.json'
# val settings
val_images_xml_dir_path = './resources/xmls/val'
output_instances_ImageNet_val2012 = './resources/annotations/instances_ImageNet_val2012.json'
# train settings
train_images_xml_dir_path = './resources/xmls/train'
output_instances_ImageNet_train2012 = './resources/annotations/instances_ImageNet_train2012.json'

wnid_2_id_name_path = sys.argv[1]
output_instances_ImageNet_val2012 = sys.argv[2]
output_instances_ImageNet_train2012 = sys.argv[3]
val_images_xml_dir_path = sys.argv[4]
train_images_xml_dir_path = sys.argv[5]

def make_dir(file_path):
    directory, filename = os.path.split(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

make_dir(output_instances_ImageNet_val2012)
make_dir(output_instances_ImageNet_train2012)

if __name__ == '__main__':
    val_data = {} # my_data.keys() : "info" "licenses" "images" "annotations" "categories"
    train_data = {} # my_data.keys() : "info" "licenses" "images" "annotations" "categories"
    convert2coco(val_data,wnid_2_id_name_path,val_images_xml_dir_path,output_instances_ImageNet_val2012,'val')
    convert2coco(train_data,wnid_2_id_name_path,train_images_xml_dir_path,output_instances_ImageNet_train2012,'train')
    
