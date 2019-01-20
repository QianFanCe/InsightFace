import os
import pickle
import zipfile

from PIL import Image
from tqdm import tqdm

from config import *
from mtcnn.detector import detect_faces


def extract(filename):
    print('Extracting {}...'.format(filename))
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall('data')
    zip_ref.close()


def get_face_attributes(full_path):
    try:
        img = Image.open(full_path).convert('RGB')
        bounding_boxes, landmarks = detect_faces(img)

        if len(landmarks) == 1:
            landmarks = [int(round(x)) for x in landmarks[0]]
            return True, landmarks

    except KeyboardInterrupt:
        raise
    except:
        pass
    return False, None


if __name__ == "__main__":
    if not os.path.isdir('data/CASIA-WebFace'):
        extract('data/CASIA-WebFace.zip')

    samples = []
    subjects = [d for d in os.listdir('data/CASIA-WebFace') if os.path.isdir(os.path.join('data/CASIA-WebFace', d))]
    assert (len(subjects) == 10575), "Number of subjects is: {}!".format(len(subjects))

    for i in tqdm(range(len(subjects))):
        sub = subjects[i]
        folder = os.path.join('data/CASIA-WebFace', sub)
        # print(folder)
        files = [f for f in os.listdir(folder) if
                 os.path.isfile(os.path.join(folder, f)) and f.lower().endswith('.jpg')]
        # print(files)
        for file in files:
            filename = os.path.join(folder, file)
            # print(filename)
            is_valid, landmarks = get_face_attributes(filename)
            if is_valid:
                samples.append(
                    {'class_id': i, 'subject': sub, 'full_path': filename, 'landmarks': landmarks})

    f = open(pickle_file, 'wb')
    save = {
        'samples': samples
    }
    pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
    f.close()
