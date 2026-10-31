# 让智能体操作浏览器

二选一即可。

## 方式一：Playwright MCP（推荐）

会另开一个由智能体控制的浏览器窗口，和你平时用的浏览器互不影响。

1. 确认已安装 Node.js 20 或更新版本：在终端运行 `node --version`。
2. 进入项目文件夹，运行：

   ```
   claude mcp add playwright -- npx @playwright/mcp@latest
   ```

   这条命令只对当前文件夹生效。
3. 启动 `claude`，输入 `/mcp`，看到 playwright 处于已连接状态即可。
4. 第一次使用时，在提示里明确说“用 playwright mcp 打开浏览器”。第一次运行会自动下载浏览器，需要等一会儿。

## 方式二：Claude in Chrome

直接使用你自己的 Chrome 和登录状态。

1. 在 Chrome 应用商店安装 Claude 扩展，并用同一个账号登录。
2. 按扩展和 Claude Code 官方文档的说明，把 Claude Code 连接到 Chrome。

## 登录

无论哪种方式，登录都由你来做。智能体打开登录页后会停下，你用手机扫码，然后在 Claude Code 里告诉它“已登录，继续”。

## 注意

- 浏览器的登录状态文件不要放进项目文件夹。`gitignore.txt` 已经列了常见的文件名，改名为 `.gitignore` 后生效。
- 遇到验证码，停下来。不要让智能体尝试绕过。
