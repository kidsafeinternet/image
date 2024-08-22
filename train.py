import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

from fastai.vision.all import *
import argparse
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a model')
    parser.add_argument('dataset', type=str, help='Path to the dataset directory')

    dataset = parser.parse_args().dataset

    if not dataset:
        print('Please provide a path to the dataset directory')
        exit(1)
    
    # Set the path to your dataset
    path = Path(dataset)

    # Create DataLoaders
    dls = ImageDataLoaders.from_folder(
        path, 
        valid_pct=0.2,  # 20% of the data will be used for validation
        item_tfms=Resize(256),  # Resize images to 256x256 pixels
        batch_tfms=aug_transforms()  # Apply data augmentation
    )

    # Create the learner
    learn = vision_learner(dls, resnet34, metrics=error_rate)

    # Train the model
    learn.fine_tune(5)  # Fine-tune for 5 epochs

    # Show the confusion matrix
    interp = ClassificationInterpretation.from_learner(learn)
    interp.plot_confusion_matrix()
    
    # Download the confusion matrix
    plt.savefig('matrixes/' + dataset + '_confusion_matrix.png')

    # Save the model
    learn.export(dataset + '_model.pkl')
