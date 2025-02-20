# Write your crossmatch function here.
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np
import time

def angular_dist(r1, d1, r2, d2):
  a = np.sin(np.abs(d1 - d2)/2)**2
  b = np.cos(d1)*np.cos(d2)*np.sin(np.abs(r1 - r2)/2)**2
  d = 2*np.arcsin(np.sqrt(a + b))
  return d

def crossmatch(set1, set2, dist):
  start = time.perf_counter()
  max_radius = dist
  
  matches = []
  no_matches = []
  
  coords1_sc = SkyCoord(set1*u.degree, frame='icrs')
  coords2_sc = SkyCoord(set2*u.degree, frame='icrs')
  
  closest_ids, closest_dists, _ = coords1_sc.match_to_catalog_sky(coords2_sc)
  
  for id1, (closest_id2, dist) in enumerate(zip(closest_ids, closest_dists)):
    closest_dist = dist.value
        
    if closest_dist > max_radius:
      no_matches.append(id1)
    else:
      matches.append([id1, closest_id2, closest_dist])
  
  time_taken = time.perf_counter() - start
  return matches, no_matches, time_taken



# You can use this to test your function.
# Any code inside this `if` statement will be ignored by the automarker.
if __name__ == '__main__':
  # The example in the question
  cat1 = np.array([[180, 30], [45, 10], [300, -45]])
  cat2 = np.array([[180, 32], [55, 10], [302, -44]])
  matches, no_matches, time_taken = crossmatch(cat1, cat2, 5)
  print('matches:', matches)
  print('unmatched:', no_matches)
  print('time taken:', time_taken)

  # A function to create a random catalogue of size n
  def create_cat(n):
    ras = np.random.uniform(0, 360, size=(n, 1))
    decs = np.random.uniform(-90, 90, size=(n, 1))
    return np.hstack((ras, decs))

  # Test your function on random inputs
  np.random.seed(0)
  cat1 = create_cat(10)
  cat2 = create_cat(20)
  matches, no_matches, time_taken = crossmatch(cat1, cat2, 5)
  print('matches:', matches)
  print('unmatched:', no_matches)
  print('time taken:', time_taken)
