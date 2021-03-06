import datetime
import numpy as np

from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing import TestCase, remove_test_file, AcquisitionH5IOMixin

from ndx_labels import LabelSeries, RepresentationSeries
from pynwb.image import ImageSeries


def set_up_nwbfile():
    nwbfile = NWBFile(
        session_description='session_description',
        identifier='identifier',
        session_start_time=datetime.datetime.now(datetime.timezone.utc)
    )
    return nwbfile


# class TestLabelSeriesConstructor(TestCase):
#
#     def setUp(self):
#         """Set up an NWB file. Necessary because TetrodeSeries requires references to electrodes."""
#         self.nwbfile = set_up_nwbfile()
#
#     def test_constructor(self):
#         """Test that the constructor for TetrodeSeries sets values as expected."""
#         all_electrodes = self.nwbfile.create_electrode_table_region(
#             region=list(range(0, 10)),
#             description='all the electrodes'
#         )
#
#         data = np.random.rand(100, 3)
#         tetrode_series = TetrodeSeries(
#             name='name',
#             description='description',
#             data=data,
#             rate=1000.,
#             electrodes=all_electrodes,
#             trode_id=1
#         )
#
#         self.assertEqual(tetrode_series.name, 'name')
#         self.assertEqual(tetrode_series.description, 'description')
#         np.testing.assert_array_equal(tetrode_series.data, data)
#         self.assertEqual(tetrode_series.rate, 1000.)
#         self.assertEqual(tetrode_series.starting_time, 0)
#         self.assertEqual(tetrode_series.electrodes, all_electrodes)
#         self.assertEqual(tetrode_series.trode_id, 1)


class TestLabelSeriesRoundtrip(TestCase):
    """Simple roundtrip test for LabelSeries."""

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = 'test.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a LabelSeries to an NWBFile, write it to file, read the file, and test that the LabelSeries from the
        file matches the original LabelSeries.
        """
        behavior_module = self.nwbfile.create_processing_module(
            name="behavior", description="behavior"
        )

        video = np.random.rand(100, 128,128)
        image_series = ImageSeries(
            name='video',
            data= video,
            rate = 30.0
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
        scores = np.random.rand(100, 5)
        vocab = np.random.rand(5).astype(str)
        label_series = LabelSeries(
            name='labels',
            description='labels',
            data=labels,
            scores=scores,
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
        self.nwbfile.add_acquisition(image_series)

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(behavior_module, read_nwbfile.processing['behavior'])


# class TestTetrodeSeriesRoundtripPyNWB(AcquisitionH5IOMixin, TestCase):
#     """Complex, more complete roundtrip test for TetrodeSeries using pynwb.testing infrastructure."""
#
#     def setUpContainer(self):
#         """ Return the test TetrodeSeries to read/write """
#         self.device = Device(
#             name='device_name'
#         )
#
#         self.group = ElectrodeGroup(
#             name='electrode_group',
#             description='description',
#             location='location',
#             device=self.device
#         )
#
#         self.table = get_electrode_table()  # manually create a table of electrodes
#         for i in range(10):
#             self.table.add_row(
#                 x=i,
#                 y=i,
#                 z=i,
#                 imp=np.nan,
#                 location='location',
#                 filtering='filtering',
#                 group=self.group,
#                 group_name='electrode_group'
#             )
#
#         all_electrodes = DynamicTableRegion(
#             data=list(range(0, 10)),
#             description='all the electrodes',
#             name='electrodes',
#             table=self.table
#         )
#
#         data = np.random.rand(100, 3)
#         tetrode_series = TetrodeSeries(
#             name='name',
#             description='description',
#             data=data,
#             rate=1000.,
#             electrodes=all_electrodes,
#             trode_id=1
#         )
#         return tetrode_series
#
#     def addContainer(self, nwbfile):
#         """Add the test TetrodeSeries and related objects to the given NWBFile."""
#         nwbfile.add_device(self.device)
#         nwbfile.add_electrode_group(self.group)
#         nwbfile.set_electrode_table(self.table)
#         nwbfile.add_acquisition(self.container)
