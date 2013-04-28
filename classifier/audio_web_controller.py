import web
import threading

from training_controller import Trainer

urls = (
    '/', 'index',
    '/train', 'Train',
    '/poll/(.+)', 'poll'
)

class TrainingControllerWrapper(threading.Thread):
    def __init__(self, dataset_id):
        super(TrainingControllerWrapper, self).__init__()
        self.training_controller = Trainer(dataset_id, base_folder = "/Users/dkislyuk/synced/audio/training_sets")
        self.training_controller.create_folders()

    def run(self):
        self.training_controller.load_from_api(resample = False)

class Train:
    def POST(self):
        data = web.input()
        print "got request", data['dataset_id']
        
        wrapper = TrainingControllerWrapper(data['dataset_id'])
        wrapper.start()

        return "OK"
    
    def GET(self):
        print "got GET"
        
        return "OK"
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()