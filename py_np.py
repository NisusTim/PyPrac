import numpy as np
import cmath
import matplotlib.pyplot as plt


# np_complex
def velo_compensation(vlen=128, sign=-1, neg_velo_only=False):
  if neg_velo_only is False:
    t = np.arange(vlen >> 1, vlen + (vlen >> 1))
  else:
    t = np.arange(vlen)
  phase = sign * 1j * (t-vlen)/vlen * np.pi  # default dtype=complex128
  c = np.exp(phase)
  print(t.dtype, phase.dtype, c.dtype)
  return c

# np_merge_1: np.concatenate()
# np_merge_2: np.stack()
def np_merge():
  a1 = np.arange(3)
  a2 = np.arange(10, 13)
  concat = np.concatenate((a1, a2))  # if list: l1 + l2
  stack = np.stack((a1, a2))
  print(concat)
  print(stack)

# np.transpose() faster of 2D array than np.column_stack()
def np_transpose():
  a = np.arange(10).reshape(2, 5)
  t1 = a.T  # a.transpose(), np.transpose(a)
  t2 = np.column_stack(t2)

# non-universal function
def np_rect(rad, phi):
  Rad = np.array(rad)
  Phi = np.array(phi)
  rect = Rad * np.exp(1j * Phi)
  return rect  # <ndarray>

def cm_rect(rad, phi):
  rect = [cmath.rect(rad[idx], phi[idx]) for idx in range(len(rad))]
  return rect  # <list>

def hamming_re(N=512, alpha=25/46, PAD=0, S=1):
  alpha = 0.54
  wn = alpha - (1-alpha) * np.cos(2*np.pi * np.arange(N)/(N-1))
  return wn

def hamming_rm(N=512, factor=0.54, PAD=0, S=1):
  alpha = factor
  beta = 1-alpha
  w = []
  for p in range(PAD):
    w.append(0)
  N -= PAD
  for n in range(N):
    wn = alpha - beta * np.cos((2*np.pi*n)/(N-1))
    w.append(wn)
  if S == 1:
    return w
  wn = (np.array(w)*S).round().astype(int)
  return wn

if __name__ == '__main__':
  rad = range(5)
  phi = range(10, 15)
  n = np_rect(rad, phi)
  c = cm_rect(rad, phi)
  c = np.array(c)


  """
  plt.figure(1)
  plt.plot(f)
  plt.show()
  """
