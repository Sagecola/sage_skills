# 清理命令手册

本手册收录常见的 Windows 磁盘清理操作，供 AI 助手在用户确认后执行。

执行前务必确认目标路径，不要误删重要数据。

---

## 1. 开发者缓存（安全清除）

这些缓存重建即可，不影响项目代码。

### NPM Cache
```powershell
npm cache clean --force
# 或直接删除缓存目录
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\npm-cache\"
```

### Yarn Cache
```powershell
yarn cache clean
# 或直接删除
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\Yarn\Cache\"
```

### PNPM Store
```powershell
pnpm store prune
```

### Bun Cache
```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:USERPROFILE\.bun\"
```

### Pip Cache
```powershell
pip cache purge
# 或直接删除
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\pip\cache\"
```

### Conda Cache
```powershell
conda clean --all -y
```

---

## 2. 系统临时文件

```powershell
# 清理当前用户临时目录
Get-ChildItem -Path "$env:TEMP" -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue

# 清理 Windows 临时目录（需管理员权限）
# Get-ChildItem -Path "C:\Windows\Temp" -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
```

---

## 3. WSL / 虚拟化清理

### 查看已安装的 WSL 发行版
```powershell
wsl -l -v
```

### 删除 WSL 发行版（⚠️ 数据不可恢复）
```powershell
wsl --unregister <DistroName>
```

### 压缩 WSL 虚拟磁盘（保留数据，回收空间）
```cmd
wsl --shutdown
diskpart
# 在 diskpart 提示符中执行：
select vdisk file="<ext4.vhdx 完整路径>"
attach vdisk readonly
compact vdisk
detach vdisk
exit
```

---

## 4. Windows Update 缓存（需管理员 CMD）

```cmd
net stop wuauserv
net stop bits
del /f /s /q C:\Windows\SoftwareDistribution\Download\*
net start wuauserv
net start bits
```

---

## 5. 回收站清理

```powershell
Clear-RecycleBin -Force -ErrorAction SilentlyContinue
```

---

## 6. 浏览器缓存

### Chrome
```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache\*"
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache\*"
```

### Edge
```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache\*"
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Code Cache\*"
```

---

## 7. 虚拟内存页面文件迁移

引导用户通过 `sysdm.cpl` 将 `pagefile.sys` 迁移到 D 盘：
1. 系统属性 → 高级 → 性能设置 → 高级 → 虚拟内存 → 更改
2. 取消 C 盘页面文件
3. 在 D 盘设置系统管理的页面文件
4. 重启生效
