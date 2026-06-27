"""
引用格式生成工具
支持APA、Vancouver、GB/T 7714、MLA格式
"""
from typing import List
from ..models.schemas import LiteratureResult, CitationFormat


def format_citation(literature: LiteratureResult, format_type: CitationFormat) -> str:
    """
    格式化单篇文献引用
    
    Args:
        literature: 文献数据
        format_type: 引用格式
        
    Returns:
        格式化后的引用字符串
    """
    authors = literature.authors
    year = literature.year
    title = literature.title
    journal = literature.journal
    doi = literature.doi
    
    if format_type == CitationFormat.GB_T_7714:
        # GB/T 7714-2015 格式
        author_str = format_authors_gb(authors)
        citation = f"{author_str}. {title}[J]. {journal}, {year}"
        if doi:
            citation += f". DOI: {doi}"
        return citation
    
    elif format_type == CitationFormat.APA:
        # APA 7th 格式
        author_str = format_authors_apa(authors)
        citation = f"{author_str} ({year}). {title}. {journal}"
        if doi:
            citation += f". https://doi.org/{doi}"
        return citation
    
    elif format_type == CitationFormat.VANCOUVER:
        # Vancouver格式
        author_str = format_authors_vancouver(authors)
        citation = f"{author_str}. {title}. {journal}. {year}"
        if doi:
            citation += f";{doi}"
        return citation
    
    elif format_type == CitationFormat.MLA:
        # MLA 9th 格式
        author_str = format_authors_mla(authors)
        citation = f'"{title}." {journal}, {year}'
        return citation
    
    else:
        return f"{title} - {journal} ({year})"


def format_authors_gb(authors) -> str:
    """GB/T 7714作者格式：张三, 李四, 王五"""
    if not authors:
        return "佚名"
    
    names = []
    for author in authors[:3]:  # 最多3个作者
        name = author.name
        # 尝试转换姓名为 姓 名 格式
        parts = name.split()
        if len(parts) >= 2:
            names.append(parts[-1] + " " + "".join(parts[:-1]))
        else:
            names.append(name)
    
    if len(authors) > 3:
        names.append("等")
    
    return ", ".join(names)


def format_authors_apa(authors) -> str:
    """APA作者格式：Zhang, S., Li, M., & Wang, X."""
    if not authors:
        return "Anonymous"
    
    if len(authors) == 1:
        return authors[0].name
    elif len(authors) == 2:
        return f"{authors[0].name} & {authors[1].name}"
    elif len(authors) <= 20:
        return ", ".join([a.name for a in authors[:-1]]) + f", & {authors[-1].name}"
    else:
        # 超过20个作者，取前19个+et al.
        return ", ".join([a.name for a in authors[:19]]) + ", . . . " + authors[-1].name


def format_authors_vancouver(authors) -> str:
    """Vancouver作者格式：Zhang S, Li M, Wang X"""
    if not authors:
        return "Anonymous"
    
    names = [a.name for a in authors[:6]]  # 最多6个
    if len(authors) > 6:
        names.append("et al.")
    
    return ", ".join(names)


def format_authors_mla(authors) -> str:
    """MLA作者格式：Zhang, San, et al."""
    if not authors:
        return "Anonymous"
    
    if len(authors) == 1:
        return authors[0].name
    elif len(authors) == 2:
        return f"{authors[0].name}, and {authors[1].name}"
    else:
        return f"{authors[0].name}, et al."
