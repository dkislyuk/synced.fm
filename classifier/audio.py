import numpy as np
from yaafelib import *
from sklearn.mixture import GMM
import heapq
import pickle

training_data_path  = "audio_data/training.gmm"
training_audio_path = "audio_library/"
audio_freq = 16000

def train(track_names, num_components = 5, em_epsilon = 0.001, em_iter = 20):
    mfcc_step_size = 256
    frames_per_second = audio_freq / mfcc_step_size
    
    audio_block_size = 5 * frames_per_second
    audio_step_size = frames_per_second / 1
    
    config = {"num_components"      : num_components,
              "em_epsilon"          : em_epsilon,
              "em_iter"             : em_iter,
              "mfcc_step_size"      : mfcc_step_size,
              "audio_block_size"    : audio_block_size,
              "audio_step_size"     : audio_step_size,
              }
    
    tracks = {}
    for (name, filename) in track_names:
        tracks[name] = {}
        tracks[name]["file"] = filename
        tracks[name]["mfcc"] = {}
    
    fp = FeaturePlan(sample_rate=audio_freq)
    params = 'mfcc: MFCC blockSize=' + str(2 * mfcc_step_size) + ' stepSize=' + str(mfcc_step_size) + ' > Derivate DOrder=1'
    fp.addFeature(params)
    
    df = fp.getDataFlow()
    
    afp = AudioFileProcessor()
    for name in tracks:
        engine = Engine()
        engine.load(df)
        afp.processFile(engine, tracks[name]["file"])
        output = engine.readAllOutputs()
        
        tracks[name]['mfcc'] = output['mfcc']
        tracks[name]['num_samples'] = tracks[name]['mfcc'].shape[0]
  
    data = {}
    for name, track in tracks.iteritems():
        index = 0
        for i in range((track['num_samples'] - audio_block_size) / audio_step_size):
            mfcc_data = track['mfcc'][index:index + audio_block_size]
      
            classifier = GMM(n_components = num_components, cvtype = 'full')
            classifier.fit(mfcc_data, thresh = em_epsilon, n_iter = em_iter)

            data[name + "_" + str(i)] = classifier
            index += audio_step_size

    data["config"] = config
    pickle.dump(data, open(training_data_path, "w"))


def classify(track):
    training_data = pickle.load(open(training_data_path, "r")) 
    config = training_data.pop("config")
    
    fp = FeaturePlan(sample_rate=audio_freq)
    params = 'mfcc: MFCC blockSize=' + str(2 * config["mfcc_step_size"]) + ' stepSize=' + str(config["mfcc_step_size"]) + ' > Derivate DOrder=1'
    fp.addFeature(params)
    
    df = fp.getDataFlow()
    
    afp = AudioFileProcessor()

    test_engine = Engine()
    test_engine.load(df)
    afp.processFile(test_engine, track)
    test_track = test_engine.readAllOutputs()
       
    test_data = test_track['mfcc'][100:100 + config["audio_block_size"]]
    test_classifier = GMM(n_components = config["num_components"], cvtype = 'full')
    test_classifier.fit(test_data, thresh = config["em_epsilon"], n_iter = config["em_iter"])

    h0 = []
    h1 = []

    p_eval = test_classifier.eval(test_data)[0]
    for key, datum in training_data.iteritems():
        res = datum.eval(test_data)
        q_eval = res[0]
           
        probs = [0.0] * 2
        
        for i in xrange(test_data.shape[0]):
            if (q_eval[i] <= 1.0):
                q_eval[i] = 1.0 
            
            KL_pq = p_eval[i] * np.log(p_eval[i] / q_eval[i])
            KL_qp = q_eval[i] * np.log(q_eval[i] / p_eval[i])
            
            probs[0] += KL_pq
            probs[1] += KL_pq + KL_qp
            
        heapq.heappush(h0, (probs[0], key))
        heapq.heappush(h1, (probs[1], key))

    return h1
