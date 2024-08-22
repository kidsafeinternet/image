from fastai.vision.all import load_learner

learn_inf = load_learner('small_set/small.pkl')

pred, _, probs = learn_inf.predict('small_set/test.png')
print(f'Prediction: {pred}; Probability: {probs}')

pred, _, probs = learn_inf.predict('small_set/test2.png')
print(f'Prediction: {pred}; Probability: {probs}')