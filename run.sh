#!/bin/bash
path="."
meta_path="${path}/resources/meta.mat"
wnid_2_id_name_path="${path}/resources/wnid_2_id_name_path.json"

val_output_path="${path}/resources/annotations/instances_ImageNet_val2012.json"
train_output_path="${path}/resources/annotations/instances_ImageNet_train2012.json"
val_images_xml_dir_path="${path}/resources/xmls/val"
train_images_xml_dir_path="${path}/resources/xmls/train"

python preprocess.py ${meta_path} ${wnid_2_id_name_path}
python convert2COCO.py ${wnid_2_id_name_path} ${val_output_path} ${train_output_path} ${val_images_xml_dir_path} ${train_images_xml_dir_path}