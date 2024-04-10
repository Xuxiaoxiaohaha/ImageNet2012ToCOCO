import scipy.io
import json
import sys
from tqdm import tqdm
"""
    用于生成后续转化需要的数据
"""
meta_path = './resources/meta.mat'
wnid_2_id_name_path = './resources/wnid_2_id_name_path.json' # the path of preprocess file
meta_path = sys.argv[1]
wnid_2_id_name_path = sys.argv[2]

synsets = scipy.io.loadmat(meta_path)['synsets']
"""
{
    "WNID":[ILSVRC2012_ID,class_name]
}
"""
if __name__ == '__main__':
    WNID2ID = {}
    for s in tqdm(synsets):
        wnid = s[0][1][0] # str
        il_id = int(s[0][0][0]) # int
        class_name = s[0][2][0] # str
        WNID2ID[wnid] = [il_id,class_name]

    with open(wnid_2_id_name_path,'w') as f:
        json.dump(WNID2ID,f)