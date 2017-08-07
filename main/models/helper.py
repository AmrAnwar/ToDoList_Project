def upload_location(instance, filename):
    if instance.id:
        new_id = instance.id
    else:
        try:
            new_id = instance.__class__.objects.order_by("id").last().id + 1
        except:
            new_id = 1
    return "list/%s/%s" % (new_id, filename)