#!/usr/bin/env python3
"""
邮件高级功能测试脚本
"""
import asyncio
import requests
import json
import base64
from datetime import datetime
from pathlib import Path

# API配置
API_BASE_URL = "http://localhost:8000"
API_KEY = "noti_aL3rBP1SGm8yy4havWd0xK-nAZlBq5kgrIoI7SmOhy8"
API_SECRET = "secret_5vEh7qvot63UhMQ_qomUM8BfToW-hJ_q"


class EmailTester:
    """邮件功能测试类"""
    
    def __init__(self):
        self.token = None
        self.test_results = []
    
    def get_token(self):
        """获取访问令牌"""
        print("=" * 80)
        print("获取访问令牌...")
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/token",
            json={
                "api_key": API_KEY,
                "api_secret": API_SECRET
            }
        )
        
        if response.status_code == 200:
            self.token = response.json()["data"]["access_token"]
            print(f"✅ 成功获取Token: {self.token[:50]}...")
            return True
        else:
            print(f"❌ 获取Token失败: {response.text}")
            return False
    
    def send_email(self, test_name, payload):
        """发送邮件通用方法"""
        print("\n" + "=" * 80)
        print(f"测试: {test_name}")
        print("-" * 80)
        print(f"请求数据:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/v1/messages/email/send",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            result = {
                "test_name": test_name,
                "status_code": response.status_code,
                "success": response.status_code == 200
            }
            
            if response.status_code == 200:
                data = response.json()
                result["message_id"] = data["data"]["message_id"]
                print(f"✅ 发送成功!")
                print(f"   Message ID: {result['message_id']}")
                print(f"   Status: {data['data']['status']}")
            else:
                result["error"] = response.text
                print(f"❌ 发送失败!")
                print(f"   错误: {response.text}")
            
            self.test_results.append(result)
            return result["success"]
            
        except Exception as e:
            print(f"❌ 发送异常: {str(e)}")
            self.test_results.append({
                "test_name": test_name,
                "success": False,
                "error": str(e)
            })
            return False
    
    def test_multiple_recipients(self):
        """测试1: 多收件人发送"""
        payload = {
            "to": [
                "205672513@qq.com",
                "test@example.com",
                "demo@example.com"
            ],
            "template_code": "test_email",
            "template_variables": {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
        return self.send_email("多收件人发送", payload)
    
    def test_cc_bcc(self):
        """测试2: 抄送和密送"""
        payload = {
            "to": ["205672513@qq.com"],
            "cc": ["cc1@example.com", "cc2@example.com"],
            "bcc": ["bcc1@example.com"],
            "template_code": "test_email",
            "template_variables": {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
        return self.send_email("抄送(CC)和密送(BCC)", payload)
    
    def test_with_attachment(self):
        """测试3: 带附件发送"""
        # 创建一个测试文件
        test_content = "这是一个测试附件文件\nTest Attachment Content\n测试时间: " + datetime.now().isoformat()
        test_file_base64 = base64.b64encode(test_content.encode('utf-8')).decode('utf-8')
        
        payload = {
            "to": ["205672513@qq.com"],
            "subject": "【测试】带附件的邮件",
            "content": f"<html><body><h2>测试附件功能</h2><p>这封邮件包含一个测试附件。</p><p>发送时间: {datetime.now()}</p></body></html>",
            "content_type": "html",
            "attachments": [
                {
                    "filename": "test_attachment.txt",
                    "content": test_file_base64
                }
            ]
        }
        
        return self.send_email("带附件发送", payload)
    
    def test_html_template(self):
        """测试4: 复杂HTML模板"""
        html_content = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; }
                .footer { background-color: #f1f1f1; padding: 10px; text-align: center; font-size: 12px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #4CAF50; color: white; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>消息通知平台测试</h1>
            </div>
            <div class="content">
                <h2>测试信息</h2>
                <table>
                    <tr>
                        <th>项目</th>
                        <th>内容</th>
                    </tr>
                    <tr>
                        <td>测试时间</td>
                        <td>{timestamp}</td>
                    </tr>
                    <tr>
                        <td>测试类型</td>
                        <td>HTML模板测试</td>
                    </tr>
                    <tr>
                        <td>系统状态</td>
                        <td>✅ 运行正常</td>
                    </tr>
                </table>
                <p>这是一封测试复杂HTML格式的邮件。</p>
                <ul>
                    <li>支持HTML标签</li>
                    <li>支持CSS样式</li>
                    <li>支持表格和列表</li>
                    <li>支持中文显示</li>
                </ul>
            </div>
            <div class="footer">
                <p>© 2025 消息通知平台 | 这是一封自动生成的测试邮件</p>
            </div>
        </body>
        </html>
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        payload = {
            "to": ["205672513@qq.com"],
            "subject": "【测试】复杂HTML模板",
            "content": html_content,
            "content_type": "html"
        }
        
        return self.send_email("复杂HTML模板", payload)
    
    def print_summary(self):
        """打印测试总结"""
        print("\n" + "=" * 80)
        print("测试总结")
        print("=" * 80)
        
        total = len(self.test_results)
        success = sum(1 for r in self.test_results if r.get("success", False))
        failed = total - success
        
        print(f"\n总计: {total} 个测试")
        print(f"成功: {success} ✅")
        print(f"失败: {failed} ❌")
        print(f"成功率: {success/total*100:.1f}%")
        
        print("\n详细结果:")
        print("-" * 80)
        for i, result in enumerate(self.test_results, 1):
            status = "✅" if result.get("success") else "❌"
            print(f"{i}. {status} {result['test_name']}")
            if result.get("message_id"):
                print(f"   Message ID: {result['message_id']}")
            if result.get("error"):
                print(f"   错误: {result['error']}")
        
        print("\n" + "=" * 80)
        print("测试完成!")
        print("=" * 80)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("邮件高级功能测试")
        print("=" * 80)
        print(f"开始时间: {datetime.now()}")
        
        # 获取Token
        if not self.get_token():
            print("❌ 无法获取Token，测试终止")
            return
        
        # 等待一下
        import time
        time.sleep(2)
        
        # 执行测试
        tests = [
            self.test_multiple_recipients,
            self.test_cc_bcc,
            self.test_with_attachment,
            self.test_html_template,
        ]
        
        for test in tests:
            try:
                test()
                time.sleep(3)  # 每个测试之间等待3秒
            except Exception as e:
                print(f"❌ 测试异常: {str(e)}")
        
        # 打印总结
        self.print_summary()


if __name__ == "__main__":
    tester = EmailTester()
    tester.run_all_tests()

