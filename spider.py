#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生财有术风向标爬虫 - Server酱版本
抓取生财有术网站的风向标中标信息，并通过Server酱推送到微信
"""

import requests
import time
import sqlite3
import hashlib
import json
from datetime import datetime
import os
import sys
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('spider.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class SCYSSpider:
    def __init__(self):
        """初始化爬虫"""
        # Server酱配置 - 从环境变量获取
        self.server_chan_key = os.getenv('SERVER_CHAN_KEY', '')
        if not self.server_chan_key:
            logger.error("❌ 未配置Server酱SendKey，请设置环境变量 SERVER_CHAN_KEY")
            sys.exit(1)
        
        # 数据库配置
        self.db_file = 'sent_posts.db'
        self.init_database()
        
        # 请求头配置
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        logger.info("🚀 生财有术爬虫初始化完成")

    def init_database(self):
        """初始化数据库"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sent_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_hash TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    author TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
            logger.info("✅ 数据库初始化完成")
        except Exception as e:
            logger.error(f"❌ 数据库初始化失败: {str(e)}")
            sys.exit(1)

    def get_post_hash(self, title, author, content):
        """生成帖子的唯一哈希值"""
        content_str = f"{title}_{author}_{content}"
        return hashlib.md5(content_str.encode('utf-8')).hexdigest()

    def is_post_sent(self, post_hash):
        """检查帖子是否已经发送过"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM sent_posts WHERE post_hash = ?', (post_hash,))
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except Exception as e:
            logger.error(f"❌ 检查帖子状态失败: {str(e)}")
            return False

    def mark_post_sent(self, post_hash, title, author, content):
        """标记帖子为已发送"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO sent_posts (post_hash, title, author, content)
                VALUES (?, ?, ?, ?)
            ''', (post_hash, title, author, content))
            conn.commit()
            conn.close()
            logger.info(f"✅ 标记帖子已发送: {title}")
        except Exception as e:
            logger.error(f"❌ 标记帖子失败: {str(e)}")

    def send_server_chan_message(self, title, content):
        """
        通过Server酱发送消息到微信
        
        Args:
            title (str): 消息标题（最大32个字符）
            content (str): 消息内容（支持Markdown，最大32KB）
        
        Returns:
            bool: 发送是否成功
        """
        try:
            # 构建API URL
            api_url = f"https://sctapi.ftqq.com/{self.server_chan_key}.send"
            
            # 准备数据
            data = {
                'title': title[:32],  # 限制标题长度
                'desp': content,      # 内容支持Markdown
                'channel': '9'        # 指定方糖服务号通道
            }
            
            # 发送POST请求
            response = requests.post(api_url, data=data, timeout=10)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            if result.get('code') == 0:
                logger.info(f"✅ Server酱推送成功: {title}")
                logger.info(f"📊 推送ID: {result.get('data', {}).get('pushid', 'N/A')}")
                return True
            else:
                logger.error(f"❌ Server酱推送失败: {result.get('message', '未知错误')}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Server酱推送网络错误: {str(e)}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"❌ Server酱响应解析错误: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ Server酱推送异常: {str(e)}")
            return False

    def format_message(self, posts):
        """
        格式化消息内容（Markdown格式）
        
        Args:
            posts (list): 帖子列表
            
        Returns:
            tuple: (标题, 内容)
        """
        if not posts:
            return None, None
        
        # 消息标题
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        title = f"🎯 生财有术-风向标中标信息"
        
        # 消息内容（Markdown格式）
        content = f"""## 🎯 生财有术-风向标中标信息

⏰ **推送时间**: {current_time}  
📊 **本次推送**: {len(posts)} 条信息

---

"""
        
        # 添加每个帖子的信息
        for i, post in enumerate(posts, 1):
            title_text = post.get('title', '无标题')
            author = post.get('author', '未知作者')
            content_text = post.get('content', '无内容')
            category = post.get('category', '未分类')
            time_ago = post.get('time', '时间未知')
            
            # 限制内容长度，避免消息过长
            if len(content_text) > 200:
                content_text = content_text[:200] + "..."
            
            content += f"""### 📈 {i}. {title_text}

🏷️ **分类**: {category}  
👤 **作者**: {author}  
⏰ **时间**: {time_ago}  
📝 **内容**: {content_text}

🏷️ **标签**: #中标 #风向标 #生财有术  
🔗 [查看原文](https://scys.com/opportunity)

---

"""
        
        # 添加底部信息
        content += """
> 💡 **温馨提示**: 这是自动推送的生财有术风向标中标信息，助你把握最新商机！

🤖 **技术支持**: 小牛马爬虫 v2.0  
📱 **推送服务**: Server酱  
⭐ **源码地址**: [GitHub](https://github.com/your-repo)
"""
        
        return title, content

    def get_demo_posts(self):
        """
        获取演示数据（高质量模拟数据）
        在实际部署时，这里应该替换为真实的网页抓取逻辑
        """
        logger.info("🎭 使用演示数据模式")
        
        demo_posts = [
            {
                'title': '简历模板项目月入190万，如何复制这个成功案例？',
                'author': '小明同学',
                'content': '分享一个朋友通过制作和销售简历模板实现月入190万的案例。他从零开始，通过精准定位、优质设计、多渠道推广，建立了简历模板帝国。核心策略包括：1）研究热门行业需求 2）打造差异化模板 3）建立品牌影响力 4）构建销售漏斗。项目启动成本低，适合个人或小团队操作。',
                'category': '案例分析',
                'time': '2小时前'
            },
            {
                'title': 'AI付费短剧新玩法，普通人也能月入过万',
                'author': '创业老王',
                'content': '最近发现一个AI短剧的新变现模式，通过AI生成剧本+真人出镜的方式制作付费短剧。单集制作成本200元，售价19.9元，转化率达到15%。关键在于选题、剧本质量和用户画像精准度。已有学员通过此方法实现月收入3-8万元。',
                'category': '项目分享',
                'time': '5小时前'
            },
            {
                'title': '声卡调试服务，一个被忽视的蓝海赛道',
                'author': '声音大师',
                'content': '随着直播和网课兴起，声卡调试需求暴增。我通过提供远程声卡调试服务，单次收费50-200元，月入稳定2万+。服务包括声卡安装、参数调试、音效配置等。客户主要是主播、老师、自媒体人。技术门槛不高，但需要耐心和专业度。',
                'category': '技能变现',
                'time': '1天前'
            }
        ]
        
        return demo_posts

    def crawl_posts(self):
        """
        抓取生财有术风向标页面
        目前使用演示数据，实际部署时需要实现真实抓取逻辑
        """
        try:
            logger.info("🕷️ 开始抓取生财有术风向标...")
            
            # 这里应该是真实的网页抓取逻辑
            # 由于目标网站使用JavaScript动
