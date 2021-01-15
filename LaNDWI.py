#!/usr/bin/env python3
"""
Author : Travis Simmons <920117874@student.ccga.edu>
Date   : 1/15/2021
Purpose: Automatically process Landsat 8 NDWI analysis
"""

import argparse
import os
import sys


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('indir',
                        metavar='indir',
                        help='a directory of lansat 8 tars')

    parser.add_argument('-roi',
                        '--roi',
                        help='Region of intrest for cropping',
                        metavar='roi',
                        type=list,
                        default=[160785, 3467622, 169515, 3462902])
    
    parser.add_argument('-s',
                        '--strict',
                        help='How strict do you want the cloud recognition to be, the lower the more strict',
                        metavar='strict',
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

    indir = args.indir

    # How strict do you want the cloud recognition to be, the lower the more strict
    how_strict= args.strict


    # GPS Bounding Box for sampling area
    x1 = args.roi[0]
    y1 = args.roi[1]
    x2 = args.roi[2]
    y2 = args.roi[3]
        




    #--------------------------------------------------------------------------

    # -Main-


    # If you ahve tars still in the directory, these will grab them and untar them
    tars = glob.glob(indir + '\*.tar')

    # if len(tars) > 1:
    for tar in tars:
        out_file = tar.split('.')[0]

        # making a file for the tars to land
        if not os.path.exists(out_file):
            os.makedirs(out_file)
        one_tar = tarfile.open(tar)
        one_tar.extractall(out_file)
            
            
    # # Function to take a lansat image and crop it to the sample area in Baker County, GA  

    lv1 = glob.glob(indir + '\*')


    for folder in lv1:
        if os.path.isdir(folder):
            folder_name = folder.split('\\')[-1]
            if folder_name.startswith('L'):
                cnt = 1
                tifs = glob.glob(folder+"\*.tif")
            #     print(folder)

                date = folder.split("_")[-4]
            #     outdir = folder+"\cropped"
                outdir = indir+'\\'+date

                if os.path.isdir(outdir):
                    outdir = outdir +f'_{cnt}'
                    cnt += 1

                os.mkdir(outdir)

                # Itterating through the image list
                for im in tifs:

                    split = im.split('_')
                    date = split[-6]
                    band = split[-1]
                    filename = date+'_'+band



            #         print(filename)

                    # Opening each one in GDAL
                    img = gdal.Open(im)


                    gdal.Translate(os.path.join(outdir, filename), img, projWin = [x1,y1,x2,y2])

    lv2 = glob.glob(indir + '\*')

    # if not os.path.exists(indir + '\cloudy'):
    #         os.makedirs(indir + '\cloudy')

    # if not os.path.exists(indir + '\clear'):
    #         os.makedirs(indir + '\clear')
            
    # if not os.path.exists(indir + r'\NDWI'):
    #         os.makedirs(indir + r'\NDWI')

    os.path.join(indir, 'cloudy')


    if not os.path.exists(os.path.join(indir, 'cloudy')):
            os.makedirs(os.path.join(indir, 'cloudy'))

    if not os.path.exists(os.path.join(indir, 'cloudy')):
            os.makedirs(os.path.join(indir, 'cloudy'))
            
    if not os.path.exists(os.path.join(indir, 'cloudy')):
            os.makedirs(os.path.join(indir, 'cloudy'))
            
    for date_folder in lv2:

        if (os.path.isdir(date_folder)):
            date = date_folder.split('\\')[-1]
            
            
            if not date.startswith('L'):
                band1_imgs = glob.glob(os.path.join(date_folder, '*B1.tif')      

                for img in band1_imgs:
                    filename = img.split("\\")[-1]
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

                    if (len([1 for i in testing_vals if i > testing_mode]) >= len(testing_vals)*how_strict) or (testing_average > 35) or (testing_average < 10):
                        print("Cloudy image")

                        print(date)
                        # shutil.move(indir + '\\' +  date, indir + '\cloudy')

                        shutil.move(os.path.join(indir, date),os.path.join(indir, 'cloudy'))

                    else:
                        print("Clear image")
                        print(date)

                        # do NDWI Then move


                        # Calculation
                        # NDWI = (3 - 5)/(3 + 5)
                        date_folder
                        band3 = glob.glob(os.path.join(date_folder, '*B3.tif'))
                        # band5 = glob.glob(date_folder + '*B5.tif')
                        band5 = glob.glob(os.path.join(date_folder, '*B5.tif')
                        b3 = rio.open(band3[0])
                        b5 = rio.open(band5[0])
                        green = b3.read()
                        nir = b5.read()
                        ndwi = (nir.astype(float)-green.astype(float))/(nir+green)




                        # Plotting
                        fig, ax = plt.subplots(1, figsize=(12, 10))
                        show(ndwi, ax=ax, cmap="coolwarm_r")
                        plt.savefig(os.path.join(date_folder, date + '_NDWI.tif'))
                        plt.savefig(os.path.join(indir, 'NDWI', date + '_NDWI.tif'))
                        
                        b3.close()
                        b5.close()


                        shutil.move(os.path.join(indir, date), os.path.join(indir, 'clear'))


    ndwi_tifs = glob.glob(os.join(indir, 'NDWI\*.tif'))

    for i in ndwi_tifs:
        pic_name = i.split('.')[-2]
        pic_name = pic_name.split('\\')[-1]
        img = cv2.imread(i)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,pic_name,(150,525), font, 1,(0,0,0),2)
        cv2.imwrite(i, img)

        
    clip = ImageSequenceClip(ndwi_tifs,fps=.25)
    clip.write_gif(os.join(indir, 'NDWI\final.gif'))






# --------------------------------------------------
if __name__ == '__main__':
    main()