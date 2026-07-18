"""
WizAgent - 磁盘空间自动扫描与分析脚本

依赖 WizTree CLI（WizTree64.exe），需自行安装并加入 PATH，
或通过 --wiztree-path 参数指定完整路径。
"""

import csv
import sys
import os
import subprocess
import ctypes
import argparse
import shutil


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def format_size(size_bytes):
    if size_bytes >= 1024**4:
        return f"{size_bytes / 1024**4:.2f} TB"
    elif size_bytes >= 1024**3:
        return f"{size_bytes / 1024**3:.2f} GB"
    elif size_bytes >= 1024**2:
        return f"{size_bytes / 1024**2:.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} Bytes"


def find_wiztree(cli_path=None):
    """Locate WizTree64.exe: CLI arg > PATH > common install locations."""
    if cli_path:
        if os.path.isfile(cli_path):
            return cli_path
        print(f"[Error] WizTree not found at specified path: {cli_path}")
        sys.exit(1)

    # Try PATH
    found = shutil.which("WizTree64.exe") or shutil.which("WizTree")
    if found:
        return found

    # Try common install locations
    common_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\WizTree\WizTree64.exe"),
        r"C:\Program Files\WizTree\WizTree64.exe",
        r"C:\Program Files (x86)\WizTree\WizTree64.exe",
    ]
    for p in common_paths:
        if os.path.isfile(p):
            return p

    print("[Error] WizTree64.exe not found.")
    print("  Please install WizTree from https://www.diskanalyzer.com/")
    print("  and either add it to PATH or use --wiztree-path to specify the location.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="WizTree Space Analyzer Wrapper")
    parser.add_argument("target", nargs="?", default="C:",
                        help="Target drive or folder to scan (e.g. C:, D:, C:\\Users)")
    parser.add_argument("--wiztree-path", default=None,
                        help="Full path to WizTree64.exe")
    args = parser.parse_args()

    # 格式化并统一目标路径为绝对路径，并以 \ 结尾
    target_raw = args.target
    if len(target_raw) == 1 and target_raw.isalpha():
        target_path = target_raw.upper() + ":\\"
    elif len(target_raw) == 2 and target_raw[1] == ':':
        target_path = target_raw.upper() + "\\"
    else:
        target_path = os.path.abspath(target_raw)
        if not target_path.endswith('\\'):
            target_path += '\\'

    print("=" * 60)
    print("  WizTree Automated Live Space Analyzer")
    print("=" * 60)
    print(f"[Info] Target Path to Scan: {target_path}")

    if not os.path.exists(target_path):
        print(f"[Error] Target path does not exist: {target_path}")
        sys.exit(1)

    # 1. 定位 WizTree64.exe
    wiztree_exe = find_wiztree(args.wiztree_path)
    print(f"[Info] Using WizTree: {wiztree_exe}")

    # 输出文件放在脚本同目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_csv = os.path.join(script_dir, "temp_live_scan.csv")
    output_md = os.path.join(script_dir, "live_analysis_report.md")

    # 2. 判断管理员权限，选择扫描参数
    admin_mode = is_admin()
    admin_flag = "1" if admin_mode else "0"
    if admin_mode:
        print("[Info] Running with Administrator privileges (MFT Fast Scan enabled).")
    else:
        print("[Info] Running with Standard privileges (Folder Scan mode).")

    # 3. 运行 WizTree 导出数据
    print(f"\n[1/3] Calling WizTree to scan '{target_path}' and export data...")
    cmd = [wiztree_exe, target_path, f"/export={temp_csv}", f"/admin={admin_flag}"]

    try:
        subprocess.run(cmd, check=True)
        print("[OK] Data export completed.")
    except subprocess.CalledProcessError as e:
        print(f"[Error] Running WizTree failed: {e}")
        sys.exit(1)

    # 4. 解析 CSV 数据
    if not os.path.exists(temp_csv):
        print(f"[Error] Failed to locate temporary CSV file: {temp_csv}")
        sys.exit(1)

    print("\n[2/3] Parsing scan data (please wait)...")

    target_capacity = 0
    target_free = 0
    target_used = 0

    top_level_items = {}
    second_level_items = {}
    top_files = []
    max_top_files = 30

    # 常见大户模式识别
    targets = {
        "Windows Temp & System Cache (系统临时与更新文件)": [
            "windows\\temp", "appdata\\local\\temp",
            "windows\\softwaredistribution", "deliveryoptimization", "temp\\",
        ],
        "Node.js / NPM / Yarn / PNPM (前端开发依赖)": [
            "node_modules", "npm-cache", "yarn\\cache", "pnpm\\store",
            "pnpm-store", "appdata\\local\\npm-cache", "appdata\\roaming\\npm",
        ],
        "WSL / Ubuntu (Windows子系统虚拟磁盘)": [
            "canonicalgroup", "ext4.vhdx",
        ],
        "Python / Pip / HuggingFace (AI/Python环境缓存)": [
            ".cache\\pip", "huggingface\\hub", ".cache\\huggingface",
            "torch\\kernels", "miniconda", "anaconda", ".conda",
            "appdata\\roaming\\python",
        ],
        "WeChat / Tencent Files (微信/QQ聊天记录与文件)": [
            "wechat files", "tencent files", "tencent\\wechat",
            "tencent\\qq", "tencent\\tim",
        ],
        "Windows Installer (系统备份安装包)": [
            "windows\\installer",
        ],
    }
    target_sizes = {k: 0 for k in targets}

    with open(temp_csv, 'r', encoding='utf-8-sig', errors='replace') as f:
        f.readline()  # 跳过 WizTree 说明行
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            print("[Error] CSV file is empty!")
            sys.exit(1)

        for row in reader:
            if len(row) < 2:
                continue
            path = row[0]
            try:
                size = int(row[1])
            except ValueError:
                continue

            is_folder = path.endswith('\\')
            path_lower = path.lower()

            # 读取磁盘容量信息
            if path.upper() == target_path.upper() and len(row) > 17:
                try:
                    target_capacity = int(row[15])
                    target_free = int(row[16])
                    target_used = int(row[17])
                except ValueError:
                    pass

            # 统计子项
            if path.upper() != target_path.upper() and path.upper().startswith(target_path.upper()):
                rel_path = path[len(target_path):]
                parts = [p for p in rel_path.split('\\') if p]

                if len(parts) == 1:
                    top_level_items[path] = (size, is_folder)
                elif len(parts) == 2:
                    second_level_items[path] = (size, is_folder)

                # 超大文件排行
                if not is_folder:
                    if len(top_files) < max_top_files:
                        top_files.append((size, path))
                        top_files.sort(reverse=True)
                    elif size > top_files[-1][0]:
                        top_files[-1] = (size, path)
                        top_files.sort(reverse=True)

                    # 分类统计
                    for cat_name, patterns in targets.items():
                        for pat in patterns:
                            if pat in path_lower:
                                target_sizes[cat_name] += size
                                break

    # 5. 生成 Markdown 报告
    print("\n[3/3] Generating Markdown report...")
    with open(output_md, 'w', encoding='utf-8') as out:
        out.write(f"# 📊 空间实时分析报告 ({target_path})\n\n")
        out.write(f"生成方式：WizTree 命令行自动扫描与解析\n\n")

        if target_capacity > 0:
            out.write("## 💾 磁盘容量概况\n")
            out.write(f"- **总容量**: {format_size(target_capacity)}\n")
            out.write(f"- **已用空间**: {format_size(target_used)} ({target_used/target_capacity*100:.1f}%)\n")
            out.write(f"- **剩余空间**: {format_size(target_free)} ({target_free/target_capacity*100:.1f}%)\n\n")

        out.write(f"## 📂 1. 【{target_path}】直接子项大小排行\n")
        out.write("| 子项类型 | 子项路径 | 占用大小 |\n")
        out.write("| --- | --- | --- |\n")
        for path, (size, is_dir) in sorted(top_level_items.items(), key=lambda x: x[1][0], reverse=True)[:25]:
            type_str = "文件夹" if is_dir else "文件"
            out.write(f"| {type_str} | `{path}` | **{format_size(size)}** |\n")

        out.write(f"\n## 📂 2. 【{target_path}】二级子目录排行 (前 20)\n")
        out.write("| 子项类型 | 子项路径 | 占用大小 |\n")
        out.write("| --- | --- | --- |\n")
        for path, (size, is_dir) in sorted(second_level_items.items(), key=lambda x: x[1][0], reverse=True)[:20]:
            type_str = "文件夹" if is_dir else "文件"
            out.write(f"| {type_str} | `{path}` | **{format_size(size)}** |\n")

        has_targets = any(size > 0 for size in target_sizes.values())
        if has_targets:
            out.write("\n## 🎯 3. 扫描范围内的"空间大户"分类统计\n")
            out.write("| 类别 | 累计大小 |\n")
            out.write("| --- | --- |\n")
            for name, size in sorted(target_sizes.items(), key=lambda x: x[1], reverse=True):
                if size > 0:
                    out.write(f"| {name} | **{format_size(size)}** |\n")

        out.write("\n## 📄 4. 扫描范围内的超大文件排行 (前 30)\n")
        out.write("| 排名 | 文件路径 | 大小 |\n")
        out.write("| --- | --- | --- |\n")
        for idx, (size, path) in enumerate(top_files):
            out.write(f"| {idx+1} | `{path}` | **{format_size(size)}** |\n")

    # 6. 清理临时 CSV 文件
    try:
        os.remove(temp_csv)
        print("[OK] Temporary scan CSV file cleaned.")
    except Exception as e:
        print(f"[Warning] Failed to delete temporary CSV file: {e}")

    # 7. 控制台输出精炼摘要
    print("\n" + "=" * 60)
    print("Live Scan Summary")
    print("=" * 60)
    print(f"* Scanned Target: {target_path}")
    if target_capacity > 0:
        print(f"* Total Capacity: {format_size(target_capacity)}")
        print(f"* Remaining Space: {format_size(target_free)} ({target_free/target_capacity*100:.1f}%)")

    print("\nTop 5 Direct Children:")
    for path, (size, is_dir) in sorted(top_level_items.items(), key=lambda x: x[1][0], reverse=True)[:5]:
        type_str = "[DIR]" if is_dir else "[FILE]"
        print(f"  - {type_str} {path}: {format_size(size)}")

    print("\nTop 5 Largest Files:")
    for idx, (size, path) in enumerate(top_files[:5]):
        print(f"  [{idx+1}] {path} ({format_size(size)})")

    print("\n" + "=" * 60)
    print(f"Detailed report saved to: {output_md}")
    print("=" * 60)


if __name__ == "__main__":
    main()
