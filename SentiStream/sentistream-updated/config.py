# pylint: disable=import-error
from gensim.models import Word2Vec, FastText

# BEST SETTING SO FAR:
# SSL_MODEL = HAN
# WORD_VEC = Word2Vec
# STEM = False

# PyFlink
PYFLINK = False

# SentiStream
SSL_MODEL = 'HAN'  # 'HAN', 'ANN'
WORD_VEC_ALGO = Word2Vec  # Word2Vec, FastText
STEM = False

# Kafka
KAFKA_TOPIC = 'sentiment-data'
BOOTSTRAP_SERVER = 'localhost:9092'  # default 9092

# Input files
DATA = 'new_train.csv'
TRAIN_DATA = 'new_ss_train.csv'

# Outputs
BATCHING = 'BATCHING'
LOW_CONF = 'LOW_CONFIDENCE'
FINISHED = 'MODEL_TRAINED'
SKIPPED = 'SKIPPED_TRAINING'

# Model filenames
US_WV = 'plstream-wv.model'
SSL_WV = 'ssl-wv.model'
SSL_CLF = 'ssl-clf.pth'

# Set up positive and negative reference words for trend detection.
POS_REF = {'love', 'best', 'beautiful', 'great', 'cool', 'awesome', 'wonderful',
           'brilliant', 'excellent', 'fantastic', 'super', 'fun', 'masterpiece',
                        'rejoice', 'admire', 'amuse', 'bliss', 'yummy', 'glamour'}
NEG_REF = {'bad', 'worst', 'stupid', 'disappointing', 'terrible', 'rubbish', 'boring',
           'awful', 'unwatchable', 'awkward', 'bullshit', 'fraud', 'abuse', 'outrange',
           'disgust'}
if STEM:  # TODO: TEMP --- DLT OTHER WHEN FINALIZED.
    POS_REF = {'love', 'best', 'beautiful', 'great', 'cool', 'awesome', 'wonderful',
               'brilliant', 'excellent', 'fantastic', 'super', 'fun', 'masterpiece',
                            'rejoice', 'admire', 'amuse', 'bliss', 'yumm', 'glamour'}
    NEG_REF = {'bad', 'worst', 'stupid', 'disappointing', 'terrible', 'rubbish',
               'boring', 'awful', 'unwatchable', 'awkward', 'bullshi', 'fraud',
               'abuse', 'outrange', 'disgust'}
