import numpy as np
import h5py

snap = #array with snapshots of the MaNGIA galaxies
shalo = #array with subhalo ID of the MaNGIA galaxies


f = h5py.File('morphs_kinematic_bars.hdf5', 'r') #From Zana+(2022) https://arxiv.org/abs/2206.04693
bulge_fraction = np.zeros_like(snap, dtype=np.float64)
pseudobulge_fraction = np.zeros_like(snap, dtype=np.float64) #spheroidal morphology but rotates
halo_fraction = np.zeros_like(snap, dtype=np.float64)
thind_fraction = np.zeros_like(snap, dtype=np.float64)
thickd_fraction = np.zeros_like(snap, dtype=np.float64)

for snapshot in range(87,99):
    subsubid = subhalo_id[snapshot==snap]
    subid_morphcat = np.array(f['Snapshot_'+str(snapshot)]['SubhaloID'])
    for shalo in subsubid:
        index = np.nonzero((snapshot==snap)&(subhalo_id==shalo))[0]
        index_morphcat = np.arange(subid_morphcat.size)[subid_morphcat==shalo]
        #print(len(index_morphcat), index_morphcat)
        if len(index_morphcat)!=0:
            #print(index, len(index_morphcat), index_morphcat[0])
            bulge_fraction[index] = f['Snapshot_'+str(snapshot)]['Bulge'][0, [index_morphcat]][0]
            pseudobulge_fraction[index] = f['Snapshot_'+str(snapshot)]['PseudoBulge'][0, [index_morphcat]][0]
            halo_fraction[index] = f['Snapshot_'+str(snapshot)]['Halo'][0, [index_morphcat]][0]
            thind_fraction[index] = f['Snapshot_'+str(snapshot)]['ThinDisc'][0, [index_morphcat]][0]
            thickd_fraction[index] = f['Snapshot_'+str(snapshot)]['ThickDisc'][0, [index_morphcat]][0]
            
spheroidal = bulge_fraction+pseudobulge_fraction+halo_fraction            
disc = thind_fraction + thickd_fraction
            
