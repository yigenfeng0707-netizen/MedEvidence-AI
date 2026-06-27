"""
检索服务测试
"""
import pytest
import asyncio
from src.models.schemas import QueryRequest, EvidenceLevel
from src.services.search_service import SearchService


@pytest.fixture
async def search_service():
    """测试用的检索服务"""
    service = SearchService()
    try:
        await service.initialize()
        yield service
    finally:
        await service.close()


@pytest.mark.asyncio
async def test_simple_search():
    """测试简单检索"""
    service = SearchService()
    await service.initialize()
    
    request = QueryRequest(
        query="diabetes treatment",
        max_results=3,
        generate_summary=False  # 测试时关闭摘要生成，节省API调用
    )
    
    result = await service.search(request)
    
    assert result.results_count >= 0
    assert result.query == "diabetes treatment"
    assert isinstance(result.evidence_distribution, dict)
    
    await service.close()


@pytest.mark.asyncio
async def test_evidence_filter():
    """测试证据等级筛选"""
    service = SearchService()
    await service.initialize()
    
    request = QueryRequest(
        query="COVID-19 vaccine safety",
        max_results=5,
        evidence_levels=[EvidenceLevel.LEVEL_1_RCT],
        generate_summary=False
    )
    
    result = await service.search(request)
    
    # 验证返回的文献证据等级符合要求
    for lit in result.results:
        assert "Level 1" in lit.evidence_info.level.value
    
    await service.close()


@pytest.mark.asyncio
async def test_year_filter():
    """测试年份筛选"""
    service = SearchService()
    await service.initialize()
    
    request = QueryRequest(
        query="artificial intelligence medicine",
        max_results=3,
        year_from=2020,
        year_to=2025,
        generate_summary=False
    )
    
    result = await service.search(request)
    
    # 验证返回的文献年份在范围内
    for lit in result.results:
        assert 2020 <= lit.year <= 2025
    
    await service.close()


def test_query_validation():
    """测试查询验证"""
    # 有效查询
    request = QueryRequest(query="diabetes", max_results=10)
    assert request.query == "diabetes"
    
    # 空查询应该抛出验证错误
    with pytest.raises(ValueError):
        QueryRequest(query="", max_results=10)


if __name__ == "__main__":
    # 运行简单测试
    async def run_tests():
        print("测试简单检索...")
        await test_simple_search()
        print("✅ 简单检索测试通过")
    
    asyncio.run(run_tests())
