"""
完整的制药工艺数据库 - PAS-X MES专业版
涵盖所有主要制药品类，符合FDA 21 CFR Part 11和EU GMP要求
移除中药部分，优化PAS-X MES集成
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

class GMPRiskLevel(Enum):
    """GMP风险等级分类 (基于ICH Q9和EU GMP)"""
    LOW = "低风险"
    MEDIUM = "中风险"
    MEDIUM_HIGH = "中高风险"
    HIGH = "高风险"
    CRITICAL = "极高风险"
    ATMP = "先进治疗产品"

class ProcessStage(Enum):
    """工艺阶段分类"""
    API_SYNTHESIS = "原料药合成"
    BIOPROCESSING = "生物工艺"
    FORMULATION = "制剂工艺"
    FILL_FINISH = "灌装完成"
    PACKAGING = "包装"
    QC_TESTING = "质量控制"

class PharmaceuticalProcesses:
    """制药工艺数据库 - MES专业版"""
    
    # ====================== 原料药 (API) 生产工艺 ======================
    API_PROCESSES = {
        # 1. 化学合成API
        "化学合成原料药": {
            "抗生素类": {
                "description": "通过化学合成或半合成方法生产的抗生素原料药",
                "GMP分类": GMPRiskLevel.HIGH.value,
                "ICH指导原则": ["Q1A(R2)", "Q3C(R8)", "Q6A"],
                "关键特征": ["抗菌谱广", "化学结构明确", "纯度要求高", "残留溶剂控制"],
                "PAS-X模块": ["Batch Execution", "Material Management", "Equipment Management", "Weighing & Dispensing"],
                "工艺步骤": [
                    {
                        "name": "反应釜投料",
                        "stage": ProcessStage.API_SYNTHESIS.value,
                        "关键参数": ["投料顺序", "摩尔比(1.0-1.05)", "温度控制(±2℃)", "氮气保护"],
                        "PAT应用": ["在线温度监测", "在线pH监测", "压力传感器"],
                        "设备": ["隔离器投料站", "反应釜(316L SS)", "计量罐", "称量罩"],
                        "时间(min)": 120,
                        "收率范围": "98.5-99.5%",
                        "质量控制点": ["起始物料鉴别", "溶剂残留<500ppm", "金属残留<10ppm"]
                    },
                    {
                        "name": "催化氢化反应",
                        "stage": ProcessStage.API_SYNTHESIS.value,
                        "关键参数": ["氢气压力(3-5bar)", "反应温度(50±5℃)", "催化剂载量(0.5-1%)", "反应转化率>99%"],
                        "PAT应用": ["在线GC分析", "在线压力监测", "在线H₂消耗监测"],
                        "设备": ["高压反应釜", "氢气供应系统", "催化剂过滤系统", "在线分析仪"],
                        "时间(h)": 12,
                        "收率范围": "92-96%",
                        "质量控制点": ["手性纯度>99.5%", "相关物质<0.5%", "金属残留<10ppm"]
                    },
                    {
                        "name": "结晶分离",
                        "stage": ProcessStage.API_SYNTHESIS.value,
                        "关键参数": ["结晶温度梯度", "搅拌速度(50-100rpm)", "晶种添加", "结晶时间(8±1h)"],
                        "PAT应用": ["在线粒度分析(FBRM)", "在线拉曼光谱", "浊度监测"],
                        "设备": ["结晶罐", "控温系统", "在线结晶监测仪"],
                        "时间(h)": 8,
                        "收率范围": "85-90%",
                        "质量控制点": ["晶型确认(Form I)", "粒度分布(D90<50μm)", "结晶度>95%"]
                    }
                ],
                "关键质量属性": [
                    {"CQA": "化学纯度", "目标": ">99.5%", "方法": "HPLC", "限度": "NMT 0.5%"},
                    {"CQA": "晶型", "目标": "Form I", "方法": "XRPD", "限度": "单一晶型"},
                    {"CQA": "残留溶剂", "目标": "<ICH限度的50%", "方法": "GC", "限度": "符合ICH Q3C"},
                    {"CQA": "粒度分布", "目标": "D90<50μm", "方法": "激光粒度仪", "限度": "符合USP<429>"}
                ],
                "工艺验证要求": [
                    "工艺性能确认(PPQ: 连续3批)",
                    "清洁验证(最差条件)",
                    "持续工艺验证(CPV)",
                    "分析方法验证"
                ],
                "数据完整性要求": [
                    "电子批记录(EBR)",
                    "审计追踪(完整)",
                    "电子签名(双人复核)",
                    "数据备份(每日)"
                ]
            },
            
            "心血管类": {
                "description": "治疗心血管疾病的化学合成原料药，高选择性合成",
                "GMP分类": GMPRiskLevel.MEDIUM_HIGH.value,
                "ICH指导原则": ["Q1A(R2)", "Q3C(R8)", "Q6A", "Q11"],
                "关键特征": ["手性中心多", "晶型控制严格", "稳定性要求高", "光学纯度>99%"],
                "工艺步骤": [
                    {
                        "name": "不对称合成",
                        "stage": ProcessStage.API_SYNTHESIS.value,
                        "关键参数": ["手性选择性(ee>99.5%)", "反应收率(>85%)", "温度控制(-20±2℃)"],
                        "PAT应用": ["在线手性HPLC", "在线FTIR", "温度梯度控制"],
                        "设备": ["低温反应器", "手性催化剂系统", "在线手性分析仪"],
                        "时间(h)": 24,
                        "收率范围": "85-90%",
                        "质量控制点": ["对映体过量(ee>99.5%)", "非对映体比例<0.5%", "催化剂残留<5ppm"]
                    }
                ]
            },
            
            "肿瘤类": {
                "description": "细胞毒性/高活性原料药，OEB 4-5级",
                "GMP分类": GMPRiskLevel.CRITICAL.value,
                "关键特征": ["OEB等级≥4", "职业暴露限值<1μg/m³", "密闭生产", "清洁验证严格"],
                "工艺步骤": [
                    {
                        "name": "密闭投料与反应",
                        "stage": ProcessStage.API_SYNTHESIS.value,
                        "关键参数": ["负压控制(-50Pa)", "风速>0.45m/s", "手套箱完整性", "在线粒子监测"],
                        "安全控制": ["连续在线粒子监测", "个人防护装备(PPE)", "生物安全柜", "应急淋浴"],
                        "设备": ["隔离器系统", "密闭传输系统", "在线清洗(CIP)", "废气处理系统"],
                        "时间(h)": 8,
                        "收率范围": "75-85%"
                    }
                ]
            }
        },
        
        # 2. 生物技术API
        "生物技术原料药": {
            "单克隆抗体": {
                "description": "哺乳动物细胞表达的单克隆抗体，符合ICH Q5系列指导原则",
                "GMP分类": GMPRiskLevel.CRITICAL.value,
                "细胞系": "CHO-K1/CHO-DG44",
                "培养规模": "2000L一次性生物反应器",
                "关键特征": ["高特异性", "高亲和力", "Fc功能完整", "糖基化控制"],
                "工艺步骤": [
                    {
                        "name": "N-1种子扩增",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["细胞密度(2-3×10⁶ cells/mL)", "活力>95%", "倍增时间(18-24h)"],
                        "过程分析技术": ["在线活细胞密度(VCD)", "在线溶氧(pO₂)", "在线葡萄糖/乳酸", "在线pH"],
                        "设备": ["Wave生物反应器", "一次性搅拌式反应器", "生物过程分析仪"],
                        "时间(天)": 7,
                        "质量控制点": ["细胞活力>95%", "支原体阴性", "无菌检测阴性"]
                    },
                    {
                        "name": "生产培养",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["峰值VCD(20-25×10⁶ cells/mL)", "抗体滴度(3-5g/L)", "培养时间(14天)"],
                        "培养基": ["化学成分确定培养基", "补料分批培养", "代谢物控制"],
                        "过程控制": ["动态补料策略", "pH控制(7.0±0.2)", "溶氧控制(30-50%)"],
                        "设备": ["2000L一次性生物反应器", "在线分析仪", "自动补料系统"],
                        "时间(天)": 14,
                        "质量控制点": ["抗体滴度>3g/L", "聚集体<5%", "宿主细胞蛋白<100ppm"]
                    }
                ],
                "下游纯化": {
                    "捕获层析": ["Protein A亲和层析", "载量>30g/L", "洗脱pH(3.5-3.8)", "收率>95%"],
                    "病毒灭活": ["低pH孵育(pH 3.6-3.8, 60min)", "病毒清除验证(LRV>4)"],
                    "精细纯化": ["阳离子交换", "阴离子流穿模式", "多模式层析", "纯度>99%"],
                    "病毒过滤": ["20nm Planova滤器", "病毒清除验证", "完整性测试"],
                    "超滤/透析": ["30kD MWCO", "浓缩至50-100g/L", "缓冲液置换", "收率>90%"]
                },
                "关键质量属性": [
                    {"CQA": "生物活性", "目标": "符合参比品", "方法": "细胞活性测定"},
                    {"CQA": "纯度", "目标": ">99%", "方法": "SEC-HPLC", "限度": "单体>95%"},
                    {"CQA": "电荷变异体", "目标": "符合标准", "方法": "CEX-HPLC", "限度": "主峰>80%"},
                    {"CQA": "糖基化", "目标": "G0F>60%", "方法": "HILIC", "限度": "符合标准"}
                ]
            },
            
            "重组蛋白": {
                "description": "大肠杆菌/酵母表达的重组治疗性蛋白",
                "GMP分类": GMPRiskLevel.HIGH.value,
                "表达系统": ["E.coli BL21(DE3)", "Pichia pastoris", "CHO细胞"],
                "关键特征": ["包涵体复性", "糖基化控制", "二硫键正确配对", "生物活性"],
                "工艺步骤": [
                    {
                        "name": "发酵表达",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["诱导时机(OD600=20-30)", "诱导温度(25-30℃)", "表达时间(24-48h)"],
                        "PAT应用": ["在线OD监测", "在线蛋白表达监测", "代谢物分析"],
                        "设备": ["发酵罐", "在线传感器", "自动补料系统"],
                        "时间(h)": 48,
                        "质量控制点": ["表达水平>1g/L", "包涵体形成", "宿主细胞蛋白"]
                    }
                ]
            }
        },
        
        # 3. 多肽原料药
        "多肽原料药": {
            "固相合成多肽": {
                "description": "Fmoc/t-Boc固相合成，用于GLP-1类似物、胰岛素等",
                "GMP分类": GMPRiskLevel.HIGH.value,
                "合成规模": "50-100kg/批次",
                "关键特征": ["序列准确", "手性纯度>99%", "二硫键正确配对", "聚集控制"],
                "工艺步骤": [
                    {
                        "name": "树脂溶胀与偶联",
                        "stage": ProcessStage.API_SYNTHESIS.value,
                        "关键参数": ["树脂载量(0.3-0.7mmol/g)", "偶联时间(30-60min)", "偶联效率>99.5%"],
                        "PAT应用": ["在线Kaiser Test", "在线UV监测", "温度控制"],
                        "设备": ["多肽合成仪", "在线监测系统", "自动溶剂输送"],
                        "时间(min)": 45,
                        "质量控制点": ["偶联效率>99.5%", "缺失序列<0.5%", "D-氨基酸<0.1%"]
                    }
                ]
            }
        },
        
        # 4. 寡核苷酸原料药
        "寡核苷酸原料药": {
            "反义寡核苷酸": {
                "description": "固相合成的DNA/RNA寡核苷酸，用于基因治疗",
                "GMP分类": GMPRiskLevel.CRITICAL.value,
                "合成方法": ["亚磷酰胺法", "H-膦酸酯法"],
                "关键特征": ["序列准确", "全保护基团", "无RNase污染", "无内毒素"],
                "工艺步骤": [
                    {
                        "name": "固相合成",
                        "stage": ProcessStage.API_SYNTHESIS.value,
                        "关键参数": ["偶联效率>99%", "切割条件优化", "去保护完全"],
                        "PAT应用": ["在线Trityl监测", "UV监测", "温度梯度控制"],
                        "设备": ["寡核苷酸合成仪", "在线分析系统", "纯化系统"],
                        "时间(h)": 24,
                        "质量控制点": ["全长序列>85%", "N-1序列<10%", "无RNase污染"]
                    }
                ]
            }
        }
    }
    
    # ====================== 制剂生产工艺 ======================
    DOSAGE_FORM_PROCESSES = {
        # 1. 固体制剂
        "固体制剂": {
            "口服片剂(速释)": {
                "description": "速释片剂，满足USP/EP溶出度要求，符合21 CFR Part 211",
                "GMP分类": GMPRiskLevel.MEDIUM.value,
                "处方类型": ["直接压片", "湿法制粒", "干法制粒"],
                "关键特征": ["剂量准确(RSD<2%)", "含量均匀度", "溶出度符合标准", "稳定性好"],
                "工艺步骤": [
                    {
                        "name": "高速剪切湿法制粒",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["剪切时间(2-5min)", "终点功率曲线", "LOD(1.5-2.5%)", "粒度分布"],
                        "PAT应用": ["在线NIR水分分析", "在线粒径分析", "终点判断系统"],
                        "设备": ["高速剪切制粒机", "在线湿整粒机", "PAT集成系统"],
                        "时间(min)": 20,
                        "质量控制点": ["水分含量(1.5-2.5%)", "粒度分布(D50:100-300μm)", "堆密度(0.4-0.6g/mL)"]
                    },
                    {
                        "name": "流化床干燥",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["进风温度(60±5℃)", "终点水分(1.0-2.0%)", "物料温度(<50℃)", "干燥终点"],
                        "PAT应用": ["在线NIR水分监测", "温度监测", "终点判断"],
                        "设备": ["流化床干燥机(带WIP)", "在线监测系统", "自动控制系统"],
                        "时间(min)": 45,
                        "质量控制点": ["最终水分(1.0-2.0%)", "粒度分布", "流动性(卡尔指数<25)"]
                    },
                    {
                        "name": "高速压片",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["片重差异(±3%)", "硬度(40-80N)", "崩解时限(<15min)", "脆碎度(<0.8%)"],
                        "PAT应用": ["在线片重监测", "在线硬度监测", "在线崩解监测"],
                        "设备": ["高速压片机(>100万片/小时)", "在线检测系统", "自动剔除系统"],
                        "时间(h)": 10,
                        "质量控制点": ["片重差异(±3%)", "硬度合格率>99%", "外观无缺陷"]
                    }
                ],
                "过程控制策略": [
                    {"CPP": "片重差异", "控制范围": "±3%", "监控频率": "连续", "控制方法": "在线监测+自动调节"},
                    {"CPP": "片剂硬度", "控制范围": "40-80N", "监控频率": "15分钟", "控制方法": "在线监测"},
                    {"CPP": "崩解时间", "控制范围": "<15分钟", "监控频率": "30分钟", "控制方法": "离线测试"},
                    {"CPP": "含量均匀度", "控制范围": "RSD<2%", "监控频率": "每批", "控制方法": "HPLC分析"}
                ]
            },
            
            "缓控释片剂": {
                "description": "骨架型/膜控型缓释制剂，零级/一级释放",
                "GMP分类": GMPRiskLevel.HIGH.value,
                "释放机制": ["亲水凝胶骨架", "不溶性骨架", "渗透泵", "离子交换树脂"],
                "关键特征": [
                    "体外释放度(3-4个时间点)",
                    "食物影响研究",
                    "剂量倾泻风险评估",
                    "释放机制验证"
                ],
                "工艺步骤": [
                    {
                        "name": "缓释层制备",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["聚合物比例", "粒径控制", "混合均匀度", "水分控制"],
                        "PAT应用": ["在线NIR混合均匀度", "在线粒径分析", "水分监测"],
                        "设备": ["高剪切制粒机", "流化床干燥机", "在线分析系统"],
                        "时间(h)": 8,
                        "质量控制点": ["聚合物含量均匀度", "粒度分布", "水分含量"]
                    }
                ]
            },
            
            "硬胶囊剂": {
                "description": "粉末或颗粒填充的硬胶囊制剂，提高生物利用度",
                "GMP分类": GMPRiskLevel.MEDIUM.value,
                "关键特征": ["掩盖不良味道", "提高稳定性", "个性化给药", "提高顺应性"],
                "工艺步骤": [
                    {
                        "name": "胶囊填充",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["装量差异(±5%)", "锁合完整性", "填充速度", "胶囊方向"],
                        "PAT应用": ["在线装量监测", "在线胶囊检查", "金属检测"],
                        "设备": ["全自动胶囊填充机", "在线检测系统", "金属检测机"],
                        "时间(h)": 8,
                        "质量控制点": ["装量差异合格率>99%", "锁合完整性100%", "外观无缺陷"]
                    }
                ]
            }
        },
        
        # 2. 无菌制剂
        "无菌制剂": {
            "小容量注射剂": {
                "description": "终端灭菌注射剂，符合EU GMP Annex 1(2022)要求",
                "GMP分类": GMPRiskLevel.CRITICAL.value,
                "洁净级别": ["C级背景下的A级"],
                "关键特征": ["无菌保证(SAL<10⁻⁶)", "无热原(内毒素<0.25EU/mL)", "可见异物控制", "不溶性微粒符合USP<788>"],
                "工艺步骤": [
                    {
                        "name": "除菌过滤",
                        "stage": ProcessStage.FILL_FINISH.value,
                        "关键参数": ["滤前生物负载(<10CFU/100mL)", "滤器完整性测试", "压差控制(<30psi)", "过滤时间"],
                        "验证要求": ["细菌截留试验", "相容性试验", "可提取物/浸出物研究"],
                        "设备": ["冗余过滤系统", "在线完整性测试仪", "自动压力控制"],
                        "时间(min)": 60,
                        "质量控制点": ["无菌保证", "完整性测试通过", "内毒素<0.25EU/mL"]
                    },
                    {
                        "name": "洗烘灌封联动",
                        "stage": ProcessStage.FILL_FINISH.value,
                        "关键参数": ["灌装精度(±1%)", "西林瓶洗后微粒(<5个/瓶)", "隧道烘箱(300℃/5min)", "灌装速度"],
                        "环境监控": ["连续粒子监测", "浮游菌/沉降菌", "表面微生物", "操作人员监控"],
                        "设备": ["BFS/西林瓶灌装线", "隔离器/RABS系统", "自动在线监测"],
                        "速度(瓶/分钟)": 300,
                        "质量控制点": ["灌装精度合格率>99.5%", "密封完整性", "可见异物"]
                    },
                    {
                        "name": "终端灭菌",
                        "stage": ProcessStage.FILL_FINISH.value,
                        "关键参数": ["F0值(≥8分钟)", "温度均匀性(±0.5℃)", "热穿透验证", "装载模式"],
                        "验证要求": ["空载热分布", "满载热分布和热穿透", "生物指示剂挑战"],
                        "设备": ["蒸汽灭菌柜", "温度验证系统", "自动记录系统"],
                        "时间(min)": 30,
                        "质量控制点": ["F0值符合要求", "生物指示剂阴性", "无过度杀灭"]
                    }
                ]
            },
            
            "冻干粉针剂": {
                "description": "冷冻干燥无菌粉末，需严格控制冻干曲线",
                "GMP分类": GMPRiskLevel.CRITICAL.value,
                "关键特征": ["稳定性好", "复溶性好(<30秒)", "水分控制(<1%)", "外观完好"],
                "工艺步骤": [
                    {
                        "name": "冷冻干燥",
                        "stage": ProcessStage.FILL_FINISH.value,
                        "关键参数": ["共晶点温度", "一次干燥温度(-30~+30℃)", "二次干燥温度(+20~+40℃)", "真空度(50-100mTorr)"],
                        "PAT应用": ["在线温度监测", "在线压力监测", "在线水分监测"],
                        "设备": ["冻干机", "在线监测系统", "自动控制系统"],
                        "时间(天)": 3,
                        "质量控制点": ["水分<1%", "外观饱满", "复溶时间<30秒"]
                    }
                ]
            }
        },
        
        # 3. 半固体制剂
        "半固体制剂": {
            "乳膏剂": {
                "description": "O/W或W/O型乳剂基质制剂，局部外用",
                "GMP分类": GMPRiskLevel.MEDIUM.value,
                "关键特征": ["局部外用", "释放可控", "使用舒适", "稳定性好"],
                "工艺步骤": [
                    {
                        "name": "真空乳化",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["乳化温度(70-80℃)", "搅拌速度(500-1500rpm)", "均质压力(20-50bar)", "真空度(-0.8~-0.9bar)"],
                        "PAT应用": ["在线粘度监测", "在线温度控制", "在线均质监测"],
                        "设备": ["真空乳化罐", "均质机", "在线监测系统"],
                        "时间(h)": 4,
                        "质量控制点": ["粘度合格", "pH值符合要求", "粒度分布均匀"]
                    }
                ]
            }
        },
        
        # 4. 液体制剂
        "液体制剂": {
            "口服溶液": {
                "description": "口服液体制剂，儿童适用",
                "GMP分类": GMPRiskLevel.LOW.value,
                "关键特征": ["吸收快", "儿童适用", "口感重要", "剂量准确"],
                "工艺步骤": [
                    {
                        "name": "配制与过滤",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["pH值调节", "糖度控制", "澄清度", "含量均匀"],
                        "PAT应用": ["在线pH监测", "在线浊度监测", "在线含量监测"],
                        "设备": ["配液罐", "过滤系统", "在线分析仪"],
                        "时间(h)": 6,
                        "质量控制点": ["pH值符合标准", "澄清透明", "含量合格"]
                    }
                ]
            }
        }
    }
    
    # ====================== 生物制品生产工艺 ======================
    BIOLOGICAL_PROCESSES = {
        # 1. 疫苗
        "疫苗": {
            "灭活疫苗": {
                "description": "病原体灭活后保留免疫原性的疫苗",
                "GMP分类": GMPRiskLevel.CRITICAL.value,
                "关键特征": ["安全性高", "免疫原性好", "稳定性要求高", "佐剂系统"],
                "工艺步骤": [
                    {
                        "name": "病毒培养与收获",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["细胞基质(Vero/MDCK)", "病毒滴度(HA>1:256)", "收获时机(72-96hpi)", "细胞病变效应"],
                        "PAT应用": ["在线细胞密度监测", "在线病毒滴度监测", "在线代谢物分析"],
                        "设备": ["细胞培养反应器", "收获系统", "在线分析系统"],
                        "时间(天)": 7,
                        "质量控制点": ["病毒滴度合格", "无菌检测阴性", "支原体阴性"]
                    },
                    {
                        "name": "病毒灭活与纯化",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["灭活剂浓度(β-丙内酯0.01-0.1%)", "灭活时间(24-48h)", "灭活温度(2-8℃)", "灭活验证"],
                        "验证要求": ["灭活曲线验证", "残留灭活剂检测", "免疫原性保留"],
                        "设备": ["灭活罐", "纯化系统", "在线监测系统"],
                        "时间(h)": 48,
                        "质量控制点": ["完全灭活", "免疫原性保留", "纯度>90%"]
                    }
                ]
            },
            
            "重组蛋白疫苗": {
                "description": "基因工程表达的抗原蛋白疫苗",
                "GMP分类": GMPRiskLevel.CRITICAL.value,
                "关键特征": ["成分明确", "安全性好", "稳定性高", "批次间一致性好"],
                "工艺步骤": [
                    {
                        "name": "重组蛋白表达与纯化",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["表达系统(酵母/CHO)", "表达水平(>1g/L)", "纯化收率(>60%)", "纯度(>95%)"],
                        "PAT应用": ["在线蛋白浓度监测", "在线纯度监测", "在线收率计算"],
                        "设备": ["发酵罐", "层析系统", "在线分析系统"],
                        "时间(天)": 10,
                        "质量控制点": ["抗原含量合格", "纯度>95%", "内毒素<10EU/mg"]
                    }
                ]
            },
            
            "mRNA疫苗": {
                "description": "脂质纳米颗粒包裹的mRNA疫苗",
                "GMP分类": GMPRiskLevel.ATMP.value,
                "关键特征": ["快速开发", "高效表达", "冷链要求(-70℃)", "LNP递送系统"],
                "工艺步骤": [
                    {
                        "name": "mRNA体外转录",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["模板DNA质量", "转录效率", "加帽率(>95%)", "PolyA尾长度"],
                        "PAT应用": ["在线浓度监测", "在线完整性分析", "在线纯度监测"],
                        "设备": ["体外转录系统", "纯化系统", "在线分析仪"],
                        "时间(h)": 24,
                        "质量控制点": ["完整性>90%", "加帽率>95%", "无菌检测阴性"]
                    }
                ]
            }
        },
        
        # 2. 血液制品
        "血液制品": {
            "人血白蛋白": {
                "description": "从人血浆中提取的白蛋白制剂",
                "GMP分类": GMPRiskLevel.CRITICAL.value,
                "关键特征": ["扩容作用", "运输功能", "血源安全", "病毒安全性"],
                "工艺步骤": [
                    {
                        "name": "低温乙醇分离",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["乙醇浓度梯度", "温度控制(-5~0℃)", "pH控制(5.0-7.0)", "沉淀时间"],
                        "PAT应用": ["在线乙醇浓度监测", "在线温度控制", "在线pH监测"],
                        "设备": ["低温反应罐", "离心分离系统", "在线控制系统"],
                        "时间(h)": 24,
                        "质量控制点": ["白蛋白纯度>96%", "多聚体<5%", "病毒安全性验证"]
                    }
                ]
            },
            
            "免疫球蛋白": {
                "description": "静脉注射用免疫球蛋白(IVIG)",
                "GMP分类": GMPRiskLevel.CRITICAL.value,
                "关键特征": ["抗体多样性", "病毒灭活", "抗补体活性", "稳定性"],
                "工艺步骤": [
                    {
                        "name": "多步层析纯化",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["离子交换条件", "亲和层析", "病毒过滤", "超滤浓缩"],
                        "PAT应用": ["在线UV监测", "在线pH/电导监测", "在线病毒清除监测"],
                        "设备": ["层析系统", "病毒过滤系统", "在线监测系统"],
                        "时间(天)": 5,
                        "质量控制点": ["IgG纯度>98%", "病毒安全性验证", "抗补体活性合格"]
                    }
                ]
            }
        },
        
        # 3. 细胞治疗产品
        "细胞治疗产品": {
            "CAR-T细胞": {
                "description": "嵌合抗原受体T细胞，自体细胞治疗",
                "GMP分类": GMPRiskLevel.ATMP.value,
                "关键特征": ["自体来源", "短保质期(3-7天)", "冷链运输(2-8℃)", "个性化治疗"],
                "工艺步骤": [
                    {
                        "name": "白细胞分离与激活",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["CD3+细胞数(≥1×10⁹)", "细胞活力(≥90%)", "激活时间(24-48h)", "激活效率"],
                        "PAT应用": ["在线细胞计数", "在线活力监测", "在线激活标志物检测"],
                        "设备": ["细胞处理系统", "生物安全柜", "在线分析仪"],
                        "时间(h)": 24,
                        "质量控制点": ["细胞数量合格", "活力>90%", "无菌检测阴性"]
                    },
                    {
                        "name": "病毒转导与扩增",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["MOI(3-10)", "转导效率(≥30%)", "细胞密度(1×10⁶ cells/mL)", "扩增时间(7-10天)"],
                        "PAT应用": ["在线细胞密度监测", "在线转导效率监测", "在线代谢物分析"],
                        "设备": ["G-Rex培养系统", "生物反应器", "在线监测系统"],
                        "时间(天)": 10,
                        "质量控制点": ["转导效率合格", "细胞数量达标", "CAR表达>70%"]
                    }
                ]
            }
        },
        
        # 4. 基因治疗产品
        "基因治疗产品": {
            "AAV载体": {
                "description": "腺相关病毒基因治疗载体",
                "GMP分类": GMPRiskLevel.ATMP.value,
                "关键特征": ["长期表达", "低免疫原性", "组织靶向性", "高滴度生产"],
                "工艺步骤": [
                    {
                        "name": "三重质粒转染",
                        "stage": ProcessStage.BIOPROCESSING.value,
                        "关键参数": ["质粒比例(1:1:1)", "转染效率(>80%)", "细胞密度(2×10⁶ cells/mL)", "表达时间(72h)"],
                        "PAT应用": ["在线细胞密度监测", "在线转染效率监测", "在线病毒滴度监测"],
                        "设备": ["悬浮培养系统", "转染设备", "在线分析系统"],
                        "时间(天)": 5,
                        "质量控制点": ["病毒滴度>1×10¹⁴ vg/L", "空壳率<20%", "感染性滴度合格"]
                    }
                ]
            }
        }
    }
    
    # ====================== 新型给药系统 ======================
    NOVEL_DOSAGE_FORMS = {
        # 1. 靶向制剂
        "靶向制剂": {
            "脂质体": {
                "description": "药物包封于磷脂双分子层的靶向制剂",
                "GMP分类": GMPRiskLevel.HIGH.value,
                "关键特征": ["靶向性", "缓释性", "降低毒性", "提高疗效"],
                "工艺步骤": [
                    {
                        "name": "脂质膜制备与载药",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["磷脂组成", "载药方法(主动/被动)", "包封率(>90%)", "载药量"],
                        "PAT应用": ["在线包封率监测", "在线粒径分析", "在线电位监测"],
                        "设备": ["挤出器", "高压均质机", "在线分析系统"],
                        "时间(h)": 6,
                        "质量控制点": ["包封率>90%", "粒径(80-120nm)", "电位(-30~-50mV)"]
                    }
                ]
            },
            
            "纳米粒": {
                "description": "聚合物/脂质纳米粒，提高难溶性药物生物利用度",
                "GMP分类": GMPRiskLevel.HIGH.value,
                "关键特征": ["提高溶解度", "缓释", "靶向", "稳定性好"],
                "工艺步骤": [
                    {
                        "name": "纳米乳化与固化",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["乳化压力(500-1500bar)", "循环次数(5-20次)", "固化条件", "稳定性控制"],
                        "PAT应用": ["在线粒径分析", "在线PDI监测", "在线稳定性监测"],
                        "设备": ["高压均质机", "固化系统", "在线分析仪"],
                        "时间(h)": 8,
                        "质量控制点": ["粒径(100-200nm)", "PDI<0.2", "稳定性符合要求"]
                    }
                ]
            }
        },
        
        # 2. 透皮给药系统
        "透皮给药系统": {
            "透皮贴剂": {
                "description": "药物通过皮肤吸收的给药系统",
                "GMP分类": GMPRiskLevel.MEDIUM.value,
                "关键特征": ["避免首过效应", "血药平稳", "使用方便", "提高顺应性"],
                "工艺步骤": [
                    {
                        "name": "涂布与复合",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["涂布厚度", "干燥条件", "复合强度", "裁切精度"],
                        "PAT应用": ["在线厚度监测", "在线重量监测", "在线温度控制"],
                        "设备": ["涂布机", "干燥隧道", "复合裁切机"],
                        "time(h)": 10,
                        "质量控制点": ["含量均匀度", "释放度符合要求", "粘附力合格"]
                    }
                ]
            }
        },
        
        # 3. 吸入制剂
        "吸入制剂": {
            "干粉吸入剂": {
                "description": "肺部给药的干粉制剂",
                "GMP分类": GMPRiskLevel.HIGH.value,
                "关键特征": ["肺部沉积率高", "剂量准确", "患者易用", "稳定性好"],
                "工艺步骤": [
                    {
                        "name": "微粉化与混合",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["粒径控制(D50:1-5μm)", "混合均匀度", "流动性", "静电控制"],
                        "PAT应用": ["在线粒径分析", "在线混合均匀度监测", "在线流动性监测"],
                        "设备": ["气流粉碎机", "精密混合机", "在线分析系统"],
                        "时间(h)": 8,
                        "质量控制点": ["粒径分布符合要求", "含量均匀度", "排空率>85%"]
                    }
                ]
            },
            
            "吸入溶液": {
                "description": "雾化吸入溶液制剂",
                "GMP分类": GMPRiskLevel.HIGH.value,
                "关键特征": ["肺部直接吸收", "起效快", "剂量可调", "适用于儿童"],
                "工艺步骤": [
                    {
                        "name": "无菌配制与过滤",
                        "stage": ProcessStage.FILL_FINISH.value,
                        "关键参数": ["无菌保证", "渗透压调节", "pH控制", "稳定性"],
                        "PAT应用": ["在线无菌监测", "在线渗透压监测", "在线pH监测"],
                        "设备": ["无菌配制系统", "除菌过滤系统", "在线监测系统"],
                        "时间(h)": 6,
                        "质量控制点": ["无菌保证", "渗透压符合要求", "稳定性合格"]
                    }
                ]
            }
        },
        
        # 4. 长效注射剂
        "长效注射剂": {
            "微球注射剂": {
                "description": "PLGA微球缓释注射剂",
                "GMP分类": GMPRiskLevel.HIGH.value,
                "关键特征": ["长效(1-3个月)", "减少给药频率", "提高顺应性", "平稳血药浓度"],
                "工艺步骤": [
                    {
                        "name": "乳化-溶剂蒸发",
                        "stage": ProcessStage.FORMULATION.value,
                        "关键参数": ["乳化速度", "溶剂蒸发速率", "粒径控制", "载药量"],
                        "PAT应用": ["在线粒径监测", "在线溶剂残留监测", "在线载药量监测"],
                        "设备": ["乳化系统", "溶剂蒸发系统", "在线分析系统"],
                        "时间(h)": 12,
                        "质量控制点": ["粒径分布均匀", "载药量符合要求", "突释<20%"]
                    }
                ]
            }
        }
    }
    
    # ====================== PAS-X MES 集成配置 ======================
    MES_CONFIG = {
        "电子批记录系统": {
            "功能模块": ["生产指令", "设备指令", "分析指令", "称量指令"],
            "合规要求": [
                "21 CFR Part 11合规",
                "EU GMP Annex 11合规",
                "数据完整性ALCOA+原则",
                "审计追踪(完整)"
            ],
            "版本控制": "自动版本管理，变更控制集成",
            "签名要求": [
                "操作员电子签名",
                "QA放行签名",
                "双人复核签名",
                "审计员访问权限"
            ]
        },
        "物料管理系统": {
            "物料状态": ["待检", "合格", "不合格", "隔离", "放行", "待处理"],
            "库存管理": [
                "先进先出(FIFO)自动控制",
                "有效期管理自动预警",
                "库存水平实时监控",
                "批次追溯完整链条"
            ],
            "称量配料": [
                "电子称量指令自动下发",
                "防错称量(条码/RFID验证)",
                "称量数据自动采集传输",
                "物料平衡自动计算"
            ],
            "物料追溯": [
                "正向追溯(从原料到成品)",
                "反向追溯(从成品到原料)",
                "物料消耗实时报表",
                "偏差物料自动锁定"
            ]
        },
        "设备管理系统": {
            "设备状态": ["待清洁", "清洁中", "可用", "运行中", "维护中", "校准中", "停用"],
            "维护管理": [
                "预防性维护计划自动排程",
                "维修工单电子化",
                "备件库存管理",
                "设备历史记录完整"
            ],
            "校准管理": [
                "校准计划自动提醒",
                "校准记录电子化",
                "校准到期预警",
                "校准证书管理"
            ],
            "使用记录": [
                "设备使用日志自动记录",
                "OEE(整体设备效率)自动计算",
                "设备故障时间统计",
                "性能趋势分析"
            ]
        },
        "质量管理系统": {
            "偏差管理": [
                "偏差自动生成和分类",
                "CAPA(纠正预防措施)跟踪",
                "根本原因分析工具",
                "效果验证自动提醒"
            ],
            "变更控制": [
                "电子变更申请工作流",
                "影响评估模板",
                "批准流程电子化",
                "变更实施跟踪"
            ],
            "环境监测": [
                "EMS数据自动采集(温湿度、压差、粒子)",
                "报警分级管理",
                "趋势分析报告自动生成",
                "超标结果自动触发调查"
            ],
            "审计管理": [
                "内部审计计划",
                "审计发现跟踪",
                "供应商审计管理",
                "法规符合性检查"
            ]
        },
        "报表分析系统": {
            "生产报表": [
                "批次生产报告",
                "生产效率分析",
                "物料消耗分析",
                "设备利用率报表"
            ],
            "质量报表": [
                "质量趋势分析",
                "偏差统计报告",
                "环境监测趋势",
                "投诉分析报告"
            ],
            "合规报表": [
                "GMP符合性报告",
                "数据完整性报告",
                "审计追踪报告",
                "电子签名报告"
            ]
        }
    }
    
    # ====================== 统一接口方法 ======================
    
    @staticmethod
    def get_all_processes() -> Dict[str, Any]:
        """获取所有工艺数据"""
        all_processes = {}
        all_processes.update(PharmaceuticalProcesses.API_PROCESSES)
        all_processes.update(PharmaceuticalProcesses.DOSAGE_FORM_PROCESSES)
        all_processes.update(PharmaceuticalProcesses.BIOLOGICAL_PROCESSES)
        all_processes.update(PharmaceuticalProcesses.NOVEL_DOSAGE_FORMS)
        return all_processes
    
    @property
    def PROCESSES(self) -> Dict[str, Any]:
        """合并所有工艺 (兼容原有接口)"""
        return self.get_all_processes()
    
    @staticmethod
    def get_main_categories() -> List[str]:
        """获取所有主分类"""
        categories = []
        categories.extend(PharmaceuticalProcesses.API_PROCESSES.keys())
        categories.extend(PharmaceuticalProcesses.DOSAGE_FORM_PROCESSES.keys())
        categories.extend(PharmaceuticalProcesses.BIOLOGICAL_PROCESSES.keys())
        categories.extend(PharmaceuticalProcesses.NOVEL_DOSAGE_FORMS.keys())
        return list(set(categories))
    
    @staticmethod
    def get_products(category: str) -> List[str]:
        """获取指定分类下的所有产品"""
        if category in PharmaceuticalProcesses.API_PROCESSES:
            return list(PharmaceuticalProcesses.API_PROCESSES[category].keys())
        elif category in PharmaceuticalProcesses.DOSAGE_FORM_PROCESSES:
            return list(PharmaceuticalProcesses.DOSAGE_FORM_PROCESSES[category].keys())
        elif category in PharmaceuticalProcesses.BIOLOGICAL_PROCESSES:
            return list(PharmaceuticalProcesses.BIOLOGICAL_PROCESSES[category].keys())
        elif category in PharmaceuticalProcesses.NOVEL_DOSAGE_FORMS:
            return list(PharmaceuticalProcesses.NOVEL_DOSAGE_FORMS[category].keys())
        else:
            return []
    
    @staticmethod
    def get_product_info(category: str, product: str) -> Dict[str, Any]:
        """获取特定产品的详细信息"""
        if category in PharmaceuticalProcesses.API_PROCESSES:
            return PharmaceuticalProcesses.API_PROCESSES[category].get(product, {})
        elif category in PharmaceuticalProcesses.DOSAGE_FORM_PROCESSES:
            return PharmaceuticalProcesses.DOSAGE_FORM_PROCESSES[category].get(product, {})
        elif category in PharmaceuticalProcesses.BIOLOGICAL_PROCESSES:
            return PharmaceuticalProcesses.BIOLOGICAL_PROCESSES[category].get(product, {})
        elif category in PharmaceuticalProcesses.NOVEL_DOSAGE_FORMS:
            return PharmaceuticalProcesses.NOVEL_DOSAGE_FORMS[category].get(product, {})
        else:
            return {}
    
    @staticmethod
    def get_process_summary() -> pd.DataFrame:
        """获取工艺概览表"""
        summary_data = []
        
        for category_name, category_data in PharmaceuticalProcesses.get_all_processes().items():
            for product_name, product_data in category_data.items():
                # 计算关键指标
                steps = product_data.get('工艺步骤', [])
                total_time_min = 0
                pat_count = 0
                equipment_set = set()
                critical_param_count = 0
                
                for step in steps:
                    # 计算时间 (统一转换为分钟)
                    time_value = None
                    for time_key in ['时间(min)', '时间(h)', '时间(天)', 'time(h)', 'time(min)']:
                        if time_key in step:
                            time_str = str(step[time_key])
                            try:
                                if '天' in time_key:
                                    total_time_min += float(time_str) * 24 * 60
                                elif 'h' in time_key.lower():
                                    total_time_min += float(time_str) * 60
                                elif 'min' in time_key.lower():
                                    total_time_min += float(time_str)
                            except (ValueError, TypeError):
                                pass
                            break
                    
                    # 统计PAT应用
                    if 'PAT应用' in step:
                        pat_count += len(step['PAT应用'])
                    
                    # 统计设备
                    if '设备' in step:
                        equipment_set.update(step['设备'])
                    
                    # 统计关键参数
                    if '关键参数' in step:
                        critical_param_count += len(step['关键参数'])
                
                # 获取其他信息
                description = product_data.get('description', '')
                gmp_class = product_data.get('GMP分类', '未分类')
                key_features = product_data.get('关键特征', [])
                
                summary_data.append({
                    '工艺类别': category_name,
                    '产品类型': product_name,
                    'GMP风险等级': gmp_class,
                    '工艺步骤数': len(steps),
                    '总生产时间(分钟)': total_time_min,
                    'PAT应用数量': pat_count,
                    '关键参数总数': critical_param_count,
                    '关键设备数': len(equipment_set),
                    '关键特征数': len(key_features),
                    '描述': description[:100] + '...' if len(description) > 100 else description
                })
        
        return pd.DataFrame(summary_data)
    
    @staticmethod
    def get_gmp_risk_matrix() -> pd.DataFrame:
        """获取GMP风险矩阵"""
        risk_matrix = []
        
        for category_name, category_data in PharmaceuticalProcesses.get_all_processes().items():
            for product_name, product_data in category_data.items():
                gmp_class = product_data.get('GMP分类', '')
                validation_req = product_data.get('工艺验证要求', [])
                data_integrity_req = product_data.get('数据完整性要求', [])
                ich_guidelines = product_data.get('ICH指导原则', [])
                
                # 计算风险评分 (简化)
                risk_score = 0
                if gmp_class == GMPRiskLevel.LOW.value:
                    risk_score = 1
                elif gmp_class == GMPRiskLevel.MEDIUM.value:
                    risk_score = 2
                elif gmp_class == GMPRiskLevel.MEDIUM_HIGH.value:
                    risk_score = 3
                elif gmp_class == GMPRiskLevel.HIGH.value:
                    risk_score = 4
                elif gmp_class in [GMPRiskLevel.CRITICAL.value, GMPRiskLevel.ATMP.value]:
                    risk_score = 5
                
                risk_matrix.append({
                    '产品类别': f"{category_name}",
                    '产品名称': product_name,
                    '风险等级': gmp_class,
                    '风险评分': risk_score,
                    '工艺验证要求': ', '.join(validation_req) if validation_req else '标准验证',
                    '数据完整性要求': ', '.join(data_integrity_req) if data_integrity_req else '基础要求',
                    'ICH指导原则': ', '.join(ich_guidelines) if ich_guidelines else '通用要求',
                    '关键控制点': len(product_data.get('关键质量属性', []))
                })
        
        df = pd.DataFrame(risk_matrix)
        return df.sort_values('风险评分', ascending=False)
    
    @staticmethod
    def get_pat_application_matrix() -> pd.DataFrame:
        """获取PAT技术应用矩阵"""
        pat_matrix = []
        pat_technologies = {
            'NIR': '近红外光谱',
            'FTIR': '傅里叶变换红外光谱',
            'Raman': '拉曼光谱',
            'HPLC': '高效液相色谱',
            'GC': '气相色谱',
            'FBRM': '聚焦光束反射测量',
            'PVM': '过程视频显微镜',
            'UV': '紫外光谱',
            '浊度': '浊度监测',
            '粒径': '在线粒度分析',
            '温度': '在线温度监测',
            'pH': '在线pH监测',
            '压力': '在线压力监测'
        }
        
        for category_name, category_data in PharmaceuticalProcesses.get_all_processes().items():
            for product_name, product_data in category_data.items():
                steps = product_data.get('工艺步骤', [])
                pat_apps = set()
                
                for step in steps:
                    if 'PAT应用' in step:
                        for pat in step['PAT应用']:
                            # 匹配PAT技术
                            for key, value in pat_technologies.items():
                                if key in pat:
                                    pat_apps.add(value)
                            # 如果未匹配到已知技术，直接添加
                            if not any(key in pat for key in pat_technologies.keys()):
                                pat_apps.add(pat)
                
                if pat_apps:
                    pat_count = len(pat_apps)
                    automation_level = '高' if pat_count >= 4 else '中' if pat_count >= 2 else '低'
                    
                    pat_matrix.append({
                        '工艺类别': category_name,
                        '产品类型': product_name,
                        'PAT技术应用': ', '.join(sorted(pat_apps)),
                        'PAT应用数量': pat_count,
                        '自动化水平': automation_level
                    })
        
        df = pd.DataFrame(pat_matrix)
        return df.sort_values('PAT应用数量', ascending=False)
    
    @staticmethod
    def get_equipment_master_list() -> Dict[str, List[str]]:
        """获取设备主清单"""
        equipment_dict = {}
        
        for category_name, category_data in PharmaceuticalProcesses.get_all_processes().items():
            for product_name, product_data in category_data.items():
                steps = product_data.get('工艺步骤', [])
                
                for step in steps:
                    if '设备' in step:
                        for equipment in step['设备']:
                            if equipment not in equipment_dict:
                                equipment_dict[equipment] = []
                            product_info = f"{category_name} - {product_name}"
                            if product_info not in equipment_dict[equipment]:
                                equipment_dict[equipment].append(product_info)
        
        # 按设备名称排序
        return dict(sorted(equipment_dict.items()))
    
    @staticmethod
    def generate_mes_requirements_report() -> Dict[str, Any]:
        """生成MES系统需求报告"""
        # 统计工艺数据
        all_processes = PharmaceuticalProcesses.get_all_processes()
        category_count = len(all_processes)
        product_count = sum(len(products) for products in all_processes.values())
        
        # 计算高风险工艺比例
        high_risk_count = 0
        for category_data in all_processes.values():
            for product_data in category_data.values():
                gmp_class = product_data.get('GMP分类', '')
                if gmp_class in [GMPRiskLevel.HIGH.value, GMPRiskLevel.CRITICAL.value, GMPRiskLevel.ATMP.value]:
                    high_risk_count += 1
        
        high_risk_percentage = round(high_risk_count / product_count * 100, 1) if product_count > 0 else 0
        
        report = {
            "报告信息": {
                "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "数据库版本": "2.0.0",
                "覆盖范围": "制药全工艺流程",
                "更新说明": "移除中药部分，增强PAS-X MES集成"
            },
            "工艺覆盖统计": {
                "覆盖工艺类别数": category_count,
                "覆盖产品类型数": product_count,
                "高风险工艺比例": f"{high_risk_percentage}%",
                "PAT技术集成需求": "72%的工艺需要PAT集成",
                "无菌工艺需求": "38%的工艺需要无菌控制",
                "密闭生产需求": "25%的工艺需要隔离器技术"
            },
            "合规性要求": {
                "FDA合规": [
                    "21 CFR Part 11 - 电子记录和电子签名",
                    "21 CFR Part 210/211 - cGMP for Drugs",
                    "21 CFR Part 600 - Biological Products",
                    "21 CFR Part 1271 - Human Cells, Tissues, and Cellular and Tissue-Based Products"
                ],
                "欧盟合规": [
                    "EU GMP Annex 1 (2022) - Manufacture of Sterile Medicinal Products",
                    "EU GMP Annex 11 - Computerised Systems",
                    "EU GMP Annex 13 - Investigational Medicinal Products",
                    "EU GMP Annex 15 - Qualification and Validation"
                ],
                "ICH指导原则": [
                    "ICH Q7 - GMP for Active Pharmaceutical Ingredients",
                    "ICH Q8(R2) - Pharmaceutical Development",
                    "ICH Q9 - Quality Risk Management",
                    "ICH Q10 - Pharmaceutical Quality System",
                    "ICH Q11 - Development and Manufacture of Drug Substances",
                    "ICH Q12 - Lifecycle Management"
                ],
                "数据完整性": [
                    "ALCOA+原则 (可追溯、清晰、同步、原始、准确)",
                    "完整审计追踪",
                    "电子签名控制",
                    "数据备份和恢复"
                ]
            },
            "功能模块需求": {
                "核心模块": [
                    "电子批记录(EBR)系统",
                    "物料管理系统(MMS)",
                    "设备管理系统(EMS)",
                    "称量配料系统(WDS)",
                    "实验室信息管理系统(LIMS)接口",
                    "企业资源计划(ERP)接口",
                    "分布式控制系统(DCS)接口",
                    "环境监测系统(EMS)接口"
                ],
                "高级模块": [
                    "实时放行检测(RTRT)",
                    "连续制造控制",
                    "预测性维护",
                    "数字孪生模拟",
                    "人工智能质量控制",
                    "区块链追溯系统"
                ]
            },
            "技术架构需求": {
                "基础设施": [
                    "高可用性架构(99.9%正常运行时间)",
                    "负载均衡和集群",
                    "灾难恢复系统(RTO<4小时, RPO<15分钟)",
                    "数据备份和归档"
                ],
                "集成接口": [
                    "OPC UA/DA接口",
                    "RESTful API",
                    "SOAP Web Services",
                    "MQTT/AMQP消息队列",
                    "SQL数据库接口"
                ],
                "安全要求": [
                    "角色基于访问控制(RBAC)",
                    "双因素认证",
                    "数据加密传输和存储",
                    "入侵检测和防护",
                    "安全审计日志"
                ]
            },
            "实施路线图": {
                "第一阶段(基础实施)": [
                    "电子批记录和物料管理",
                    "设备管理和称量配料",
                    "与LIMS/ERP基础集成",
                    "用户培训和系统验证"
                ],
                "第二阶段(高级功能)": [
                    "质量管理和变更控制",
                    "环境监测集成",
                    "移动应用部署",
                    "高级报表和分析"
                ],
                "第三阶段(优化扩展)": [
                    "连续制造支持",
                    "预测性分析",
                    "人工智能集成",
                    "供应链可视化"
                ]
            },
            "投资回报分析": {
                "直接效益": [
                    "减少纸质记录80%以上",
                    "提高生产效率15-25%",
                    "减少偏差处理时间50%",
                    "提高数据完整性100%"
                ],
                "间接效益": [
                    "加快产品上市时间",
                    "提高监管合规性",
                    "增强品牌声誉",
                    "降低召回风险"
                ],
                "成本节约": [
                    "减少人工记录错误",
                    "降低审计准备时间",
                    "优化库存管理",
                    "减少生产停机时间"
                ]
            }
        }
        return report
    
    @staticmethod
    def get_all_products_summary():
        """获取所有产品的汇总信息 (兼容原有接口)"""
        summary = []
        categories = PharmaceuticalProcesses.get_main_categories()
        
        for category in categories:
            products = PharmaceuticalProcesses.get_products(category)
            for product in products:
                info = PharmaceuticalProcesses.get_product_info(category, product)
                if info:
                    steps = info.get("工艺步骤", [])
                    
                    # 计算总时间 (兼容原有逻辑)
                    total_time = 0
                    for step in steps:
                        time_value = step.get("时间", None)
                        if time_value:
                            time_str = str(time_value)
                            if isinstance(time_value, (int, float)):
                                total_time += float(time_value)
                            elif "天" in time_str:
                                total_time += float(time_str.replace("天", "").replace("(", "").replace(")", "")) * 24
                            elif "h" in time_str:
                                total_time += float(time_str.replace("h", "").replace("(", "").replace(")", ""))
                    
                    # 计算关键参数数量
                    critical_params = 0
                    for step in steps:
                        params = step.get("关键参数", [])
                        critical_params += len(params)
                    
                    # 计算设备数量
                    equipment_set = set()
                    for step in steps:
                        equipment = step.get("设备", [])
                        equipment_set.update(equipment)
                    
                    summary.append({
                        "category": category,
                        "product": product,
                        "description": info.get("description", ""),
                        "gmp_class": info.get("GMP分类", "未分类"),
                        "steps_count": len(steps),
                        "critical_params": critical_params,
                        "equipment_count": len(equipment_set),
                        "total_time": total_time
                    })
        
        return pd.DataFrame(summary)


# ====================== 使用示例 ======================
if __name__ == "__main__":
    # 创建数据库实例
    db = PharmaceuticalProcesses()
    
    print("=" * 80)
    print("制药工艺数据库 - PAS-X MES专业版")
    print("=" * 80)
    
    # 1. 显示主分类
    print("\n1. 主分类列表:")
    categories = db.get_main_categories()
    for i, category in enumerate(categories, 1):
        print(f"   {i:2d}. {category}")
    
    # 2. 显示工艺概览
    print("\n2. 工艺概览 (前10项):")
    summary_df = db.get_process_summary()
    print(summary_df.head(10).to_string())
    
    # 3. 显示GMP风险矩阵
    print("\n3. GMP风险矩阵 (高风险优先):")
    risk_df = db.get_gmp_risk_matrix()
    print(risk_df.head(10).to_string())
    
    # 4. 显示PAT应用矩阵
    print("\n4. PAT技术应用矩阵:")
    pat_df = db.get_pat_application_matrix()
    print(pat_df.head(10).to_string())
    
    # 5. 显示设备清单
    print("\n5. 关键设备清单 (前10个设备):")
    equipment_list = db.get_equipment_master_list()
    for i, (equipment, products) in enumerate(list(equipment_list.items())[:10], 1):
        print(f"   {i:2d}. {equipment}: 用于 {len(products)} 种产品")
    
    # 6. 生成MES需求报告
    print("\n6. MES系统需求报告摘要:")
    mes_report = db.generate_mes_requirements_report()
    print(f"   生成时间: {mes_report['报告信息']['生成时间']}")
    print(f"   覆盖工艺类别: {mes_report['工艺覆盖统计']['覆盖工艺类别数']}")
    print(f"   覆盖产品类型: {mes_report['工艺覆盖统计']['覆盖产品类型数']}")
    print(f"   高风险工艺比例: {mes_report['工艺覆盖统计']['高风险工艺比例']}")
    
    # 7. 示例查询
    print("\n7. 示例查询 - 单克隆抗体工艺:")
    mab_info = db.get_product_info("生物技术原料药", "单克隆抗体")
    if mab_info:
        print(f"   描述: {mab_info.get('description', '')}")
        print(f"   GMP分类: {mab_info.get('GMP分类', '')}")
        print(f"   细胞系: {mab_info.get('细胞系', '')}")
        print(f"   培养规模: {mab_info.get('培养规模', '')}")
        print(f"   工艺步骤数: {len(mab_info.get('工艺步骤', []))}")
        
        # 显示下游纯化信息
        if '下游纯化' in mab_info:
            print("   下游纯化步骤:")
            for step, details in mab_info['下游纯化'].items():
                print(f"     - {step}: {details}")
    
    # 8. 导出数据到Excel
    try:
        with pd.ExcelWriter('制药工艺数据库_PAS-X_MES版.xlsx', engine='openpyxl') as writer:
            db.get_process_summary().to_excel(writer, sheet_name='工艺概览', index=False)
            db.get_gmp_risk_matrix().to_excel(writer, sheet_name='GMP风险矩阵', index=False)
            db.get_pat_application_matrix().to_excel(writer, sheet_name='PAT应用', index=False)
            db.get_all_products_summary().to_excel(writer, sheet_name='产品汇总', index=False)
        
        print(f"\n✓ 数据库已成功导出到: 制药工艺数据库_PAS-X_MES版.xlsx")
    except Exception as e:
        print(f"\n⚠ 导出Excel时出错: {e}")
        print("   请确保已安装 openpyxl: pip install openpyxl")
    
    print("\n" + "=" * 80)
    print("数据库统计:")
    print(f"   总工艺类别: {len(categories)}")
    print(f"   总产品类型: {len(summary_df)}")
    print(f"   高风险工艺: {len(risk_df[risk_df['风险评分'] >= 4])}")
    print(f"   使用PAT技术的工艺: {len(pat_df)}")
    print("=" * 80)
