from nudenet import NudeDetector
import json, os, argparse, matplotlib.pyplot as plt, matplotlib.patches as patches
from PIL import Image, ImageFilter

# Globals
blurred = False
noc = 0

classes = [
    "FEMALE_GENITALIA_COVERED",
    "FACE_FEMALE",
    "BUTTOCKS_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_BREAST_EXPOSED",
    "ANUS_EXPOSED",
    "FEET_EXPOSED",
    "BELLY_COVERED",
    "FEET_COVERED",
    "ARMPITS_COVERED",
    "ARMPITS_EXPOSED",
    "FACE_MALE",
    "BELLY_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
    "ANUS_COVERED",
    "FEMALE_BREAST_COVERED",
    "BUTTOCKS_COVERED",
]

ok_classes = [
    "FACE_FEMALE",
    "MALE_BREAST_EXPOSED",
    "FEET_EXPOSED",
    "BELLY_COVERED",
    "FEET_COVERED",
    "ARMPITS_EXPOSED",
    "ARMPITS_COVERED",
    "FACE_MALE",
    "ANUS_COVERED",
    "FEMALE_BREAST_COVERED",
    "BUTTOCKS_COVERED",
    "BELLY_EXPOSED",
    "FEMALE_GENITALIA_COVERED",
]

not_ok_classes = classes.copy()
for c in ok_classes:
    not_ok_classes.remove(c)

detector = NudeDetector()


def detect(image_path):
    result = detector.detect(image_path)
    if result is None:
        raise ValueError(f"Detection failed for image: {image_path}")
    return result


def tojson(path):
    result = detect(path)
    if result is None:
        raise ValueError(f"No result from detection for image: {path}")
    return json.dumps(result)


def show_result(image_path, result):
    image = Image.open(image_path)
    censored_image = image.copy()
    
    if blurred:
        blur(censored_image, result, "censored/" + image_path.split("/")[-1])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Original image with detection results
    ax1.imshow(image)
    for r in result:
        x, y, w, h = r["box"]
        if r["class"] in ok_classes:
            rect = patches.Rectangle(
                (x, y), w, h, linewidth=1, edgecolor="g", facecolor="none"
            )
        else:
            rect = patches.Rectangle(
                (x, y), w, h, linewidth=1, edgecolor="r", facecolor="none"
            )
        ax1.add_patch(rect)
    ax1.set_title('Original Image with Detections')
    
    # Reload the censored image to ensure it is correctly updated
    if blurred:
        censored_image = Image.open("censored/" + image_path.split("/")[-1])

    # Censored image
    ax2.imshow(censored_image)
    ax2.set_title('Censored Image')
    
    plt.show()


def score(result):
    global noc
    # 0 - 1 score for the image. 0 means no nudity, 1 means full nudity
    # Use not_ok_classes to penalize the score
    if not result:
        return 0.5  # Default score when there are no results

    score = 0
    ok_count = 0
    not_ok_count = 0

    for r in result:
        if r["class"] in not_ok_classes:
            score += 1
            not_ok_count += 1
        elif r["class"] in ok_classes:
            ok_count += 1

    # If all classes are ok_classes, return 0
    if not_ok_count == 0:
        return 0
    noc = not_ok_count
    return 1


def blur(image, result, result_path):
    # Create directory if it doesn't exist
    if not os.path.exists("censored"):
        os.makedirs("censored")
    
    for r in result:
        for c in not_ok_classes:
            if r["class"] == c:
                x, y, w, h = r["box"]
                box = (x, y, x + w, y + h)
                area = image.crop(box)
                blurred_area = area.filter(ImageFilter.GaussianBlur(50))
                image.paste(blurred_area, box)
    
    image.save(result_path)


def process_images(image_paths, result_paths):
    for image_path, result_path in zip(image_paths, result_paths):
        result = detect(image_path)
        image = Image.open(image_path)
        blur(image, result, result_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect nudity in images")
    parser.add_argument("path", type=str, help="Path to the image")
    parser.add_argument(
        "--show", "-s", action="store_true", help="Show the image with the detection results"
    )
    parser.add_argument(
        "--directory", "-d", action="store_true", help="Path is a directory"
    )
    parser.add_argument(
        "--output", "-o", action="store_true", help="Print the output as json"
    )
    parser.add_argument(
        "--blur", "-b", action="store_true", help="Blur the detected areas"
    )
    args = parser.parse_args()
    try:
        blurred = args.blur
        if args.directory:
            for i in os.listdir(args.path):
                if i.endswith(".jpg") or i.endswith(".jpeg") or i.endswith(".png"):
                    image_path = os.path.join(args.path, i)
                    print(f"Processing image: {image_path}")
                    result = tojson(image_path)
                    if args.show:
                        show_result(image_path, json.loads(result))
                    if args.output:
                        print(result)
                    print(f"Score: {score(json.loads(result))}")
        else:
            result = tojson(args.path)
            if args.show:
                show_result(args.path, json.loads(result))
            if args.output:
                print(result)
            print(f"Score: {score(json.loads(result))}")
    except ValueError as e:
        print(e)
    except AttributeError as e:
        print(f"AttributeError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    except KeyboardInterrupt:
        pass
