"""
MES专业分析模块
包含工艺风险评估、合规性检查、质量指标计算等功能
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
import streamlit as st

class MESAnalyzer:
    """MES专业分析器"""
    
    @staticmethod
    def assess_process_risk(steps: List[Dict]) -> Dict:
        """评估工艺风险 - 基于ICH Q9质量风险管理"""
        risk_score = 0
        critical_steps = []
        risk_factors = []
        
        for i, step in enumerate(steps, 1):
            step_risk = 0
            step_name = step.get("name", "")
            
            # 风险因素评估
            step_risk += MESAnalyzer._evaluate_step_risk_factors(step)
            
            # 如果是关键步骤，增加权重
            if any(keyword in step_name for keyword in ["灭菌", "无菌", "灌装", "层析", "病毒"]):
                step_risk *= 1.5
                critical_steps.append({
                    "step": step_name,
                    "step_number": i,
                    "risk_level": "关键",
                    "risk_score": step_risk
                })
            
            risk_score += step_risk
            
            if step_risk > 5:  # 高风险步骤
                risk_factors.append({
                    "step": step_name,
                    "risk_score": step_risk,
                    "factors": MESAnalyzer._identify_risk_factors(step)
                })
        
        # 风险等级划分
        avg_risk = risk_score / max(len(steps), 1)
        risk_level = MESAnalyzer._determine_risk_level(avg_risk)
        
        return {
            "total_risk_score": round(risk_score, 2),
            "average_risk_score": round(avg_risk, 2),
            "risk_level": risk_level,
            "critical_steps": critical_steps,
            "high_risk_factors": risk_factors,
            "recommendations": MESAnalyzer._generate_risk_recommendations(risk_level, critical_steps)
        }
    
    @staticmethod
    def _evaluate_step_risk_factors(step: Dict) -> float:
        """评估单个步骤的风险因素"""
        risk_score = 0
        
        # 参数复杂度
        params = step.get("关键参数", [])
        for param in params:
            if any(keyword in param for keyword in ["温度", "压力", "pH", "时间"]):
                risk_score += 1
            if any(keyword in param for keyword in ["无菌", "病毒", "内毒素"]):
                risk_score += 3
            if any(keyword in param for keyword in ["含量", "纯度", "杂质"]):
                risk_score += 2
        
        # 设备复杂度
        equipment = step.get("设备", [])
        for equip in equipment:
            if any(keyword in equip for keyword in ["生物反应器", "层析", "冻干", "灭菌"]):
                risk_score += 2
            elif any(keyword in equip for keyword in ["灌装", "过滤", "离心"]):
                risk_score += 1.5
            else:
                risk_score += 1
        
        return risk_score
    
    @staticmethod
    def _identify_risk_factors(step: Dict) -> List[str]:
        """识别具体风险因素"""
        factors = []
        step_name = step.get("name", "")
        params = step.get("关键参数", [])
        
        if any(keyword in step_name for keyword in ["灭菌", "无菌"]):
            factors.append("无菌操作风险")
        
        if any(keyword in step_name for keyword in ["病毒", "生物"]):
            factors.append("生物安全风险")
        
        for param in params:
            if "温度" in param:
                factors.append("温度控制风险")
            if "压力" in param:
                factors.append("压力控制风险")
            if "pH" in param:
                factors.append("pH控制风险")
        
        return list(set(factors))
    
    @staticmethod
    def _determine_risk_level(score: float) -> str:
        """确定风险等级"""
        if score >= 8:
            return "极高风险 (红色)"
        elif score >= 6:
            return "高风险 (橙色)"
        elif score >= 4:
            return "中风险 (黄色)"
        elif score >= 2:
            return "低风险 (蓝色)"
        else:
            return "可接受风险 (绿色)"
    
    @staticmethod
    def _generate_risk_recommendations(risk_level: str, critical_steps: List) -> List[str]:
        """生成风险控制建议"""
        recommendations = []
        
        if "极高风险" in risk_level or "高风险" in risk_level:
            recommendations.append("建议进行详细的工艺验证和风险评估")
            recommendations.append("建立额外的过程控制和监测点")
            recommendations.append("实施更严格的变更控制程序")
        
        if critical_steps:
            recommendations.append(f"重点监控{len(critical_steps)}个关键步骤")
            for step in critical_steps[:3]:  # 显示前3个关键步骤
                recommendations.append(f"  - 步骤{step['step_number']}: {step['step']}")
        
        recommendations.append("定期进行质量回顾和趋势分析")
        recommendations.append("确保操作人员经过充分培训")
        
        return recommendations
    
    @staticmethod
    def calculate_process_metrics(steps: List[Dict]) -> Dict:
        """计算工艺关键指标"""
        total_steps = len(steps)
        total_params = sum(len(step.get("关键参数", [])) for step in steps)
        
        # 设备使用统计
        all_equipment = []
        for step in steps:
            all_equipment.extend(step.get("设备", []))
        unique_equipment = set(all_equipment)
        
        # 时间统计
        total_time = 0
        time_units = []
        for step in steps:
            if "时间" in step:
                time_str = str(step["时间"])
                if "天" in time_str:
                    time_value = float(time_str.replace("天", "").replace("(", "").replace(")", "")) * 24
                elif "h" in time_str:
                    time_value = float(time_str.replace("h", "").replace("(", "").replace(")", ""))
                else:
                    try:
                        time_value = float(time_str)
                    except:
                        time_value = 0
                total_time += time_value
                time_units.append("小时")
        
        # 复杂度评分
        complexity_score = MESAnalyzer._calculate_complexity_score(steps)
        
        return {
            "total_steps": total_steps,
            "total_parameters": total_params,
            "unique_equipment": len(unique_equipment),
            "total_time_hours": round(total_time, 2),
            "avg_params_per_step": round(total_params / total_steps, 2) if total_steps > 0 else 0,
            "complexity_score": complexity_score,
            "equipment_list": list(unique_equipment)
        }
    
    @staticmethod
    def _calculate_complexity_score(steps: List[Dict]) -> float:
        """计算工艺复杂度评分"""
        score = 0
        
        # 步骤数量权重
        score += len(steps) * 0.5
        
        # 关键参数权重
        critical_params = 0
        for step in steps:
            params = step.get("关键参数", [])
            for param in params:
                if any(keyword in param for keyword in ["无菌", "病毒", "内毒素", "关键"]):
                    critical_params += 3
                elif any(keyword in param for keyword in ["温度", "pH", "压力", "含量"]):
                    critical_params += 2
                else:
                    critical_params += 1
        
        score += critical_params * 0.3
        
        # 设备复杂度权重
        equipment_score = 0
        for step in steps:
            equipment = step.get("设备", [])
            for equip in equipment:
                if any(keyword in equip for keyword in ["生物反应器", "层析", "冻干"]):
                    equipment_score += 3
                elif any(keyword in equip for keyword in ["灌装", "灭菌", "过滤"]):
                    equipment_score += 2
                else:
                    equipment_score += 1
        
        score += equipment_score * 0.2
        
        return round(score, 2)
    
    @staticmethod
    def check_gmp_compliance(product_info: Dict) -> Dict:
        """检查GMP合规性"""
        steps = product_info.get("工艺步骤", [])
        gmp_class = product_info.get("GMP分类", "未分类")
        
        compliance_items = []
        
        # 检查关键步骤控制
        for i, step in enumerate(steps, 1):
            step_name = step.get("name", "")
            params = step.get("关键参数", [])
            
            # 检查是否有必要的参数控制
            if any(keyword in step_name for keyword in ["灭菌", "无菌"]):
                if not any("无菌" in param or "灭菌" in param for param in params):
                    compliance_items.append({
                        "step": step_name,
                        "issue": "无菌步骤缺少无菌保证参数",
                        "severity": "严重",
                        "recommendation": "增加无菌相关监测参数"
                    })
            
            if any(keyword in step_name for keyword in ["过滤", "层析", "纯化"]):
                if not any("压力" in param or "流量" in param for param in params):
                    compliance_items.append({
                        "step": step_name,
                        "issue": "分离步骤缺少过程控制参数",
                        "severity": "中等",
                        "recommendation": "增加压力或流量监测"
                    })
        
        # 检查工艺描述完整性
        if not product_info.get("description"):
            compliance_items.append({
                "step": "整体工艺",
                "issue": "缺少工艺描述",
                "severity": "中等",
                "recommendation": "补充工艺描述信息"
            })
        
        # 风险评估
        severity_counts = {
            "严重": sum(1 for item in compliance_items if item["severity"] == "严重"),
            "中等": sum(1 for item in compliance_items if item["severity"] == "中等"),
            "轻微": sum(1 for item in compliance_items if item["severity"] == "轻微")
        }
        
        overall_status = "合规" if severity_counts["严重"] == 0 else "需改进"
        
        return {
            "gmp_classification": gmp_class,
            "overall_status": overall_status,
            "compliance_items": compliance_items,
            "severity_counts": severity_counts,
            "recommendations": [item["recommendation"] for item in compliance_items[:5]]
        }
    
    @staticmethod
    def generate_batch_record_template(product_info: Dict) -> Dict:
        """生成批记录模板"""
        steps = product_info.get("工艺步骤", [])
        
        batch_template = {
            "header": {
                "产品名称": "",
                "批号": "",
                "生产日期": "",
                "有效期至": "",
                "批量": "",
                "生产线": "",
                "班次": ""
            },
            "steps": []
        }
        
        for i, step in enumerate(steps, 1):
            step_template = {
                "step_number": i,
                "step_name": step.get("name", ""),
                "parameters": {},
                "equipment": step.get("设备", []),
                "time_required": step.get("时间", ""),
                "operator_signature": "",
                "supervisor_signature": "",
                "qc_check": "",
                "remarks": ""
            }
            
            # 为每个参数添加记录字段
            for param in step.get("关键参数", []):
                step_template["parameters"][param] = {
                    "target_value": "",
                    "actual_value": "",
                    "lower_limit": "",
                    "upper_limit": "",
                    "unit": ""
                }
            
            batch_template["steps"].append(step_template)
        
        return batch_template
