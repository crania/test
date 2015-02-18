import logging

from tornado.options import options
from tornado.httpclient import HTTPError
from tornado_botocore import Botocore


logger = logging.getLogger(__name__)


class DDBBase(object):

    TABLE_NAME = ''

    # The data type for the attribute. You can specify S for string data,
    # N for numeric data, or B for binary data.
    ATTRIBUTE_DEFINITIONS = []

    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DataModel.html#DataModelPrimaryKey
    KEY_SCHEMA = []

    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html
    LOCAL_SECONDARY_INDEXES = []
    GLOBAL_SECONDARY_INDEXES = []

    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughputIntro.html
    PROVISIONED_THROUGHPUT = {}

    ATTRIBUTES = {}

    def __init__(self):
        pass

    def dynamodb(self, operation):
        session = getattr(self, '_session', None)
        ddb = Botocore(
            service='dynamodb', operation=operation,
            session=session,
            region_name=options.amazon_region,
            endpoint_url=options.amazon_ddb_host,
            )
        '''if options.amazon_access_key and options.amazon_secret_key:
            ddb.session.set_credentials(
                options.amazon_access_key,
                options.amazon_secret_key, token=None)'''
        self._session = ddb.session
        return ddb

    @property
    def table_kwargs(self):
        kwargs = {
            'table_name': self.TABLE_NAME,
            'attribute_definitions': self.ATTRIBUTE_DEFINITIONS,
            'key_schema': self.KEY_SCHEMA,
            'provisioned_throughput': self.PROVISIONED_THROUGHPUT,
        }
        if getattr(self, 'LOCAL_SECONDARY_INDEXES', None):
            kwargs['local_secondary_indexes'] = self.LOCAL_SECONDARY_INDEXES
        if getattr(self, 'GLOBAL_SECONDARY_INDEXES', None):
            kwargs['global_secondary_indexes'] = self.GLOBAL_SECONDARY_INDEXES
        return kwargs

    def create_table_if_not_exists(self):
        ddb_describe_table = self.dynamodb(operation='DescribeTable')
        try:
            res = ddb_describe_table.call(table_name=self.TABLE_NAME)
        except HTTPError as a:
            ddb_describe_table = self.dynamodb(operation='DescribeTable')
            try:
                res = ddb_describe_table.call(table_name=self.TABLE_NAME)
            except HTTPError as b:
                print b.response.body
                # table does not exist
                logger.info('Creating {table_name} table ...'.format(table_name=self.TABLE_NAME))
                ddb_create_table = self.dynamodb(operation='CreateTable')
                try:
                    res = ddb_create_table.call(**self.table_kwargs)
                except HTTPError as e:
                    msg = '{table_name} table creation failed: {error}.'.format(
                        table_name=self.TABLE_NAME,
                        error=e.response.body)
                    logger.error(msg)
                    raise Exception(msg)

    def with_types(self, attributes_dict):
        result = {}
        print attributes_dict
        for key, val in attributes_dict.iteritems():
            '''print 'VARIABLE TYPE FOR TEST!!!!'
            print type(val)
            print val
            if isinstance(val, list):
                print 'THIS IS A LIST YO'
                l2 = []
                for a in val:
                    l2.append(unicode(a))
                    print 'LIST'
                result[key] ={self.ATTRIBUTES[key]: l2}
            elif val is dict:
                result2 = {}
                for key2, val2 in val.iteritems():
                    result2[key2] = unicode(val2)
                result[key] = result2
            else:
                result[key] = {self.ATTRIBUTES[key]: unicode(val)}
            print result'''
            if self.ATTRIBUTES[key] == 'L':
                l2 = []
                for a in val:
                    l2.append(dict(S= str(a)))
                val = l2
            elif self.ATTRIBUTES[key] == 'M':
                d2 = {}
                for dkey, dval in val.iteritems():
                    d2[dkey] = dict(S=dval)
                val = d2

            result[key] = {self.ATTRIBUTES[key]: val}
        return result
