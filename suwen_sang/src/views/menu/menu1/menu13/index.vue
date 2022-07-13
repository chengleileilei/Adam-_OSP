<!--
 * @Author: 78644 786442541@qq.com
 * @Date: 2022-06-03 16:23:20
 * @LastEditors: 78644 786442541@qq.com
 * @LastEditTime: 2022-06-03 21:23:02
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
						<p>根据不同设置，评估模型在单个数据集上的统计结果</p>
					</div>
					<div class="pic_center">
						<i class="el-icon-right"></i>
					</div>
					<div class="pic_right">
						<div class="pie_chart_area">
							<div id="pie_chart_left" style="height: 400px; width: 400px"></div>
							<div id="pie_chart_right" style="height: 400px; width: 400px"></div>
						</div>
					</div>
				</div>
				<div class="content-footer-test">
					<p style="font-size: 22px">步骤：</p>
					<ul>
						<li><p>1、选择设置并提交</p></li>
						<li><p>2、预览结果</p></li>
					</ul>
				</div>
			</el-card>
			<el-card class="box-card">
				<div slot="header" class="clearfix">
					<span class="title">功能实现</span>
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
								<el-form-item label="扰动阈值">
									<el-select v-model="form.disturbance" placeholder="请选择扰动阈值">
										<el-option v-for="item in disturbanceList" :key="item.value" :label="item.label" :value="item.value"> </el-option>
									</el-select>
								</el-form-item>
							</div>
							<div class="attack_bottom">
								<el-form-item label="迭代次数" style="margin-right: 15px">
									<el-select v-model="form.iteration" placeholder="请选择迭代次数">
										<el-option v-for="item in iterationList" :key="item.value" :label="item.label" :value="item.value"> </el-option>
									</el-select>
								</el-form-item>
								<el-form-item label="有攻击目标" style="margin-right: 150px">
									<el-switch v-model="form.have_attackTarget" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
								</el-form-item>
							</div>
							<el-divider>数据集设置</el-divider>
							<div class="data_set_setting">
								<el-form-item label="数据集" style="margin-right: 15px">
									<el-select v-model="form.dataSet" placeholder="请选择数据集">
										<el-option v-for="item in dataSetList" :key="item.value" :label="item.label" :value="item.value"> </el-option>
									</el-select>
								</el-form-item>
								<el-form-item style="margin-right: 20px" class="option_area">
									<el-button type="primary" @click="onSubmit">提交设置</el-button>
									<el-button @click="clean">清空</el-button>
								</el-form-item>
							</div>
						</el-form>
					</div>
					<div class="form_right">
						<div class="pie_chart_area">
							<div id="result_chart_left" style="height: 400px; width: 400px"></div>
							<div id="result_chart_right" style="height: 400px; width: 400px"></div>
						</div>
					</div>
				</div>
			</el-card>
		</div>
	</div>
</template>

<script>
import * as echarts from 'echarts';
import { evaluateModel } from '@/api/face';

export default {
	name: 'menu13',
	data() {
		return {
			val: '',
			dialogImageUrl: '',
			dialogVisible: false,
			titleSrc:'https://pdb-wrl.oss-cn-beijing.aliyuncs.com/algorithm/v2-801108ef77f34644d615e31cfd590e2b_r.jpg',
			src: '',
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
			dataSetList: [
				{ id: 0, label: 'lfw', value: 'lfw' },
				{ id: 1, label: 'agedb_30', value: 'agedb_30' },
			],
			form: {
				model: 'MobieFaceNet',
				attackedModel: 'GhostNet',
				attackMethod: 'PGD',
				disturbance: '0.5',
				iteration: '10',
				have_attackTarget: false,
				dataSet: 'lfw',
			},
		};
	},
	mounted() {
		this.pieChartLeftInit();
		this.pieChartRightInit();
	},
	methods: {
		onSubmit() {
			let param = this.form
			console.log(param);
			evaluateModel(param).then((res) => {
				console.log(res);
			});
			this.resultChartLeftInit();
			this.resultChartRightInit();
		},
		clean() {
			this.form = {
				model: '',
				attackedModel: '',
				attackMethod: '',
				disturbance: '',
				iteration: '',
				have_attackTarget: false,
				dataSet: '',
			};
		},
		// 左饼图初始化
		pieChartLeftInit() {
			var chartDom = document.getElementById('pie_chart_left');
			var myChart = echarts.init(chartDom);
			var option;
			option = {
				title: {
					text: '干净样本',
					left: 'center',
				},
				tooltip: {
					trigger: 'item',
				},
				series: [
					{
						name: '样本数据',
						type: 'pie',
						radius: '50%',
						data: [
							{ value: 240, name: '正确' },
							{ value: 10, name: '错误' },
						],
						emphasis: {
							itemStyle: {
								shadowBlur: 10,
								shadowOffsetX: 0,
								shadowColor: 'rgba(0, 0, 0, 0.5)',
							},
						},
					},
				],
			};
			option && myChart.setOption(option);
			window.addEventListener('resize', () => {
				myChart.resize();
			});
		},
		// 右饼图初始化
		pieChartRightInit() {
			var chartDom = document.getElementById('pie_chart_right');
			var myChart = echarts.init(chartDom);
			var option;
			option = {
				title: {
					text: '对抗样本',
					left: 'center',
				},
				tooltip: {
					trigger: 'item',
				},
				series: [
					{
						name: '样本数据',
						type: 'pie',
						radius: '50%',
						data: [
							{ value: 120, name: '正确' },
							{ value: 130, name: '错误' },
						],
						emphasis: {
							itemStyle: {
								shadowBlur: 10,
								shadowOffsetX: 0,
								shadowColor: 'rgba(0, 0, 0, 0.5)',
							},
						},
					},
				],
			};
			option && myChart.setOption(option);
			window.addEventListener('resize', () => {
				myChart.resize();
			});
		},
		// 左饼图初始化
		resultChartLeftInit() {
			var chartDom = document.getElementById('result_chart_left');
			var myChart = echarts.init(chartDom);
			var option;
			option = {
				title: {
					text: '干净样本',
					left: 'center',
				},
				tooltip: {
					trigger: 'item',
				},
				series: [
					{
						name: '样本数据',
						type: 'pie',
						radius: '50%',
						data: [
							{ value: 240, name: '正确' },
							{ value: 10, name: '错误' },
						],
						emphasis: {
							itemStyle: {
								shadowBlur: 10,
								shadowOffsetX: 0,
								shadowColor: 'rgba(0, 0, 0, 0.5)',
							},
						},
					},
				],
			};
			option && myChart.setOption(option);
			window.addEventListener('resize', () => {
				myChart.resize();
			});
		},
		// 右饼图初始化
		resultChartRightInit() {
			var chartDom = document.getElementById('result_chart_right');
			var myChart = echarts.init(chartDom);
			var option;
			option = {
				title: {
					text: '对抗样本',
					left: 'center',
				},
				tooltip: {
					trigger: 'item',
				},
				series: [
					{
						name: '样本数据',
						type: 'pie',
						radius: '50%',
						data: [
							{ value: 120, name: '正确' },
							{ value: 130, name: '错误' },
						],
						emphasis: {
							itemStyle: {
								shadowBlur: 10,
								shadowOffsetX: 0,
								shadowColor: 'rgba(0, 0, 0, 0.5)',
							},
						},
					},
				],
			};
			option && myChart.setOption(option);
			window.addEventListener('resize', () => {
				myChart.resize();
			});
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
					font-size: 22px;
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
					.pie_chart_area {
						display: flex;
					}
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
					display: flex;
					flex: 6;
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
					.data_set_setting {
						display: flex;
						flex-direction: row;
						justify-content: space-around;
						align-items: center;
						.option_area ::v-deep .el-form-item__content {
							margin-left: 0 !important;
						}
					}
				}
				.form_right {
					display: flex;
					flex-direction: column;
					flex: 4;
					margin-left: 30px;
					font-size: 22px;
					.pie_chart_area {
						display: flex;
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
