def get_data(**kwargs):
    obj = kwargs['obj']
    serializer = kwargs['serializer']
    Child = kwargs['Child']
    parent = kwargs['parent']
    qs = Child.objects.filter(list=obj)
    qs_serializer = serializer(qs, many=True).data
    return qs_serializer
