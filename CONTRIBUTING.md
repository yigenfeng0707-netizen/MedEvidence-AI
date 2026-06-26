# 贡献指南

感谢您对MedEvidence AI项目的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告问题

1. 在提交Issue前，请先搜索是否已有相关问题
2. 使用Issue模板提交Bug报告或功能建议
3. 提供详细的复现步骤和环境信息

### 提交代码

1. Fork本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范

- 遵循PEP 8 Python编码规范
- 使用类型注解
- 编写单元测试
- 确保测试通过
- 更新相关文档

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/your-username/MedEvidence-AI.git
cd MedEvidence-AI

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 运行测试
pytest
```

### 提交信息规范

- `feat:` 新功能
- `fix:` 修复Bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具相关

### 医疗合规要求

- **禁止**: 使用真实患者数据
- **禁止**: 做出诊断承诺
- **必须**: 明确声明工具局限性
- **必须**: 遵守HIPAA等医疗隐私法规

## 许可证

通过提交代码，您同意您的贡献将在Apache License 2.0下发布。
