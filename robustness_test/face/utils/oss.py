import uuid
import oss2 

AccessKeyId = "LTAI4GAxmV2THzBgf9V2iZL4"
AccessKeySecret = "a4vI3I3c8v5GyKlQtYujPWnhg0IBmf"

# 用户账号密码，第三部说明的Access
auth = oss2.Auth(AccessKeyId, AccessKeySecret)
# 这个是需要用特定的地址，不同地域的服务器地址不同，不要弄错了 
endpoint = 'http://oss-cn-beijing.aliyuncs.com'
# 你的项目名称，类似于不同的项目上传的图片前缀url不同
# 因为我用的是ajax传到后端方法接受的是b字节文件，需要如下配置。 阿里云oss支持更多的方式，下面有链接可以自己根据自己的需求去写
bucket = oss2.Bucket(auth, endpoint, 'pdb-wrl')  # 项目名称

# 这个是上传图片后阿里云返回的uri需要拼接下面这个url才可以访问，根据自己情况去写这步
base_image_url = 'https://pdb-wrl.oss-cn-beijing.aliyuncs.com/'


def update_img_file(image):
    """
    ！ 上传单张图片
    :param image: b字节文件
    :return: 若成功返回图片路径，若不成功返回空
    """
    # 生成文件编号，如果文件名重复的话在oss中会覆盖之前的文件
    number = uuid.uuid4()
    # 生成文件名
    base_img_name = str(number) + '.jpg'
    # 生成外网访问的文件路径
    image_name = base_image_url + base_img_name
    # 这个是阿里提供的SDK方法 bucket是调用的4.1中配置的变量名
    print(type(bucket))
    res = bucket.put_object(base_img_name, image)
    # 如果上传状态是200 代表成功 返回文件外网访问路径
    # 下面代码根据自己的需求写
    if res.status == 200:
        return image_name
    else:
        return False