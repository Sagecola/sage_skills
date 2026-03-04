# sage_skills

鐢?[Sagecola](https://github.com/Sagecola) 缁存姢鐨勫彲澶嶇敤鎶€鑳藉簱銆?
鏈粨搴撴槸涓汉涓庡彲鍒嗕韩鎶€鑳界殑鍞竴浜嬪疄鏉ユ簮銆? 
鎵€鏈夋妧鑳界粺涓€缁存姢鍦?`skills/`锛岄€氳繃鑴氭湰鍚屾鍒版湰鍦板杩愯鏃讹紙Codex銆丆laude Code銆丟emini銆丱penCode锛夈€?
## 浠撳簱鐩爣

- 瀵瑰鍒嗕韩鑷繁闀挎湡浣跨敤涓旂ǔ瀹氱殑鎶€鑳姐€?- 姣忎釜鎶€鑳藉彧缁存姢涓€浠芥爣鍑嗗畾涔夈€?- 鏀寔澶氳澶囥€佸杩愯鏃跺揩閫熷悓姝ャ€?
## 鎶€鑳界洰褰?
褰撳墠鎶€鑳芥竻鍗曡 [skills/CATALOG.md](skills/CATALOG.md)銆?
绀轰緥锛?- `daily-journal`锛氬皢闆舵暎鐢熸椿璁板綍鏁寸悊涓虹粨鏋勫寲鏃ヨ锛屽苟鏀寔鍐欎綔椋庢牸妗ｆ涓庤法鏃ヨ鍏宠仈寮曠敤銆?
## 鐩綍缁撴瀯

```text
skills/
  <skill-name>/
    SKILL.md
    references/   (鍙€?
    scripts/      (鍙€?
    assets/       (鍙€?
scripts/
  install-skills.ps1
  targets.example.json
```

## 蹇€熷紑濮?
1. 鍏嬮殕浠撳簱骞惰繘鍏ョ洰褰曘€?```powershell
git clone https://github.com/Sagecola/sage_skills.git
cd sage_skills
```

2. 澶嶅埗骞剁紪杈戠洰鏍囪繍琛屾椂閰嶇疆銆?```powershell
Copy-Item ./scripts/targets.example.json ./scripts/targets.json
```

3. 鍏?dry-run锛屽啀瀹夎銆?```powershell
./scripts/install-skills.ps1 -DryRun
./scripts/install-skills.ps1
```

瀹夎鍏ㄩ儴鎶€鑳斤細
```powershell
./scripts/install-skills.ps1
```

浠呭畨瑁呭埌鎸囧畾杩愯鏃讹細
```powershell
./scripts/install-skills.ps1 -SkillName daily-journal -Tool codex,claude_code
```

## 鍙戝竷娴佺▼

棰勮鍙戝竷鍐呭锛堜笉鏀规枃浠讹級锛?```powershell
```

鎵ц鍙戝竷锛堟洿鏂?changelog + 鏇存柊 marketplace 鐗堟湰 + 鎻愪氦 + 鎵?tag锛夛細
```powershell
```

寮哄埗鐗堟湰绫诲瀷锛?```powershell
```

## 鐗堟湰涓庡彉鏇?

## Claude Code Marketplace 安装

本仓库已提供 Claude marketplace 元数据：
- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`

可在 Claude Code 中执行：

```text
/plugin marketplace add Sagecola/sage_skills
/plugin install sage-skills@sage-skills
```

