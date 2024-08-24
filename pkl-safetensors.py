from safetensors.torch import save_file
import torch
import argparse
from fastai.learner import Learner

def convert(pkl_path, safetensors_path):
    # Load the object from the .pkl file
    obj = torch.load(pkl_path)
    
    # Check if the loaded object is a fastai Learner
    if isinstance(obj, Learner):
        # Extract the model's state_dict
        weights = obj.model.state_dict()
    elif isinstance(obj, dict) and all(isinstance(k, str) and isinstance(v, torch.Tensor) for k, v in obj.items()):
        weights = obj
    else:
        raise ValueError(f"Expected a dict of [str, torch.Tensor] or a fastai Learner but received {type(obj)}")
    
    # Save the weights to a .safetensors file
    save_file(weights, safetensors_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a .pkl file to a .safetensors file')
    parser.add_argument('pkl_path', type=str, help='Path to the .pkl file')
    parser.add_argument('safetensors_path', type=str, help='Path to save the .safetensors file')
    args = parser.parse_args()

    pkl_path = args.pkl_path
    safetensors_path = args.safetensors_path
    print(f'Converting {pkl_path} to {safetensors_path}')
    convert(pkl_path, safetensors_path)