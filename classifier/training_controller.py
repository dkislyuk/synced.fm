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

default_home = '/home/ec2-user/train_data'

class Trainer():
    def __init__(self, set_id=None, set_name=None, base_folder=None, conf=conf_default):
        self.connection = Connection(conn_str)
        self.connection.register([DataSet])
        
        print "set_id: ", set_id
        
        if base_folder != None:
            default_home = base_folder

        if set_id == None:
            
            print "creating new set"
            self.train_set = self.connection.DataSet()
            self.train_set.config = conf
            self.train_set.name = set_name
            
            self.train_set.save()
        else:
            self.train_set = self.connection.DataSet.one({"_id": ObjectId(set_id)})
            
            print "obj:"
            print self.train_set.name
            #self.config = conf_default
            
        self.folder_path = default_home + '/' + self.generate_name()
        self.validation_path = self.folder_path + '/validation/'
        
    def generate_name(self):
        return self.train_set.name.strip().replace(" ", "_").lower()

    def create_folders(self):
        subprocess.call(['mkdir', self.folder_path], stdout=subprocess.PIPE)
        subprocess.call(['mkdir', self.validation_path + '/validation/'], stdout=subprocess.PIPE)
    
    # using user input to do labeling
    def load_from_folder(self, resample):
        os.chdir(self.folder_path)
        
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
        
        self.train_set.data = [ObjectId('5151e437cb32158bbc000001'), ObjectId('5151e481cb32158bbc000002'), ObjectId('5151e4a4cb32158bbc000003'), ObjectId('5151e4dfcb32158bbc000004'), ObjectId('5151e513cb32158bbc000005')]
#audio.train(training_files, self.folder_path, conf_default, self.train_set.name, conn_str)
        

        self.train_set.s3_links = []
        self.train_set.status = "trained"
        
        self.train_set.save()
        
        
        return self.train_set._id
    
    def load_from_api(self, resample):
        os.chdir(self.folder_path)
        
        training_files = []
        try:
            for i in range(len(self.train_set.s3_links)):
                track = self.train_set.s3_links[i]
                
                label = track['label']
                url = track['url']
                filename = track['filename']
                
                subprocess.call(['curl', '-X', 'GET', url], stdout=subprocess.PIPE)
                
                
                
                # WONT WORK, gotta do a HEAD request to get the filename here
                #filename = "track_" + str(i) + ".mp3"
  
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
  
        except:
            print " could not do training."
            
        print 'finished resampling!'
        
        self.train_set.data = audio.train(training_files, self.folder_path, self.track_set.config, self.train_set.set_name, conn_str)
        self.train_set.status = "trained"
        
        
        self.train_set.save()
            
 
    def train(self):
        pass
        
    def validate(self, classify_path):        
        #connection = Connection(conn_str)
        #connection.register([DataSet])
        
        #train_set = connection.DataSet.one({"_id": ObjectId(training_set_id)})
    
        audio.classify(self.train_set, self.validation_path + classify_path)

class Experiment():
    def __init__(self):
        pass
    
    #def run_experiment(self, *kwargs):
    def run_experiment(self, param):
        # USE PANDAS HERE
        
        step_size = 0.1
        min_val = 0
        max_val = 1
        
        current = min_val
        while (current <= max_val):
            
            current += step_size
            
            t = Trainer(set_name="exp")
        
        pass
        

#t = Trainer(set_name = "set1", base_folder = "/Users/dkislyuk/synced/audio/training_sets")
#training_set_id = t.load_from_folder(False)
#t2 = Trainer(set_id = training_set_id, base_folder = "/Users/dkislyuk/synced/audio/training_sets")
#t2.validate("pompo_boost_sped.mp3")

#todo resample validations
