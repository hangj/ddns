#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# created by hangj(hangj.cnblogs.com)
 
import http.client
import json
 
 
 
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
 
    print(data.decode("utf-8"))
 
 
 
# identifier: record id
def dns_detail(identifier):
 
    conn = http.client.HTTPSConnection("api.cloudflare.com")
 
    conn.request("GET", f"/client/v4/zones/{CF_Zone_ID}/dns_records/{identifier}", headers=headers)
 
    res = conn.getresponse()
    data = res.read()
 
    print(data.decode("utf-8"))
 
 
 
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
 
    print(data.decode("utf-8"))
 
 
 
# 如果 record 原来的 ttl 是 auto, 则此操作无法将 ttl 改成制定的值, 需要先用 dns_update 全量修改该 record
def dns_patch(identifier, IP):
 
    conn = http.client.HTTPSConnection("api.cloudflare.com")
 
    payload = {
        "content": IP,
        "ttl": 120,
    }
 
    conn.request("PATCH", f"/client/v4/zones/{CF_Zone_ID}/dns_records/{identifier}", json.dumps(payload), headers)
 
    res = conn.getresponse()
    data = res.read()
 
    print(data.decode("utf-8"))
 
 
 
def main():
 
    # dns_list()
    dns_update('09f0ea0', name="example.com", IP="113.90.37.101")
    # dns_patch('09f0ea0', IP="113.90.37.101")
    # dns_detail('09f0ea0')
 
 
 
if __name__ == '__main__':
    main()
 
 
#
