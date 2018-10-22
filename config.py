import configparser

config = configparser.ConfigParser()
config.read('todo.ini')
format = config['Serializer']['format']


def get_serializer():
    if format == 'pickle':
        import serializers.pickle_
        return serializers.pickle_.PickleSerializer()
    elif format == 'json':
        import serializers.json_
        return serializers.json_.JsonSerializer()
    else:
        raise ImportError
