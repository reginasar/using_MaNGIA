import numpy as np
import os
from astropy.io import fits
#import matplotlib.pyplot as plt

cat_dir = ''
ssp_dir = ''
mask_dir = ''

hdu_cat = fits.open(cat_dir + 'TNG50_MaNGA_v13_Nview.fits')
snaps = hdu_cat[1].data['snapshot']
subhalo_id = hdu_cat[1].data['subhalo_id']
ifu_dsn = hdu_cat[1].data['manga_ifu_dsn']
views = hdu_cat[1].data['view']

# mocks are not available for view>5, snap=0 or a few that got stopped 
# in the mocking process. Total mocks should be >10,0030.


ifu_masks, hdr = fits.getdata(mask_dir+'masks.fits', 0, header=True)
SN = 3 # signal to noise cut in the i-flux, 
       # generally 3 is enough to remove the large voronoi-like bins of the edges,
       # some galaxies might need a greater SN threshold

ind_in_cat = []
band_maps = []
vel_maps = []
disp_maps = []
for ii in range(10):#len(snaps)):
    ssp_name = ssp_dir + 'ilust-'+str(snaps[ii])+'-'+str(subhalo_id[ii])+\
                        '-'+str(views[ii])+'-127.cube.SSP.cube.fits.gz'
    if not os.path.exists(ssp_name):
        continue

    ssp_f = fits.open(ssp_name)
    sn_mask = np.where(ssp_f[0].data[3]/ssp_f[0].data[4]>SN, 1, np.nan)
    ifu_mask_ = np.where(ifu_masks[hdr['MASK'+str(ifu_dsn[0])]]==1, 1, np.nan)
    band_map_ = ssp_f[0].data[0] * ifu_mask_ * sn_mask
    band_maps.append(band_map_)
    vel_map_ = ssp_f[0].data[13] * ifu_mask_ * sn_mask
    vel_maps.append(vel_map_)
    disp_map_ = ssp_f[0].data[15] * ifu_mask_ * sn_mask
    disp_maps.append(disp_map_)
    
    ind_in_cat.append(ii)
    #plt.imshow(vel_map_)
    #plt.colorbar()
    #plt.show()

band_maps = np.array(band_maps, dtype=np.float32)
vel_maps = np.array(vel_maps, dtype=np.float32)
disp_maps = np.array(disp_maps, dtype=np.float32)

