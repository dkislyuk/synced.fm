import audio
import os
import subprocess

from mongokit import Connection
from mongokit import ObjectId

from models import DataSet
from conn import conn_str

conf_default = {
    'mfcc_step_size'    : 256,
    'mfcc_block_size'   : 512,
    'num_components'    : 6,
    'em_epsilon'        : 0.001,
    'em_iter'           : 100,
    'audio_freq'        : 16000,
    'block_overlap'     : 5,
    'cv_type'           : 'diag'
}

class Trainer():
    def __init__(self, set_name, folder_path):
        self.folder_path = folder_path
        self.validation_path = folder_path + '/validation/'
    
    # using user input to do labeling
    def load_from_folder(self, set_name, folder_path, resample):
        self.folder_path = folder_path
        self.validation_path = folder_path + '/validation/'

        os.chdir(folder_path)
        
        training_files = []
        for filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
            print " enter label for '" + filename + "' >"
            label = raw_input()
            
            if len(label) == 0: label = filename
            print "label is %s\n" % label
            
            target = filename
            if (resample):
                print "resampling in 16000..."
                target = 'resample_' + filename
                try:
                    subprocess.call(['/usr/local/bin/lame', '-V5', '--vbr-new', '--resample', '16', filename, target], 
                                    stdout=subprocess.PIPE)
                except:
                    print " could not resample file '%s'!" % filename
                
            training_files.append((label, target))

        print 'finished resampling!'
        
        
        connection = Connection(conn_str)
        connection.register([DataSet])
        
        training_set = connection.DataSet()
        
        training_set.config = conf_default
        training_set.name = set_name
        training_set.data = audio.train(training_files, folder_path, conf_default, set_name, conn_str)
        
        training_set.save()
        
        return training_set._id
    
    def load_from_web_app(self):
        pass

    def train(self):
        pass
        
    def validate(self, training_set_id, classify_path):        
        connection = Connection(conn_str)
        connection.register([DataSet])
        
        train_set = connection.DataSet.one({"_id": ObjectId(training_set_id)})
    
        audio.classify(train_set, self.validation_path + classify_path)
        
