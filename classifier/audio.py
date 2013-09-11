import conn
import heapq
import math
import numpy as np
import warnings

from models import TrackData
from sklearn.mixture import GMM
from util import logger
from yaafelib import FeaturePlan, AudioFileProcessor, Engine

def get_engine(audio_freq, mfcc_block_size, mfcc_step_size):
    fp = FeaturePlan(sample_rate=audio_freq)
    fp.addFeature('mfcc: MFCC blockSize=%d stepSize=%d > Derivate DOrder=1' % \
                  (mfcc_block_size, mfcc_step_size))

    df = fp.getDataFlow()
    
    afp = AudioFileProcessor()
    engine = Engine()
    engine.load(df)
    
    return (afp, engine)

def train(tracks, training_audio_path, conf, set_name, conn_str):
    logger.log('begin training sequence on %s ' % training_audio_path)
    
    # set up all model parameters
    num_components      = conf['num_components']
    em_epsilon          = conf['em_epsilon']
    em_iter             = conf['em_iter']
    cv_type             = conf['cv_type']
    
    audio_freq          = conf['audio_freq']
    mfcc_step_size      = conf['mfcc_step_size']
    mfcc_block_size     = conf['mfcc_block_size']
    frames_per_second   = audio_freq / mfcc_step_size
    
    audio_block_size    = frames_per_second * conf['sample_length']
    audio_step_size     = frames_per_second * conf['sample_step_size']
    
    # set up Yaafe
    afp, engine = get_engine(audio_freq, mfcc_block_size, mfcc_step_size)

    connection = conn.get()
    connection.register([TrackData])
    result = []
    
    for label, filename in tracks:
        logger.log('begin processing %s.' % filename)
        afp.processFile(engine, training_audio_path + '/' + filename)
        
        output      = engine.readAllOutputs()['mfcc']
        mfcc        = output     
        num_samples = mfcc.shape[0]
        track_gmms  = []
        
        track       = connection.TrackData()
        track.label = label
        track.set   = set_name

        for index in range(0, (num_samples - audio_block_size), audio_step_size):
            with warnings.catch_warnings(record=True) as w:
                mfcc_data = mfcc[index:index + audio_block_size]
    
                classifier = GMM(n_components = num_components, cvtype = cv_type)
                classifier.fit(mfcc_data, thresh = em_epsilon, n_iter = em_iter)
    
                means = classifier._get_means().tolist()  
                
                if cv_type == 'diag':          
                    covars = [np.diag(diag).tolist() for diag in classifier._get_covars()]
                else:
                    covars = classifier._get_covars().tolist()
                weights = classifier._get_weights().tolist()
                
                for weight in weights:
                    if math.isnan(weight):
                        logger.warn("Warning: invalid GMM entry, skipping at label: %s, index %s" % (label, str(index)))
                        break
                else:
                    track_gmms.append([means, covars, weights])

        track.data = track_gmms
        track.save()
        
        result.append(track._id)

    return result

def classify(train_set, classify_path):
    config = train_set.config
    
    afp, engine = get_engine(config.audio_freq, config.mfcc_block_size, config.mfcc_step_size)
    afp.processFile(engine, classify_path)

    prefix_index = math.floor((0.2) * train_set.audio_block_size())
    input_data = engine.readAllOutputs()['mfcc'][prefix_index:prefix_index + train_set.audio_block_size()]
    classifier = GMM(n_components = config.num_components, cvtype = config.cv_type)
    classifier.fit(input_data, thresh = config.em_epsilon, n_iter = config.em_iter)

    p_eval = classifier.eval(input_data)[0]
    
    ordered_best_scores = []
    for key, track_samples in train_set.get_tracks():
        best_score = float('inf')
        for datum in track_samples:
            gmm = GMM(n_components = config.num_components, cvtype = config.cv_type)    
            gmm._set_means(datum[0])
            gmm._set_covars(datum[1])
            gmm._set_weights(datum[2])
            
            q_eval = gmm.eval(input_data)[0]
               
            kld = 0.0
            
            for i in xrange(input_data.shape[0]):
                if p_eval[i] <= 0 or q_eval[i] <= 0: continue
                KL_pq = p_eval[i] * np.log(p_eval[i] / q_eval[i])
                KL_qp = q_eval[i] * np.log(q_eval[i] / p_eval[i])
                
                kld += KL_pq + KL_qp
    
            if kld < best_score:
                best_score = kld

        heapq.heappush(ordered_best_scores, (best_score, key))    
    return ordered_best_scores
