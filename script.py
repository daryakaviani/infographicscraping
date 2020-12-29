import cv2
import pytesseract
import os
import json

def stats(path, movement):
    years = ["2014", "2015", "2016", "2017", "2018", "2019", "2020"]
    action_words = ["petition", "call", "vote", "march", "rise", "text", "action", "act", "demand", "fight", "protest", "share", "come", "support", "help", "urge", "sign", "prosecute", "donate", "defend", "change", "command", "shout", "cry", "react", "now", "justice"]
    num_images_with_text = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}
    num_characters = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}
    num_images = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}
    num_action_words = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}
    num_total_comments = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}
    num_infographic_comments = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}
    num_total_likes = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}
    num_infographic_likes = {"2014": 0, "2015": 0, "2016": 0, "2017": 0, "2018": 0, "2019": 0, "2020": 0}

    for year in years:
        # A text file is created and flushed 
        file = open(year + ".txt", "w+") 
        file.write("") 
        file.close()

    for filename in os.listdir(path):
        if filename.endswith(".jpg"):
            # Get the image
            print(filename)
            new_path = os.path.join(path, filename)
            img = cv2.imread(new_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(img_rgb)
            lowercase_text = text.lower()
            print(lowercase_text)

            # Get the JSON for the image
            json_filename = filename[:-4]
            if not json_filename.endswith("UTC"):
                json_filename = json_filename.split("UTC",1)[0] + "UTC"
            json_filename = json_filename + ".json"
            new_json_path = os.path.join(path, json_filename)
            file = open(new_json_path,)
            data = json.load(file)
            post_likes = data["node"]["edge_media_preview_like"]["count"];
            post_comments = data["node"]["edge_media_to_comment"]["count"];
            file.close()

            # Read image and update statistics
            for year in years:
                if filename.startswith(year):
                    if len(text) > 10:
                        num_images_with_text[year] += 1
                        num_characters[year] += len(text) - 3
                        num_infographic_comments[year] += post_comments;
                        num_infographic_likes[year] += post_likes;
                    num_images[year] += 1
                    num_total_comments[year] += post_comments;
                    num_total_likes[year] += post_likes;
                    # Open the file in append mode 
                    file = open(year + ".txt", "a") 
                    # Appending the text into file 
                    file.write(text)
                    file.close()
                    for word in action_words:
                        if word in lowercase_text:
                            num_action_words[year] += 1
    print("Stats for: " + movement +":")
    overall_num_total_likes = overall_num_total_comments = overall_num_infographic_likes = overall_num_infographic_comments = overall_num_images_with_text = overall_num_images = 0
    for year in years:
        print("The total number of images with text in " + year + " is: " + str(num_images_with_text[year]))
        print("The total number of characters in " + year + " is: " + str(num_characters[year]))
        print("The total number of images in " + year + " is: " + str(num_images[year]))
        print("The percentage of images in " + year + " that contained text is: " + str(100 * num_images_with_text[year]/num_images[year]))
        print("The character to image quantity ratio in " + year + " is: " + str(num_characters[year]/num_images[year]))
        print("The number of action words in " + year + " is: " + str(num_action_words[year]))
        print("The percentage of likes that belonged to infographics in " + year + " is: " + str(100 * num_infographic_likes[year]/num_total_likes[year]))
        print("The percentage of comments that belonged to infographics in " + year + " is: " + str(100 * num_infographic_comments[year]/num_total_comments[year]))
        overall_num_total_likes += num_total_likes[year]
        overall_num_total_comments += num_total_comments[year]
        overall_num_infographic_likes += num_infographic_likes[year]
        overall_num_infographic_comments += num_infographic_comments[year]
        overall_num_images_with_text += num_images_with_text[year]
        overall_num_images += num_images[year]

    print("The OVERALL percentage of images that contained text is: " + str(100 * overall_num_images_with_text/overall_num_images))
    print("The OVERALL percentage of likes that belonged to infographics is: " + str(100 * overall_num_infographic_likes/overall_num_total_likes))
    print("The OVERALL percentage of comments that belonged to infographics is: " + str(100 * overall_num_infographic_comments/overall_num_total_comments))

stats('/Users/daryakaviani/Desktop/instaloader/blklivesmatter/', "Black Lives Matter")
