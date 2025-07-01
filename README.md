# 🎯 SCYS-Spider | 生财有术风向标爬虫

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![GitHub Actions](https://img.shields.io/github/actions/workflow/status/jiangxiong180/scys-spider/spider.yml)

**🤖 智能抓取生财有术风向标信息，自动推送到微信**

*把握最新商机，不错过任何中标机会！*

[🚀 快速开始](#-快速开始) • [📖 使用文档](#-使用文档) • [🔧 配置说明](#-配置说明) • [📱 效果展示](#-效果展示)

</div>

---

## 📋 项目简介

SCYS-Spider 是一个专为生财有术社群打造的智能风向标爬虫工具。它能够：

- 🕷️ **自动抓取** 生财有术风向标的最新中标信息
- - 📱 **智能推送** 通过Server酱将信息推送到微信
  - - 🔄 **去重处理** 基于SQLite数据库，避免重复推送
    - - ⏰ **定时运行** 每天1点和10点自动执行
      - - 📊 **美观展示** Markdown格式，信息清晰易读
       
        - ## ✨ 核心功能
       
        - ### 🎯 智能爬取
        - - 抓取生财有术风向标页面的最新中标信息
          - - 解析帖子标题、作者、内容、分类等关键信息
            - - 自动识别新增内容，避免重复处理
             
              - ### 📱 微信推送
              - - 通过Server酱API推送到微信
                - - 支持Markdown格式，展示美观
                  - - 消息包含标题、作者、内容摘要等完整信息
                    - - 一键直达原文链接
                     
                      - ### 🛡️ 智能去重
                      - - SQLite数据库存储已推送内容的哈希值
                        - - MD5算法确保内容唯一性
                          - - 防止同一内容多次推送
                           
                            - ### ⚡ 自动化运行
                            - - GitHub Actions定时调度
                              - - 每天1点、10点自动运行
                                - - 支持手动触发执行
                                  - - 完整的日志记录和错误处理
                                   
                                    - ## 🚀 快速开始
                                   
                                    - ### 1️⃣ Fork项目
                                    - 点击右上角的 `Fork` 按钮，将项目复制到你的GitHub账户
                                   
                                    - ### 2️⃣ 获取Server酱SendKey
                                    - 1. 访问 [Server酱官网](https://sct.ftqq.com/)
                                      2. 2. 使用微信扫码登录
                                         3. 3. 复制你的SendKey
                                           
                                            4. ### 3️⃣ 配置GitHub Secrets
                                            5. 1. 进入你Fork的仓库
                                               2. 2. 点击 `Settings` → `Secrets and variables` → `Actions`
                                                  3. 3. 点击 `New repository secret`
                                                     4. 4. 添加以下配置：
                                                        5.    - **Name**: `SERVER_CHAN_KEY`
                                                              -    - **Value**: 你的Server酱SendKey
                                                               
                                                                   - ### 4️⃣ 启用GitHub Actions
                                                                   - 1. 点击 `Actions` 标签页
                                                                     2. 2. 点击 `I understand my workflows, go ahead and enable them`
                                                                        3. 3. 选择 `SCYS Spider ServerChan` 工作流
                                                                           4. 4. 点击 `Enable workflow`
                                                                             
                                                                              5. ### 5️⃣ 测试运行
                                                                              6. 1. 在Actions页面点击 `Run workflow`
                                                                                 2. 2. 选择 `main` 分支，点击 `Run workflow`
                                                                                    3. 3. 等待执行完成，检查微信是否收到推送
                                                                                      
                                                                                       4. ## 🔧 配置说明
                                                                                      
                                                                                       5. ### 环境变量
                                                                                       6. | 变量名 | 必填 | 说明 | 示例 |
                                                                                       7. |--------|------|------|------|
                                                                                       8. | `SERVER_CHAN_KEY` | ✅ | Server酱的SendKey | `SCT123456...` |
                                                                                      
                                                                                       9. ### 定时设置
                                                                                       10. 默认运行时间（UTC时区）：
                                                                                       11. - 🌅 **每天 01:00** (北京时间 09:00)
                                                                                           - - 🌞 **每天 10:00** (北京时间 18:00)
                                                                                            
                                                                                             - 如需修改时间，编辑 `.github/workflows/spider.yml` 文件中的 cron 表达式。
                                                                                            
                                                                                             - ### 推送格式
                                                                                             - 推送消息采用Markdown格式，包含：
                                                                                             - - 📊 推送时间和条数统计
                                                                                               - - 📈 每条信息的标题、作者、分类
                                                                                                 - - 📝 内容摘要（限制200字符）
                                                                                                   - - 🔗 原文链接和相关标签
                                                                                                    
                                                                                                     - ## 📱 效果展示
                                                                                                    
                                                                                                     - ### 微信推送效果
                                                                                                     - ```
                                                                                                       🎯 生财有术-风向标中标信息

                                                                                                       ⏰ 推送时间: 2025-01-02 18:00
                                                                                                       📊 本次推送: 3 条信息

                                                                                                       ### 📈 1. 简历模板项目月入190万，如何复制？
                                                                                                       🏷️ 分类: 案例分析
                                                                                                       👤 作者: 小明同学
                                                                                                       ⏰ 时间: 2小时前
                                                                                                       📝 内容: 分享一个朋友通过制作和销售简历模板...
                                                                                                       🏷️ 标签: #中标 #风向标 #生财有术

                                                                                                       [查看原文](https://scys.com/opportunity)
                                                                                                       ```
                                                                                                       
                                                                                                       ## 🛠️ 本地开发
                                                                                                       
                                                                                                       ### 环境要求
                                                                                                       - Python 3.9+
                                                                                                       - - pip
                                                                                                        
                                                                                                         - ### 安装依赖
                                                                                                         - ```bash
                                                                                                           git clone https://github.com/你的用户名/scys-spider.git
                                                                                                           cd scys-spider
                                                                                                           pip install -r requirements.txt
                                                                                                           ```
                                                                                                           
                                                                                                           ### 环境配置
                                                                                                           ```bash
                                                                                                           # 设置环境变量
                                                                                                           export SERVER_CHAN_KEY="你的SendKey"

                                                                                                           # 运行程序
                                                                                                           python spider.py
                                                                                                           ```
                                                                                                           
                                                                                                           ## 📊 项目结构
                                                                                                           
                                                                                                           ```
                                                                                                           scys-spider/
                                                                                                           ├── 📄 spider.py              # 主程序
                                                                                                           ├── 📄 requirements.txt       # 依赖包
                                                                                                           ├── 📄 README.md              # 项目说明
                                                                                                           ├── 📁 .github/
                                                                                                           │   └── 📁 workflows/
                                                                                                           │       └── 📄 spider.yml      # GitHub Actions配置
                                                                                                           ├── 📄 spider.log             # 运行日志（生成）
                                                                                                           └── 📄 sent_posts.db          # 数据库文件（生成）
                                                                                                           ```
                                                                                                           
                                                                                                           ## 🤝 贡献指南
                                                                                                           
                                                                                                           欢迎提交 Issue 和 Pull Request！
                                                                                                           
                                                                                                           1. Fork 本仓库
                                                                                                           2. 2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
                                                                                                              3. 3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
                                                                                                                 4. 4. 推送到分支 (`git push origin feature/AmazingFeature`)
                                                                                                                    5. 5. 打开一个 Pull Request
                                                                                                                      
                                                                                                                       6. ## 📝 更新日志
                                                                                                                      
                                                                                                                       7. ### v2.0.0 (2025-01-02)
                                                                                                                       8. - ✅ 完善README文档和使用说明
                                                                                                                          - - ✅ 优化推送消息格式
                                                                                                                            - - ✅ 增加定时调度功能
                                                                                                                              - - ✅ 完善错误处理和日志记录
                                                                                                                               
                                                                                                                                - ### v1.0.0 (2025-01-01)
                                                                                                                                - - ✅ 基础爬虫功能实现
                                                                                                                                  - - ✅ Server酱微信推送
                                                                                                                                    - - ✅ SQLite数据库去重
                                                                                                                                      - - ✅ GitHub Actions自动化
                                                                                                                                       
                                                                                                                                        - ## ⚠️ 免责声明
                                                                                                                                       
                                                                                                                                        - 本项目仅用于学习和技术交流，请遵守相关网站的使用条款和robots.txt规定。使用本项目产生的任何法律后果，与项目作者无关。
                                                                                                                                       
                                                                                                                                        - ## 📄 开源协议
                                                                                                                                       
                                                                                                                                        - 本项目基于 [MIT License](LICENSE) 开源协议。
                                                                                                                                       
                                                                                                                                        - ## 💖 支持项目
                                                                                                                                       
                                                                                                                                        - 如果这个项目对你有帮助，请：
                                                                                                                                        - - ⭐ 给项目一个Star
                                                                                                                                          - - 🔀 Fork项目并贡献代码
                                                                                                                                            - - 📢 推荐给更多朋友
                                                                                                                                             
                                                                                                                                              - ---
                                                                                                                                              
                                                                                                                                              <div align="center">
                                                                                                                                              
                                                                                                                                              **🤖 Made with ❤️ by [jiangxiong180](https://github.com/jiangxiong180)**
                                                                                                                                              
                                                                                                                                              *把握商机，从这里开始！*
                                                                                                                                              
                                                                                                                                              </div>
