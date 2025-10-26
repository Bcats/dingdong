# API调用示例

**版本**: 1.0  
**更新时间**: 2025-10-25

本文档提供多种编程语言的API调用示例。

---

## 📋 目录

1. [Python示例](#python示例)
2. [JavaScript/Node.js示例](#javascriptnodejs示例)
3. [Java示例](#java示例)
4. [PHP示例](#php示例)
5. [Go示例](#go示例)
6. [cURL示例](#curl示例)

---

## 🐍 Python示例

### 基础邮件发送

```python
import requests
from typing import Dict, Any

class DingDongClient:
    """消息通知平台客户端"""
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "http://localhost:8000"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.token = None
    
    def get_token(self) -> str:
        """获取访问令牌"""
        response = requests.post(
            f"{self.base_url}/api/v1/auth/token",
            json={
                "api_key": self.api_key,
                "api_secret": self.api_secret
            }
        )
        response.raise_for_status()
        self.token = response.json()["data"]["access_token"]
        return self.token
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        if not self.token:
            self.get_token()
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def send_email(
        self,
        to: list,
        subject: str = None,
        content: str = None,
        template_code: str = None,
        template_variables: dict = None,
        cc: list = None,
        bcc: list = None,
        content_type: str = "plain",
        attachments: list = None
    ) -> Dict[str, Any]:
        """
        发送邮件
        
        Args:
            to: 收件人列表
            subject: 邮件主题（使用模板时可选）
            content: 邮件内容（使用模板时可选）
            template_code: 模板编码
            template_variables: 模板变量
            cc: 抄送列表
            bcc: 密送列表
            content_type: 内容类型 (plain/html)
            attachments: 附件列表
        
        Returns:
            API响应数据
        """
        payload = {"to": to}
        
        if template_code:
            payload["template_code"] = template_code
            if template_variables:
                payload["template_variables"] = template_variables
        else:
            payload["subject"] = subject
            payload["content"] = content
            payload["content_type"] = content_type
        
        if cc:
            payload["cc"] = cc
        if bcc:
            payload["bcc"] = bcc
        if attachments:
            payload["attachments"] = attachments
        
        response = requests.post(
            f"{self.base_url}/api/v1/messages/email/send",
            headers=self._get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_message_status(self, message_id: int) -> Dict[str, Any]:
        """查询消息状态"""
        response = requests.get(
            f"{self.base_url}/api/v1/messages/{message_id}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()


# 使用示例
if __name__ == "__main__":
    # 初始化客户端
    client = DingDongClient(
        api_key="noti_aL3rBP1SGm8yy4havWd0xK-nAZlBq5kgrIoI7SmOhy8",
        api_secret="secret_5vEh7qvot63UhMQ_qomUM8BfToW-hJ_q"
    )
    
    # 示例1: 发送简单邮件
    result = client.send_email(
        to=["user@example.com"],
        subject="测试邮件",
        content="这是一封测试邮件"
    )
    print(f"Message ID: {result['data']['message_id']}")
    
    # 示例2: 使用模板发送
    result = client.send_email(
        to=["user@example.com"],
        template_code="test_email",
        template_variables={
            "username": "张三",
            "timestamp": "2025-10-25"
        }
    )
    
    # 示例3: 发送HTML邮件
    html_content = """
    <html>
    <body>
        <h1>欢迎！</h1>
        <p>感谢您的注册。</p>
    </body>
    </html>
    """
    result = client.send_email(
        to=["user@example.com"],
        subject="欢迎注册",
        content=html_content,
        content_type="html"
    )
    
    # 示例4: 带附件
    import base64
    with open("document.pdf", "rb") as f:
        file_content = base64.b64encode(f.read()).decode()
    
    result = client.send_email(
        to=["user@example.com"],
        subject="报告文档",
        content="请查收附件",
        attachments=[
            {
                "filename": "document.pdf",
                "content": file_content
            }
        ]
    )
    
    # 查询状态
    message_id = result['data']['message_id']
    status = client.get_message_status(message_id)
    print(f"Status: {status['data']['status']}")
```

---

## 🟨 JavaScript/Node.js示例

### 使用axios

```javascript
const axios = require('axios');

class DingDongClient {
    constructor(apiKey, apiSecret, baseUrl = 'http://localhost:8000') {
        this.apiKey = apiKey;
        this.apiSecret = apiSecret;
        this.baseUrl = baseUrl;
        this.token = null;
    }
    
    async getToken() {
        const response = await axios.post(`${this.baseUrl}/api/v1/auth/token`, {
            api_key: this.apiKey,
            api_secret: this.apiSecret
        });
        this.token = response.data.data.access_token;
        return this.token;
    }
    
    async sendEmail(options) {
        if (!this.token) {
            await this.getToken();
        }
        
        const payload = {
            to: options.to,
            ...options
        };
        
        const response = await axios.post(
            `${this.baseUrl}/api/v1/messages/email/send`,
            payload,
            {
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        
        return response.data;
    }
}

// 使用示例
(async () => {
    const client = new DingDongClient(
        'noti_aL3rBP1SGm8yy4havWd0xK-nAZlBq5kgrIoI7SmOhy8',
        'secret_5vEh7qvot63UhMQ_qomUM8BfToW-hJ_q'
    );
    
    // 发送邮件
    const result = await client.sendEmail({
        to: ['user@example.com'],
        subject: '测试邮件',
        content: '这是一封测试邮件',
        content_type: 'plain'
    });
    
    console.log('Message ID:', result.data.message_id);
})();
```

### 使用fetch (浏览器/Node.js 18+)

```javascript
async function sendEmail(to, subject, content) {
    // 1. 获取Token
    const tokenResponse = await fetch('http://localhost:8000/api/v1/auth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            api_key: 'noti_aL3rBP1SGm8yy4havWd0xK-nAZlBq5kgrIoI7SmOhy8',
            api_secret: 'secret_5vEh7qvot63UhMQ_qomUM8BfToW-hJ_q'
        })
    });
    const { data: { access_token } } = await tokenResponse.json();
    
    // 2. 发送邮件
    const emailResponse = await fetch('http://localhost:8000/api/v1/messages/email/send', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            to: [to],
            subject: subject,
            content: content
        })
    });
    
    return await emailResponse.json();
}

// 使用
sendEmail('user@example.com', '测试', '内容')
    .then(result => console.log('Success:', result))
    .catch(error => console.error('Error:', error));
```

---

## ☕ Java示例

### 使用OkHttp

```java
import okhttp3.*;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class DingDongClient {
    private final String apiKey;
    private final String apiSecret;
    private final String baseUrl;
    private String token;
    
    private final OkHttpClient client = new OkHttpClient();
    private final Gson gson = new Gson();
    private final MediaType JSON = MediaType.get("application/json; charset=utf-8");
    
    public DingDongClient(String apiKey, String apiSecret, String baseUrl) {
        this.apiKey = apiKey;
        this.apiSecret = apiSecret;
        this.baseUrl = baseUrl;
    }
    
    public String getToken() throws IOException {
        Map<String, String> credentials = new HashMap<>();
        credentials.put("api_key", apiKey);
        credentials.put("api_secret", apiSecret);
        
        RequestBody body = RequestBody.create(
            gson.toJson(credentials),
            JSON
        );
        
        Request request = new Request.Builder()
            .url(baseUrl + "/api/v1/auth/token")
            .post(body)
            .build();
        
        try (Response response = client.newCall(request).execute()) {
            JsonObject jsonResponse = gson.fromJson(response.body().string(), JsonObject.class);
            this.token = jsonResponse.getAsJsonObject("data")
                .get("access_token")
                .getAsString();
            return this.token;
        }
    }
    
    public JsonObject sendEmail(
        List<String> to,
        String subject,
        String content
    ) throws IOException {
        if (token == null) {
            getToken();
        }
        
        Map<String, Object> payload = new HashMap<>();
        payload.put("to", to);
        payload.put("subject", subject);
        payload.put("content", content);
        payload.put("content_type", "plain");
        
        RequestBody body = RequestBody.create(
            gson.toJson(payload),
            JSON
        );
        
        Request request = new Request.Builder()
            .url(baseUrl + "/api/v1/messages/email/send")
            .addHeader("Authorization", "Bearer " + token)
            .post(body)
            .build();
        
        try (Response response = client.newCall(request).execute()) {
            return gson.fromJson(response.body().string(), JsonObject.class);
        }
    }
    
    public static void main(String[] args) {
        try {
            DingDongClient client = new DingDongClient(
                "noti_aL3rBP1SGm8yy4havWd0xK-nAZlBq5kgrIoI7SmOhy8",
                "secret_5vEh7qvot63UhMQ_qomUM8BfToW-hJ_q",
                "http://localhost:8000"
            );
            
            JsonObject result = client.sendEmail(
                Arrays.asList("user@example.com"),
                "测试邮件",
                "这是一封测试邮件"
            );
            
            System.out.println("Result: " + result);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

---

## 🐘 PHP示例

```php
<?php

class DingDongClient {
    private $apiKey;
    private $apiSecret;
    private $baseUrl;
    private $token;
    
    public function __construct($apiKey, $apiSecret, $baseUrl = 'http://localhost:8000') {
        $this->apiKey = $apiKey;
        $this->apiSecret = $apiSecret;
        $this->baseUrl = $baseUrl;
    }
    
    public function getToken() {
        $url = $this->baseUrl . '/api/v1/auth/token';
        $data = [
            'api_key' => $this->apiKey,
            'api_secret' => $this->apiSecret
        ];
        
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json'
        ]);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        $result = json_decode($response, true);
        $this->token = $result['data']['access_token'];
        return $this->token;
    }
    
    public function sendEmail($to, $subject, $content, $contentType = 'plain') {
        if (!$this->token) {
            $this->getToken();
        }
        
        $url = $this->baseUrl . '/api/v1/messages/email/send';
        $data = [
            'to' => (array)$to,
            'subject' => $subject,
            'content' => $content,
            'content_type' => $contentType
        ];
        
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $this->token
        ]);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
}

// 使用示例
$client = new DingDongClient(
    'noti_aL3rBP1SGm8yy4havWd0xK-nAZlBq5kgrIoI7SmOhy8',
    'secret_5vEh7qvot63UhMQ_qomUM8BfToW-hJ_q'
);

$result = $client->sendEmail(
    ['user@example.com'],
    '测试邮件',
    '这是一封测试邮件'
);

echo "Message ID: " . $result['data']['message_id'] . "\n";
?>
```

---

## 🔵 Go示例

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

type DingDongClient struct {
    APIKey    string
    APISecret string
    BaseURL   string
    Token     string
}

type TokenResponse struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
    Data    struct {
        AccessToken string `json:"access_token"`
    } `json:"data"`
}

type EmailResponse struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
    Data    struct {
        MessageID int    `json:"message_id"`
        Status    string `json:"status"`
    } `json:"data"`
}

func NewClient(apiKey, apiSecret string) *DingDongClient {
    return &DingDongClient{
        APIKey:    apiKey,
        APISecret: apiSecret,
        BaseURL:   "http://localhost:8000",
    }
}

func (c *DingDongClient) GetToken() error {
    url := c.BaseURL + "/api/v1/auth/token"
    payload := map[string]string{
        "api_key":    c.APIKey,
        "api_secret": c.APISecret,
    }
    
    jsonData, _ := json.Marshal(payload)
    resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    body, _ := ioutil.ReadAll(resp.Body)
    var tokenResp TokenResponse
    json.Unmarshal(body, &tokenResp)
    
    c.Token = tokenResp.Data.AccessToken
    return nil
}

func (c *DingDongClient) SendEmail(to []string, subject, content string) (*EmailResponse, error) {
    if c.Token == "" {
        if err := c.GetToken(); err != nil {
            return nil, err
        }
    }
    
    url := c.BaseURL + "/api/v1/messages/email/send"
    payload := map[string]interface{}{
        "to":           to,
        "subject":      subject,
        "content":      content,
        "content_type": "plain",
    }
    
    jsonData, _ := json.Marshal(payload)
    
    req, _ := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Authorization", "Bearer "+c.Token)
    
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, _ := ioutil.ReadAll(resp.Body)
    var emailResp EmailResponse
    json.Unmarshal(body, &emailResp)
    
    return &emailResp, nil
}

func main() {
    client := NewClient(
        "noti_aL3rBP1SGm8yy4havWd0xK-nAZlBq5kgrIoI7SmOhy8",
        "secret_5vEh7qvot63UhMQ_qomUM8BfToW-hJ_q",
    )
    
    result, err := client.SendEmail(
        []string{"user@example.com"},
        "测试邮件",
        "这是一封测试邮件",
    )
    
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    
    fmt.Printf("Message ID: %d\n", result.Data.MessageID)
    fmt.Printf("Status: %s\n", result.Data.Status)
}
```

---

## 🌐 cURL示例

### 获取Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "noti_aL3rBP1SGm8yy4havWd0xK-nAZlBq5kgrIoI7SmOhy8",
    "api_secret": "secret_5vEh7qvot63UhMQ_qomUM8BfToW-hJ_q"
  }'
```

### 发送简单邮件

```bash
TOKEN="YOUR_TOKEN_HERE"

curl -X POST http://localhost:8000/api/v1/messages/email/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["user@example.com"],
    "subject": "测试邮件",
    "content": "这是一封测试邮件",
    "content_type": "plain"
  }'
```

### 使用模板发送

```bash
curl -X POST http://localhost:8000/api/v1/messages/email/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["user@example.com"],
    "template_code": "test_email",
    "template_variables": {
      "username": "张三",
      "timestamp": "2025-10-25"
    }
  }'
```

### 多收件人 + 抄送

```bash
curl -X POST http://localhost:8000/api/v1/messages/email/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["user1@example.com", "user2@example.com"],
    "cc": ["manager@example.com"],
    "bcc": ["admin@example.com"],
    "subject": "通知",
    "content": "重要通知内容"
  }'
```

### 查询消息状态

```bash
MESSAGE_ID=123

curl -X GET http://localhost:8000/api/v1/messages/$MESSAGE_ID \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔐 错误处理

### 错误响应格式

```json
{
  "code": 40001,
  "message": "Invalid API key",
  "data": null,
  "request_id": "uuid-xxx"
}
```

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|-------|------|---------|
| 40001 | API Key无效 | 检查API Key是否正确 |
| 40002 | Token过期 | 重新获取Token |
| 40003 | 权限不足 | 检查API Key权限 |
| 42201 | 模板不存在 | 检查template_code |
| 50001 | 内部服务器错误 | 联系技术支持 |

### Python错误处理示例

```python
try:
    result = client.send_email(
        to=["user@example.com"],
        subject="测试",
        content="内容"
    )
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        # Token过期，重新获取
        client.token = None
        result = client.send_email(...)
    elif e.response.status_code == 422:
        # 参数验证失败
        print("参数错误:", e.response.json())
    else:
        # 其他错误
        print("请求失败:", e)
```

---

## 📚 相关文档

- [快速开始指南](./快速开始指南.md)
- [模板使用指南](./模板使用指南.md)
- [API完整文档](http://localhost:8000/docs)

---

**文档版本**: 1.0  
**最后更新**: 2025-10-25

