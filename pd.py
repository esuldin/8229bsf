import sigrokdecode as srd


class SamplerateError(Exception):
    pass


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
    options = (
        {'id': 'key_num', 'desc': 'Key number', 'default': 8,
            'values': (8, 16)},
    )
    annotations = (
        ('dv', 'Data valid'),
        ('tw', 'Tw'),
        ('bit', 'Bit'),
    )
    annotation_rows = (
        ('fields', 'Fields', (0, 1, 2,)),
    )

    def __init__(self):
        self.key_num = None
        self.out_ann = None

        self.timeout_samples_num = None

        self.dv_block_ss = None
        self.tw_block_ss = None
        self.bt_block_ss = None

    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.timeout_samples_num = int(2 * (value / 1000.0))

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)
        self.key_num = self.options['key_num']

    def reset(self):
        self.dv_block_ss = None
        self.tw_block_ss = None
        self.bt_block_ss = None

    def decode(self):
        if not self.timeout_samples_num:
            raise SamplerateError('Cannot decode without samplerate.')

        self.wait({0: 'h', 1: 'f'})
        self.dv_block_ss = self.samplenum

        self.wait({0: 'h', 1: 'r'})
        self.put(self.dv_block_ss, self.samplenum, self.out_ann, [0, ['Data valid', 'DV']])
        self.tw_block_ss = self.samplenum

        self.wait([{0: 'f', 1: 'h'}, {0: 'f', 1: 'f'}])
        self.put(self.tw_block_ss, self.samplenum, self.out_ann, [1, ['Tw', 'Tw']])
        self.bt_block_ss = self.samplenum

        for i in range(self.key_num):
            (scl, sdo) = self.wait({0: 'r'})
            sdo = 0 if sdo else 1

            self.wait([{0: 'f'}, {'skip': self.timeout_samples_num}])
            self.put(self.bt_block_ss, self.samplenum, self.out_ann, [2, ['Bit: %d' % sdo, '%d' % sdo]])

            if (self.matched & 0b10) and i != (self.key_num - 1):
                break

            self.bt_block_ss = self.samplenum
