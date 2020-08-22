from PIL import Image
import glob

#empty list

image_list = []
resized_images = []

for filename in sorted(glob.glob('imagesFirst/images/*.png')):
	temp = Image.open(filename)
	img = temp.copy()
	img = img.resize((512,512))
	image_list.append(img)

# save resize image to a new folder
i = 0

# You need to create a folder name new first

for(i ,new) in enumerate(image_list):
	new.save('{}{}{}'.format('new/','image'+ str(i),'.png'))


