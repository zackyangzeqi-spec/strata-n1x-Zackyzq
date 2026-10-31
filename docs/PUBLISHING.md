# 项目说明页与公开入口维护

本页面向维护者。普通用户请从[安装指南](INSTALL.md)开始。

## 公开入口与资料分工

| 入口 | 内容 |
|---|---|
| [项目说明页](https://zackyangzeqi-spec.github.io/strata-n1x-Zackyzq/) | 目标设备、模型身份、下载入口、Strata 与 DSH 关系、已有观察及限制 |
| [GitHub 仓库](https://github.com/zackyangzeqi-spec/strata-n1x-Zackyzq) | 安装文档、固定上游补丁、历史记录与反馈 |
| [项目事实表](PROJECT-FACTS.md) | 身份、版本、量化、证据与未知项的详细依据 |
| [维护者主页](https://github.com/zackyangzeqi-spec) | Zack_yzq 的公开项目与后续活动 |

项目页由 `site/` 中的普通 HTML/CSS 构成，正文直接存在于 HTML 中。它复用仓库事实，不另立一套性能记录。网站更新不代表安装器、权重或已验证范围变化。

## 发布 GitHub Pages

1. 仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**。
2. 将经过审阅的 `site/` 和 `.github/workflows/pages.yml` 合并到 `main`。该工作流只上传 `site/`，使用官方 Pages Actions；没有模型或程序构建步骤。
3. 在 Actions 查看 **Publish project page** 的部署结果。工作流只允许从 `main` 部署；手动触发时也选择 `main`。
4. 打开项目 URL，确认正文、图片、CSS 与下载入口正常；再把仓库 About 的 Website 填为相同 URL。
5. 如果首次合并时 Pages 还没有启用，完成第 1 步后，在 Actions 手动运行该工作流。

部署成功与搜索收录是不同状态。以工作流返回的实际 `page_url` 为准；如果使用自定义域名或仓库改名，应同时修改 HTML 的 canonical、Open Graph、JSON-LD、sitemap 和所有对外入口。

官方资料：[Pages 发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)、[自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。工作流中的官方 Action 提交固定于 2026-10-31 查询的标签版本，更新时应重新核对来源。

## 页面事实如何更新

先更新有依据的详细资料，再同步项目页和 README。速度数字必须带量化、请求范围、缓存和设备条件；历史界面汇总不能改写成通用承诺。DSH 连接说明继续指向 [DSH.md](DSH.md)，尤其保留历史超时扩展与版本前提。

如果从本地既有记录补充开发过程，只公开可核对的实现、版本与脱敏摘要。当前软件版本不能反推历史测试版本。原始会话、机器路径、令牌与未获授权的截图不属于默认发布材料。

## GitHub 简介与分享图

About 保持完整模型名、N1X、128GB、Windows ARM64、量化与 DeepSeek Harness。中文检索别名可以在自然句子中出现；Topics 最多 20 个，已有相关标签可保持稳定。

分享图为 `site/assets/social-preview.png`（1280 × 640）。在仓库 Settings → Social preview 上传同一张图；HTML 中也引用它作为网页分享图。各社交平台的缓存与卡片展示方式不同，不能保证微信自动显示相同封面。

维护者署名链接个人主页；Star 用于收藏项目，Follow 用于关注维护者，Watch 的 Releases 订阅用于版本通知。

## Search Console：上线后的可选步骤

1. 访问 [Google Search Console](https://search.google.com/search-console)，使用维护者自己的账号添加 **URL-prefix / 网址前缀** 属性：`https://zackyangzeqi-spec.github.io/strata-n1x-Zackyzq/`。
2. 选择 HTML tag 验证，将控制台实际生成的 `google-site-verification` meta 放到 `site/index.html` 的 `<head>` 中，保留已有站点验证标签。提交并部署；确认线上源代码含真实标签，再完成验证。
3. 可提交 `https://zackyangzeqi-spec.github.io/strata-n1x-Zackyzq/sitemap.xml`。本项目是一页说明站，sitemap 只有这个实际页面。
4. 在 URL Inspection 检查公开页面是否可读取，并按控制台实际结果申请索引。记录“已申请”和“已收录”的区别。

无需为 GitHub Pages 的 `github.io` 公共域名购买域名或做你无法控制的 DNS 验证。上面的 URL-prefix 只对应你的项目页面路径。

`robots.txt` 必须位于主机根路径，例如 `https://zackyangzeqi-spec.github.io/robots.txt`。在项目子目录里放 `robots.txt` 不会变成该主机的爬虫控制文件，所以本项目不放一个误导性的子路径文件。上线后检查主机根路径是否已有阻止本项目的规则；若存在，应由该根站点维护者处理。

Google 说明：抓取可能需要数天到数周，申请不保证立即或最终收录，重复提交同一 URL 不会加快抓取。可读正文、有效链接和准确事实有帮助，但 Pages、sitemap、结构化数据或额外 AI 文件都不保证排名。

来源：[所有权验证](https://support.google.com/webmasters/answer/9008080)、[请求重新抓取](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)、[robots.txt 位置](https://developers.google.com/crawling/docs/robots-txt/create-robots-txt)、[Google AI 搜索功能](https://developers.google.com/search/docs/appearance/ai-features)。

## 同步公开文件清单

`PACKAGE.json` 记录公开 Git 文件的 SHA256 和字节数，排除清单自身。网页文件也应进入该清单。

先只暂存本次准备公开的文件，再运行：

```powershell
python tools/update_public_inventory.py
if ($LASTEXITCODE -ne 0) { throw "Inventory preview failed" }
python tools/update_public_inventory.py --write
if ($LASTEXITCODE -ne 0) { throw "Inventory was not written" }
git diff -- PACKAGE.json
if ($LASTEXITCODE -ne 0) { throw "Could not inspect inventory diff" }
git add PACKAGE.json
if ($LASTEXITCODE -ne 0) { throw "Inventory was not staged" }
python tools/update_public_inventory.py --check
if ($LASTEXITCODE -ne 0) { throw "Inventory does not match the Git index" }
```

脚本只读取 Git 暂存区中的文件，不扫描未跟踪文件，不运行安装器或模型，也不提交或推送。Windows 工作区换行可能与 Git 实际存储字节不同，因此以暂存区为准。脚本发现未暂存的 PACKAGE 元数据、冲突或符号链接时会停止，让维护者先处理该具体问题。生成后若其他暂存内容变化，应重新生成并通过 `--check`。

完成标志：公开分支内容可读、Pages 部署成功、Website 指向可访问的页面、公开文件清单与最终提交一致。Search Console 与第三方目录是否完成，分别按实际状态记录。
