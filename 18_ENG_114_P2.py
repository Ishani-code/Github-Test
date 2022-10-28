import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image
import random
import cv2




image_org  = cv2.imread("/Desktop/computer vision practical/image1.bmp")

gray = cv2.cvtColor(image_org, cv2.COLOR_BGR2GRAY)
  

def neighbor(i,j,label):
    left = label[i,j-1]
    above = label[i-1,j]
    neighbor_label = [left,above]
    return neighbor_label

def generateColors(img):
    height, width = img.shape

    colors = []
    colors.append([])
    colors.append([])
    color = 1
    
    coloured_img = Image.new("RGB", (width, height))
    coloured_data = coloured_img.load()

    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] > 0:
                if img[i][j] not in colors[0]:
                    colors[0].append(img[i][j])
                    colors[1].append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

                ind = colors[0].index(img[i][j])
                coloured_data[j, i] = colors[1][ind]

    return coloured_img



def connected_component_labelling(image_org) :
       
    size = image_org.shape  
    m = size[0] 
    n = size[1]  

    threshold = 50
    
    
    for i in range(m):
        for j in range(n):
            if gray[i,j] > threshold:
                gray[i,j] = 1
                
            else:
                gray[i,j] = 0
                
        
    image = gray
    
    label = np.ones([m,n])
    new = 0   
    link = []
    id = 0 
    

    # first pass
    for row in range(m):
        for column in range(n):
            
            # If current pixel is background pixel
            if image[row,column] == [0] :
                label[row, column] = 0
                
            #If current pixel is not background pixel
            else : 
                current_neighbor = neighbor(row,column,label)# check the neighbor label

                # If current is new label
                if current_neighbor == [0,0]:
                    new= new + 1
                    label[row, column] = new
                    

                # If one of the pixels on the left and above is not the background pixel, got neighbor's label
                else :
                    
                    if np.min(current_neighbor) == 0 or current_neighbor[0] == current_neighbor[1] :
                        label[row,column] = np.max(current_neighbor)                        
                        

                    else:
                        label[row,column] = np.min(current_neighbor)                    
                        
                        
                        if id == 0:
                            link.append(current_neighbor)
                            id = id +1
                        
                        else:
                            check = 0
                            for k in range(id) :                        
                                tmp = set(link[k]).intersection(set(current_neighbor))                                
                                if len(tmp) != 0 :
                                    link[k] = set(link[k]).union(current_neighbor)
                                    np.array(link)
                                    check = check + 1
                                    
                            if check == 0:
                                id = id +1
                                np.array(link)
                                link.append(set(current_neighbor))
                                
        


    # second pass
    for row in range(m):
        for column in range(n):
            for x in range(id):
                if (label[row, column] in link[x]) and label[row, column] !=0 :
                    label[row, column] = min(link[x])
        

    for row in range(m):
        for column in range(n):
            for x in range(id):
                if (label[row, column] == min(link[x])):
                    label[row, column] = x+1
            
        
    
    return label,image


label,image = connected_component_labelling(image_org)

coloured_img = generateColors(label)



plt.figure(figsize=(15,5))

plt.subplot(1,2,1), plt.title('Input')
plt.imshow(image_org ,cmap = 'gray'),plt.axis('off')
plt.subplot(1,2,2), plt.title('Output')
plt.imshow(coloured_img),plt.axis('off') 
 
plt.show()
