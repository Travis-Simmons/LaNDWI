#!/usr/bin/env python3
"""
Author : Travis Simmons <travissimmons@email.arizona.edu>
Date   : 2/20/2021
Purpose: 
"""

import argparse
import os
import sys
import cv2
import glob
import tarfile
import gdal
import shutil
import statistics
import rasterio as rio
import matplotlib.pyplot as plt
from rasterio.plot import show
from moviepy.editor import ImageSequenceClip



# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('indir',
                        metavar='indir',
                        type = str,
                        help="Directory containing tar'd or foldered lansat data")



    parser.add_argument('-b',
                        '--bounding_box',
                        help='GPS Bounding Box for sampling area, [xmin, xmax, ymin, ymax]',
                        metavar='bounding_box',
                        type= int,
                        nargs = '+',
                        required = True
                        )

    parser.add_argument('-c',
                        '--how_strict',
                        help='How strict do you want the cloud recognition to be, the lower the more strict',
                        metavar='how_strict',
                        type=float,
                        default=0.7)

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    # Variables

    # Directory containing tar'd or foldered lansat data
    # indir = r'D:\lansat\Bulk Order Large_lansat_8\test'

    # How strict do you want the cloud recognition to be, the lower the more strict
    # how_strict= 0.7


    # # GPS Bounding Box for sampling area, [xmin, xmax, ymin, fymax]
    # x1 = 160785
    # y1 = 3467622
    # x2 = 169515
    # y2 = 3462902
    bb = args.bounding_box
    x1 = bb[0]
    x2 = bb[1]
    y1 = bb[2]
    y2 = bb[3]




    #--------------------------------------------------------------------------

    # -Main-


    # If you ahve tars still in the directory, these will grab them and untar them
    
    tars = glob.glob(os.path.join(args.indir ,'*.tar'))
    print('Extracting tar files...')

    # if len(tars) > 1:
    for tar in tars:
        out_file = tar.split('.')[0]


        # making a file for the tars to land
        if not os.path.exists(out_file):
            os.makedirs(out_file)
        one_tar = tarfile.open(tar)
        one_tar.extractall(out_file)
            
            
    # # Function to take a lansat image and crop it to the sample area in Baker County, GA  

    lv1 = glob.glob(os.path.join(args.indir , '*'))
    # print(lv1)


    print('Cropping Lansat Images...')
    for folder in lv1:

        if os.path.isdir(folder):
            folder_name = os.path.basename(folder)


            if folder_name.startswith('L'):
                cnt = 1
                # print(os.path.join(folder, '*.TIF'))
                TIFs = glob.glob(os.path.join(folder, '*.TIF'))
                # print(TIFs)

                date = folder.split("_")[-4]

                outdir = os.path.join(args.indir, date)

                if os.path.isdir(outdir):
                    outdir = outdir + f'_{cnt}'
                    cnt += 1

                os.mkdir(outdir)

                # Itterating through the image list
                for im in TIFs:
                    # print(im)

                    split = im.split('_')
                    date = split[-6]
                    band = split[-1]
                    filename = date+'_'+band



            #         print(filename)

                    # Opening each one in GDAL
                    img = gdal.Open(im)

                    # print('translating')
                    gdal.Translate(os.path.join(outdir, filename), img, projWin = [x1,y1,x2,y2])

    lv2 = glob.glob(os.path.join(args.indir, '*'))

    if not os.path.exists(os.path.join(args.indir, 'cloudy')):
            os.makedirs(os.path.join(args.indir, 'cloudy'))

    if not os.path.exists(os.path.join(args.indir, 'clear')):
            os.makedirs(os.path.join(args.indir, 'clear'))
            
    if not os.path.exists(os.path.join(args.indir, 'NDWI')):
            os.makedirs(os.path.join(args.indir, 'NDWI'))
            
    for date_folder in lv2:

        if (os.path.isdir(date_folder)):
            date = os.path.basename(date_folder)
            
            
            if not date.startswith('L'):
                band1_imgs = glob.glob(os.path.join(date_folder , '*B1.TIF'))      

                for img in band1_imgs:
                    filename = os.path.basename(img)
    #                     print(img)
    #                     pil_im = Image.open(img)
    #                     display(pil_im)
                    # Open it, histogram mean, sort
                    testing_img = cv2.imread(img)
                    testing_vals = testing_img.mean(axis=2).flatten()
                    testing_mode = statistics.mode(testing_vals)
                    testing_average = statistics.mean(testing_vals)

                    print('Testing mode: ',testing_mode)
                    print('Testing Average: ', testing_average)
                    if testing_mode == 0.0:
                        print("Black image")

                    if (len([1 for i in testing_vals if i > testing_mode]) >= len(testing_vals)*args.how_strict) or (testing_average > 35) or (testing_average < 10):
                        print("Cloudy image")

                        print(date)
                        shutil.move(os.path.join(args.indir, date), os.path.join(args.indir, 'cloudy'))

                    else:
                        print("Clear image")
                        print(date)

                        # do NDWI Then move


                        # Calculation
                        # NDWI = (3 - 5)/(3 + 5)
                        date_folder
                        band3 = glob.glob(os.path.join(date_folder, '*B3.TIF'))
                        band5 = glob.glob(os.path.join(date_folder, '*B5.TIF'))
                        b3 = rio.open(band3[0])
                        b5 = rio.open(band5[0])
                        green = b3.read()
                        nir = b5.read()
                        ndwi = (nir.astype(float)-green.astype(float))/(nir+green)




                        # Plotting
                        fig, ax = plt.subplots(1, figsize=(12, 10))
                        show(ndwi, ax=ax, cmap="coolwarm_r")
                        plt.savefig(os.path.join(date_folder, date + '_NDWI.TIF'))
                        plt.savefig(os.path.join(args.indir, 'NDWI' , date + '_NDWI.TIF'))
                        
                        b3.close()
                        b5.close()


                        shutil.move(os.path.join(args.indir,  date), os.path.join(args.indir, 'clear'))

    ndwi_TIFs = glob.glob(os.path.join(args.indir, 'NDWI', '*.TIF'))

    for i in ndwi_TIFs:
        print('start',i)
        pic_name = os.path.basename(i)
        pic_name = pic_name.replace('.TIF', '')
        # print('after split', pic_name)
        # pic_name = pic_name.split('\\')[-1]
        print('befre writing', pic_name)
        img = cv2.imread(i)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,pic_name,(150,230), font, 1,(0,0,0),2)
        cv2.imwrite(i, img)

        
    clip = ImageSequenceClip(ndwi_TIFs,fps=.25)
    clip.write_gif(os.path.join(args.indir, 'NDWI', 'final.gif'))




# --------------------------------------------------
if __name__ == '__main__':
    main()
