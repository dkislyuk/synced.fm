import numpy as np
from yaafelib import *
from sklearn.mixture import GMM
import heapq

import math

from models import TrackData
from models import DataSet
from mongokit import Connection

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
    print 'begin training sequence on %s ' % training_audio_path
    
    # set up all parameters
    num_components      = conf['num_components']
    em_epsilon          = conf['em_epsilon']
    em_iter             = conf['em_iter']
    cv_type             = conf['cv_type']
    
    audio_freq          = conf['audio_freq']
    mfcc_step_size      = conf['mfcc_step_size']
    mfcc_block_size     = conf['mfcc_block_size']
    frames_per_second   = audio_freq / mfcc_step_size
    
    audio_block_size    = conf['block_overlap'] * frames_per_second
    audio_step_size     = frames_per_second / 1
    
    # set up Yaafe

    afp, engine = get_engine(audio_freq, mfcc_block_size, mfcc_step_size)
   
    connection = Connection(conn_str)
    connection.register([TrackData])
    result = []
    
    for label, filename in tracks:
        print 'begin processing %s' % filename
        afp.processFile(engine, training_audio_path + '/' + filename)
        output = engine.readAllOutputs()['mfcc']
        
        mfcc = output     
        num_samples = mfcc.shape[0]
        track_gmms = []
        
        index = 0
        
        print 'begin construction of GMMs for %s ' % filename

        track = connection.TrackData()
        track.label = label
        track.set = set_name
        
        for _ in range((num_samples - audio_block_size) / audio_step_size):
            mfcc_data = mfcc[index:index + audio_block_size]
            
            classifier = GMM(n_components = num_components, cvtype = cv_type)
            classifier.fit(mfcc_data, thresh = em_epsilon, n_iter = em_iter)

            means = classifier._get_means().tolist()            
            covars = [np.diag(diag).tolist() for diag in classifier._get_covars()]
            weights = classifier._get_weights().tolist()

            track_gmms.append([means, covars, weights])
            
            index += audio_step_size

        track.data = track_gmms
        track.save()
        
        result.append(track._id)
        
        print "done training: ", label

    return result



def classify(train_set, classify_path):
    config = train_set.config
    
    afp, engine = get_engine(train_set.config.audio_freq, config.mfcc_block_size, config.mfcc_step_size)
    afp.processFile(engine, classify_path)

    input_data = engine.readAllOutputs()['mfcc'][100:100 + train_set.audio_block_size()]
    classifier = GMM(n_components = config.num_components, cvtype = config.cv_type)
    classifier.fit(input_data, thresh = config.em_epsilon, n_iter = config.em_iter)

    p_eval = classifier.eval(input_data)[0]
    
    ordered_scores = []
    results = {}
    for key, track_samples in train_set.get_tracks():
        
        track_scores = []
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
    
            heapq.heappush(track_scores, kld)
        
        # use heaps, because we want to extend this in the future to take top k results of every track   
        results[key] = heapq.heappop(track_scores)
        heapq.heappush(ordered_scores, results[key])

    score_list = results.values()
    num_entries = len(score_list)
    diff_sum = 0.0
    
    for i in range(num_entries):
        for j in range(num_entries - i - 1):
            diff_sum += math.fabs(score_list[i] - score_list[j + i + 1])
            
    diff_avg = diff_sum / (((num_entries - 1) * num_entries) / 2)
    diff_computed_label = -1 * (heapq.heappop(ordered_scores) - heapq.heappop(ordered_scores))
    
    print diff_avg
    print results
    
    print diff_computed_label * diff_avg
