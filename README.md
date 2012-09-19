Synced.fm
====================

Description
---------------------

The classifier, with default settings, trains in the following manner:

1.  Split the initial audio sample into 5-­‐second subsections, taken every second for an overlap ratio of 5.
2.  For every sub-sample, compute the first derivative (via splines) of the mel-frequency cepstral coefficient (MFCC) features for every 30ms interval, with a step size of 15ms.
3.  The collection of feature vectors for each sub-sample can now be organized into a 13-­‐dimensional, 6-component Gaussian mixture model (GMM), described by a mean vector, a covariance matrix, and a weight vector. GMMs are considered to be one of the most mature statistical models for clustering, and audio data is well suited for such representations, since beat and melody structures can be assumed to repeat themselves and thus form clusters in the feature space. We also used expectation maximization (EM), a standard technique to fit the components of the GMM to the clusters.
4.  Each GMM can be compared with another GMM with the symmetrical version of Kullback-Leibler divergence. The server returns the sub-­‐sample with the lowest divergence as the classification value.


The mobile Android app to provide recording & display capabilities is not currently released in this project. Meanwhile, tag results are rendered in a web app powered with a AngularJS/Flask/MongoDB setup.

The classifier runs inside the `classifier/audio.py` file, while the Flask API server resides in `app.py`. The AngularJS app which renders the web app is found at `static/app.js`.


Installation
---------------------

Required libraries:

+ [Yaafe](http://yaafe.sourceforge.net/): An audio library which enables MFCC extraction for training & classification.
+ [scikit-learn](http://scikit-learn.org/): The standard Python machine learning library, used to construct Gaussian Mixture Models (GMM) to represent the the MFCC variance.
+ [Flask](http://flask.pocoo.org/): A popular, highly-extendible, web microframework to build fast and simple API's. 


Authors
---------------------
Dmitry Kislyuk (~dkislyuk)
