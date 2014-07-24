# -*- coding: utf-8 -*-
from __future__ import print_function, division
import importlib
import random
import collections

spac = '   '
down = '│  '
tndw = '├──'
turn = '└──'

def print_explorer(cfg):
    s = _explorers(cfg)
    return ''.join(s)

def _explorers(cfg, prefix=''):
    name = cfg.classname.rsplit('.', 1)[1]
    if name == 'Mix2Explorer':
        return _mix_explorer(cfg, prefix=prefix)
    else:
        return ['{}{}\n'.format(prefix, name)]

def _mix_explorer(cfg, prefix=''):
    # s = ['{}Mix2\n'.format(prefix)]
    s = []
    s.append('{}├── {}\n'.format(prefix, _timeline(cfg)))
    s.extend(_explorers(cfg.explorer_a, prefix=prefix+'│   '))
    s.append('{}└── else\n'.format(prefix))
    s.extend(_explorers(cfg.explorer_b, prefix=prefix+'    '))
    return s

def _timeline(cfg):
    if cfg.bootstrap_a > 0:
        if cfg.permitted_a < 1e308:
            return '100% (0-{}), then {}% until {}'.format(int(cfg.bootstrap_a), int(100*cfg.ratio_a), cfg.permitted_a)
        else:
            return '100% (0-{}), then {}%'.format(int(cfg.bootstrap_a), int(100*cfg.ratio_a))
    else:
        return '{}%'.format(int(100*cfg.ratio_a))

def _load_class(classname):
    """Load a class from a string"""
    module_name, class_name = classname.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

def to_vector(signal, channels=None):
    """Convert a signal to a vector"""
    if channels is None:
        # we need consistent ordering
        assert isinstance(signal, collections.OrderedDict)
        return tuple(signal.values())
    else:
        return tuple(signal[c.name] for c in channels)

def to_signal(vector, channels):
    """Convert a vector to a signal"""
    assert len(vector) == len(channels)
    return {c_i.name: v_i for c_i, v_i in zip(channels, vector)}

def random_signal(channels, bounds=None):
    if bounds is None:
        return {c.name: c.fixed if c.fixed is not None else random.uniform(*c.bounds)
                for c in channels}
    else:
        return {c.name: c.fixed if c.fixed is not None else random.uniform(*b)
                for c, b in zip(channels, bounds)}

def avg_signal(channels, bounds=None):
    if bounds is None:
        return {c.name: c.fixed if c.fixed is not None else 0.5*(c.bounds[0]+c.bounds[1])
                for c in channels}
    else:
        return {c.name: c.fixed if c.fixed is not None else 0.5*(b[0]+b[1])
                for c, b in zip(channels, bounds)}

def roulette_wheel(proba):
    assert len(proba) >= 1
    """Given a vector p, return index i with probability p_i/sum(p).
    Elements of p are positive numbers.
    @param proba    list of positive numbers
    """
    sum_proba = sum(proba)
    dice = random.uniform(0., sum_proba)
    if sum_proba == 0.0:
        return random.randint(0, len(proba)-1)
    s, i = proba[0], 0
    while (i < len(proba)-1 and dice >= s):
        i += 1
        assert proba[i] >= 0, "all elements are not positive {}".format(proba)
        s += proba[i]
    return i

def belongs(p, bounds):
    if p is None or bounds is None:
        return False
    assert len(p) == len(bounds)
    return all(b_i[0] <= p_i <= b_i[1] for p_i, b_i in zip(p, bounds))



def vec_norm(a, b):
    return math.sqrt(sum((a_i-b_i)**2 for a_i, b_i in zip(a, b)))

def vec_norm_sq(a, b):
    return sum((a_i-b_i)**2 for a_i, b_i in zip(a, b))

def sgn_norm(a, b, channels):
    return math.sqrt(sum((a[c]-b[c])**2 for c in channels))

def sgn_norm_sq(a, b, channels):
    return sum((a[c]-b[c])**2 for c in channels)

