import numpy as np
from scipy.optimize import minimize

# ---------- Define your WVP here ----------
# Replace with your actual 4x4 numpy array
#WVP = np.identity(4)  # placeholder
#209 CBV 2: CB1

#WARNING: numpy convention is COLUMN major
#row major defined, .T on the end transposes to column major
WVP = np.array([

 [1.33797, 0.955281, -0.546106, -0.546052],
 [-0.937522, 2.05715, -0.0830864, -0.0830781],
 [0.782967, 0.830887, 0.83375, 0.833667],
 [0, 0, 4.37257, 4.47214]

], dtype=np.float32).T

# ---------- Cube geometry ----------
cube = np.array([
    [0,0,0,1],
    [1,0,0,1],
    [0,1,0,1],
    [0,0,1,1],
    [1,1,0,1],
    [1,0,1,1],
    [0,1,1,1],
    [1,1,1,1]
], dtype=float)

edges = [(0,1),(0,2),(0,3),
         (1,4),(1,5),
         (2,4),(2,6),
         (3,5),(3,6),
         (4,7),(5,7),(6,7)]

# ---------- Perspective utility ----------
def perspectiveGL(fov_y_deg, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fov_y_deg)/2.0)
    m = np.zeros((4,4))
    m[0,0] = f/aspect
    m[1,1] = f
    m[2,2] = (far+near)/(near-far)
    m[2,3] = (2*far*near)/(near-far)
    m[3,2] = -1
    return m
    
#DX
def perspective(fov_y_deg, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fov_y_deg)/2.0)
    m = np.zeros((4,4))
    m[0,0] = f/aspect
    m[1,1] = f
    m[2,2] = far/(far-near)
    m[2,3] = (-far*near)/(far-near)
    m[3,2] = 1
    return m

def cube_edge_error(WVP, P, printIt=False):
    try:
        P_inv = np.linalg.inv(P)
    except np.linalg.LinAlgError:
        return 1e9
#    M = WVP @ P_inv #GL
    M = np.linalg.inv(P) @ WVP #DX
    if printIt:
        print("Estimated World-View matrix (WVP * P_inv):\n", M)
    pts = (M @ cube.T).T
    pts = pts[:,:3] / np.clip(pts[:,3,None], 1e-9, None)
    err = 0.0
    for i,j in edges:
        d = np.linalg.norm(pts[i]-pts[j])
        err += (d-1.0)**2
    return err

# ---------- Coarse grid search ----------
def coarse_search(WVP, aspect, far, 
                  fov_range=(30,120,2.0),
                  near_values=(0.05,0.1,0.2,0.5,1.0)):
    best, best_err = None, float("inf")
    fmin, fmax, fstep = fov_range
    for fov in np.arange(fmin,fmax+1e-9,fstep):
        for n in near_values:
            if n >= far: 
                continue
            P = perspective(fov, aspect, n, far)
            err = cube_edge_error(WVP, P)
            if err < best_err:
                best_err = err
                best = (fov,n)
    return best, best_err

# ---------- Refine with Nelder–Mead ----------
def refine_params(WVP, aspect, far, init_guess):
    def cost(x):
        fov, n = x
        if fov <= 1 or fov >= 179: return 1e9
        if n <= 0 or far <= n: return 1e9
        P = perspective(fov, aspect, n, far)
        return cube_edge_error(WVP, P)

    res = minimize(cost, init_guess,
                   method="Nelder-Mead",
                   options={"maxiter":500,"xatol":1e-6,"fatol":1e-9})
    return res.x, res.fun

# ---------- Run ----------
aspect = 800/600  # set your aspect ratio
far = 10000

coarse_guess, coarse_err = coarse_search(WVP, aspect, far)
print("Coarse guess: fov=%.2f, near=%.3f, far=%.1f, err=%.6f" %
      (coarse_guess[0],coarse_guess[1],far,coarse_err))

refined_params, refined_err = refine_params(WVP, aspect, far, coarse_guess)
print("Refined: fov=%.6f, near=%.6f, far=%.6f, err=%.12f" %
      (refined_params[0],refined_params[1],far,refined_err))

#P = perspective(43.929014, aspect, 0.108044, 5000)
#e = cube_edge_error(WVP, P)
#print("Attempt: "+str(e));
        
#P = perspective(43.949189, aspect, 0.147386, 10000)
#e = cube_edge_error(WVP, P, True)
#print("Attempt: "+str(e));

