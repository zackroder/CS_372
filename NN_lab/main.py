import os
import numpy as np
from PIL import Image
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
import random
from image_downloader import simple_image_download

# constants
QUERIES = ["john lennon face", "paul mccartney face"]  # used in image searches
SUBDIRS = [s.replace(" ", "_") for s in QUERIES] # same as the queries, but no spaces
IMG_DIR = "simple_images"

#setup a standard image size; this will distort some images but will get everything into the same shape
STANDARD_SIZE = (200, 200)

def download_images(query):
    subdir = query.replace(" ", "_")
    if os.path.isdir(IMG_DIR + "/" + subdir) and len([f for f in os.listdir(IMG_DIR + "/" + subdir)]) >= 3:
        print("It looks like you've already downloaded images for '" + query + "'.")
        print("  Skipping download.")
        print("  To re-download images, remove all images in the " + query + " folder.")
        return
    
    response = simple_image_download()
    print("Downloading images for", query, "(might take 30 seconds)")
    response.download(query, 50)
    # print(response.urls(subdir, 30))
    
    # make sure images can be loaded
    imglist = [IMG_DIR + "/" + subdir + "/" + f for f in os.listdir(IMG_DIR + "/" + subdir) if not f.startswith('.')]
    for img in imglist:
        try:
            Image.open(img)
        except OSError:
            print(img, "can't be opened--will delete.")
            os.remove(img)
    
    
def img_to_matrix(filename, verbose=False):
    """
    takes a filename and turns it into a numpy array of RGB pixels
    """
    img = Image.open(filename)
    if verbose==True:
        print("changing size from %s to %s" % (str(img.size), str(STANDARD_SIZE)))
    img2 = img.resize(STANDARD_SIZE, Image.BILINEAR)
    img3 = list(zip(list(img2.getdata(0)), list(img2.getdata(1)), list(img2.getdata(2))))
    img4 = [list(x) for x in img3]
    img5 = np.array(img4)
    return img5

def flatten_image(img):
    """
    takes in an (m, n) numpy array and flattens it 
    into an array of shape (1, m * n)
    """
    s = img.shape[0] * img.shape[1]
    img_wide = img.reshape(1, s)
    return img_wide[0]

def evaluate(classifier, test_set, correct_outputs):
    right = 0
    wrong = 0
    predictions = classifier.predict(test_set)
    for i in range(0, len(predictions)):
        if predictions[i] == correct_outputs[i]:
            right += 1
        else:
            wrong += 1
    return right, wrong

def shuffle_data(X, y):
    # horribly inefficient shuffling algorithm
    for i in range(0, len(y)*2):
        a = random.randint(0, len(y)-1)
        b = random.randint(0, len(y)-1)
        temp = X[a]
        X[a] = X[b]
        X[b] = temp
        temp = y[a]
        y[a] = y[b]
        y[b] = temp

download_images(QUERIES[0])
download_images(QUERIES[1])

DIRS = [IMG_DIR + "/" + SUBDIRS[0], IMG_DIR + "/" + SUBDIRS[1]]
tag0images = [DIRS[0] + "/" + f for f in os.listdir(DIRS[0]) if not f.startswith('.')]
tag1images = [DIRS[1] + "/" + f for f in os.listdir(DIRS[1]) if not f.startswith('.')]
images = tag0images + tag1images
labels = [SUBDIRS[0]] * len(tag0images) + [SUBDIRS[1]] * len(tag1images)

print("Transforming images into big arrays... (might take up to 30 seconds)")
shuffle_data(images, labels)
data = []
for image in images:
    img = img_to_matrix(image)
    img = flatten_image(img)
    data.append(img)
data = np.array(data)
print("Shape of the data =", data.shape)
print("First image as an array =", data[0])

print("Running PCA...")
pca = PCA(n_components=50)
X = pca.fit_transform(data)
df = pd.DataFrame({"x": X[:, 0], "y": X[:, 1], "label":labels})
colors = ["blue", "red"]
for label, color in zip(df['label'].unique(), colors):
    mask = df['label']==label
    plt.scatter(df[mask]['x'], df[mask]['y'], c=color, label=label)
plt.legend()
plt.savefig("plot.png")  # Can also replace with plt.show() if you're in PyCharm.
print("Training a neural network...")
nn_trainer = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5,5))
labels_ints = [SUBDIRS.index(x) for x in labels]
classifier = nn_trainer.fit(X, labels_ints)
print("Training and testing on same data (poor practice).")
results = evaluate(classifier, X, labels_ints)
print("Number predicted correctly:", results[0])
print("Number predicted incorrectly:", results[1])
print("Accuracy: ", results[0] / (results[0] + results[1]))

# divide our data in half for training/testing
data_length = X.shape[0]
half_length = int(data_length / 2)
X_first_half = X[:half_length]
X_second_half = X[half_length:]
y_first_half = labels_ints[:half_length]
y_second_half = labels_ints[half_length:]

# train on first half, test on second
classifier = nn_trainer.fit(X_first_half, y_first_half)

print("\nTraining on first half, testing on first half (poor practice).")
results = evaluate(classifier, X_first_half, y_first_half)
print("Number predicted correctly:", results[0])
print("Number predicted incorrectly:", results[1])
print("Accuracy: ", results[0] / (results[0] + results[1]))

print("\nTraining on first half, testing on second half (good practice).")
results = evaluate(classifier, X_second_half, y_second_half)
print("Number predicted correctly:", results[0])
print("Number predicted incorrectly:", results[1])
print("Accuracy:", results[0] / (results[0] + results[1]))