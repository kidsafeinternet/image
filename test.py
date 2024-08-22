from fastai.vision.all import load_learner
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict the class of an image')
    parser.add_argument('model', type=str, help='Path to model file')
    parser.add_argument('directory', type=str, help='Path to the testing directory')

    if not parser.parse_args().model:
        print('Please provide a path to the model file')
        exit(1)
    
    if not parser.parse_args().directory:
        print('Please provide a path to the testing directory')
        exit(1)

    learn_inf = load_learner(parser.parse_args().model)

    # for image in the testing directory
    for image in os.listdir(parser.parse_args().directory):
        pred, _, probs = learn_inf.predict(parser.parse_args().directory + image if parser.parse_args().directory.endswith('/') else parser.parse_args().directory + '/' + image)
        print(f'Prediction: {pred}; Probability: {probs}')
