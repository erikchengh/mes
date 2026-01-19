"""
MES专业功能模块
包含批记录管理、趋势分析、异常检测等MES核心功能
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import streamlit as st

class MESFeatures:
    """MES系统专业功能"""
    
    @staticmethod
    def generate_batch_records(product_info: Dict[str, Any], num_batches: int = 10) -> pd.DataFrame:
        """生成模拟批记录数据"""
        # 确保传入的是字典
        if not isinstance(product_info, dict):
            st.error(f"product_info 必须是字典，但收到的是 {type(product_info)}")
            return pd.DataFrame()
            
        # 获取产品名称
        product_name = product_info.get("description", "未知产品").split()[0] if product_info.get("description") else "产品"
        
        steps = product_info.get("工艺步骤", [])
        if not steps:
            st.warning("没有工艺步骤信息")
            return pd.DataFrame()
        
        # 生成批次数据
        records = []
        base_date = datetime.now() - timedelta(days=num_batches * 2)
        
        for batch_num in range(1, num_batches + 1):
            batch_date = base_date + timedelta(days=batch_num * 2)
            
            # 生成随机参数（模拟实际生产）
            np.random.seed(batch_num)  # 确保可重复性
            
            batch_record = {
                "batch_number": f"BATCH-{batch_num:04d}",
                "product_name": product_name,
                "manufacturing_date": batch_date.strftime("%Y-%m-%d"),
                "expiry_date": (batch_date + timedelta(days=730)).strftime("%Y-%m-%d"),  # 2年有效期
                "batch_size": np.random.choice([100, 200, 300, 500]),
                "line": np.random.choice(["Line-1", "Line-2", "Line-3"]),
                "shift": np.random.choice(["A", "B", "C"]),
                "operator": f"OP{batch_num % 5 + 1:03d}",
                "supervisor": f"SUP{(batch_num % 3) + 1:02d}",
                "yield_percent": round(np.random.uniform(85, 98), 2),
                "quality_status": np.random.choice(["合格", "待定", "不合格"], p=[0.95, 0.04, 0.01]),
                "overall_status": "通过" if np.random.random() > 0.1 else "需调查"
            }
            
            # 为每个步骤生成数据
            for i, step in enumerate(steps, 1):
                step_name = step.get("name", f"步骤{i}")
                
                # 模拟步骤参数（只取前3个参数）
                params = step.get("关键参数", [])[:3]
                for param in params:
                    param_key = f"step_{i}_{param[:10].replace(' ', '_').lower()}"
                    
                    # 根据不同参数类型生成模拟数据
                    if "温度" in param:
                        batch_record[f"{param_key}_target"] = 25.0
                        batch_record[f"{param_key}_actual"] = round(np.random.normal(25, 1.5), 1)
                        batch_record[f"{param_key}_status"] = "正常" if abs(batch_record[f"{param_key}_actual"] - 25) <= 2 else "偏离"
                    
                    elif "压力" in param:
                        batch_record[f"{param_key}_target"] = 1.0
                        batch_record[f"{param_key}_actual"] = round(np.random.normal(1.0, 0.15), 2)
                        batch_record[f"{param_key}_status"] = "正常" if abs(batch_record[f"{param_key}_actual"] - 1.0) <= 0.2 else "偏离"
                    
                    elif "pH" in param.lower():
                        batch_record[f"{param_key}_target"] = 7.0
                        batch_record[f"{param_key}_actual"] = round(np.random.normal(7.0, 0.2), 2)
                        batch_record[f"{param_key}_status"] = "正常" if 6.5 <= batch_record[f"{param_key}_actual"] <= 7.5 else "偏离"
                    
                    elif "时间" in param:
                        time_str = step.get("时间", "4h")
                        try:
                            if "天" in time_str:
                                target_time = float(time_str.replace("天", "").replace("(", "").replace(")", "")) * 24
                            elif "h" in time_str:
                                target_time = float(time_str.replace("h", "").replace("(", "").replace(")", ""))
                            else:
                                target_time = 4.0
                        except:
                            target_time = 4.0
                        
                        batch_record[f"{param_key}_target"] = target_time
                        batch_record[f"{param_key}_actual"] = round(np.random.normal(target_time, target_time * 0.1), 1)
                        batch_record[f"{param_key}_status"] = "正常" if abs(batch_record[f"{param_key}_actual"] - target_time) <= target_time * 0.15 else "偏离"
                    
                    else:
                        batch_record[f"{param_key}_target"] = 100
                        batch_record[f"{param_key}_actual"] = round(np.random.normal(100, 2), 1)
                        batch_record[f"{param_key}_status"] = "正常" if 95 <= batch_record[f"{param_key}_actual"] <= 105 else "偏离"
            
            records.append(batch_record)
        
        return pd.DataFrame(records)
    
    @staticmethod
    def analyze_batch_trends(batch_data: pd.DataFrame, parameters: List[str]) -> Dict[str, Any]:
        """分析批次趋势"""
        if batch_data.empty or not parameters:
            return {}
        
        analysis_results = {}
        
        for param_pattern in parameters:
            # 找到相关参数列
            param_cols = [col for col in batch_data.columns if param_pattern.lower() in col.lower() and "_actual" in col]
            
            if param_cols:
                for param_col in param_cols:
                    param_name = param_col.replace("_actual", "").replace("_", " ").title()
                    values = pd.to_numeric(batch_data[param_col], errors='coerce')
                    
                    if not values.empty:
                        valid_values = values.dropna()
                        if len(valid_values) > 0:
                            analysis_results[param_name] = {
                                "mean": round(valid_values.mean(), 3),
                                "std": round(valid_values.std(), 3),
                                "min": round(valid_values.min(), 3),
                                "max": round(valid_values.max(), 3),
                                "cv": round(valid_values.std() / valid_values.mean() * 100, 2) if valid_values.mean() != 0 else 0,
                                "trend": MESFeatures._calculate_trend(valid_values),
                                "cpk": MESFeatures._calculate_cpk(valid_values),
                                "outliers": MESFeatures._detect_outliers(valid_values)
                            }
        
        return analysis_results
    
    @staticmethod
    def _calculate_trend(values: pd.Series) -> str:
        """计算趋势方向"""
        if len(values) < 3:
            return "数据不足"
        
        try:
            x = np.arange(len(values))
            slope, intercept = np.polyfit(x, values, 1)
            
            if slope > 0.05:
                return "上升趋势 ⬆️"
            elif slope < -0.05:
                return "下降趋势 ⬇️"
            else:
                return "稳定趋势 ➡️"
        except:
            return "计算失败"
    
    @staticmethod
    def _calculate_cpk(values: pd.Series) -> float:
        """计算过程能力指数Cpk"""
        if len(values) < 2:
            return 0
        
        try:
            mean = values.mean()
            std = values.std()
            
            if std == 0 or pd.isna(std):
                return 0
            
            # 假设规范限（可根据实际情况调整）
            usl = mean + 3 * std  # 上规范限
            lsl = mean - 3 * std  # 下规范限
            
            cpu = (usl - mean) / (3 * std) if std > 0 else 0
            cpl = (mean - lsl) / (3 * std) if std > 0 else 0
            
            return min(cpu, cpl)
        except:
            return 0
    
    @staticmethod
    def _detect_outliers(values: pd.Series, threshold: float = 2.0) -> List[int]:
        """检测异常值"""
        if len(values) < 3:
            return []
        
        try:
            mean = values.mean()
            std = values.std()
            
            if std == 0 or pd.isna(std):
                return []
            
            outliers = []
            for idx, value in enumerate(values):
                z_score = abs((value - mean) / std)
                if z_score > threshold:
                    outliers.append(idx)
            
            return outliers
        except:
            return []
    
    @staticmethod
    def generate_quality_report(batch_data: pd.DataFrame) -> Dict[str, Any]:
        """生成质量报告"""
        if batch_data.empty:
            return {}
        
        try:
            report = {
                "summary": {
                    "total_batches": len(batch_data),
                    "passed_batches": len(batch_data[batch_data["overall_status"] == "通过"]),
                    "failed_batches": len(batch_data[batch_data["overall_status"] != "通过"]),
                    "yield_average": round(batch_data["yield_percent"].mean(), 2),
                    "yield_range": f"{batch_data['yield_percent'].min():.1f} - {batch_data['yield_percent'].max():.1f}"
                },
                "quality_distribution": {
                    "合格": len(batch_data[batch_data["quality_status"] == "合格"]),
                    "待定": len(batch_data[batch_data["quality_status"] == "待定"]),
                    "不合格": len(batch_data[batch_data["quality_status"] == "不合格"]) if "不合格" in batch_data["quality_status"].values else 0
                },
                "parameter_stability": {},
                "recommendations": []
            }
            
            # 分析参数稳定性
            param_cols = [col for col in batch_data.columns if "_actual" in col]
            for param_col in param_cols[:5]:  # 只分析前5个参数
                param_name = param_col.replace("_actual", "").replace("_", " ").title()
                values = pd.to_numeric(batch_data[param_col], errors='coerce')
                
                if not values.empty:
                    valid_values = values.dropna()
                    if len(valid_values) > 0:
                        cv = valid_values.std() / valid_values.mean() * 100 if valid_values.mean() != 0 else 0
                        stability = "高" if cv < 5 else "中" if cv < 10 else "低"
                        
                        report["parameter_stability"][param_name] = {
                            "cv_percent": round(cv, 2),
                            "stability": stability
                        }
            
            # 生成建议
            if report["summary"]["failed_batches"] > 0:
                report["recommendations"].append(f"需要调查{report['summary']['failed_batches']}个失败批次")
            
            if report["summary"]["yield_average"] < 90:
                report["recommendations"].append("收率偏低，建议优化工艺")
            
            for param, data in report["parameter_stability"].items():
                if data["stability"] == "低":
                    report["recommendations"].append(f"{param}稳定性低，建议加强控制")
            
            return report
        except Exception as e:
            st.error(f"生成质量报告时出错: {e}")
            return {}
    
    @staticmethod
    def calculate_oee(batch_data: pd.DataFrame) -> Dict[str, Any]:
        """计算设备综合效率OEE"""
        if batch_data.empty:
            return {}
        
        try:
            # 模拟数据
            availability = round(np.random.uniform(85, 95), 2)  # 可用率
            performance = round(np.random.uniform(90, 98), 2)   # 性能率
            quality = round(batch_data["yield_percent"].mean() / 100, 2)  # 质量率
            
            oee = round(availability * performance * quality / 10000, 4) * 100
            
            return {
                "availability_percent": availability,
                "performance_percent": performance,
                "quality_percent": quality * 100,
                "oee_percent": oee,
                "oee_level": "世界级" if oee >= 85 else "优秀" if oee >= 75 else "一般" if oee >= 65 else "需要改进",
                "loss_analysis": {
                    "availability_loss": 100 - availability,
                    "performance_loss": 100 - performance,
                    "quality_loss": 100 - (quality * 100)
                }
            }
        except Exception as e:
            st.error(f"计算OEE时出错: {e}")
            return {}
