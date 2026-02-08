# GopenKAG

基于《狂飙》剧本/小说文本构建的知识图谱应用，支持图谱抽取、存储 (Neo4j) 与问答 (GraphRAG)。

## 功能特性
- **数据抽取**: 基于 LLM 从非结构化文本中提取实体与关系 (cnSchema 标准扩展)。
- **图存储**: 自动导入 Neo4j 图数据库。
- **交互应用**: 提供 Streamlit 前端，支持图谱可视化与自然语言问答。
- **跨平台**: 支持 Windows 和 Linux。

## 快速开始

### 1. 环境准备
- Python 3.9+
- Neo4j Desktop 或 Docker 实例

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置
复制 `config/config.yaml` 并填入您的 API Key 和 Neo4j 密码。

### 4. 运行
```bash
streamlit run src/ui/app.py
```

## 目录结构
- `src/extract`: 信息抽取模块
- `src/store`: 图数据库交互模块
- `src/rag`: 检索增强生成模块
- `src/ui`: 前端界面
- `data`: 存放输入 TXT 和输出 CSV
