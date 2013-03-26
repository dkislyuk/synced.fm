Synced.fm
====================

Description
---------------------

Synced.fm began as a mobile app with a classifier to tag song snippets recorded in noisy enviroments. Using several excellent Python machine learning libraries, a reliable server-backend was built which accurately classifies clips of audio recordings, and posts the results in an online web-app.

The classifier, with default settings, trains in the following manner:

1.  Split the initial audio sample into 5-­‐second subsections, taken every second for an overlap ratio of 5.
2.  For every sub-sample, compute the first derivative (via splines) of the [mel-frequency cepstral coefficient](http://en.wikipedia.org/wiki/Mel-frequency_cepstrum) (MFCC) features for every 30ms interval, with a step size of 15ms.
3.  The collection of feature vectors for each sub-sample can now be organized into a 13-­‐dimensional, 6-component Gaussian mixture model (GMM), described by a mean vector, a covariance matrix, and a weight vector. GMMs are considered to be one of the most mature statistical models for clustering, and audio data is well suited for such representations, since beat and melody structures can be assumed to repeat themselves and thus form clusters in the feature space. We also used expectation maximization (EM), a standard technique to fit the components of the GMM to the clusters. This training process is described in depth in the [mixture model](http://en.wikipedia.org/wiki/Gaussian_mixture_model#Parameter_estimation_and_system_identification) wikipedia page.
4.  Each GMM can be compared with another GMM with the symmetrical version of [Kullback-Leibler divergence](http://en.wikipedia.org/wiki/Kullback-Leibler_divergence). The server returns the sub-­‐sample with the lowest divergence as the classification value.


The mobile Android app to provide recording & display capabilities is not currently released in this project. Meanwhile, tag results are rendered in a web app powered with a AngularJS/Flask/MongoDB setup, and D3.js for data visualization.

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





Copyright 2013 Dmitry Kislyuk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
