"""
数据模型定义
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class EvidenceLevel(str, Enum):
    """循证医学证据等级"""
    LEVEL_1_META = "Level 1 - Meta分析"
    LEVEL_1_RCT = "Level 1 - 随机对照试验"
    LEVEL_2_COHORT = "Level 2 - 队列研究"
    LEVEL_2_CASE_CONTROL = "Level 2 - 病例对照研究"
    LEVEL_3_CASE_SERIES = "Level 3 - 病例系列"
    LEVEL_4_EXPERT = "Level 4 - 专家意见"
    LEVEL_5_ANECDOTAL = "Level 5 - 个案报道"


class QueryRequest(BaseModel):
    """检索请求模型"""
    query: str = Field(..., description="检索查询内容（支持中文/英文）", min_length=2, max_length=500)
    evidence_levels: List[EvidenceLevel] = Field(default=[], description="筛选的证据等级（为空表示全部）")
    max_results: int = Field(default=10, ge=1, le=50, description="最大返回结果数")
    year_from: Optional[int] = Field(default=None, ge=1900, le=2030, description="起始年份")
    year_to: Optional[int] = Field(default=None, ge=1900, le=2030, description="截止年份")
    generate_summary: bool = Field(default=True, description="是否生成智能摘要")
    include_abstract: bool = Field(default=True, description="是否包含摘要")


class AuthorInfo(BaseModel):
    """作者信息"""
    name: str
    affiliation: Optional[str] = None


class EvidenceInfo(BaseModel):
    """证据信息"""
    level: EvidenceLevel
    study_type: Optional[str] = None  # 研究类型（如RCT、队列研究等）
    sample_size: Optional[str] = None  # 样本量
    follow_up: Optional[str] = None  # 随访时间
    quality_score: Optional[float] = None  # 质量评分（0-10）


class LiteratureResult(BaseModel):
    """单篇文献结果"""
    pmid: str
    title: str
    title_zh: Optional[str] = None
    authors: List[AuthorInfo] = []
    journal: str
    year: int
    doi: Optional[str] = None
    abstract: Optional[str] = None
    abstract_zh: Optional[str] = None
    keywords: List[str] = []
    evidence_info: EvidenceInfo
    clinical_significance: Optional[str] = None  # 临床意义摘要
    citation_count: Optional[int] = None
    relevance_score: float = Field(default=0.0, ge=0, le=1)
    full_text_url: Optional[str] = None


class SearchResponse(BaseModel):
    """检索响应模型"""
    query: str
    original_query: str
    results_count: int
    evidence_distribution: Dict[str, int] = Field(default={}, description="证据等级分布统计")
    results: List[LiteratureResult]
    summary: Optional[str] = None  # 整体摘要
    clinical_takeaway: Optional[str] = None  # 临床要点
    search_time_ms: int
    cached: bool = False


class CitationFormat(str, Enum):
    """引用格式"""
    APA = "apa"
    VANCOUVER = "vancouver"
    GB_T_7714 = "gb_t_7714"
    MLA = "mla"


class CitationRequest(BaseModel):
    """引用导出请求"""
    pmids: List[str]
    format: CitationFormat = Field(default=CitationFormat.GB_T_7714)


class CitationResponse(BaseModel):
    """引用导出响应"""
    citations: List[str]
    format: CitationFormat


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    version: str
    timestamp: str
    services: Dict[str, bool]  # 各服务状态


class ErrorResponse(BaseModel):
    """错误响应"""
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
