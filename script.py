import cv2
import pytesseract
import os

path = '/Users/daryakaviani/Desktop/instaloader/blklivesmatter/'

years = ["2014", "2015", "2016", "2017", "2018", "2019", "2020"]
num_images_with_text = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}
num_characters = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}
num_images = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}

for filename in os.listdir(path):
    if filename.endswith(".jpg"):
        print(filename)
        new_path = os.path.join(path, filename)
        img = cv2.imread(new_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)
        for year in years:
            if filename.startswith(year):
                if len(text) > 3:
                    num_images_with_text[year] += 1
                    num_characters[year] += len(text) - 3
                num_images[year] += 1
    else:
        print("NOT AN IMAGE, SKIP")
for year in years:
    print("The total number of images with text in " + year + " is: " + str(num_images_with_text[year]))
    print("The total number of characters in " + year + " is: " + str(num_characters[year]))
    print("The total number of images in " + year + " is: " + str(num_images[year]))
    print("The percentage of images in " + year + " that contained text is: " + str(100 * num_images_with_text[year]/num_images[year]))
    print("The character to image quantity ratio in " + year + " is: " + str(num_characters[year]/num_images[year]))

