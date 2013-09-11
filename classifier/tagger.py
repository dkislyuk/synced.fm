import inspect
from collections import Counter as multiset

UNKNOWN_CLASSIFICATION_LABEL = "Unknown Track"

class Observation():
    """
    A classification result, along with the confidence score of that classification.
    
    Multiple observations can be combined into a single observation (which we can refer
    to as 'cluster') if the criteria of certain rules are met. Therefore, the 
    constructor accepts `number_observations` to indicate the number of single 
    observations that were combined. This is useful because certain rules will only be
    applied to clusters.
    """
    def __init__(self, classification, confidence, number_observations=1):
        self.classification = classification
        self.confidence = confidence
        self.number_observations = number_observations

    @property
    def unknown(self):
        return self.classification == UNKNOWN_CLASSIFICATION_LABEL 
    
    @property
    def cluster(self):
        return self.number_observations > 1
    
    @property
    def elements(self):
        return [self.classification] * self.number_observations
    
    def __str__(self):
        return "Classification: %s (confidence: %.2f, nodes: %s)" % (self.classification, 
                                                                     self.confidence, 
                                                                     self.number_observations)
    

class Rule():
    def test_condition(self):
        raise NotImplementedError("test_condition must be implemented.")
    
    def apply_rule(self):
        raise NotImplementedError("apply_rule must be implemented.")

    """ Number of observations that the rule attempts to consume """
    def arg_count(self):
        return len(inspect.getargspec(self.test_condition).args) - 1
    
    def above_threshold(self, threshold, *args):
        return all(node.confidence > threshold for node in args)
    
    def confidence_boost(self, *args):
        return max(node.confidence for node in args)


class NoisyLabelRule(Rule):
    passing_threshold = 0.5
    
    def test_condition(self, obs1):
        return not obs1.unknown and obs1.confidence < self.passing_threshold
    
    def apply_rule(self, obs1):
        return Observation(UNKNOWN_CLASSIFICATION_LABEL, 0.0, 1)


class NeighborsClusteringRule(Rule):
    threshold = 0.90
    
    def test_condition(self, obs1, obs2):        
        return (obs1.classification == obs2.classification 
                and (self.above_threshold(self.threshold, obs1, obs2) or obs1.unknown))

    def apply_rule(self, obs1, obs2): 
        return Observation(obs1.classification,
                           self.confidence_boost(obs1, obs2),
                           obs1.number_observations + obs2.number_observations)


class SmoothingRule(Rule):
    # Do not smooth a classification that we are extremely confident about
    keep_threshold = 0.99
 
    def test_condition(self, obs1, obs2, obs3):
        return (obs1.classification == obs3.classification
                and obs2.confidence < self.keep_threshold
                and not obs2.cluster
                and obs1.cluster
                and obs3.cluster)
    
    def apply_rule(self, obs1, obs2, obs3):
        return Observation(obs1.classification,
                           self.confidence_boost(obs1, obs3),
                           obs1.number_observations + obs3.number_observations)
        
class JaccardSimilarityRule(Rule):
    similarity_distance_threshold = 0.8

    def _compute_jaccard_similarity(self, mset1, mset2):
        intersection = list((mset1 & mset2).elements()) 
        union = list((mset1 | mset2).elements())
               
        return float(len(intersection)) / float(len(union))
    
    def test_condition(self, obs1, obs2, obs3):
        mset1 = multiset(obs1.elements + obs2.elements)
        mset2 = multiset(obs2.elements + obs3.elements)

        return self._compute_jaccard_similarity(mset1, mset2) > self.similarity_distance_threshold
    
    def apply_rule(self, obs1, obs2, obs3):
        label, count = multiset(obs1.elements + obs2.elements + obs3.elements).most_common()[0]

        return Observation(label,
                           self.confidence_boost(obs1, obs2, obs3),
                           number_observations=count)
    
def consume(iterator, n):
    [iterator.next() for _ in range(n)]

def ngrams(observations, n, fillvalue=None):
    observations.extend([fillvalue] * (n-1))
    for i in xrange(0, len(observations) - n + 1):
        yield observations[i:i+n]

class Tagger():
    def __init__(self, rules):
        self.rules = rules

    def tag(self, classification_results):
        nodes = [Observation(label, confidence) for label, confidence in classification_results]
        for rule in self.rules:
            arg_count = rule.arg_count()
            
            while True:
                new_nodes, rule_applied = [], False
        
                tokens = ngrams(list(nodes), arg_count)
                for observation_list in tokens:
                    if all(observation_list) and rule.test_condition(*observation_list):
                        new_nodes.append(rule.apply_rule(*observation_list))
                        rule_applied = True

                        # The remaining tokens consumed by this rule should be skipped
                        consume(tokens, arg_count - 1)
                    else:
                        # Only add the first element of any n-gram to avoid duplicates
                        new_nodes.append(observation_list[0])
                
                if rule_applied:
                    nodes = new_nodes
                else:
                    break
                
        return nodes


RULES = [NoisyLabelRule(),
         NeighborsClusteringRule(),
         SmoothingRule(),
         JaccardSimilarityRule()]

results = [('Track A', 0.96),
           ('Track A', 0.97),
           ('Track A', 0.97),
           ('Track X', 0.31),  # Noisy data
           ('Track A', 0.96),
           ('Track A', 0.99),
           ('Track A', 0.92),
           ('Track A', 0.99),
           ('Track Y', 0.28),  # Transition
           ('Track Z', 0.09),  # Transition
           ('Track B', 0.91),
           ('Track B', 0.98),
           ('Track B', 0.94),
           ('Track B', 0.95),
           ('Track B', 0.98),
           ('Track B', 0.99),
           ('Track V', 0.28),  # Noisy data
           ('Track B', 0.99),
           ('Track B', 0.96),
           ('Track B', 0.97),
           ('Track W', 0.42)]

for tag in Tagger(RULES).tag(results):
    print tag
        

