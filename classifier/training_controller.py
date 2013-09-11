import audio
import conn
import copy
import os
import subprocess

from mongokit import ObjectId

from models import DataSet
from conn import training_folder
from conn import conn_str
from util import logger

conf_default = {
    'mfcc_step_size'    : 256,
    'mfcc_block_size'   : 512,
    'num_components'    : 6,
    'em_epsilon'        : 0.001,
    'em_iter'           : 100,
    'audio_freq'        : 16000,
    'sample_step_size'  : 1,
    'sample_length'     : 5,
    'cv_type'           : 'full'
}

class Trainer():
    def __init__(self, set_id=None, set_name=None, conf=conf_default):          
        self.connection = conn.get();
        self.connection.register([DataSet])
    
        if set_id == None:
            self.train_set = self.connection.DataSet()
            self.train_set.config = conf
            self.train_set.name = set_name
            
            self.train_set.save()
        else:
            self.train_set = self.connection.DataSet.one({"_id": ObjectId(set_id)})

        self.folder_path = training_folder + '/' + self.generate_name()
        self.validation_path = self.folder_path + '/validation/'
        
    def generate_name(self):
        return self.train_set.name.strip().replace(" ", "_").lower()

    def create_folders(self):
        subprocess.call(['mkdir', self.folder_path], stdout=subprocess.PIPE)
        subprocess.call(['mkdir', self.validation_path], stdout=subprocess.PIPE)
    
    # using user input to do labeling
    def load_from_folder(self, resample, use_default_labels):
        os.chdir(self.folder_path)
        
        training_files = []
        if use_default_labels:
            for filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
                label = filename.replace('_', ' ').replace('.mp3', '').title()
                training_files.append((label, filename))
                
                logger.log("Using %s with label %s" % (filename, label))
        else:    
            resample_prefix = 'resample_'
            for filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
                print " enter label for '" + filename + "' >"
                label = raw_input()
                
                if len(label) == 0: label = filename
                
                target = filename
                if resample:
                    target = resample_prefix + filename
                    try:
                        subprocess.call(['/usr/local/bin/lame', '-V5', '--vbr-new', '--resample', '16', filename, target], 
                                        stdout=subprocess.PIPE)
                        
                        generated_name = label.strip().replace(" ", "_").lower() + '.mp3'
                        subprocess.call(['rm', filename])
                        subprocess.call(['mv', target, generated_name])
                        
                        training_files.append((label, generated_name))
                    except:
                        logger.warn(" could not resample file '%s'!" % filename)
                else:
                    training_files.append((label, target))
            print 'finished resampling!'
        
        self.train_set.data = audio.train(training_files, self.folder_path, self.train_set.config, self.train_set.name, conn_str)
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
                #filename = track['filename'] 
                
                print "fetching: ", url        
                        
                subprocess.call(['curl', '-O', url], stdout=subprocess.PIPE)
                filename = url.split('/')[-1]
                
                subprocess.call(['mv', filename, filename + '.mp3'])
                filename = filename + '.mp3'
                target = filename
                if resample:
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
        
        self.train_set.data = audio.train(training_files, self.folder_path, self.train_set.config, self.train_set.name, conn_str)
        self.train_set.status = "trained"
        self.train_set.save()

    def validate(self, classify_path = None):        
        total_score = 0.0
        K = 3

        if classify_path is None:
            for filename in [f for f in os.listdir(self.validation_path) if os.path.isfile(self.validation_path + f)]:
                logger.log("classifying %s" % filename)
                scores = audio.classify(self.train_set, self.validation_path + filename)
                label = filename.replace('_', ' ').replace('.mp3', '').title()
                
                top_pick = scores[0]
                second = scores[1]
                third = scores[2]
                fourth = scores[3]
                
                if top_pick[1] == label:
                    confidence_1 = (float(second[0]) - float(top_pick[0])) / float(second[0])
                    confidence_2 = (float(third[0]) - float(top_pick[0])) / float(third[0])
                    confidence_3 = (float(fourth[0]) - float(top_pick[0])) / float(fourth[0])
                    
                    total_score += (confidence_1 + confidence_2 + confidence_3) / float(K)
                    print "classify correct, confidence: ", (confidence_1 + confidence_2 + confidence_3) / float(K)
                else:
                    print "incorrect classify %s %s" % (top_pick[1], label)
                
                print " first  > ", top_pick
                print " second > ", second 
                    
        else:
            logger.log(audio.classify(self.train_set, self.validation_path + classify_path))   
    
        self.train_set.default_validation_score = total_score
        self.train_set.save()
           
        return total_score
        
    def cleanup(self):
        self.train_set.delete_data()
        self.status = "completed"
        self.train_set.save()

class Experiment():
    def test_gmm_params(self):
        conf_test = copy.deepcopy(conf_default)
        
        num_components_min = 5
        num_components_max = 9
        num_components_step = 2
        
        em_iter_min = 50
        em_iter_max = 200
        em_iter_step_exp = 2
        
        mfcc_block_size_min = 256
        mfcc_block_size_max = 2048
        mfcc_block_size_step_exp = 2
        
        block_overlap = 2
        
        num_components = num_components_min
        em_iter = em_iter_min
        mfcc_block_size = mfcc_block_size_min
        
        results = []
        while num_components <= num_components_max:
            while em_iter <= em_iter_max:
                while mfcc_block_size <= mfcc_block_size_max:
                    conf_test['num_components']     = num_components
                    conf_test['mfcc_block_size']    = mfcc_block_size
                    conf_test['mfcc_step_size']     = mfcc_block_size / block_overlap
                    conf_test['em_iter']            = em_iter
                    
                    print ">>> begin: ", (mfcc_block_size, num_components, em_iter)
                    
                    t = Trainer(set_name = "galactica", conf=conf_test)
                    training_set_id = t.load_from_folder(False, True)
                    
                    t2 = Trainer(set_id = training_set_id)
                    validation_score = t2.validate()

                    t2.cleanup()
                    
                    results.append([mfcc_block_size, num_components, em_iter, validation_score])
                    print ">>> completed: ", [mfcc_block_size, num_components, em_iter, validation_score]
                    
                    mfcc_block_size *= mfcc_block_size_step_exp
                
                mfcc_block_size = mfcc_block_size_min
                em_iter *= em_iter_step_exp
            em_iter = em_iter_min
            num_components += num_components_step
        
        print results
        
    def test_all_params(self):
        conf_test = copy.deepcopy(conf_default)
        
        num_components_min = 11
        num_components_max = 12
        num_components_step = 1

        
        mfcc_block_size_min = 512
        mfcc_block_size_max = 2048
        mfcc_block_size_step_exp = 2
        
        block_overlap_min = 2
        block_overlap_max = 4
        block_overlap_step_size = 2 
        
        num_components = num_components_min
        mfcc_block_size = mfcc_block_size_min
        block_overlap = block_overlap_min
        
        results = []
        while num_components <= num_components_max:            
            while block_overlap <= block_overlap_max:
                while mfcc_block_size <= mfcc_block_size_max:
                    
                    conf_test['num_components']     = num_components
                    conf_test['mfcc_block_size']    = mfcc_block_size
                    conf_test['mfcc_step_size']     = mfcc_block_size / block_overlap

                    print ">>> begin: ", (mfcc_block_size, num_components, block_overlap)
                    
                    t = Trainer(set_name = "galactica", conf=conf_test)
                    training_set_id = t.load_from_folder(False, True)
                    
                    t2 = Trainer(set_id = training_set_id)
                    validation_score = t2.validate()

                    t2.cleanup()
                    
                    results.append([mfcc_block_size, num_components, block_overlap, validation_score])
                    print ">>> completed: ", [mfcc_block_size, num_components, block_overlap, validation_score]
                    
                    mfcc_block_size *= mfcc_block_size_step_exp
                
                mfcc_block_size = mfcc_block_size_min
                block_overlap += block_overlap_step_size
            block_overlap = block_overlap_min
            num_components += num_components_step
        
        print results
        
        
    def test_covar_param(self):
        conf_test = copy.deepcopy(conf_default)
        
        num_components_min = 4
        num_components_max = 12
        num_components_step = 1

        mfcc_block_size_min = 512
        mfcc_block_size_max = 2048
        mfcc_block_size_step_exp = 2
        
        block_overlap_min = 2
        block_overlap_max = 2
        block_overlap_step_size = 2 
        
        num_components = num_components_min
        mfcc_block_size = mfcc_block_size_min
        block_overlap = block_overlap_min
        
        results = []
        while num_components <= num_components_max:            
            while block_overlap <= block_overlap_max:
                while mfcc_block_size <= mfcc_block_size_max:
                    
                    conf_test['num_components']     = num_components
                    conf_test['mfcc_block_size']    = mfcc_block_size
                    conf_test['mfcc_step_size']     = mfcc_block_size / block_overlap

                    print ">>> begin: ", (mfcc_block_size, num_components, block_overlap)
                    
                    t = Trainer(set_name = "galactica", conf=conf_test)
                    training_set_id = t.load_from_folder(False, True)
                    
                    t2 = Trainer(set_id = training_set_id)
                    validation_score = t2.validate()

                    t2.cleanup()
                    
                    results.append([mfcc_block_size, num_components, block_overlap, validation_score])
                    print ">>> completed: ", [mfcc_block_size, num_components, block_overlap, validation_score]
                    
                    mfcc_block_size *= mfcc_block_size_step_exp
                
                mfcc_block_size = mfcc_block_size_min
                block_overlap += block_overlap_step_size
            block_overlap = block_overlap_min
            num_components += num_components_step
        
        print results
        
e = Experiment()
#e.test_gmm_params()
#e.test_all_params()
e.test_covar_param()


#t_c = Trainer(set_id = "517d1139c1e3df1ea5000096")
#t_c.train_set.default_validation_score = 11.8857716973
#t_c.cleanup()

#print t_c.validate()




#t = Trainer(set_name = 'kickstarts', base_folder = "/Users/dkislyuk/synced/audio/training_sets")
#t = Trainer(set_name = "galactica", base_folder = "/Users/dkislyuk/synced/audio/training_sets")
#t = Trainer(set_name = "set1", base_folder = "/Users/dkislyuk/synced/audio/training_sets")
#training_set_id = t.load_from_folder(False, True)
#t2 = Trainer(set_id = training_set_id, base_folder = "/Users/dkislyuk/synced/audio/training_sets")
#t2.validate("innocence.mp3")


#t2 = Trainer(set_id = "517485e6c1e3df0a29000000", base_folder = "/Users/dkislyuk/synced/audio/training_sets")
#t2.validate()

#todo resample validations


