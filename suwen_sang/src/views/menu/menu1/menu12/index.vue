<!--
 * @Author: 78644 786442541@qq.com
 * @Date: 2022-06-03 16:23:20
 * @LastEditors: 78644 786442541@qq.com
 * @LastEditTime: 2022-06-07 00:28:48
 * @FilePath: \vue-next-admin\src\views\menu\menu1\menu11\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
	<div class="attack">
		<div class="head_introduction">
			<div class="block picture">
				<el-image :src="titleSrc"></el-image>
			</div>
			<div class="introduction_area">
				<div class="top">
					<div class="title">人脸对抗</div>
					<!-- <div class="contact"><el-button type="info" plain>联系我们</el-button></div> -->
				</div>

				<div class="footer">
					<div class="footer_item">
						<span>功能简介：</span>
						<p>在人像中加入设计的对抗噪声，在保持人像原貌的前提下，防止其在社交平台上被识别为人脸，从而有效保护人脸隐私。</p>
					</div>
					<div class="footer_item">
						<span>适用场景：</span>
						<p>人脸检测，人脸识别</p>
					</div>
				</div>
			</div>
		</div>
		<div class="content">
			<el-card class="box-card">
				<div slot="header" class="clearfix">
					<span class="title">基本介绍</span>
				</div>
				<div class="content-top-test">
					<div class="pic_left">
						<div class="block">
							<el-image :src="testSrc1" style="width: 250px; height: 250px"></el-image>
							<el-image :src="testSrc2" style="width: 250px; height: 250px; margin-left: 10px"></el-image>
						</div>
						<div class="test_pic_btn">
							<!-- <el-button type="primary" round>选择图像</el-button> -->
						</div>
					</div>
					<div class="pic_center">
						<i class="el-icon-right"></i>
					</div>
					<div class="pic_right">
						<div class="block">
							<el-image :src="testSrcResult1" style="width: 250px; height: 250px"></el-image>
							<el-image :src="testSrcResult2" style="width: 250px; height: 250px; margin-left: 10px"></el-image>
						</div>
						<div class="test_pic_btn">
							<!-- <el-button type="primary" round>生成图像</el-button> -->
						</div>
					</div>
				</div>
				<div class="content-footer-test">
					<p style="font-size: 22px">步骤：</p>
					<ul>
						<li><p>1、选择图像上传</p></li>
						<li><p>2、使用功能生成对应图像与对抗补丁</p></li>
						<li><p>3、预览或下载生成图像</p></li>
					</ul>
				</div>
			</el-card>
			<el-card class="box-card">
				<div slot="header" class="clearfix">
					<span class="title">功能实现</span>
				</div>
				<div class="content-top">
					<div class="pic_left">
						<div class="block upload-wrap">
							<el-upload
								:class="{ hide: photoHide }"
								:action="uploadImage"
								:limit="picCount"
								:file-list="fileList"
								:on-exceed="handleExceed"
								:on-success="handleSuccess"
								:on-remove="handleRemove"
								:before-upload="beforeUpload"
								accept=".jpg, .jpeg, .png, .gif, .bmp"
								list-type="picture-card"
							>
								<i class="el-icon-plus"></i>
							</el-upload>
							<el-upload
								:class="{ hide: photoHide }"
								:action="uploadImage"
								:limit="picCount"
								:file-list="fileList"
								:on-exceed="handleExceed"
								:on-success="handleSuccess"
								:on-remove="handleRemove"
								:before-upload="beforeUpload"
								accept=".jpg, .jpeg, .png, .gif, .bmp"
								list-type="picture-card"
							>
								<i class="el-icon-plus"></i>
							</el-upload>
							<el-dialog :visible.sync="imgVisible">
								<img width="100%" :src="dialogImageUrl" alt="" />
							</el-dialog>
						</div>
						<div class="test_pic_btn">
							<el-button type="primary" round>上传图像(需要两张)</el-button>
						</div>
					</div>
					<div class="pic_center">
						<i class="el-icon-right"></i>
					</div>
					<div class="pic_right">
						<div class="block">
							<div v-if="src1 && src2">
								<el-image :src="src1" style="width: 250px; height: 250px"></el-image>
								<el-image :src="src2" style="width: 250px; height: 250px; margin-left: 10px"></el-image>
							</div>
						</div>
						<div class="test_pic_btn">
							<el-button type="primary" round @click="settingSubmit">点击生成图像</el-button>
						</div>
					</div>
				</div>
				<div class="param_form">
					<div class="form_left">
						<el-form ref="form" :model="form" label-width="auto">
							<el-divider>模型设置</el-divider>
							<div class="model-setting">
								<el-form-item label="生成模型">
									<el-select v-model="form.model" placeholder="请选择模型">
										<el-option v-for="item in modelList" :key="item.value" :label="item.label" :value="item.value"> </el-option>
									</el-select>
								</el-form-item>
								<el-form-item label="被攻击模型">
									<el-select v-model="form.attackedModel" placeholder="请选择模型">
										<el-option v-for="item in attackedModelList" :key="item.value" :label="item.label" :value="item.value"> </el-option>
									</el-select>
								</el-form-item>
							</div>
							<el-divider>攻击设置</el-divider>
							<div class="attack_top">
								<el-form-item label="攻击方法">
									<el-select v-model="form.attackMethod" placeholder="请选择攻击方法">
										<el-option v-for="item in attackMethodList" :key="item.value" :label="item.label" :value="item.value"> </el-option>
									</el-select>
								</el-form-item>
								<el-form-item label="补丁大小">
									<el-input v-model="form.patch" placeholder="请输入补丁大小"></el-input>
								</el-form-item>
							</div>
							<div class="attack_bottom">
								<el-form-item label="迭代次数" style="margin-right: 15px">
									<el-select v-model="form.iteration" placeholder="请选择迭代次数">
										<el-option v-for="item in iterationList" :key="item.value" :label="item.label" :value="item.value"> </el-option>
									</el-select>
								</el-form-item>
								<el-form-item label="有攻击目标" style="margin-right: 165px">
									<el-switch v-model="form.have_attackTarget" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
								</el-form-item>
							</div>
						</el-form>
					</div>
					<div class="form_right">
						<transition name="fade" mode="out-in" appear>
							<div v-if="resultVisible">
								<div class="right_item">
									干净样本：
									<p class="right_result" v-if="clean['distance']">相似度{{ clean['distance'] }}，为同一人</p>
									<p class="right_result" v-else>相似度{{ clean['distance'] }}，不为同一人</p>
								</div>
								<div class="right_item">
									对抗样本：
									<p class="right_result" v-if="adversarial['distance']">相似度{{ adversarial['distance'] }}，为同一人</p>
									<p class="right_result" v-else>相似度{{ adversarial['distance'] }}，不为同一人</p>
								</div>
							</div>
						</transition>
					</div>
				</div>
			</el-card>
		</div>
	</div>
</template>

<script>
import { generatePatch } from '@/api/face';

export default {
	name: 'menu12',
	data() {
		return {
			val: '',
			dialogImageUrl: '',
			imgVisible: false,
			dialogVisible: false,
			resultVisible: false,
			uploadImage: process.env.VUE_APP_BASE_API + 'face/imageUpload',
			testSrcResult1: 'https://pdb-wrl.oss-cn-beijing.aliyuncs.com/4108b2bf-3de4-4291-822e-f1ecd55ef838.jpg',
			testSrcResult2: 'https://pdb-wrl.oss-cn-beijing.aliyuncs.com/35dccbb2-8fe3-4cf4-b82d-c1d05110a348.jpg',
			testSrc1:'https://pdb-wrl.oss-cn-beijing.aliyuncs.com/45a31851-58b4-46c6-8516-d0bcc228e346.jpg',
			testSrc2:'https://pdb-wrl.oss-cn-beijing.aliyuncs.com/algorithm/src%3Dhttp___static.lieyunwang.com_upload2_file_201812_1546067107161558.jpg%26refer%3Dhttp___static.lieyunwang%20%281%29.png',
			titleSrc: 'https://pdb-wrl.oss-cn-beijing.aliyuncs.com/algorithm/v2-801108ef77f34644d615e31cfd590e2b_r.jpg',
			src1: '',
			src2: '',
			fileList: [],
			clean: { distance: '', positive: false },
			adversarial: { distance: '', positive: false },
			form: {
				model: 'MobieFaceNet',
				attackedModel: 'GhostNet',
				attackMethod: 'PGD',
				patch: '0.5',
				iteration: '10',
				have_attackTarget: false,
			},
			// 模型选项列表
			modelList: [{ id: 0, label: 'MobieFaceNet', value: 'MobieFaceNet' }],
			// 被攻击模型选项列表
			attackedModelList: [{ id: 0, label: 'GhostNet', value: 'GhostNet' }],
			// 攻击方法选项列表
			attackMethodList: [
				{ id: 0, label: 'PGD', value: 'PGD' },
				{ id: 1, label: 'MI', value: 'MI' },
			],
			// 扰动阀值选项列表
			disturbanceList: [
				{ id: 0, label: '0.5', value: '0.5' },
				{ id: 1, label: '1', value: '1' },
				{ id: 2, label: '2', value: '2' },
				{ id: 3, label: '4', value: '4' },
				{ id: 4, label: '8', value: '8' },
			],
			// 迭代次数选项列表
			iterationList: [
				{ id: 0, label: '10', value: '10' },
				{ id: 1, label: '40', value: '40' },
			],
		};
	},
	methods: {
		handlePictureCardPreview(file) {
			this.dialogImageUrl = file.url;
			this.dialogVisible = true;
		},
		settingSubmit() {
			this.form.image_pair = [];

			for (let index = 0; index < this.fileList.length; index++) {
				let image_url = this.fileList[index].response.image_url;
				this.form.image_pair.push(image_url);
			}
			let param = this.form;
			generatePatch(param).then(async (res) => {
				this.clean.distance = res.data.clean.distance;
				this.clean.positive = res.data.clean.positive;
				this.adversarial.distance = res.data.adversarial.distance;
				this.adversarial.positive = res.data.adversarial.positive;
				this.src1 = res.data.img;
				this.src2 = res.data.patch;
				console.log(this.src1);
				console.log(this.src2);
				if (this.src1 && this.src2) {
					if (!this.resultVisible) {
						this.resultVisible = true;
					}
				}
			});
		},
		beforeUpload(file) {
			//上传图片前
			const isLt2M = file.size / 1024 / 1024 < 2;
			if (!isLt2M) {
				this.$message.error('图片大小不能超过 2MB!');
			}
			return isLt2M;
		},
		handleSuccess(file, fileList) {
			//此处的fileList是个对象
			if (file.code === 200) {
				this.fileList.push(fileList);
			}
		},
		handleExceed() {
			//图片超出上限
			this.$message.error('当前限制选择 2 个文件');
		},
		handleRemove(file, fileList) {
			//移除图片
			this.fileList = [];
		},
	},
};
</script>

<style scoped lang="scss">
.attack {
	width: 100%;
	height: 100%;
	display: flex;
	flex-direction: column;
	.head_introduction {
		flex: 3;
		width: 100%;
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		padding-left: 20px;
		padding-right: 20px;
		.picture {
			flex: 3;
			display: flex;
			justify-content: center;
			align-items: center;
		}
		.introduction_area {
			display: flex;
			flex: 7;
			flex-direction: column;
			justify-content: center;
			margin-left: 20px;
			.top {
				display: flex;
				justify-content: space-between;
				.title {
					font-size: 36px;
				}
				.contact {
					span {
						font-size: 30px;
						font-weight: 800;
					}
				}
			}
			.footer {
				display: flex;
				flex-direction: column;
				.footer_item {
					display: flex;
					margin-top: 30px;
					span {
						flex: 1.2;
						width: 30px;
						font-size: 22px;
					}
					p {
						flex: 8.8;
						display: inline-block;
						font-family: SourceHanSansSC-regular;
						color: #818386;
						font-size: 22px;
					}
				}
			}
		}
	}
		.upload-wrap {
		display: flex;
		flex-direction: row;
	}
	.content {
		display: flex;
		flex: 7;
		width: 100%;
		margin-top: 20px;
		flex-direction: column;
		.box-card {
			margin-top: 20px;
			.title {
				font-size: 28px;
			}
			.content-top-test {
				display: flex;
				align-items: center;
				justify-content: space-around;
				.pic_left {
					display: flex;
					flex-direction: column;
					justify-content: center;
					align-items: center;
					.test_pic_btn {
						margin-top: 10px;
						width: 100%;
						text-align: center;
					}
				}
				.pic_center {
					display: flex;
					font-size: 160px;
					justify-content: center;
					align-items: center;
				}
				.pic_right {
					.test_pic_btn {
						margin-top: 10px;
						width: 100%;
						text-align: center;
					}
					display: flex;
					flex-direction: column;
					justify-content: center;
					align-items: center;
				}
			}
			.content-top {
				display: flex;
				align-items: center;
				justify-content: space-around;
				.pic_left {
					display: flex;
					flex-direction: column;
					justify-content: center;
					align-items: center;
					.test_pic_btn {
						margin-top: 10px;
						width: 100%;
						text-align: center;
					}
				}
				.pic_center {
					display: flex;
					font-size: 160px;
					justify-content: center;
					align-items: center;
				}
				.pic_right {
					.test_pic_btn {
						margin-top: 10px;
						width: 100%;
						text-align: center;
					}
					display: flex;
					flex-direction: column;
					justify-content: center;
					align-items: center;
				}
			}
			.param_form {
				display: flex;
				width: 100%;
				.form_left {
					flex: 5;
					display: flex;
					flex-direction: column;
					.model-setting {
						display: flex;
						justify-content: space-around;
						align-items: center;
					}
					.attack_top {
						display: flex;
						justify-content: space-around;
					}
					.attack_bottom {
						display: flex;
						justify-content: space-around;
						align-items: center;
					}
				}
				.form_right {
					display: flex;
					flex-direction: column;
					flex: 5;
					margin-left: 30px;
					font-size: 22px;
					.right_item {
						margin: 20px;
						color: #818386;
					}
				}
			}
			.content-footer-test {
				display: flex;
				ul {
					list-style-type: none;
					color: #818386;
					p {
						font-size: 22px;
					}
				}
			}
		}
	}
}
</style>
