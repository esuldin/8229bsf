import sigrokdecode as srd


class Decoder(srd.Decoder):
    api_version = 3
    id = '8229bsf'
    name = '8229BSF'
    longname = '8229BSF serial output interface'
    desc = 'Synchronous, serial bus.'
    license = 'mit'
    inputs = ['logic']
    outputs = ['8229bsf']
    tags = ['Debug/trace']
    channels = (
        {'id': 'scl', 'name': 'SCL', 'desc': 'Clock'},
        {'id': 'sdo', 'name': 'SDO', 'desc': 'Data'},
    )
    annotations = (
        ('dv', 'Data valid'),
    )
    annotation_rows = (
        ('fields', 'Fields', (0,)),
    )

    def __init__(self):
        self.out_ann = None
        self.dv_block_ss = None

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def reset(self):
        self.dv_block_ss = None

    def decode(self):
        self.wait({0: 'h', 1: 'f'})
        self.dv_block_ss = self.samplenum

        self.wait({0: 'h', 1: 'r'})
        self.put(self.dv_block_ss, self.samplenum, self.out_ann, [0, ['Data valid', 'DV']])
