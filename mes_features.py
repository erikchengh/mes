"""
MES专业功能模块
包含批记录管理、趋势分析、异常检测等MES核心功能
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class MESFeatures:
    """MES系统专业功能"""
    
    @staticmethod
    def generate_batch_records(product_info: Dict, num_batches: int = 10) -> pd.DataFrame:
        """生成模拟批记录数据"""
        steps = product_info.get("工艺步骤", [])
        if not steps:
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
                "product_name": product_info.get("product", "未知产品"),
                "manufacturing_date": batch_date.strftime("%Y-%m-%d"),
                "expiry_date": (batch_date + timedelta(days=730)).strftime("%Y-%m-%d"),  # 2年有效期
                "batch_size": np.random.choice([100, 200, 300, 500]),
                "line": np.random.choice(["Line-1", "Line-2", "Line-3"]),
                "shift": np.random.choice(["A", "B", "C"]),
                "operator": f"OP{batch_num % 5 + 1:03d}",
                "supervisor": f"SUP{(batch_num % 3) + 1:02d}",
                "yield_percent": round(np.random.uniform(85, 98), 2),
                "quality_status": np.random.choice(["合格", "合格", "合格", "合格", "待定"], p=[0.8, 0.1, 0.05, 0.04, 0.01]),
                "overall_status": "通过" if np.random.random() > 0.1 else "需调查"
            }
            
            # 为每个步骤生成数据
            for i, step in enumerate(steps, 1):
                step_key = f"step_{i}"
                step_name = step.get("name", f"步骤{i}")
                
                # 模拟步骤参数
                params = step.get("关键参数", [])
                step_data = {}
                
                for param in params[:3]:  # 只取前3个参数
                    param_key = param.replace(" ", "_").lower()[:15]
                    
                    # 根据不同参数类型生成模拟数据
                    if "温度" in param:
                        step_data[f"{param_key}_target"] = 25.0
                        step_data[f"{param_key}_actual"] = round(np.random.normal(25, 1.5), 1)
                        step_data[f"{param_key}_status"] = "正常" if abs(step_data[f"{param_key}_actual"] - 25) <= 2 else "偏离"
                    
                    elif "压力" in param:
                        step_data[f"{param_key}_target"] = 1.0
                        step_data[f"{param_key}_actual"] = round(np.random.normal(1.0, 0.15), 2)
                        step_data[f"{param_key}_status"] = "正常" if abs(step_data[f"{param_key}_actual"] - 1.0) <= 0.2 else "偏离"
                    
                    elif "pH" in param or "ph" in param:
                        step_data[f"{param_key}_target"] = 7.0
                        step_data[f"{param_key}_actual"] = round(np.random.normal(7.0, 0.2), 2)
                        step_data[f"{param_key}_status"] = "正常" if 6.5 <= step_data[f"{param_key}_actual"] <= 7.5 else "偏离"
                    
                    elif "时间" in param:
                        step_data[f"{param_key}_target"] = 4.0
                        step_data[f"{param_key}_actual"] = round(np.random.normal(4.0, 0.3), 1)
                        step_data[f"{param_key}_status"] = "正常" if 3.5 <= step_data[f"{param_key}_actual"] <= 4.5 else "偏离"
                    
                    else:
                        step_data[f"{param_key}_target"] = 100
                        step_data[f"{param_key}_actual"] = round(np.random.normal(100, 2), 1)
                        step_data[f"{param_key}_status"] = "正常" if 95 <= step_data[f"{param_key}_actual"] <= 105 else "偏离"
                
                batch_record.update(step_data)
            
            records.append(batch_record)
        
        return pd.DataFrame(records)
    
    @staticmethod
    def analyze_batch_trends(batch_data: pd.DataFrame, parameters: List[str]) -> Dict:
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
                        analysis_results[param_name] = {
                            "mean": round(values.mean(), 3),
                            "std": round(values.std(), 3),
                            "min": round(values.min(), 3),
                            "max": round(values.max(), 3),
                            "cv": round(values.std() / values.mean() * 100, 2) if values.mean() != 0 else 0,
                            "trend": MESFeatures._calculate_trend(values),
                            "cpk": MESFeatures._calculate_cpk(values),
                            "outliers": MESFeatures._detect_outliers(values)
                        }
        
        return analysis_results
    
    @staticmethod
    def _calculate_trend(values: pd.Series) -> str:
        """计算趋势方向"""
        if len(values) < 3:
            return "数据不足"
        
        x = np.arange(len(values))
        slope, intercept = np.polyfit(x, values, 1)
        
        if slope > 0.05:
            return "上升趋势 ⬆️"
        elif slope < -0.05:
            return "下降趋势 ⬇️"
        else:
            return "稳定趋势 ➡️"
    
    @staticmethod
    def _calculate_cpk(values: pd.Series) -> float:
        """计算过程能力指数Cpk"""
        if len(values) < 2:
            return 0
        
        mean = values.mean()
        std = values.std()
        
        if std == 0:
            return 0
        
        # 假设规范限（可根据实际情况调整）
        usl = mean + 3 * std  # 上规范限
        lsl = mean - 3 * std  # 下规范限
        
        cpu = (usl - mean) / (3 * std) if std > 0 else 0
        cpl = (mean - lsl) / (3 * std) if std > 0 else 0
        
        return min(cpu, cpl)
    
    @staticmethod
    def _detect_outliers(values: pd.Series, threshold: float = 2.0) -> List[int]:
        """检测异常值"""
        if len(values) < 3:
            return []
        
        mean = values.mean()
        std = values.std()
        
        if std == 0:
            return []
        
        outliers = []
        for idx, value in enumerate(values):
            z_score = abs((value - mean) / std)
            if z_score > threshold:
                outliers.append(idx)
        
        return outliers
    
    @staticmethod
    def generate_quality_report(batch_data: pd.DataFrame) -> Dict:
        """生成质量报告"""
        if batch_data.empty:
            return {}
        
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
                cv = values.std() / values.mean() * 100 if values.mean() != 0 else 0
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
    
    @staticmethod
    def calculate_oee(batch_data: pd.DataFrame) -> Dict:
        """计算设备综合效率OEE"""
        if batch_data.empty:
            return {}
        
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
