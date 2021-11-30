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
#         print(prefix + path)
        if os.path.isdir(path):
            print_files_in_dir(path, prefix + "    ")
#         print(path)
        filedir.append(path) # 하위폴더의 세부 파일경로를 리스트에 저장

if __name__ == "__main__":
    root_dir = workdir
    # root_dir = "W:/PWV_deID_IMAGE/CASE_TEST/TEST6-1"
    print_files_in_dir(root_dir, "")

filelist = [filedir for filedir in filedir if '.PNG' in filedir.upper()]

filelist

#%%
img_list = []

# 1st page set
img_path = filelist[0]
im_buf = Image.open(img_path)
cvt_rgb_0 = im_buf.convert('RGB')

for file in filelist:
    im_buf = Image.open(file)
    cvt_rgb = im_buf.convert('RGB')
    img_list.append(cvt_rgb)

img_list

# %%
del img_list[0]
cvt_rgb_0.save('{}/test.pdf'.format(workdir),save_all=True, append_images=img_list)
# %%
