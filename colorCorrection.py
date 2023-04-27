import argparse
import os

import numpy as np
from PIL import Image
import cv2

from utils import Modify,LoadImage

class Main:

   #Function to colour correct images for people with colour blindness types protanopia, deutranopia, or both.
   #Disclaimer: degree_of_protanopia & degree_of_deutranopia changes from person to person. (This is diagnosed by a doctor using the Isihara test.)
    @staticmethod
    def correctImage(get_path:str,
                     degree_of_protanopia : float = 1.0,
                     degree_of_deutranopia : float = 1.0,
                     return_type_image: str = 'save',
                     save_path: str = None
                     ):
                     #get_path --> Input path of the image
                     #degree_of_protanopia --> Protanopia degree
                     #degree_of_deutranopia --> Deutranopia degree
                     #return_type_image --> How to return the correctd image. Use 'pil' for PIL.Image , 'np' for Numpy array , 'save' for Saving to path.
                     #save_path --> Where to save the corrected image if return type is provided as 'save'.
         
     
        #Loading the image file in LMS colour space. 
         rgb_image = LoadImage.process_RGB(get_path)

         modify = Modify.colour_correction_matrix(degree_of_protanopia = degree_of_protanopia,
                                                   degree_of_deutranopia = degree_of_deutranopia) 
         
         corrected_image = np.uint8(np.dot(rgb_image,modify)*255)

         if return_type_image == 'save':
            assert save_path is not None , 'Save path is not provided for image!'
            cv2.imwrite(save_path,corrected_image)
            return
         
         if return_type_image == 'np':
            return corrected_image
         
         if return_type_image == 'pil':
            return Image.fromarray(corrected_image)

    
 #parses the command-line arguments passed to the script 
def parse_args():
   parse= argparse.ArgumentParser(
      description = 'Colour Correct Images for Colour-Blindness')
   parse.add_argument(
      '-input', type =str, help ='Path to input image.')
   parse.add_argument(
      '-output' , type = str, help = 'Path to save the output image dir.')
   parse.add_argument('-colours_correct', action = 'store_true', default=False, 
                       help = 'Corrected Image for Protonopia')
   parse.add_argument('-run_all',action = 'store_true', default=False,
                        help = 'Perform all corrections.' )
   parse.add_argument('-degree_of_protanopia', type = float, default =1.0, 
                       help = 'Adjust the degree of protanopia. Default is 1.0')
   parse.add_argument('-degree_of_deutranopia', type = float, default =1.0,
                        help = 'Adjust the degree of deutranopia. Default is 1.0')
   parse.add_argument('-degree_of_tritanopia', type = float, default= 1.0,
                       help = 'Adjust the degree of tritanopia. Default is 1.0')
   
   args = parse.parse_args()
 
   return args  
 


def main():
   
    args = parse_args()

   #Get the input and output path.
    get_path = args.input
    name_of_image = get_path.split('/')[-1]
    image_output_path = args.output

   #Check whether output path is a directory.
    assert os.path.isdir(image_output_path),'Output path should be a Directory.'

   #Setup the run_all flag.
    run_all = False
    if args.run_all:
        run_all = True

    if args.colours_correct or run_all:
        Main.correctImage(get_path= get_path,
                          return_type='save',
                          save_path = '{}/{}_{}'.format(image_output_path,'colours_correct', name_of_image),
                          degree_of_protanopia=args.degree_of_protanopia,
                          degree_of_deutranopia=args.degree_of_deutranopia)

    print('ReColorLib Completed running! Check output Image in {}'.format(image_output_path))

if __name__== '__main__':
   main()  