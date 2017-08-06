from rest_framework.response import Response


def create_item(*args, **kwargs):
    Serializer = kwargs['Serializer']
    pk = kwargs['pk']
    Model = kwargs['Model']
    ModelSerializer = kwargs['ModelSerializer']
    request = kwargs['request']
    self = kwargs['self']
    try:
        object = Model.objects.get(pk=pk)
    except:
        return Response(status=404)
    serializer = Serializer(data=request.data)
    if serializer.is_valid():
        if 'user' in args:
            serializer.validated_data['user'] = request.user
        if 'task' in args:
            serializer.validated_data['task'] = object
        if 'list' in args:
            serializer.validated_data['list'] = object
        created_obj = ModelSerializer.objects.create(**serializer.validated_data)
        return Response(Serializer(created_obj).data, status=201)
    else:
        return Response(serializer.errors)
