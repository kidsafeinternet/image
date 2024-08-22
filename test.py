from fastai.vision.all import load_learner
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict the class of an image')
    parser.add_argument('model', type=str, help='Path to model file')
    parser.add_argument('directory', type=str, help='Path to the testing directory')
    parser.parse_args()

    model = parser.parse_args().model
    directory = parser.parse_args().directory

    if not model:
        print('Please provide a path to the model file')
        exit(1)
    
    if not directory:
        print('Please provide a path to the testing directory')
        exit(1)

    learn_inf = load_learner(parser.parse_args().model)

    # for image in the testing directory
    for image in os.listdir(directory):
        if image == '.gitignore':
            continue
        image_path = os.path.join(directory, image)
        pred, _, probs = learn_inf.predict(image_path)
        class_probs = {learn_inf.dls.vocab[i]: f'{probs[i]*100:.2f}%' for i in range(len(probs))}
        print(f'{image}\n==============\nPrediction: {pred}\nProbability: {class_probs}\n')
