import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Função de tokenização personalizada
def custom_tokenizer(text):
    return text.split()

class Treinar:
    def __init__(self, intents_file, model_filename="modelos/chatbot_model.pkl", vectorizer_filename="modelos/vectorizer.pkl", encoder_filename="modelos/encoder.pkl"):
        self.intents_file = intents_file
        self.model_filename = model_filename
        self.vectorizer_filename = vectorizer_filename
        self.encoder_filename = encoder_filename

    def load_intents(self):
        with open(self.intents_file, 'r', encoding='utf-8-sig') as file:
            return json.load(file)

    def train_model(self):
        intents = self.load_intents()
        patterns = []
        tags = []

        for intent in intents['intents']:
            for pattern in intent['patterns']:
                patterns.append(pattern)
                tags.append(intent['tag'])


        vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer, stop_words='english', ngram_range=(1, 2))
        X = vectorizer.fit_transform(patterns).toarray()

        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(tags)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = SVC(kernel='linear', C=1.5, probability=True)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

        self.save_model(model, vectorizer, label_encoder)

    def save_model(self, model, vectorizer, label_encoder):
        with open(self.model_filename, 'wb') as model_file:
            pickle.dump(model, model_file)
        with open(self.vectorizer_filename, 'wb') as vectorizer_file:
            pickle.dump(vectorizer, vectorizer_file)
        with open(self.encoder_filename, 'wb') as encoder_file:
            pickle.dump(label_encoder, encoder_file)

        print("Modelo treinado e salvo com sucesso.")
