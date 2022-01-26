from pycocotools.coco import COCO
import json
import os
import numpy as np
import argparse

def get_ids(data, imgIds):
    Ids = []
    for c,i in enumerate(imgIds):
        print(c)
        id_dict = {}
        id_dict['bbox_category'] = []
        id_dict['id'] = i
        for val in data['annotations']:
            if val['image_id'] == i and val['category_id'] == 1:
                bbox = ' '.join(map(str, val['bbox']))
                label = str(val['category_id'])
                ann = label + " " + bbox
                id_dict['bbox_category'].append(ann)
        Ids.append(id_dict)
    return Ids

def get_label(data, val_dict):
    Ids = []
    for i in val_dict:
        id_dict = {}
        id_dict['id'] = i
        id_dict['bbox_category'] = []
        for val in data['annotations']:
            if val['image_id'] == i:
                bbox = ' '.join([str(elem) for elem in val['bbox']])
                label = str(val['category_id'])
                ann = label + " " + bbox
                id_dict['bbox_category'].append(ann)
    Ids.append(id_dict)
    return Ids

def new_bbox(bbox):
    bbox[0] = (bbox[0]+bbox[2])/2
    bbox[1] = (bbox[1]+bbox[3])/2
    minb, maxb = min(bbox), max(bbox)
    bbox = [round((a-minb)/(maxb-minb),2) for a in bbox]  
    print(bbox) 
    return bbox

def get_val_dict(data, imgIds):
    val_dict = {}
    for val in data['annotations']:
        if val['image_id'] in imgIds and val['category_id'] ==1:
            print(val['image_id'])
            bbox = new_bbox(val['bbox'])
            bbox = ' '.join([str(elem) for elem in bbox])
            ann =  str(val['category_id']) + " " + bbox
            if val['image_id'] not in val_dict:
                val_dict[val['image_id']] = [ann]
            else:
                val_dict[val['image_id']].append(ann)
            # print(val_dict[val['image_id']])       
            
    return val_dict
            
def new_imgs(val_dict,sc_img_dir_path,des_img_dir_path):
    for i in val_dict:     
        img_file_name = str(i).zfill(12) +'.jpg'
        sc_img_file_path = os.path.join(sc_img_dir_path, img_file_name)
        des_img_file_path = os.path.join(des_img_dir_path, img_file_name)

        if (os.path.isfile(sc_img_file_path)):
            os.rename(sc_img_file_path, des_img_file_path)

def new_annotations(Ids,ann_dir_path):  
    for id, bbox in Ids.items():   
        ann_file_name = str(id).zfill(12) +'.txt'
        ann_file_path = os.path.join(ann_dir_path,ann_file_name)
        if not os.path.isfile(ann_file_path):
            with open(ann_file_path, 'a') as f:
                for b in bbox:
                    f.write(b)
                    f.write('\n')



def main(args):

    dataDir= args.master_dir
    filter_coco = args.filter_dir
    filter_labels = args.labels_dir
    dataType= args.datatype
    
    annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)
    sc_img_dir_path = '{}/{}'.format(dataDir,dataType)
    des_img_dir_path = '{}/{}'.format(filter_coco, dataType)
    ann_dir_path = '{}/{}'.format(filter_labels,dataType)
    
    file_data = open('{}/annotations/{}'.format(dataDir,args.jsonfile))
    data = json.load(file_data)

    coco=COCO(annFile)
    filterClasses = args.category

    catIds = coco.getCatIds(catNms=filterClasses) 
    imgIds = coco.getImgIds(catIds=catIds)

    val_dict = get_val_dict(data, imgIds)
    new_imgs(val_dict,sc_img_dir_path,des_img_dir_path)
    new_annotations(val_dict,ann_dir_path)
    print("Total Items filtered: ", len(val_dict))
    print("Total Images files filtered : ", len([fil for fil in os.listdir(des_img_dir_path)]))
    print("Total Annotation files filtered : ", len([fil for fil in os.listdir(ann_dir_path)]))





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter COCO JSON: ")
    parser.add_argument("-m", "--master_dir", default = "/Users/breenda/Desktop/coco/coco-manager/coco",help="")
    parser.add_argument("-f", "--filter_dir", default = "/Users/breenda/Desktop/coco/coco-manager/coco_new/images",help="")
    parser.add_argument("-l", "--labels_dir", default = "/Users/breenda/Desktop/coco/coco-manager/coco_new/labels_per",help="")
    parser.add_argument("-j", "--jsonfile", default = "instances_train2017.json",help="")
    parser.add_argument("-d", "--datatype", default = "train2017",help="")
    parser.add_argument("-c", "--category", default = "person",help="")
    args = parser.parse_args()
    main(args)
