"""
配置参数文件 - GMP和MES相关配置
"""

class GMPConfig:
    # 关键质量属性阈值
    CQA_THRESHOLDS = {
        "purity_min": 98.0,
        "impurity_max": 2.0,
        "moisture_max": 5.0,
        "sterility_requirement": "Sterile",
        "endotoxin_limit": 0.25  # EU/mg
    }
    
    # 关键工艺参数范围
    CPP_RANGES = {
        "temperature_tolerance": 2.0,  # ±2°C
        "pressure_tolerance": 0.1,     # ±0.1 bar
        "ph_tolerance": 0.2,           # ±0.2
        "time_tolerance": 0.1          # ±10%
    }
    
    # 风险评估矩阵
    RISK_MATRIX = {
        "critical": {"severity": 5, "probability": 5},
        "high": {"severity": 4, "probability": 3},
        "medium": {"severity": 3, "probability": 2},
        "low": {"severity": 2, "probability": 1}
    }

class MESConfig:
    # MES系统接口配置
    BATCH_RECORD_FIELDS = [
        "batch_number", "product_name", "manufacturing_date",
        "expiry_date", "yield", "quality_status", "operator_id",
        "equipment_used", "critical_parameters", "deviations"
    ]
    
    # 数据采集频率
    DATA_COLLECTION = {
        "continuous": ["temperature", "pressure", "ph", "flow_rate"],
        "periodic": ["samples", "quality_tests", "equipment_checks"],
        "batch_end": ["yield_calculation", "documentation"]
    }
    
    # 报警级别
    ALERT_LEVELS = {
        "critical": ["sterility_failure", "cross_contamination", "safety_issue"],
        "major": ["parameter_deviation", "equipment_failure", "quality_alert"],
        "minor": ["warning", "maintenance_required", "calibration_due"]
    }
