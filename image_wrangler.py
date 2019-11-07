import pandas as pd
import shutil, os, random, re
from pathlib import Path


def no_occ(csv, sample = 25, name = 'anonXXX'):
        """ Fuction that removes the occuled frames (in csv) and 
        subsets the remaining imges by a user defined factor"""
        home = str(Path.home())   
        #reads no ocultion csv
        df= pd.read_csv(csv)
        df_no_occlusion = df[df['class'] == 'no_occlusion']

        #converts data_frame to list
        files = df_no_occlusion['filename'].to_list()

        #randomly down samples the no_occlusion list by factor (defult 25)
        sampled_files = random.sample(files, round(len(files)/sample))

        os.makedirs(f'no_occlusion_{name}_sampled', exist_ok = True)

        dest = f'{home}/no_occlusion_{name}_sampled'

        for img in sampled_files:
                shutil.copy(f'{home}/{img}', dest)

        print(f'''Non occluded subset complete!!\n
        Downsample rate: {sample}\n
        Output dir: {dest}''')


def mask_tidy(directory):
        """ Fuction that removes the ..._watershed and _color png files 
        from PixelAnnotationTool and moves mask.png files into ...dir/mask/"""
        home = str(Path.home())
        os.chdir(f'{home}/{directory}')

        #(name00 x _ nx (_watershed *or* _color)_mask.png)
        patten= re.compile(r'anon\d{3}.\d+(_watershed|_color)_mask.png') 

        files = os.listdir(f'{home}/{directory}')
        matches = patten.finditer(str(files))

        print('Files that have been removed... hope you got the regex right! \n')

        #removes _watershed and _color .png 
        for match in matches:
                os.remove(match.group(0))
                print(f'{match.group(0)} removed')

        print('\nFiles that have been moved to ...files\n')

        patten2= re.compile(r'anon\d{3}.\d+_mask.png')
        matches2 = patten2.findall(str(files))

        #makes masks dir
        os.makedirs('masks', exist_ok= True)

        dest = f'{home}/{directory}/masks'

        #moves masks.png to .../masks/
        for match in matches2:
                shutil.move(match, dest)
                print(f'{match} moved to .../mask')
                
def mask_tidyer(target_dir):
    """ Sorts your anoated images into 'mask' and 'image' folders, using copy"""
    
    target_dir = Path(target_dir)
    os.chdir(target_dir)
    
    mask_patten= re.compile(r'anon\d{3}.\d+_mask.png')
    
    all_files = os.listdir(target_dir)
    mask_matches = mask_patten.findall(str(all_files))
    
    img_matches = []
    
    for img in mask_matches:
        img_file = f'{img[:-9]}.png'
        img_matches.append(img_file)
    
    os.makedirs('masks',exist_ok=True)
    
    for mask_file in mask_matches:
        shutil.copy(mask_file, target_dir/'masks')
        print(f'{mask_file} coppied to {target_dir}/mask')

    os.makedirs('images',exist_ok=True)
    
    for img_file in img_matches:
        shutil.copy(img_file, target_dir/'images')
        print(f'{img_file} moved to {target_dir}/images')
        
        

def mask_floor(target_dir):
    """ re-sets your mask to 0, 1 vaules"""
    target_dir = Path(target_dir)
    os.chdir(target_dir)
    
    all_files = os.listdir(target_dir)
    if '.DS_Store' in all_files:
        all_files.remove('.DS_Store')

    #os.makedirs('mask_floor',exist_ok= True)
    
    for img_file in all_files:
        # open image 
        im = imageio.imread(img_file)
        #set_trace()
        arr = np.where(im > 0, 1, 0)
        arr = arr.astype('uint8')
        print(f'{img_file} floored')
        
        imageio.imwrite(target_dir/img_file, arr)
