import idrc
from fastai.vision.all import load_learner, PILImage
import requests
from io import BytesIO

api = idrc.idrc()
learn_inf = load_learner('medium_set/medium_set_model.pkl')

def ai(image_path):
    try:
        # Check if the image_path is a URL
        if image_path.startswith('http://') or image_path.startswith('https://'):
            response = requests.get(image_path)
            img = PILImage.create(BytesIO(response.content))
        else:
            # Load the image from local path
            img = PILImage.create(image_path)
        
        # Make a prediction
        pred, _, probs = learn_inf.predict(img)
        
        # Create a dictionary of class probabilities
        class_probs = {learn_inf.dls.vocab[i]: f'{probs[i]*100:.2f}%' for i in range(len(probs))}
        
        # Print the prediction and probabilities
        print(f'{image_path}\n==============\nPrediction: {pred}\nProbability: {class_probs}\n')
        
        return pred, class_probs
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    api.define(ai)
    api.run(port=5347)