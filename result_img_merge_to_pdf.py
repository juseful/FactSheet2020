#%%
from PIL import Image
import os

#%%
workdir = ''

filedir = []

def print_files_in_dir(root_dir, prefix):
    files = os.listdir(root_dir)
    for file in files:
        path = os.path.join(root_dir, file)
        if os.path.isdir(path):
            print_files_in_dir(path, prefix + "    ")
        filedir.append(path) # 하위폴더의 세부 파일경로를 리스트에 저장

if __name__ == "__main__":
    root_dir = workdir
    print_files_in_dir(root_dir, "")

filelist = [filedir for filedir in filedir if '.PNG' in filedir.upper()]

filelist

#%%
img_list = []

for file in filelist:
    im_buf = Image.open(file)
    cvt_rgb = im_buf.convert('RGB')
    img_list.append(cvt_rgb)

img_list

# %%
# in the order of image list
img_list[0].save('{}/test_21120102.pdf'.format(workdir),save_all=True, append_images=img_list[1:])
