import datetime
import numpy as np

from pynwb import NWBFile, NWBHDF5IO
from ndx_labels import LabelSeries, RepresentationSeries
from pynwb.image import ImageSeries

nwbfile = NWBFile(
        session_description='session_description',
        identifier='identifier',
        session_start_time=datetime.datetime.now(datetime.timezone.utc)
)

behavior_module = nwbfile.create_processing_module(
    name="behavior", description="behavior"
)

video = np.random.rand(100, 128, 128)
image_series = ImageSeries(
    name='video',
    data=video,
    rate=30.0
)

pcs = np.random.rand(100, 4).astype('float64')
representation_series = RepresentationSeries(
    name='pcs',
    description='pc projections',
    data=pcs,
    method='iterated SVD',
    rate=30.0,
    starting_time=0.0,
    video=image_series
)

labels = np.random.rand(100, 5).astype(bool)
vocab = np.random.rand(5).astype(str)
label_series = LabelSeries(
    name='labels',
    description='labels',
    data=labels,
    vocabulary=vocab,
    rate=30.0,
    starting_time=0.0,
    exclusive=False,
    method='jim did it',
    representation=representation_series,
    video=image_series
)

behavior_module.add(label_series)
behavior_module.add(representation_series)
nwbfile.add_acquisition(image_series)

with NWBHDF5IO('test.nwb', mode='w') as io:
    io.write(nwbfile)