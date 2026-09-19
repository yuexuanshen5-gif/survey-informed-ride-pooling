# GitHub 发布指南

## 发布前先确认

1. 不要把原始 `.sav` 问卷文件直接放进公开仓库，除非知情同意、伦理审批和数据所有权都明确允许公开。
2. 在 `README.md` 补上论文题目、作者、论文链接或 DOI（如已有）。
3. 确认你和合作者同意使用 MIT License；若代码权利属于课题组或学校，应先按其要求调整。
4. 如果要公开生成的 CSV/PNG，逐个检查是否含 respondent index、派生的个体级信息或不应公开的文件名。

## 方法一：用 PowerShell 发布（推荐）

先登录 GitHub，在网页右上角选择 **New repository**，建议仓库名：

```text
survey-informed-ride-pooling
```

选择 `Public`，并且不要勾选自动创建 README、`.gitignore` 或 License，因为这些文件已经在本项目中。

然后在解压后的项目文件夹中打开 PowerShell，运行：

```powershell
git init
git add .
git status
git commit -m "Initial public release"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/survey-informed-ride-pooling.git
git push -u origin main
```

把 `YOUR_USERNAME` 替换为你的 GitHub 用户名。如果 GitHub 要求登录，按浏览器提示授权，或使用 GitHub Desktop 登录后重试。

## 方法二：使用 GitHub Desktop

1. 安装并登录 GitHub Desktop。
2. 选择 **File → Add local repository**，选中解压后的项目文件夹。
3. 如果提示这还不是 Git 仓库，选择创建仓库，名称保持为 `survey-informed-ride-pooling`。
4. 在左下角填写提交信息 `Initial public release`，点击 **Commit to main**。
5. 点击 **Publish repository**。
6. 取消 `Keep this code private`，然后发布。

## 发布后检查

在 GitHub 网页逐项确认：

- 首页能正确显示 `README.md`；
- 两个 notebook 可以打开，且页面中没有旧的报错输出；
- 仓库中不存在 `.sav`、原始问卷、个人信息或无关大文件；
- **Actions** 页面中的 `Validate notebooks` 显示绿色通过；
- `LICENSE` 页面显示 MIT；
- 仓库描述和 Topics 已补充，例如 `ride-pooling`、`transportation`、`survey-data`、`simulation`、`ordinal-logit`。

## 论文投稿时建议引用固定版本

代码稳定后，在 GitHub 中选择 **Releases → Draft a new release**，创建如 `v1.0.0` 的版本。随后可将 GitHub 仓库连接到 Zenodo，为该 release 生成 DOI。论文中引用 release/DOI，而不是只引用会继续变化的 `main` 分支。
