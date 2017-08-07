from django.core.urlresolvers import reverse
import json


def view_test(**kwargs):
    self = kwargs['self']
    test_obj = kwargs['test_obj']
    url = kwargs['url']
    data = kwargs['data']
    response = self.client.get(self.list_url)
    self.assertEqual(response.status_code, 200)
    response = self.client.get(self.list_url)
    self.assertEqual(response.status_code, 200)

    response = self.client.post(url, data=data)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data.get('user'), self.user.id)
    re_data = {
        "title": "re-test",
    }
    detail_url = "%s-detail" % test_obj
    new_list_url = reverse(detail_url,
                           kwargs={'pk': response.data.get('id')})
    response = self.client.patch(new_list_url,
                                 json.dumps(re_data),
                                 content_type='application/json')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data.get('title'), 're-test')


def create_patch(**kwargs):
    test_obj = kwargs['test_obj']
    self = kwargs['self']
    url = kwargs['url']
    data = {
        'title': "tester"
    }
    res = self.client.post(url,
                           data=json.dumps(data),
                           content_type='application/json')
    self.assertEqual(res.status_code, 201)
    res_id = res.data.get("id")
    data = {
        'title': "re-test",
    }
    url_detail = reverse("%s-detail" % test_obj, kwargs={'pk': res_id})
    res = self.client.get(url_detail)
    self.assertEqual(res.status_code, 200)
    res = self.client.patch(url_detail,
                            data=json.dumps(data),
                            content_type='application/json')
    self.assertEqual(res.status_code, 200)
    self.assertEqual(res.data.get("title"), "re-test")
    # test fail create
    data = {
        'my_title': 'tester'
    }
    res = self.client.post(url,
                           data=json.dumps(data),
                           content_type='application/json')
    self.assertEqual(res.status_code, 200)
