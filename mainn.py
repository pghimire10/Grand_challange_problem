import pandas as pd 
import os

BASE_DIR = r"Data"
label = r"Data\ODIR-5K_Training_Annotations(Updated)_V2.xlsx"
df = pd.read_excel(label)
csv_data = df.to_csv(os.path.join(BASE_DIR, "Data.csv"))

left_eye = df[['Left-Fundus', 'Left-Diagnostic Keywords']].copy()
left_eye.columns = ['Image', 'Labels']


left_eye.to_csv(os.path.join(BASE_DIR, "left_eye.csv"))

right_eye = df[['Right-Fundus', 'Right-Diagnostic Keywords']].copy()
right_eye.columns = ['Image', 'Labels']

right_eye.to_csv(os.path.join(BASE_DIR, "right_eye.csv"))
right_eye_path = r"Data\right_eye.csv"

# dir = os.listdir(right_eye_path)


# print(dir)

# get unique diagnostic keywords
keywords = [ keyword  for keywords in df['Left-Diagnostic Keywords'] for keyword in keywords.split('，')]
unique_keywords = set(keywords)

# print(keywords[:10])
# print(unique_keywords)
# print(len(unique_keywords),len(keywords))

# create a mapping from keywords to class labels
class_labels = ['N','D','G','C','A','H','M','O']
keyword_label_mapping  = {
    'normal':'N',
    'retinopathy':'D',
    'glaucoma':'G',
    'cataract':'C',
    'macular degeneration':'A',
    'hypertensive':'H',
    'myopia':'M',
    'lens dust' : 'O',
    'optic disk photographically invisible':'O', 
    'low image quality':'O', 
    'image offset':'O',
}
non_decisive_labels = ["lens dust", "optic disk photographically invisible", "low image quality", "image offset"]

# if the keyword contains label outside of the above then, label them as others 'O'
def generate_individual_label(diagnostic_keywords):
    
    keywords = [ keyword  for keyword in diagnostic_keywords.split('，')]
    contains_normal = False
    for k in keywords:
        for label in keyword_label_mapping.keys():
            if label in k:
                if label == 'normal':
                    contains_normal = True # if found a 'normal' keyword, check if there are other keywords but keep in mind that a normal keyword was found
                else:
                    return keyword_label_mapping[label] # found a proper keyword label, use the first occurence

    # did not find a proper keyword label, see if there are labels other than non-decisive labels, if so, categorize them as 'others'
    decisive_label = False
    for k in keywords:
        if k not in non_decisive_labels and (('normal' not in k) or ('abnormal' in k)):
            decisive_label = True
    if decisive_label:
        # contains decisive label other than the normal and abnormal categories
        return 'O' 
    if contains_normal:
        return 'N'
    
    
    # if any of the above criteria do not match, then return as is
    return keywords[0] # useful for diagnostics, check if there are cases that are not covered by the above

# generate_individual_label('normal fundus'),generate_individual_label('lens dust，drusen，normal fundus	')
df['Left-label']= df['Left-Diagnostic Keywords'].apply(generate_individual_label)
df['Right-label'] = df['Right-Diagnostic Keywords'].apply(generate_individual_label)
df[df['Left-label'].isin(non_decisive_labels)]



left_data = pd.read_csv(r"Data\left_eye.csv")
# print(left_data)
left_column = 'left_labels'
l=[]

for left in left_data['Labels']:
    out = generate_individual_label(left)
    l.append(out)
print(l)

left_data['left_colums']=l
left_data.to_csv(r"Data\left_eye.csv", index="False")















