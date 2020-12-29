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

    for filename in os.listdir(path):
        if filename.endswith(".jpg"):
            # Get the image
            new_path = os.path.join(path, filename)
            img = cv2.imread(new_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Extract text from the image
            text = pytesseract.image_to_string(img_rgb)

            # Make text lowercase (for action word detection) and remove newlines (for readability)
            lowercase_text = text.lower()
            lowercase_text = lowercase_text.replace("\n", " ")

            # Get the JSON for the image
            json_filename = filename[:-4]
            if not json_filename.endswith("UTC"):
                json_filename = json_filename.split("UTC",1)[0] + "UTC"
            json_filename = json_filename + ".json"
            new_json_path = os.path.join(path, json_filename)
            file = open(new_json_path,)
            data = json.load(file)

            # Get the like and comment count of the image's post
            post_likes = data["node"]["edge_media_preview_like"]["count"];
            post_comments = data["node"]["edge_media_to_comment"]["count"];
            file.close()

            # Check all years
            for year in years:
                # If the image corresponds to the particular year
                if filename.startswith(year):
                    # Remove spaces and newlines
                    lowercase_text_no_space = lowercase_text.replace(" ", "").replace("\n", "")

                    # If we detect sufficient text (15 characters is the average of 3 words), we classify it as an infographic
                    if len(lowercase_text_no_space) > 15:
                        # Increment number of images with text
                        num_images_with_text[year] += 1
                        # Add length (no spaces) to character count
                        num_characters[year] += len(lowercase_text_no_space) - 1
                        # Add number of post comments to infographic comments
                        num_infographic_comments[year] += post_comments;
                        # Add number of post likes to infographic likes
                        num_infographic_likes[year] += post_likes;
                    # Increment total images
                    num_images[year] += 1
                    # Add number of post comments to total comments
                    num_total_comments[year] += post_comments;
                    # Add number of post likes to total likes
                    num_total_likes[year] += post_likes;

                    # Add number of action words to action words
                    image_action_words = 0
                    for word in action_words:
                        image_action_words += lowercase_text_no_space.count(word)
                    num_action_words[year] += image_action_words

    print("Stats for: " + movement +":")
    overall_num_total_likes = overall_num_total_comments = overall_num_infographic_likes = overall_num_infographic_comments = overall_num_images_with_text = overall_num_images = 0
    for year in years:
        # Print statistics for each year
        print("The total number of images with text in " + year + " is: " + str(num_images_with_text[year]))
        print("The total number of characters in " + year + " is: " + str(num_characters[year]))
        print("The total number of images in " + year + " is: " + str(num_images[year]))
        print("The percentage of images in " + year + " that contained text is: " + str(100 * num_images_with_text[year]/num_images[year]))
        print("The character to image quantity ratio in " + year + " is: " + str(num_characters[year]/num_images[year]))
        print("The number of action words in " + year + " is: " + str(num_action_words[year]))
        print("The percentage of likes that belonged to infographics in " + year + " is: " + str(100 * num_infographic_likes[year]/num_total_likes[year]))
        print("The percentage of comments that belonged to infographics in " + year + " is: " + str(100 * num_infographic_comments[year]/num_total_comments[year]))
        print("The number of likes that belonged to infographics in " + year + " is: " + str(num_infographic_likes[year]))
        print("The number of comments that belonged to infographics in " + year + " is: " + str(num_infographic_comments[year]))
        
        # Calculate overall statistics across years
        overall_num_total_likes += num_total_likes[year]
        overall_num_total_comments += num_total_comments[year]
        overall_num_infographic_likes += num_infographic_likes[year]
        overall_num_infographic_comments += num_infographic_comments[year]
        overall_num_images_with_text += num_images_with_text[year]
        overall_num_images += num_images[year]

    # Print overall statistics
    print("The OVERALL percentage of images that contained text is: " + str(100 * overall_num_images_with_text/overall_num_images))
    print("The OVERALL percentage of likes that belonged to infographics is: " + str(100 * overall_num_infographic_likes/overall_num_total_likes))
    print("The OVERALL percentage of comments that belonged to infographics is: " + str(100 * overall_num_infographic_comments/overall_num_total_comments))

# Function call
stats('/Users/daryakaviani/Desktop/instaloader/blklivesmatter/', "Black Lives Matter")
