
from TY_RMS_Multiple_Manage.settings import *
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityClient import *
from Lib.Utils import *
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading


#用户操作业务逻辑类
class BllClient(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllClient, "_instance"):
    #         with BllClient._instance_lock:
    #             if not hasattr(BllClient, "_instance"):
    #                 BllClient._instance = object.__new__(cls)
    #     return BllClient._instance

    def __init__(self, entityType=EntityClient):
        return super().__init__(entityType)

    # 模糊查询根据客户端编号和客户端名字
    def like_ClientId_or_Name(self, searchValue):
        # return self.findList(EntityClient.FlowNo==FlowNo).filter(or_(EntityClient.ClientCode.like('%' + searchValue + '%'),EntityClient.ClientName.like('%' + searchValue + '%'))).all()
        return self.findList().filter(or_(EntityClient.ClientCode.like('%' + searchValue + '%'),EntityClient.ClientName.like('%' + searchValue + '%'))).all()
        
    def getAllClientList(self):
        return self.findList().order_by(asc(EntityClient.ClientCode)).all()
    #获取终端选择列表
    def getSelectClient(self,ClientUseCode=''):
        clientList=[]
        if(ClientUseCode!=''):
            # clientList=self.findList(EntityClient.ClientUseCode==ClientUseCode, EntityClient.FlowNo==FlowNo).order_by(asc(EntityClient.ClientCode)).all()
            clientList=self.findList(EntityClient.ClientUseCode==ClientUseCode).order_by(asc(EntityClient.ClientCode)).all()
        else:
            # clientList= self.findList(EntityClient.FlowNo==FlowNo).order_by(asc(EntityClient.ClientCode)).all()
            clientList= self.findList().order_by(asc(EntityClient.ClientCode)).all()
        selectList=[{'name':x.ClientTitle,'value':x.ClientId,'code':x.ClientCode} for x in clientList]
        return selectList

