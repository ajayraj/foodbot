import NaiveBayes as nb

train_classifier = nb.NaiveBayes()
train_classifier.train()
train_classifier.store_pickle()