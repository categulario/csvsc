from csvsc.input import InputStream
from csvsc.mapper import Mapper
from csvsc.distributor import Distributor
from csvsc.reducer import Reducer
from csvsc.flusher import Flusher


class Process:

    def __init__(self, input=None, input_encoding='utf-8', output=None,
                 add_columns=None, grouping=None, reducer_columns=None):
        self.input = input
        self.output = output
        self.add_columns = add_columns
        self.input_encoding = input_encoding
        self.grouping = grouping
        self.reducer_columns = reducer_columns

    def __call__(self):
        # Step 1. Get the source
        input_stream = InputStream(self.input, encoding=self.input_encoding)

        # Step 2. Map the info, add/remove, transform each row
        mapper = Mapper(input_stream, add_columns=self.add_columns)

        # Step 3. Stablish destination
        dist = Distributor(mapper, self.output)

        # Step 4. Reduce, aggregate
        reducer = Reducer(dist, grouping=self.grouping)

        # Step 5. Flush to destination
        Flusher(reducer).flush()
