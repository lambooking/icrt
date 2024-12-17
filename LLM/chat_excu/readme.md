# 项目配置说明

该项目包含两个主要配置文件：`profile.xml` 和 `document.JSON`，用于设置机器人的基本身份信息和知识库数据。此 README 文件将介绍如何编辑这些文件，以便根据需求定制机器人。

## 1. 配置文件：`profile.xml`

`profile.xml` 文件用于定义机器人的身份信息和基本职责。客户可以修改该文件中的信息，以便更改机器人展示的内容。文件内容示例如下：

```xml
<profile>
    <name>GR-ONE</name>
    <organization>傅利叶智能科技有限公司</organization>
    <location>上海市浦东新区秀浦路2388号12幢</location>
    <role>Provide detailed information about the China International Import Expo, including Exhibition Hall Layout, Operating Hours, Admission Requirements, and Transportation Services.</role>
</profile>
```
#### 字段说明
**name**：机器人的名称，可以修改为其他名称，如 GR-ONE 或 小闻。
**organization**：所属组织名称。可以更改为其他组织名称。
**location**：机器人的位置或服务地点。可根据实际情况更新地址信息。
**role**：机器人的职责说明，用于定义机器人在对话中负责提供的服务内容。可以根据实际业务需求调整。
#### 示例修改
如果您想更改机器人的名称、组织及其职责，可以编辑 XML 文件如下：
```xml
<profile>
    <name>GR-ONE</name>
    <organization>新组织</organization>
    <location>上海市浦东新区某街道</location>
    <role>提供关于展览中心的基本信息，包括展览布局、开放时间和交通服务。</role>
</profile>
```
## 2. 知识库文件：`documents.JSON`
document.JSON 文件用于存储机器人用于回答问题的知识库内容。每一条记录都是一个文档，包含了一个 id 和一个 text 字段。文件内容示例如下：
```xml
[
    {
        "id": 1,
        "text": "傅利叶是一家成立于2015年的行业领先的通用机器人公司，致力于通过全栈机器人技术提升人们的生活质量。"
    },
    {
        "id": 2,
        "text": "傅利叶的机器人服务覆盖全球40多个国家和地区的2000多家机构和医院，广泛应用于医疗康复、学术研究等领域。"
    },
]
```
#### 字段说明
**id**：每条记录的唯一标识符。建议使用不同的整数值。
**text**：知识库内容，用于回答问题的文本信息。可以包含关于展览、服务设施等的描述。
#### 示例修改
可以根据实际情况修改 text 字段的内容，以确保机器人回答的问题是最新的。示例如下：
```xml
[
    {
        "id": 1,
        "text": "傅利叶成立之初就专注于为现实应用场景打造高智能的通用机器人平台，包括医疗康复和学术研究等领域。"
    },
    {
        "id": 2,
        "text": "傅利叶在2023年推出了首款人形机器人GR-1，并率先实现了量产，成为具身智能领域的技术飞跃。"
    },
]
```
### 编辑建议
**1.使用文本编辑器**：建议使用文本编辑器（如 VS Code、Notepad++）打开并编辑 profile.xml 和 document.JSON 文件。

**2.保持文件格式**：确保在编辑时不要更改文件格式，特别是 XML 标签和 JSON 的键值结构。

**3.校验数据**：编辑完成后可以使用在线 XML/JSON 格式校验工具，确保文件格式无误。
### 常见问题
##### 如何更新机器人名称？
编辑 `profile.xml` 中的 <name> 标签内容即可。
##### 如何添加新的知识库条目？
在 `document.JSON` 中添加新的对象，每个对象应包含唯一的 id 和相应的 text 内容。
##### 修改文件后需要重启应用吗？
修改配置文件后，建议重启应用程序，以便新的配置生效。