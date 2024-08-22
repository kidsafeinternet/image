import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

from fastai.vision.all import *

# Set the path to your dataset
path = Path('small_set')

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

# Evaluate the model
learn.show_results()

# Save the model
learn.export('small.pkl')
