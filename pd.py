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

    def start(self):
        pass

    def reset(self):
        pass

    def decode(self):
        pass
