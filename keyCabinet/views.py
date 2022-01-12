from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import json
import base64
import copy
import pdfkit
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote
from TY_RMS_Multiple_Manage.settings import *

from Business.BllApproveInfo import *
from Business.BllApproveInfoProcess import *
from Business.BllPurchaseOrder import *
from Business.BllPurchaseOrderDetailed import *
from Business.BllAcceptanceOrder import *
from Business.BllAcceptanceOrderDetailed import *
from Business.BllMedicamentTemplate import *
from Business.BllMedicament import *
from Business.BllPeriodCheck import *
from Business.BllPeriodCheckDetailed import *
from DataEntity.EntityPurchaseOrder import *
from DataEntity.EntityPurchaseOrderDetailed import *
from DataEntity.EntityAcceptanceOrder import *
from DataEntity.EntityAcceptanceOrderDetailed import *
from DataEntity.EntityMedicamentTemplate import *
from DataEntity.EntityPeriodCheck import *
from DataEntity.EntityPeriodCheckDetailed import *
from DataEntity.EntityMedicament import *
from Lib.searchDrug import GetDrugTypeData
from Lib.Utils import *
from Lib.create_barcode import CreateBarcode
from Lib.reportExcel import *
from Lib.Model import *
from Lib.readExcel import *

@require_http_methods(['GET'])
def materialStockIn(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/materialStockIn.html', locals())

@require_http_methods(['GET'])
def materialUse(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/materialUse.html', locals())

@require_http_methods(['GET'])
def materialReturn(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/materialReturn.html', locals())

@require_http_methods(['GET'])
def materialSupply(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/materialSupply.html', locals())

@require_http_methods(['GET'])
def addMaterialForm(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/addMaterialForm.html', locals())

@require_http_methods(['GET'])
def shelfSelect(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/shelfSelect.html', locals())

@require_http_methods(['GET'])
def keyCabinetSelect(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/keyCabinetSelect.html', locals())

@require_http_methods(['GET'])
def keyCabinetView(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/keyCabinetView.html', locals())

@require_http_methods(['GET'])
def shelfUse(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/shelfUse.html', locals())

@require_http_methods(['GET'])
def shelfReturn(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/shelfReturn.html', locals())

@require_http_methods(['GET'])
def printFlowCode(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/printFlowCode.html', locals())

# 绑定模板入库
@require_http_methods(['POST'])
@csrf_exempt
def materialStockInDo(request):
    #try:
        drugInfo = json.loads(request.POST.get("drugInfo","{}"))
        print('1111111111111111111111111111111111111111111111111',drugInfo)
        user = request.session['login_user']
        ClientId=drugInfo.get('ClientId','')
        clent=BllClient().findEntity(ClientId)
        drugInfo['Speci'] = 0
        if drugInfo['Speci'] == '':
                drugInfo['Speci'] = 0
        # drugVariety = BllMedicamentVariety().createDrugVariety('', drugInfo.get('Name')
        #                                                         , drugInfo.get('CASNumber'), drugInfo.get('EnglishName'), drugInfo.get('Purity'),
        #                                                         drugInfo.get('Unit'), drugInfo.get('SpeciUnit'),
        #                                                         drugInfo.get('Speci'),
        #                                                         BllUser().findEntity(user.get('UserId')))
        drugVariety = BllMedicamentVariety().createDrugVariety('', drugInfo.get('Name')
                                                                , '', drugInfo.get('EnglishName'), '',
                                                                drugInfo.get('Unit'), drugInfo.get('SpeciUnit'),
                                                                drugInfo.get('Speci'),
                                                                BllUser().findEntity(user.get('UserId')))
        drugEntity = EntityMedicament()
        drugEntity.MedicamentId = str(Utils.UUID())
        drugEntity.VarietyId = drugVariety.VarietyId
        drugEntity.BarCode = ""
        drugEntity.CustomerId = ""
        drugEntity.ClientId = ClientId
        drugEntity.CASNumber = drugInfo.get('CASNumber')
        drugEntity.Name = drugInfo.get('Name')
        drugEntity.EnglishName = drugInfo.get('EnglishName')
        drugEntity.Purity = drugInfo.get('Purity')
        drugEntity.Manufacturer = drugInfo.get('Manufacturer')
        drugEntity.Distributor = drugInfo.get('Distributor')
        drugEntity.FlowNo = FlowNo
        pDate=datetime.datetime.now()
        # if(drugInfo.get('ProductionDate','')!=''):
        #     pDate= datetime.datetime.strptime(drugInfo.get('ProductionDate'), "%Y-%m-%d")
        drugEntity.ProductionDate = pDate.strftime("%Y-%m-%d")
        # drugEntity.ShelfLife = int(drugInfo.get('ShelfLife','3650') or '3650')
        if(drugInfo.get('ExpirationDate','')!=''):
            drugEntity.ExpirationDate = datetime.datetime.strptime(drugInfo.get('ExpirationDate'), "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
        # drugEntity.ExpirationDate = (
        #             pDate + datetime.timedelta(
        #         days=drugEntity.ShelfLife)).strftime("%Y-%m-%d %H:%M:%S")
        drugEntity.InventoryWarningValue = 10
        drugEntity.ShelfLifeWarningValue = 10
        drugEntity.UseDaysWarningValue = 10
        drugEntity.FlowPositionCode = drugInfo.get('FlowPositionCode')
        drugEntity.CellPositionCode = drugInfo.get('CellPositionCode')
        drugEntity.Unit = drugInfo.get('Unit')
        drugEntity.SpeciUnit = drugInfo.get('SpeciUnit')
        drugEntity.Speci = drugInfo.get('Speci')
        drugEntity.Price = drugInfo.get('Price')
        drugEntity.Place = drugInfo.get('Place').replace('1号钥匙柜-','')
        drugEntity.IsSupervise = 0  # 默认非重点监管
        drugEntity.Remain = drugInfo.get('Speci') or '0'
        drugEntity.PutInDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        drugEntity.PutInUserId = user.get('UserId')
        drugEntity.PutInUserName = user.get('RealName')
        drugEntity.Status = 1
        drugEntity.Remark5 = drugInfo.get('Remark5') or ''
        drugEntity.Remark3 = drugInfo.get('Catetgory') if drugInfo.get('Catetgory') else ''
        count= int(drugInfo.get('Count','1')) or 1
        boolean_=False
        SQL = """
        SELECT MAX(BarCode+0) as StartBarCode  from RMS_Medicament
        """
        tem_obj = BllMedicament().execute(SQL).fetchone()
        max_barcode=100001
        if tem_obj is None:
            max_barcode = 100001
        else:
            #max_barcode = int(tem_obj.StartBarCode+1)
            if(int(max_barcode)<100001):
                max_barcode = 100001
        for i in range(count):
            drugEntity1=copy.deepcopy(drugEntity)
            drugEntity1.MedicamentId = str(Utils.UUID())
            if(drugInfo.get('CellPositionCode')==101):
                drugEntity1.BarCode = max_barcode+i
            boolean_ = BllMedicament().drugPutIn(drugEntity1, clent,
                                        BllUser().findEntity(user.get('UserId')))
        if boolean_:
            print('ggggggggggggggggggggg:',drugInfo.get('CellPositionCode'))
            if(drugInfo.get('CellPositionCode')==101):
                for barcode in range(max_barcode, max_barcode+count):
                    CreateBarcode().create_Code128_img(str(barcode))
                    time.sleep(0.1)
            return JsonResponse(Utils.resultData(0, '试剂入库成功！'))
        else:
            return JsonResponse(Utils.resultData(1, '数据异常，入库失败！'))
   # except Exception as e:
   #     print(e, 888888888888)
    #    return JsonResponse(Utils.resultData(1, '数据异常, 入库失败！'))

@require_http_methods(['GET'])
def getSupplyDrugCategoryListJson(request):
    if request.method == 'GET':
        page = int(request.GET.get("page", '1'))
        limit = int(request.GET.get("limit", '15'))
        pageParam=PageParam(page, limit)
        drug_list = BllMedicamentVariety().getSupplyDrugCategoryList(pageParam)
        return JsonResponse({'data': drug_list,'code' : 0,'msg':'','count':pageParam.totalRecords})



# 导入入库模板
@require_http_methods(['GET'])
def exportPutInTemplate(request):
    try:
        file_path = Utils.getUDiskPath()
        print(file_path)
        if file_path:
            ClientId = request.GET.get('ClientId', '')
            template_name = request.GET.get('template_name', '')
            print(ClientId)
            a = ReadExcel(file_path + '/' + template_name)
            print(template_name, "aaaaaaaaaaaaaaaaaaaa")
            SQL = """
                SELECT  BarCodeCount, StartBarCode FROM `RMS_MedicamentTemplate` where StartBarCode =  (SELECT MAX(StartBarCode) from RMS_MedicamentTemplate)
                """
            tem_obj = BllMedicament().execute(SQL).fetchone()
            if tem_obj is None:
                max_barcode = 100001
            else:
                max_barcode = tem_obj.StartBarCode
                BarCodeCount = tem_obj.BarCodeCount
                # 获取最大的开始barcode + 数量
                max_barcode = int(max_barcode) + int(BarCodeCount)
            StartBarCode = max_barcode
            result_list = a.read()
            print(result_list, 9999999999999)
            client = BllClient().findEntity(ClientId)
            print('fffffffff')
            user = request.session['login_user']
            user = BllUser().findEntity(user['UserId'])
            status = 0
            if result_list is not None:
                medicament_obj_list = []
                for value in result_list:
                    totalCount = 0
                    TemplateContent_list = eval(value)
                    # 如果TemplateContent 子模板ExportCount 里面的数量大于1 数量为多少则存放多少个子模板
                    for template_content in TemplateContent_list:
                        # 获取子模板存放的数量
                        # totalCount += int(template_content['ExportCount'])

                        print('入库数量：',int(template_content['ExportCount']),template_content['FlowPositionCode'][-1])
                        print('入库数量2：', int(template_content['ExportCount']), template_content['FlowPositionCode'].replace('B', '号柜下'))

                        # place = template_content['FlowPositionCode'].replace('A', '号柜上')
                        if template_content['FlowPositionCode'][-1] =='A':
                            place = template_content['FlowPositionCode'].replace('A', '号柜上')
                        else:
                            place = template_content['FlowPositionCode'].replace('B', '号柜下')
                    # medicament_obj = EntityMedicamentTemplate(
                    #     TemplateId=str(Utils.UUID()), CustomerId='client.CustomerId', ClientId='client.ClientId', ClientName='client.ClientName',
                    #     TemplateName='入库模板_'+Utils.getFileName(), TemplateContent=value, IsWaitExport=1, StartBarCode=str(StartBarCode), BarCodeCount=totalCount,
                    #     CreateDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CreateUserId=user.UserId, CreateUserName=user.RealName,
                    # )
                    # medicament_obj_list.append(medicament_obj)

                # status = BllMedicamentTemplate().insert_many(medicament_obj_list)

                        user = request.session['login_user']
                        ClientId = 'a4ca9400-bf26-11ea-a110-9cb6d0bdee0c'
                        clent = BllClient().findEntity(ClientId)
                        # print('1111111111111111111111111111111111111111',template_content['EnglishName'])
                        # if drugInfo['Speci'] == '':
                        #     drugInfo['Speci'] = 0
                        drugVariety = BllMedicamentVariety().createDrugVariety('', template_content['Name']
                                                                               ,
                                                                               template_content['EnglishName'],
                                                                               '',
                                                                               template_content['Purity'],
                                                                               template_content['Unit'],
                                                                               template_content['SpeciUnit'],
                                                                               template_content['Speci'],
                                                                               BllUser().findEntity(user.get('UserId')))
                        #print('2222222222222222222222222222222222')
                        drugEntity = EntityMedicament()
                        drugEntity.MedicamentId = str(Utils.UUID())
                        drugEntity.VarietyId = drugVariety.VarietyId
                        drugEntity.BarCode = ""
                        drugEntity.CustomerId = ""
                        drugEntity.ClientId = ClientId
                        # drugEntity.CASNumber = template_content['CASNumber']
                        drugEntity.Name = template_content['Name']
                        drugEntity.EnglishName = template_content['EnglishName']
                        drugEntity.Purity = template_content['Purity']
                        drugEntity.Manufacturer = template_content['Manufacturer']
                        # drugEntity.Distributor = drugInfo.get('Distributor')
                        drugEntity.FlowNo = FlowNo
                        pDate = datetime.datetime.now()
                        # if(drugInfo.get('ProductionDate','')!=''):
                        #     pDate= datetime.datetime.strptime(drugInfo.get('ProductionDate'), "%Y-%m-%d")
                        drugEntity.ProductionDate = pDate.strftime("%Y-%m-%d")
                        # drugEntity.ShelfLife = int(drugInfo.get('ShelfLife','3650') or '3650')
                        # if (template_content['ExpirationDate']!= ''):
                        #     drugEntity.ExpirationDate = datetime.datetime.strptime(template_content['ExpirationDate'],
                        #                                                            "%Y-%m-%d").strftime(
                        #         "%Y-%m-%d %H:%M:%S")
                        # drugEntity.ExpirationDate = (
                        #             pDate + datetime.timedelta(
                        #         days=drugEntity.ShelfLife)).strftime("%Y-%m-%d %H:%M:%S")
                        drugEntity.InventoryWarningValue = 10
                        drugEntity.ShelfLifeWarningValue = 10
                        drugEntity.UseDaysWarningValue = 10
                        drugEntity.FlowPositionCode = template_content['FlowPositionCode']
                        drugEntity.CellPositionCode = 100
                        drugEntity.Unit = template_content['Unit']
                        drugEntity.SpeciUnit = template_content['SpeciUnit']
                        # drugEntity.Speci = template_content['Speci']
                        drugEntity.Price = template_content['Price']
                        drugEntity.Place = place
                        drugEntity.IsSupervise = 0  # 默认非重点监管
                        # drugEntity.Remain = drugInfo.get('Speci') or '0'
                        drugEntity.PutInDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        drugEntity.PutInUserId = user.get('UserId')
                        drugEntity.PutInUserName = user.get('RealName')
                        drugEntity.Status = 1
                        drugEntity.Remark5 = template_content['Remark5'] or ''  # 货号
                        drugEntity.Remark3 = template_content['Remark3'] or ''  # 货号
                        count = int(template_content['ExportCount'])
                        boolean_ = False
                        SQL = """
                               SELECT MAX(BarCode+0) as StartBarCode  from RMS_Medicament
                               """
                        tem_obj = BllMedicament().execute(SQL).fetchone()
                        max_barcode = 100001
                        if tem_obj is None:
                            max_barcode = 100001
                        else:
                            #max_barcode = int(tem_obj.StartBarCode + 1)
                            if (int(max_barcode) < 100001):
                                max_barcode = 100001
                        for i in range(int(count)):
                            drugEntity1 = copy.deepcopy(drugEntity)
                            drugEntity1.MedicamentId = str(Utils.UUID())
                            # if (drugInfo.get('CellPositionCode') == 101):
                            #     drugEntity1.BarCode = max_barcode + i
                            boolean_ = BllMedicament().drugPutIn(drugEntity1, clent,
                                                                 BllUser().findEntity(user.get('UserId')))
                        if boolean_:
                            print('ggggggggggggggggggggg:')
                            # if (drugInfo.get('CellPositionCode') == 101):
                            #     for barcode in range(max_barcode, max_barcode + count):
                            #         CreateBarcode().create_Code128_img(str(barcode))
                            #         time.sleep(0.1)
                            # # return JsonResponse(Utils.resultData(0, '试剂入库成功！'))
                            # else:
                            #     # return JsonResponse(Utils.resultData(1, '数据异常，入库失败！'))
                            #     pass

                            status = 1
                if status:
                    return JsonResponse({'data': Utils.resultData(0, '导入成功！')})
                else:
                    return JsonResponse({'data': Utils.resultData(1, '入库单异常, 导入失败！')})
            else:
                return JsonResponse({'data': Utils.resultData(1, '入库单格式不正确, 请检查之后重新导入！')})
        else:
            return JsonResponse({'data': Utils.resultData(1, '请插入U盘！')})
    except FileNotFoundError as e:
        return JsonResponse({'data': Utils.resultData(1, '当前U盘下暂无reagentTemplate.xlsx文件！')})
    except Exception as e:
        print(e)
        return JsonResponse({'data': Utils.resultData(1, '模板错误：'+str(e))})


# 获取U盘模板列表
@require_http_methods(['GET'])
def getUpanTemplateFile(request):
    fileList = []
    file_path = Utils.getUDiskPath()
    if(file_path != ''):
        for i in [os.sep.join([file_path, v]) for v in os.listdir(file_path)]:
            if(os.path.basename(i).startswith('tem_') and (os.path.isfile(i)) and (os.path.basename(i).endswith('.xlsx'))):
                fileList.append(os.path.basename(i))
    print(fileList)
    return JsonResponse({'data': fileList})