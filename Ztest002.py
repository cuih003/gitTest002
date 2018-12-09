#coding:utf-8
import unittest
import requests
import time

class AddCase(unittest.TestCase):
    def setUp(self):
        # 登陆
        login_url = 'http://47.92.88.246:8087/x_springboot/sys/login'
        data={"username": "test","password": "test"}
        r=requests.post(url=login_url,json=data)
        self.assertEqual(r.json()['msg'],'success',msg='正常登陆,登陆成功')
        print(r.text)
        self.token=r.json()['token']
        self.headers = {'token': self.token}
        self.userId=''

    # 新增正确用户
    def test_add001(self):
        add_url='http://47.92.88.246:8087/x_springboot/sys/user/save'
        data={"status":1,"roleIdList":[],"username":"test0003"+str(time.time()),"password":"test","email":"test@test.com"}
        r=requests.post(url=add_url,json=data,headers=self.headers)
        self.assertEqual(r.json()['msg'],'success',msg='新增正确用户成功')
        print(r.text)
        # 新增成功用户后查询用户
        query_url='http://47.92.88.246:8087/x_springboot/sys/user/list'
        params={'limit':'10','page':'1'}
        r=requests.get(url=query_url,params=params,headers=self.headers)
        print(r.text)
        userId=r.json()['page']['list'][0]['userId']
        print(userId)

    # 新增空用户名
    def test_add002(self):
        add_url='http://47.92.88.246:8087/x_springboot/sys/user/save'
        data={"status":1,"roleIdList":[],"username":"","password":"test","email":"test@test.com"}
        headers={'token':self.token}
        r=requests.post(url=add_url,json=data,headers=headers)
        self.assertEqual(r.json()['message'],'用户名不能为空<br>',msg='新增空用户名，新增失败')
        print(r.text)

    # 新增重复用户名，新增失败
    def test_add003(self):
        add_url='http://47.92.88.246:8087/x_springboot/sys/user/save'
        data={"status":1,"roleIdList":[],"username":"test","password":"test","email":"test@test.com"}
        headers={'token':self.token}
        r=requests.post(url=add_url,json=data,headers=headers)
        self.assertEqual(r.json()['message'],'数据库中已存在该记录',msg='新增重复用户名，新增失败')
        print(r.text)
    # 新增用户密码为空，新增失败
    def test_add004(self):
        add_url='http://47.92.88.246:8087/x_springboot/sys/user/save'
        data={"status":1,"roleIdList":[],"username":"test"+str(time.time()),"password":"","email":"test@test.com"}
        headers={'token':self.token}
        r=requests.post(url=add_url,json=data,headers=headers)
        self.assertEqual(r.json()['message'],'密码不能为空<br>',msg='新增用户密码为空，新增失败')
        print(r.text)
    # 新增用户且登陆成功
    def test_add005(self):
        add_url='http://47.92.88.246:8087/x_springboot/sys/user/save'
        data={"status":1,"roleIdList":[],"username":"test000311","password":"test","email":"test@test.com"}
        headers={'token':self.token}
        r=requests.post(url=add_url,json=data,headers=headers)
        # self.assertEqual(r.json()['message'],'success',msg='新增成功')
        print(r.text)
        login_url = 'http://47.92.88.246:8087/x_springboot/sys/login'
        data={"username": "test000311","password": "test"}
        r=requests.post(url=login_url,json=data)
        # self.assertEqual(r.json()['msg'],'success',msg='正常登陆,登陆成功')
        print(r.text)

    def tearDown(self):
        # 删除用户
        delete_url='http://47.92.88.246:8087/x_springboot/sys/user/delete'
        data=[self.userId]
        r=requests.post(url=delete_url,json=data,headers=self.headers)
        self.assertEqual(r.json()['msg'],'success',msg='清除新增用户成功')
        print(r.text)
        print('清除数据')
