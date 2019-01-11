from csvsc.input import InputStream
from csvsc.mapper import Mapper
from csvsc.distributor import Distributor


class Process:

    def __init__(self, input=None, input_encoding='utf-8', output=None, add_columns=None):
        self.input = input
        self.output = output
        self.add_columns = add_columns
        self.input_encoding = input_encoding

    def __call__(self):
        # Step 1. Get the source
        input_stream = InputStream(self.input, encoding=self.input_encoding)

        # Step 2. Map the info, add/remove, transform each row
        mapper = Mapper(input_stream, add_columns=self.add_columns)

        # Step 3. Reduce, aggregate

        # Step 4. Redistribute to destinations
        dist = Distributor(mapper, self.output)
        dist.flush()
