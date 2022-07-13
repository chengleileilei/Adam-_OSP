<template>
	<!-- <div>
		<div class="layout-view-bg-white flex h100" v-loading="iframeLoading">
			<iframe :src="meta.isLink" frameborder="0" height="100%" width="100%" id="iframe"></iframe>
		</div>
	</div> -->
	<div>
		<h1>{{ 123456 }}</h1>
		<div class="main">
			<div class="title">图像变换</div>
			<div class="imgshow">
				<div class="imgshowbox">
					<div class="note_txt">输入</div>
					<form method="POST" enctype="multipart/form-data">
						<div class="imgbox" id="origin_img" @click="moveClick()">
							<label id="upload_label">点击上传</label>
							<img src="" id="uploadpic" v-show="upImage" class="img" />
						</div>
						<input type="file" name="file" id="photo" @change="uploadPicFile()" hidden />
					</form>
					<div class="note_txt">变换类型</div>
					<div class="radio-input" id="tran_select_level1">
						<div class="mybox" @click="change_level1_type(1)">
							<img src="@/assets/img/circle0.png" alt="" class="circle" />
							<label class="tran_label">几何</label>
						</div>
						<div class="mybox" @click="change_level1_type(2)">
							<img src="@/assets/img/circle0.png" alt="" class="circle" />
							<label class="tran_label">镜像</label>
						</div>
						<div class="mybox" @click="change_level1_type(3)">
							<img src="@/assets/img/circle0.png" alt="" class="circle" />
							<label class="tran_label">颜色</label>
						</div>
						<div class="mybox" @click="change_level1_type(4)">
							<img src="@/assets/img/circle0.png" alt="" class="circle" />
							<label class="tran_label">滤波</label>
						</div>
						<div class="mybox" @click="change_level1_type(5)">
							<img src="@/assets/img/circle0.png" alt="" class="circle" />
							<label class="tran_label">噪声</label>
						</div>
						<div class="mybox" @click="change_level1_type(6)">
							<img src="@/assets/img/circle0.png" alt="" class="circle" />
							<label class="tran_label">掩码</label>
						</div>
					</div>
					<div class="note_txt">变换参数</div>
					<div id="tran_select_level2">
						<div class="level2_box" style="display: none">
							<div class="value_box">
								<label class="mygray">平移：</label>
								<label class="mygray">-1</label>
								<input type="range" id="rangeTranslation" value="50" />
								<label class="mygray">1</label>
							</div>
							<div class="value_box">
								<label class="mygray">旋转：</label>
								<label class="mygray">-1</label>
								<input type="range" id="rangeRotation" value="50" />
								<label class="mygray">1</label>
							</div>
							<div class="value_box">
								<label class="mygray">缩放：</label>
								<label class="mygray">0</label>
								<input type="range" id="rangeScale" value="50" />
								<label class="mygray">2</label>
							</div>
						</div>
						<div class="level2_box" style="display: none">
							<div class="value_box">
								<label class="mygray sm-right-margin">镜像类型:</label>
								<select id="flip_type" class="bg-right-margin">
									<option value="1" selected>水平镜像</option>
									<option value="2">竖直镜像</option>
									<option value="3">混合镜像</option>
								</select>
							</div>
							<div class="value_box">
								<label class="mygray">概率值：&nbsp;</label>
								<label class="mygray">0</label>
								<input type="range" id="rangeFlip" value="100" />
								<label class="mygray">1</label>
							</div>
						</div>
						<div class="level2_box" style="display: none">
							<div class="value_box">
								<label class="mygray">明暗度：</label>
								<label class="mygray">0</label>
								<input type="range" id="rangeBrightness" value="50" />
								<label class="mygray">2</label>
							</div>
							<div class="value_box">
								<label class="mygray">对比度：</label>
								<label class="mygray">0</label>
								<input type="range" id="rangeContrast" value="50" />
								<label class="mygray">2</label>
							</div>
							<div class="value_box">
								<label class="mygray">饱和度：</label>
								<label class="mygray">0</label>
								<input type="range" id="rangeSaturation" value="50" />
								<label class="mygray">2</label>
							</div>
							<div class="value_box">
								<label class="mygray">色相：</label>
								<label class="mygray">-0.5</label>
								<input type="range" id="rangeHue" value="50" />
								<label class="mygray">0.5</label>
							</div>
						</div>
						<div class="level2_box" style="display: none">
							<div class="value_box">
								<label class="mygray sm-right-margin">滤波类型:</label>
								<select id="filter_type" class="bg-right-margin">
									<option value="1" selected>模糊滤波</option>
									<option value="2">边界增强滤波</option>
									<option value="3">平滑滤波</option>
									<option value="4">锐化滤波</option>
									<option value="5">细节滤波</option>
								</select>
							</div>
							<div class="value_box">
								<label class="mygray">概率值： </label>
								<label class="mygray">0</label>
								<input type="range" id="rangeFilter" value="100" />
								<label class="mygray">1</label>
							</div>
						</div>
						<div class="level2_box" style="display: none">
							<div class="value_box">
								<label class="mygray sm-right-margin">噪声类型:</label>
								<select id="noise_type" class="bg-right-margin">
									<option value="1" selected>高斯噪声</option>
									<option value="2">泊松噪声</option>
									<option value="3">乘性噪声</option>
									<option value="4">椒盐噪声</option>
								</select>
								<label class="mygray sm-right-margin">噪声强度:</label>
								<select id="noise_value" class="bg-right-margin">
									<option value="1">1</option>
									<option value="2">2</option>
									<option value="3" selected>3</option>
									<option value="4">4</option>
									<option value="5">5</option>
								</select>
							</div>
						</div>
						<div class="level2_box" style="display: none">
							<div class="value_box">
								<label class="mygray">掩码区域个数：</label>
								<input type="text" placeholder="正整数" id="maskNum" class="myinput" value="2" />
							</div>
							<div class="value_box">
								<label class="mygray">掩码相对大小：</label>
								<label class="mygray">0</label>
								<input type="range" id="maskWidth" value="20" />
								<label class="mygray">1</label>
							</div>
							<div class="value_box">
								<label class="mygray">掩码灰度值：</label>
								<label class="mygray">0</label>
								<input type="range" id="rangeMask" value="50" />
								<label class="mygray">255</label>
							</div>
						</div>
					</div>
					<div class="operate_area">
  <el-button type="primary" class="tran_btn" @click="imgTransform()">主要按钮</el-button>
						<!-- <div class="tran_btn" @click="imgTransform()">图像变换</div> -->
						  <el-button type="primary" class="tran_btn" @click="refresh()">重置</el-button>

						<!-- <div class="tran_btn" @click="refresh()">重置</div> -->
					</div>
					<div class="note_txt">图像识别</div>
					<div class="value_box">
						<label class="mygray sm-right-margin">分类器选择:</label>
						<select id="model1" class="bg-right-margin">
							<option value="1">ANN MNIST</option>
							<option value="2">VGG16 ImageNet</option>
							<option value="3" selected>ResNet50 ImageNet</option>
						</select>
					</div>

					<div class="operate_area">
						  <el-button type="primary" class="tran_btn" @click="predict(1)">图像分类</el-button>

						<!-- <div class="tran_btn" @click="predict(1)">图像分类</div> -->
					</div>

					<div class="result" id="pre1" style="display: none">
						<label class="note_txt">top3结果：</label>
						<div style="padding: 4px 0" v-for="(item, index) in items1" :key="index">
							<label class="note_txt"> {{ item.label }} : {{ item.proba }} </label>
						</div>
					</div>
				</div>

				<div class="imgshowbox">
					<div class="note_txt">输出</div>
					<div class="imgbox" id="new_img">
						<img src="" id="traned_pic" hidden class="img" />
					</div>

					<div class="note_txt">图像识别</div>
					<div class="value_box">
						<label class="mygray sm-right-margin">分类器选择:</label>
						<select id="model2" class="bg-right-margin">
							<option value="1">ANN MNIST</option>
							<option value="2">VGG16 ImageNet</option>
							<option value="3" selected>ResNet50 ImageNet</option>
						</select>
					</div>
					<div class="operate_area" id="new_predict">
					<el-button type="primary" class="tran_btn" @click="predict(2)">图像分类</el-button>

						<!-- <div class="tran_btn" @click="predict(2)">图像分类</div> -->
					</div>

					<div class="result" id="pre2" style="display: none">
						<label class="note_txt">top3结果：</label>
						<div style="padding: 4px 0" v-for="(item, index) in items2" :key="index">
							<label class="note_txt"> {{ item.label }} : {{ item.proba }} </label>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
export default {
	name: 'menu2',
	data() {
		return {
			tran_type: 0,
			history_data: '',
			pre_type: 0,
			items1:{},
			items2:{},
			upImage:false,
			myData:{}
		};
	},
	methods: {
		moveClick(){
			document.getElementById('photo').click()
		},
		// 上传图像文件
		uploadPicFile() {
			let imgfile = document.getElementById('photo').files[0];
			let imgUrl = window.URL.createObjectURL(imgfile);
			document.getElementById('upload_label').setAttribute('hidden', true);
			document.getElementById('uploadpic').setAttribute('src', imgUrl);
			this.upImage = true
			// document.getElementById('uploadpic').setAttribute('hidden', false);

			// $('#upload_label').attr('hidden', true);
			// $('#uploadpic').attr('src', imgUrl);
			// $('#uploadpic').attr('hidden', false);
		},
		// 改变第一级变换父类型
		change_level1_type(t) {
			this.tran_type = t;
			this.change_select_style('tran_select_level1', 'mybox', t);
			this.change_show_display('tran_select_level2', 'level2_box', t);
		},
		// 改变第一级选中样式
		change_select_style(parent, children, t) {
			let level1_div = document.getElementById(parent);
			let level1_items = level1_div.getElementsByClassName(children);
			// 重置所有元素样式
			for (let i = 0; i < level1_items.length; ++i) {
				let icon = level1_items[i].getElementsByClassName('circle')[0];
				icon.setAttribute('src', '@/assets/img/circle0.png');
				let label = level1_items[i].getElementsByClassName('tran_label')[0];
				label.style.color = '#4B5563';
			}
			// 更新选中元素的样式
			let new_icon = level1_items[t - 1].getElementsByClassName('circle')[0];
			new_icon.setAttribute('src', '@/assets/img/circle1.png');
			let new_label = level1_items[t - 1].getElementsByClassName('tran_label')[0];
			new_label.style.color = '#6366F1';
		},
		// 改变第二级显示情况
		change_show_display(parent, children, t) {
			// 更新下一级参数设置
			let level2_div = document.getElementById(parent);
			let level2_items = level2_div.getElementsByClassName(children);
			// 重置所有元素样式
			for (let i = 0; i < level2_items.length; ++i) {
				level2_items[i].style.display = 'none';
			}
			// 更新选中元素的样式
			level2_items[t - 1].style.display = 'block';
		},
		// 刷新页面
		refresh() {
			window.location.reload();
		},

		// 获取变换类型和参数
		get_tran_type_and_value(tran_type, value) {
			if (tran_type == 1) {
				// 几何变换
				let translation = parseFloat(document.getElementById('rangeTranslation').value);
				translation = (translation - 50) / 50.0;
				let rotation = parseFloat(document.getElementById('rangeRotation').value);
				rotation = (rotation - 50) / 50.0;
				let scale = parseFloat(document.getElementById('rangeScale').value);
				scale = scale / 50.0;
				// 添加数据
				this.myData = {};
				this.myData['translation'] = [translation, translation];
				this.myData['rotation'] = rotation * 180;
				this.myData['scale'] = scale;
				value.append('key', 'geometric');
				value.append('value', JSON.stringify(this.myData));
			} else if (tran_type == 2) {
				// 镜像变换
				let flip_type = parseInt(document.getElementById('flip_type').value);
				let p_value = parseFloat(document.getElementById('rangeFlip').value);
				p_value = p_value / 100;
				// 添加数据
				this.myData = {};
				this.myData['mode'] = flip_type;
				this.myData['p'] = p_value;
				value.append('key', 'flip');
				value.append('value', JSON.stringify(this.myData));
			} else if (tran_type == 3) {
				// 颜色变换
				let brightness = parseFloat(document.getElementById('rangeBrightness').value);
				brightness = brightness / 50.0;
				let contrast = parseFloat(document.getElementById('rangeContrast').value);
				contrast = contrast / 50.0;
				let saturation = parseFloat(document.getElementById('rangeSaturation').value);
				saturation = saturation / 50.0;
				let hue = parseFloat(document.getElementById('rangeHue').value);
				hue = (hue - 50) / 100;
				// 添加数据
				this.myData = {};
				this.myData['brightness'] = brightness;
				this.myData['contrast'] = contrast;
				this.myData['saturation'] = saturation;
				this.myData['hue'] = hue;
				value.append('key', 'color');
				value.append('value', JSON.stringify(this.myData));
			} else if (tran_type == 4) {
				// 滤波变换
				let filter_type = parseInt(document.getElementById('filter_type').value);
				let name = ['BLUR', 'EDGE_ENHANCE', 'SMOOTH', 'SHARPEN', 'DETAIL'];
				let p_value = parseFloat(document.getElementById('rangeFilter').value);
				p_value = p_value / 100;
				// 添加数据
				this.myData = {};
				this.myData['mode'] = name[filter_type - 1];
				this.myData['p'] = p_value;
				value.append('key', 'filter');
				value.append('value', JSON.stringify(this.myData));
			} else if (tran_type == 5) {
				// 噪声变换
				let noise_type = parseInt(document.getElementById('noise_type').value);
				let name = ['gaussian', 'poisson', 'speckle', 's&p'];
				let level = parseInt(document.getElementById('noise_value').value);
				// 添加数据
				this.myData = {};
				this.myData['mode'] = name[noise_type - 1];
				this.myData['level'] = level;
				value.append('key', 'noise');
				value.append('value', JSON.stringify(this.myData));
			} else if (tran_type == 6) {
				// 掩码变换
				let num = parseInt(document.getElementById('maskNum').value);
				num < 0 ? (num = 0) : (num = num);
				let width = parseFloat(document.getElementById('maskWidth').value);
				width = width / 100;
				let fillcolor = parseFloat(document.getElementById('rangeMask').value);
				fillcolor = parseInt((fillcolor / 100) * 255);
				// 添加数据
				this.myData = {};
				this.myData['num'] = num;
				this.myData['width'] = width;
				this.myData['fillcolor'] = fillcolor;
				value.append('key', 'mask');
				value.append('value', JSON.stringify(data));
			}
			return value;
		},
		// 获取分类模型
		get_model(type) {
			if (type == 1) {
				let model_type = parseInt(document.getElementById('model1').value);
				if (model_type == 1) {
					return 'MNIST';
				} else if (model_type == 2) {
					return 'VGG16';
				} else if (model_type == 3) {
					return 'ResNet50';
				}
			} else if (type == 2) {
				let model_type = parseInt(document.getElementById('model2').value);
				if (model_type == 1) {
					return 'MNIST';
				} else if (model_type == 2) {
					return 'VGG16';
				} else if (model_type == 3) {
					return 'ResNet50';
				}
			}
		},

		// 变换图像
		imgTransform() {
			let imgfile = document.getElementById('photo').files[0];
			if (imgfile == undefined) {
				alert('请先上传图片');
				return;
			}
			if (this.tran_type == 0) {
				alert('请选择变换类型');
				return;
			}
			let value = new FormData();
			value = this.get_tran_type_and_value(this.tran_type, value);
			this.history_data = value;
			value.append('file', imgfile);
			axios
				.post('http://8.141.162.184:5000' + '/imgTransform', value)
				.then((data) => {
					if (data['code'] == 200) {
						document.getElementById("traned_pic").setAttribute('src', data['data'])
						document.getElementById("traned_pic").setAttribute('hidden', false)
						// $('#traned_pic').attr('src', data['data']);
						// $('#traned_pic').attr('hidden', false);
					}
				})
				.catch((e) => {
					alert('图片变换出错！');
					// window.location.reload();
				});
			// $.ajax({
			//     url: '/imgTransform',
			//     data: value,
			//     type: "post",
			//     dataType: 'json',
			//     processData: false,
			//     contentType: false,
			//     success: (data) {
			//         if (data["code"] == 200) {
			//             $('#traned_pic').attr('src', data["data"]);
			//             $('#traned_pic').attr('hidden', false);
			//         }
			//     },
			//     error: (error) {
			//         alert('图片变换出错！');
			//         window.location.reload();
			//     }
			// });
		},
		// 图像分类预测
		 predict(k) {
		    let imgfile = document.getElementById("photo").files[0];
		    if (imgfile == undefined) {
		        alert('请先上传图片');
		        return;
		    }
			// document.getElementById("traned_pic").getAttribute('src')== ''
		    // if (k == 2 && $('#traned_pic').attr('src') == '') {
		    if (k == 2 && document.getElementById("traned_pic").getAttribute('src')== '') {
		        alert('请先变换图像');
		        return;
		    }
		    let value = new FormData();
		    if (k == 2) {
		        value = history_data;
		    }
		    value.append("file", imgfile);
		    value.append("model", get_model(k));
		    pre_type = k;

			axios
				.post('http://8.141.162.184:5000' + '/predict', value)
				.then((data) => {
					if (data['code'] == 200) {
		                if (pre_type == 1) {
							document.getElementById("pre1").style["display"]="flex"
		                    // $('#pre1').css('display', 'flex');
		                    this.items1 = data["data"];
		                } else if (pre_type == 2) {
							document.getElementById("pre2").style["display"]="flex"
		                    this.items2 = data["data"];
		                }
					}
				})
				.catch((e) => {
		            alert('图像分类出错！');
					// window.location.reload();
				});
		    // $.ajax({
		    //     url: '/predict',
		    //     data: value,
		    //     type: "post",
		    //     dataType: 'json',
		    //     processData: false,
		    //     contentType: false,
		    //     success: (data) {
		    //         if (data["code"] == 200) {
		    //             if (pre_type == 1) {
		    //                 $('#pre1').css('display', 'flex');
		    //                 pre1.items = data["data"];
		    //             } else if (pre_type == 2) {
		    //                 $('#pre2').css('display', 'flex');
		    //                 pre2.items = data["data"];
		    //             }
		    //         }
		    //     },
		    //     error: (error) {
		    //         alert('图像分类出错！');
		    //         window.location.reload();
		    //     }
		    // });
		}
	},
	// props: {
	// 	meta: {
	// 		type: Object,
	// 		default: () => {},
	// 	},
	// },
	// data() {
	// 	return {
	// 		iframeLoading: true,
	// 	};
	// },
	// created() {
	// 	this.bus.$on('onTagsViewRefreshRouterView', (path) => {
	// 		if (this.$route.path !== path) return false;
	// 		this.$emit('getCurrentRouteMeta');
	// 	});
	// },
	// mounted() {
	// 	this.initIframeLoad();
	// },
	// methods: {
	// 	// 初始化页面加载 loading
	// 	initIframeLoad() {
	// 		this.$nextTick(() => {
	// 			this.iframeLoading = true;
	// 			const iframe = document.getElementById('iframe');
	// 			if (!iframe) return false;
	// 			iframe.onload = () => {
	// 				this.iframeLoading = false;
	// 			};
	// 		});
	// 	},
	// },
};
</script>
<style scoped>
.header {
	width: 100%;
	height: 100px;
	background-color: #fdfdfd;
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
}

.container {
	width: 100%;
	margin-top: 50px;
	margin-bottom: 50px;
	display: flex;
	flex-direction: column;
	justify-content: flex-start;
	align-items: center;
}

.main {
	width: 100%;
	padding: 20px;
	border: 3px solid #dddddd;
	border-radius: 10px;
}

.title {
	/*width: 100%;*/
	height: 100px;
	font-size: 28px;
	color: #374151;
	text-align: center;
	letter-spacing: 2px;
	line-height: 100px;
	text-align: center;
	/*padding: 0 50px;*/
}

.imgshow {
	width: 100%;
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: flex-start;
}

.imgshowbox {
	width: 47%;
	background-color: white;
	border-radius: 8px;
	padding: 1%;
}

.note_txt {
	color: #555d6b;
	margin: 8px 0;
}

.imgbox {
	height: 300px;
	border: 6px dashed #d1d5db;
	color: #a0a7b2;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.imgbox label {
	text-align: center;
	font-size: 34px;
	letter-spacing: 2px;
}

.imgbox .img {
	height: 300px;
}

.radio-input {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
}

.mybox {
	padding: 0 12px;
	height: 40px;
	background-color: #f4f5f7;
	border-radius: 3px;
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	border: 1px solid #dddddd;
}

.mybox .circle {
	width: 24px;
	height: 24px;
}

.mybox .tran_label {
	margin-left: 10px;
	text-align: center;
	font-size: 18px;
	letter-spacing: 2px;
	color: #4b5563;
	font-weight: bold;
}

.mybox:hover {
	background-color: #e4e5e7;
}

.bg-right-margin {
	margin-right: 20px;
}

.sm-right-margin {
	margin-right: 10px;
}

.value_box {
	padding: 20px 4px 10px;
	display: flex;
	flex-direction: row;
	justify-content: flex-start;
	align-items: center;
}

input[type='range'] {
	-webkit-appearance: none;
	width: 240px;
	height: 16px;
	border-radius: 8px;
	outline: none;
	background-color: #6366f1;
}

input[type='range']::-webkit-slider-thumb {
	-webkit-appearance: none;
	position: relative;
	width: 10px;
	height: 16px;
	border-radius: 5px;
	background-color: white;
}

.mygray {
	padding: 0 4px;
	font-size: 16px;
	color: #888888;
}

select {
	outline: none;
	padding: 4px 10px;
}

.myinput {
	width: 80px;
	height: 24px;
	border: 1px solid #dddddd;
	outline: none;
	padding: 2px 4px;
	border-radius: 5px;
	margin: 0 20px 0 4px;
	font-size: 14px;
}

/* .tran_btn {
	width: 120px;
	height: 40px;
	background-color: #c2e0a3;
	text-align: center;
	line-height: 40px;
	color: #374151;
	font-size: 18px;
	margin: 10px 0;
	border-radius: 4px;
} */

.operate_area {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
}

.result {
	display: flex;
	flex-direction: column;
	justify-content: flex-start;
	align-items: flex-start;
}
</style>
