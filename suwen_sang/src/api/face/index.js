/*
 * @Author: 78644 786442541@qq.com
 * @Date: 2022-06-06 21:00:32
 * @LastEditors: 78644 786442541@qq.com
 * @LastEditTime: 2022-06-07 01:31:19
 * @FilePath: \suwen_sang\src\api\face\index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import request from '@/utils/request';

// 样本数字攻击
export function generateImage(params) {
	return request({
		url: '/face/generateImage',
		method: 'post',
		data: JSON.stringify(params),
	});
}

// 样本物理攻击
export function generatePatch(params) {
	return request({
		url: '/face/generatePatch',
		method: 'post',
		data: JSON.stringify(params),
	});
}

// 模型对抗鲁棒性
export function evaluateModel(params) {
	return request({
		url: '/face/evaluateModel',
		method: 'post',
		data: params,
	});
}