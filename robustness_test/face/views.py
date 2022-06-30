
import torch
from torchvision import transforms
from io import BytesIO
from PIL import Image
from .utils.robustness import functionSample
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from rest_framework.views import APIView
from .utils import oss
import json
import sys
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
print(os.getcwd())

# Create your views here.


class GenerateImageView(APIView):
    """样本数字攻击
    """

    def post(self, request):
        res = request.data
        backbone_type = (res["model"], res["attackedModel"])
        yzmdata = requests.get(res["image_pair"][0])
        yzmdata1 = requests.get(res["image_pair"][1])
        tempIm = BytesIO(yzmdata.content)
        tempIm1 = BytesIO(yzmdata1.content)
        im = Image.open(tempIm)
        im1 = Image.open(tempIm1)
        image_pair = [im, im1]
        attacker_type = ""
        epsilon = 0
        num_iters = 0
        targeted = True
        result = functionSample.generate_adversarial_image(
            backbone_type, image_pair, attacker_type, epsilon, num_iters, targeted)
        img = result["img"]
        toPIL = transforms.ToPILImage()  # 这个函数可以将张量转为PIL图片，由小数转为0-255之间的像素值
        pic = toPIL(img)
        img_path = r'face/tmp/random.jpg'
        pic.save(img_path)
        with open(img_path, 'rb') as f:
            f_read = f.read()
        res = oss.update_img_file(f_read)
        result["img"] = res
        return JsonResponse({
            'code': 200,
            'data': result,
        }, json_dumps_params = {'ensure_ascii': False})


class GeneratePatchView(APIView):
    """样本物理攻击
    """
    def post(self, request):
        res = request.data
        print(res)
        backbone_type = (res["model"], res["attackedModel"])
        yzmdata = requests.get(res["image_pair"][0])
        yzmdata1 = requests.get(res["image_pair"][1])
        tempIm = BytesIO(yzmdata.content)
        tempIm1 = BytesIO(yzmdata1.content)
        im = Image.open(tempIm)
        im1 = Image.open(tempIm1)
        image_pair = [im, im1]
        print(image_pair)
        attacker_type = ""
        epsilon = 0
        num_iters = 0
        targeted = True
        result = functionSample.generate_adversarial_patch(
            backbone_type, image_pair, attacker_type, epsilon, num_iters, targeted)
        print(result)
        tmp_img_list = []
        # 图片转码上传处理
        for img in [result["img"], result["patch"]]:
            toPIL = transforms.ToPILImage()  # 这个函数可以将张量转为PIL图片，由小数转为0-255之间的像素值
            pic = toPIL(img)
            img_path = r'face/tmp/random.jpg'
            pic.save(img_path)
            with open(img_path, 'rb') as f:
                f_read = f.read()
            res = oss.update_img_file(f_read)
            tmp_img_list.append(res)
        result["img"] = tmp_img_list[0]
        result["patch"] = tmp_img_list[1]
        return JsonResponse({
            'code': 200,
            'data': result,
        }, json_dumps_params = {'ensure_ascii': False})


class ImageUploadView(APIView):
    """图片上传"""

    def post(self, request):
        file_obj=request.FILES.get('file')
        res=oss.update_img_file(file_obj)
        return JsonResponse({"code": 200, "image_url": res}, json_dumps_params = {'ensure_ascii': False})


class MenuAdminView(APIView):
    """传入动态菜单
    """
    def get(self, request):
        json_data={}
        with open('./face/admin.json', 'r', encoding = 'utf8')as fp:
            json_data=json.load(fp)
        return JsonResponse(json_data, json_dumps_params = {'ensure_ascii': False})


class EvaluateModelView(APIView):
    """模型对抗鲁棒性
    """
    def post(self, request):
        res=request.data
        print(res)
        backbone_type=(res["model"], res["attackedModel"])
        bin_file=""
        attacker_type=""
        epsilon=""
        num_iters=""
        targeted=""
        functionSample.evaluate_model(backbone_type, bin_file, attacker_type, epsilon, num_iters, targeted)
        return JsonResponse({"code": 200, "data": {}}, json_dumps_params = {'ensure_ascii': False})
