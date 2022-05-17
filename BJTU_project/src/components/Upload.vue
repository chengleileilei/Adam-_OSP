<template>
  <div>
    <h1>upload页</h1>
    <input type="file" @change="changeFile" />
    <button @click="upload()">上传</button>
    <br />

    <div class="input-wrap">
      <p>参数1：</p>
      <el-input
        v-model="arg1"
        placeholder="请输入内容"
        class="upload-input"
      ></el-input>
    </div>

    <div class="input-wrap">
      <p>参数2：</p>
      <el-input
        v-model="arg2"
        placeholder="请输入内容"
        class="upload-input"
      ></el-input>
    </div>

    <!-- 参数2：<el-input v-model="arg2" placeholder="请输入内容" class="upload-input"></el-input> -->
    <div class="res-wrap">
      <h2>返回结果</h2>
      <p>{{ this.result }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Upload",
  data() {
    return {
      file: null,
      baseUrl: "",
      arg1: "",
      arg2: "",
      result: "",
    };
  },
  methods: {
    upload() {
      // 上传图像通常要将文件参数放在fromdata 对象中
      // 创建formData实例
      let formData = new FormData();
      // 向formData实例中追加属性 (参数1：属性名 参数2：属性值)
      formData.append("files", this.file);
      formData.append("trans_type", this.arg1);
      formData.append("trans_value", this.arg2);
      console.log(formData); //这里输出的是一个空的formData对象，因为formData是加密处理的我们看不到其内容，但的的确确添加进去了。
      axios
        .post(baseUrl+"/api/imgTransform", formData)
        .then((res) => {
          this.result = res;
          console.log(res);
        })
        .catch((error) => {
          alert("上传失败", error);
          console.log(error);
        });
    },
    changeFile(e) {
      // 获取文件信息 e.target.files
      console.log(e.target.files[0]);
      this.file = e.target.files[0];
    },
  },
};
</script>


<style>
.res-wrap {
  border: 1px solid black;
  min-height: 200px;
  margin: 0 auto;
  width: 70%;
  margin-top: 20px;
}
.input-wrap {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
.upload-input {
  width: 500px;
  border-radius: 10px;
}
</style>