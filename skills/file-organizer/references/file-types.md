# 文件类型读取方式

按扩展名决定怎么读取文件内容，用于推断文件类型和主题。

## 读取方式对照表

| 扩展名 | 读取方式 | 说明 |
|--------|----------|------|
| `.md` `.txt` `.csv` `.json` `.xml` `.yaml` `.yml` | 直接读取前 50 行 | 文本文件，直接看内容 |
| `.xlsx` `.xls` | python 转 csv 后读取 | `python -c "import pandas as pd; print(pd.read_excel('路径').head().to_csv())"` |
| `.pdf` | Read 工具读取前 2 页 | 能看到大部分内容 |
| `.png` `.jpg` `.jpeg` `.webp` `.gif` `.heic` `.bmp` | Read 工具直接查看 | 图片能直接识别内容 |
| `.mp4` `.mov` `.avi` `.mkv` `.flv` `.wmv` | 看文件名推断 | 视频无法直接读取 |
| `.mp3` `.flac` `.wav` `.aac` `.ogg` | 看文件名推断 | 音频无法直接读取 |
| `.zip` `.rar` `.7z` `.tar` `.gz` `.tar.gz` | 看文件名推断 | 压缩包不自动解压 |
| `.py` `.js` `.ts` `.html` `.css` `.bat` `.ps1` `.sh` | 读取前 30 行 | 代码文件，看用途 |
| `.exe` `.msi` `.dmg` `.apk` `.deb` `.rpm` | 看文件名推断 | 安装包/软件 |
| `.xmind` `.mm` `.fdx` `.opju` `.key` `.pptx` | 看文件名推断 | 专用格式，无法直接读取 |
| `.doc` `.docx` `.ppt` `.pptx` | python 转文本 或看文件名 | 需要额外处理 |
| 其他 | 读取前 20 行尝试 | 尽力而为，不行就问用户 |

## Windows 中文编码

在 Windows 上读取中文文件名或中文文本时，优先显式使用 UTF-8。PowerShell 默认编码可能导致中文乱码。

文本文件读取：

```powershell
Get-Content -LiteralPath "文件路径" -Encoding UTF8 -TotalCount 50
```

CSV/JSON/Markdown 等文件如果第一次读取出现乱码，先用 UTF-8 重试：

```powershell
Get-Content -Raw -LiteralPath "文件路径" -Encoding UTF8
```

写入或保存中间结果时也使用 UTF-8：

```powershell
Set-Content -LiteralPath "输出路径" -Value $content -Encoding UTF8
```

如果文件实际不是 UTF-8，再尝试系统默认编码或根据用户说明判断。不要因为第一次读取乱码就认定文件损坏。

## 扫描文件夹

扫描阶段只列出文件和元数据，不移动、不重命名。

Windows PowerShell：

```powershell
Get-ChildItem -LiteralPath "目标路径" -File |
  Where-Object { $_.Name -notin @('desktop.ini', 'Thumbs.db', 'sync.ffs_db') } |
  Select-Object Name, Extension, Length, LastWriteTime
```

macOS/Linux：

```bash
find "目标路径" -maxdepth 1 -type f \
  ! -name "desktop.ini" ! -name "Thumbs.db" ! -name "sync.ffs_db" \
  -printf "%f\t%s\t%TY-%Tm-%Td %TH:%TM\n"
```

## 大目录摘要

当目标文件夹包含大量子文件夹或超过 200 个文件时，先做摘要，不逐个读取。

摘要应包括：

- 直接子文件夹列表
- 每个子文件夹的文件数量
- 常见扩展名分布
- 总大小或大文件提示
- 最近修改时间
- 3-10 个代表性文件名样本

Windows PowerShell 可先用：

```powershell
Get-ChildItem -LiteralPath "目标路径" -Directory |
  ForEach-Object {
    $files = Get-ChildItem -LiteralPath $_.FullName -File -ErrorAction SilentlyContinue
    [PSCustomObject]@{
      Folder = $_.Name
      FileCount = $files.Count
      TotalBytes = ($files | Measure-Object Length -Sum).Sum
      Recent = ($files | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime
      Samples = ($files | Select-Object -First 5 -ExpandProperty Name) -join '; '
    }
  }
```

不要默认进入 `node_modules`、`.git`、`.venv`、`dist`、`build`、大型照片库、笔记库、应用缓存目录。

## 特殊处理

### Excel 文件

```bash
python -c "
import pandas as pd
try:
    df = pd.read_excel('文件路径')
    print('列名:', list(df.columns))
    print(df.head(3).to_csv())
except Exception as e:
    print('读取失败:', e)
"
```

如果系统没有 `pandas` 或读取失败，不要安装依赖，退回到文件名、大小、修改时间和用户说明。

### PDF 文件

使用 Read 工具，指定页数：
```
Read 工具读取文件路径，pages="1-2"
```

### 图片文件

直接用 Read 工具查看，AI 能识别：
- 证件照片 → 判断为「证件」类
- 合同截图 → 判断为「合同」类
- 风景照片 → 判断为「素材」类
- 表格截图 → 读取内容后判断

## 无法读取时

如果文件无法读取（加密、损坏、专用格式），按以下顺序：
1. 看文件名能推断出什么
2. 看文件大小和修改时间
3. 问用户这是什么文件

不要自动解压压缩包。除非用户明确要求，否则只根据压缩包文件名、大小和修改时间判断。
