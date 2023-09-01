#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# created by hangj(hangj.cnblogs.com)
 
import http.client
import json
import sys
 
 
 
CF_Email="alice@example.com"
CF_Token="0932a09c9a9d"
CF_Zone_ID="a900b9a9d8a9"
CF_API_Key="cb7de90"
 
 
 
headers = {
    'Content-Type': "application/json",
    'X-Auth-Email': CF_Email,
    'X-Auth-Key': CF_API_Key,
    'Authorization': 'Bearer ' + CF_Token,
}
 
 
 
def dns_list():

    conn = http.client.HTTPSConnection("api.cloudflare.com")

    conn.request("GET", f"/client/v4/zones/{CF_Zone_ID}/dns_records", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))



# identifier: record id
def dns_detail(identifier):

    conn = http.client.HTTPSConnection("api.cloudflare.com")

    conn.request("GET", f"/client/v4/zones/{CF_Zone_ID}/dns_records/{identifier}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))



# identifier: record id
def dns_update(identifier, name, IP):

    conn = http.client.HTTPSConnection("api.cloudflare.com")

    payload = {
        "type": "A",
        "name": name,
        "content": IP,
        "ttl": 120,
    }

    conn.request("PUT", f"/client/v4/zones/{CF_Zone_ID}/dns_records/{identifier}", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))



def dns_patch(identifier, IP):

    conn = http.client.HTTPSConnection("api.cloudflare.com")

    payload = {
        "content": IP,
        "ttl": 120, # 非 auto(1) 的 ttl, 需要设置 proxied 为 False
        "proxied": False,
    }

    conn.request("PATCH", f"/client/v4/zones/{CF_Zone_ID}/dns_records/{identifier}", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))



def get_my_global_ip():
    conn = http.client.HTTPSConnection("httpbin.org")
    conn.request("GET", "/ip")
    res = conn.getresponse()
    data = json.loads(res.read())

    return data['origin']
 
 
 
def main():
 
    # example.com
    identifier = '09f0e075483c89723093834'


    my_ip = get_my_global_ip()

    detail = dns_detail(identifier)
    if not detail['success']:
        print(detail, file=sys.stderr)
        return

    # print(detail)


    result = detail["result"]

    if result['content'] != my_ip:

        patch = dns_patch(identifier, my_ip)

        if not patch['success']:
            print(patch, file=sys.stderr)
            return
        else:
            # send an email to notify this change
            pass


    # dns_list()
    # dns_update(identifier, "example.com", IP="203.88.44.119")
    # dns_patch(identifier, IP="203.88.44.119")
    # dns_detail(identifier)
 
 
 
if __name__ == '__main__':
    main()
 
 
#
