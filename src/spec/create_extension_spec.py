# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, \
    export_spec, \
    NWBGroupSpec, \
    NWBAttributeSpec,\
    NWBLinkSpec,\
    NWBDatasetSpec
# TODO: import the following spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""labels for behavior or neural data""",
        name="""ndx-labels""",
        version="""0.1.0""",
        author=list(map(str.strip, """Akshay Jaggi, Kanishk Jain, Jim Robinson-Bohnslav""".split(','))),
        contact=list(map(str.strip, """akshay.x.jaggi@gmail.com""".split(',')))
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types
    # as of HDMF 1.6.1, the full ancestry of the neurodata_types that are used by
    # the extension should be included, i.e., the neurodata_type and its parent
    # type and its parent type and so on. this will be addressed in a future
    # release of HDMF.
    ns_builder.include_type('ElectricalSeries', namespace='core')
    ns_builder.include_type('TimeSeries', namespace='core')
    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('NWBContainer', namespace='core')
    ns_builder.include_type('DynamicTableRegion', namespace='hdmf-common')
    ns_builder.include_type('VectorData', namespace='hdmf-common')
    ns_builder.include_type('Data', namespace='hdmf-common')

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information

    representation_series = NWBGroupSpec(
        neurodata_type_def='RepresentationSeries',
        neurodata_type_inc='TimeSeries',
        doc=('Extends TimeSeries to include abstract representations of raw data (e.g. PCs, tSNE)'),
        attributes=[
            NWBAttributeSpec(
                name='method',
                doc='a description of the method used to derive the representation',
                dtype='text'
            ),
            NWBAttributeSpec(
                name='unit',
                doc='required unit for RepresentationSeries, default to "a.u."',
                default_value="a.u.",
                dtype='text',
                required=False
            ),
        ],
        links=[
            NWBLinkSpec(
                name="video",
                target_type="ImageSeries",
                doc="ref to video that's being labeled",
                quantity="?"
            )
        ],
        datasets=[
            NWBDatasetSpec(
                name='data',
                doc='float array of the value of m factors for n time steps',
                dtype='float64',
                dims=['num_frames', 'num_factors'],
                shape=(None, None),
            ),
        ]
    )

    label_series = NWBGroupSpec(
        neurodata_type_def='LabelSeries',
        neurodata_type_inc='TimeSeries',
        doc=('Extends TimeSeries to capture labels encoded'),
        attributes=[
            NWBAttributeSpec(
                name='exclusive',
                doc='whether the labels are exclusive or not',
                dtype='bool'
            ),
            NWBAttributeSpec(
                name='method',
                doc='a description of the method used to derive the labels (e.g. DeepEthogram v0.1.0)',
                dtype='text'
            ),
            NWBAttributeSpec(
                name='unit',
                doc='required unit for LabelSeries, default to "label"',
                default_value="label",
                dtype='text',
                required=False
            ),
        ],
        links=[
            NWBLinkSpec(
                name="representation",
                target_type="RepresentationSeries",
                doc="ref to representation series",
                quantity="?"
            ),
            NWBLinkSpec(
                name="video",
                target_type="ImageSeries",
                doc="ref to video that's being labeled",
                quantity="?"
            )
        ],
        datasets=[
            NWBDatasetSpec(
                name='data',
                doc='Binary array of k labels for all n time steps',
                dtype='bool',
                dims=['num_frames', 'num_labels'],
                shape=(None, None),
            ),
            NWBDatasetSpec(
                name='scores',
                doc='Float array of the probabilities of each of the k labels for all n time steps',
                dtype='float64',
                dims=['num_frames', 'num_labels'],
                shape=(None, None),
                quantity="?"
            ),
            NWBDatasetSpec(
                name="vocabulary",
                doc="list of k labels for the behaviors",
                dtype="text",
                dims=['num_labels'],
                shape=(None,),
                quantity="?"
            )
        ]
    )

    # TODO: add all of your new data types to this list
    new_data_types = [label_series, representation_series]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
