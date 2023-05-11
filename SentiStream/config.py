# pylint: disable=import-error
from gensim.models import Word2Vec, FastText

# BEST SETTING SO FAR:
# SSL_MODEL = HAN
# WORD_VEC = Word2Vec
# STEM = False

# SentiStream
SSL_MODEL = 'HAN'  # 'HAN', 'ANN'
WORD_VEC_ALGO = Word2Vec  # Word2Vec, FastText

# Kafka
KAFKA_TOPIC = 'sentiment-data'
BOOTSTRAP_SERVER = 'localhost:9092'  # default 9092

# Input files
DATA = 'data/data_0_1_percent.csv'
TRAIN_DATA = 'data/data_train_0_1_percent.csv'

# Outputs
BATCHING = 'BATCHING'
LOW_CONF = 'LOW_CONFIDENCE'
FINISHED = 'MODEL_TRAINED'
SKIPPED = 'SKIPPED_TRAINING'

# Model filenames
SSL_WV = 'ssl-wv.model'
SSL_CLF = 'ssl-clf.pth'
